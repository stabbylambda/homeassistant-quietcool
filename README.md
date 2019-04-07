# quietcool-homeassistant

This component integrates with the [QuietCool Python Library](https://github.com/stabbylambda/quietcool-python) to control QuietCool fans from [Home Assistant](https://www.home-assistant.io/)

## Usage

Add the quietcool platform to the fan section of your configuration.yaml file:

```yaml
fan:
  - platform: quietcool
    host: 10.0.0.1 # Obviously you should change this to match the IP address of your own Master Hub
```

## Tests / Disclaimer

Just like the python library, there aren't any tests as I think that would kind of be a waste of time. Also, same disclaimer as the python library: open a window before you play with this. Automating a house fan without also automating your windows (not that I'm suggesting you do that either) means you can blow out pilot lights, suck air in through the sewer, and damage weather stripping on your doors and windows. Don't do it.
