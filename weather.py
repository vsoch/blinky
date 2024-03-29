# Original example by Zach Hoeken Smith (http://hoektronics.com)
# Modified for the new Blinkyboard library by Max Henstell 3/2013
# Modified for Weather Underground by Marty McGuire 4/2013
# Modified to use tomorrow API by @vsoch 07/2021

import requests
import blinkytape
import glob
import os
import colorsys
import tempfile
import json
import time
import sys

if sys.version_info > (3, 0):
    import urllib.request as requestlib
else:
    import urllib2 as requestlib

latlong = os.environ.get("LATLONG")
apikey = os.environ.get("TOMORROW_KEY")
url = "https://api.tomorrow.io/v4/timelines"


def connect(port):

    if not port:
        sys.exit("Could not locate a BlinkyTape.")

    print("BlinkyTape found at: %s" % port)

    bt = blinkytape.BlinkyTape(port)
    bt.displayColor(0, 0, 0)
    return bt


def get_hourly_data():
    print("[%d] Fetching %s" % (time.time(), url))

    try:
        querystring = {
            "timesteps": "1h",
            "apikey": apikey,
            "location": latlong,
            "fields": "temperature",
            "units": "imperial",
            "timezone": "US/Mountain",
        }
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()
    except Exception as ex:
        print(ex)


color_map = {
    -10: (255, 0, 255),
    0: (158, 0, 255),
    10: (0, 0, 255),
    20: (0, 126, 255),
    30: (0, 204, 255),
    40: (5, 247, 247),
    50: (127, 255, 0),
    60: (247, 247, 5),
    70: (255, 204, 0),
    80: (255, 153, 0),
    90: (255, 79, 0),
    100: (204, 0, 0),
    110: (169, 3, 3),
    120: (186, 50, 50),
}


def color_for_temp(temp):
    """Returns an RGB color triplet for the given (Fahrenheit scale) temp.

    Temps colors taken from the Weather Channel mapping found at:
    http://wattsupwiththat.com/2008/06/26/color-and-temperature-perception-is-everything/
    """
    color = None
    for temp_ceil in sorted(color_map.keys()):
        color = color_map[temp_ceil]
        if temp < temp_ceil:
            break
    return adjust_color(color)


def adjust_color(color, dim_factor=0.10):
    r, g, b = color
    h, s, v = colorsys.rgb_to_hsv(r / 256.0, g / 256.0, b / 256.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, v * dim_factor)
    return int(r * 256), int(g * 256), int(b * 256)


if __name__ == "__main__":

    import optparse

    parser = optparse.OptionParser()
    parser.add_option(
        "-p",
        "--port",
        dest="portname",
        help="serial port (ex: /dev/ttyUSB0)",
        default=None,
    )
    (options, args) = parser.parse_args()

    while True:
        bt = connect(options.portname)
        data = get_hourly_data()

        if not data:
            sys.exit(
                "Could not fetch weather data. Check your proxy settings and try again. Try: export http_proxy=PROXY_IP:PROXY_PORT before running this script."
            )

        for hour in data["data"]["timelines"][0]["intervals"][:60]:
            temp = int(hour["values"]["temperature"])
            r, g, b = color_for_temp(temp)
            print("Temp: {}. Color: {},{},{}".format(temp, r, g, b))
            bt.sendPixel(r, g, b)
        bt.show()

        # Update every hour
        time.sleep(3600)
