I've added a feature to the code that allows for us to pull historical finance data. In order to pull today's data like in the past, it needs to be run a little differently now. First, run:

```
python stock_pusher.py
```

Then there will be a series of prompts. To get today's here is the series of prompts:

```
python stock_pusher.py
today/historical?: today
Path: <your path here>
```

If you want to pull historical data, here is the series of prompts:

```
python stock_pusher.py
today/historical?: historical
Path: <your path here>
Start Date (in mm/dd/yy format): mm/dd/yy
End Date (in mm/dd/yy format): mm/dd/yy
```

Be careful where you store historical data, though, because a separate file will be produced for each stock symbol.