# Event Collectors

Use these event collectors with proper config files (more on that below) to find events for women in tech through the Meetup and Eventbrite APIs

## Meetup

Python version: 2.7

### Setting up the config file

Format config.py like so:

```
api_key = "YOUR_API_KEY"
```
Be sure to replace space in quotes with your Meetup API key, which you can get from [here](https://secure.meetup.com/meetup_api/key/). Once you've made config.py, be sure that your code has the following line in the imports:

```
import config
```

### Running the script

When you're ready to run the event collector, run the following code from your command line:

```
python get_meetup_data.py > YOUR_FILENAME.csv
```
Again, replace YOUR_FILENAME with the desired filename for the csv. **NOTE:** this script is written for Python 2.7.

## Eventbrite

Python version: 3

### Setting up the config file

(pending)


### Running the script

(pending)

## Contributors

Click [here](https://github.com/SheCanCodeHQ/event-collector/graphs/contributors) to see the contributors.


## Acknowledgments

*Thanks to Andrew Ba Tran for his in-depth [tutorial](https://trendct.org/2015/04/03/using-python-and-r-to-pull-and-analyze-meetup-com-api-data) on accessing and using Meetup's API.
