# Minted - Personal Spending Tracker

## Deployed version of the application:
The deployed version of the application can be found at **[Minted](https://minted-aymskyt.azurewebsites.net/)**

## Installation instructions:
To setup for development, you must edit `settings.py` inside the *PersonalSpendingTracker* directory to be `DEBUG=True` from the existing `DEBUG=False`

To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:
```
$ virtualenv venv
$ source venv/bin/activate
```
Install mysqlclient:
*For more info see [here](https://pypi.org/project/mysqlclient/)*
```
# Debian
$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# macOS (Homebrew)
$ brew install mysql
```
Install all required packages:
```
$ pip3 install -r requirements.txt
```
Set up environment variables:
- *Copy `.env.sample` into a new file `.env`  at the root directory and replace with your own variables*

Make migrations:
```
python3 manage.py makemigrations
```
Migrate the database:
```
$ python3 manage.py migrate
```
Create default notification subscriptions:
```
$ python3 manage.py create_subscriptions
```
Collect static files:
```
$ python3 manage.py collectstatic
```
Seed the development database with:
```
$ python3 manage.py seed
```
Run all tests with:
```
$ python3 manage.py test
```
Setup cronjobs:
*Note: Your file path must not include spaces*
```
$ python3 manage.py crontab add
```
To remove cronjobs after development:
```
$ python3 manage.py crontab remove
```

## Sources:
*Packages:*
The packages used by this application are specified in `requirements.txt`.
The exact version of each package used by this application can also be found in this same file.
