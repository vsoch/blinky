# Blinkin Lights Scripts

This is a small collection of modified or new scripts for [BlinkinLights]().

## Weather

The [weather.py](weather.py) script will show the hourly forecast across the 
lights. It's modified to use the Tomorrow API, as the original Wunderground
seems to be only available for people with weather stations! To use it, you should

1. Connect your blinkin lights to USB.
2. Create a free account and get your API key from [https://www.tomorrow.io/](https://www.tomorrow.io/)
3. Identify the port it's using (for me it was `/dev/ttyACM0`)
4. Export your API keys and the latitude and longitude you want
5. Run the script (you likely will need sudo and to pass the environment)


```bash
export TOMORROW_KEY=xxxxxxxxxxxxxxxx
export LATLONG="xxx,-xxx"
```

If you aren't using system Python you'll likely find it easier to provide the direct path.
In my case I made a virtual environment here so I could install dependencies
and then use it:

```bash
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ sudo -E ./env/bin/python weather.py -p /dev/ttyACM0
```

