# STOCK_CHECKER_DJ

Stock checking application that allows user to save daily stock price data.  


## Installation

```bash
create directory
virtualenv venv
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py runserver
```

## Special Considerations

```bash
API restricts stock calls to 5 per minute (free version).
Stock data is based on New York Stock Exchange which is open from 9:30AM to 4PM EST.
API requests made on the weekends will take Friday stock data.
Calls made prior to open will take previous days info (unless previous day is weekend).

App uses Alpha Vantage API.  To request unique API or to review official documenation visit:
https://www.alphavantage.co/
```


