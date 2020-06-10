# Looker Content Cleanup

Disable Looker users who have not logged into the platform or used the API in X number of days. 

### Prerequisites

This script rely on the new Looker [Python SDK](https://github.com/looker-open-source/sdk-codegen/tree/master/python), which requires Python 3.6+.


### Getting started

* Clone this repo, and configure a file called `looker.ini` in the same directory as the two Python scripts. Follow the instructions [here](https://github.com/looker-open-source/sdk-codegen/tree/master/python#configuring-the-sdk) for more detail on how to structure the `.ini` file. The docs also describe how to use environment variables for API authentication if you so prefer.
* Install all Python dependencies in `requirements.txt`

### Usage

``` optional arguments:
  -h, --help            show this help message and exit
  --days DAYS, -d DAYS  The number of days of inactivity required to be
                        disabled (e.g. 90 days).
  --test, -t            Use this flag to see unengaged users but not disable
                        them.
```

To run the script, run the following:

```
python disable_unengaged_users.py --days {number of days}
```

#### Test Mode

Before disabling users, it is recommended to run the script in test mode. This allows you to observe the list of users to be disabled before actually disabling them. 

```
python disable_unengaged_users.py --days {number of days} --test
```