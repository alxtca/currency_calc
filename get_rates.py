import os
import psycopg2

from flask import Flask, render_template, request
from models import *
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Danepereblago1@localhost/currency"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


full_names = {
    "USD": "US Dollar", "EUR": "Euro", "NOK": "Norwegian krone", "UAH": "Ukrainian hryvna", "CNY": "Chinese yuan",
    "GBP": "Pounds sterling"
}


#  get rates and store inside db
def main():
    res = requests.get("http://data.fixer.io/api/latest?access_key=53b9312d9464e65927bc025bdb0700b4"
                       "&base=EUR&symbols=USD,NOK,GBP,UAH,CNY")
    # status code to be checked
    # .json extracting data and save it into data variable in JSON format
    data = res.json()
    # print(data)
    date = data["date"]
    # I want to loop all currencies on the list and create a row in a table for each.
    for i in data["rates"]:
        # print(i)  # key name
        # print(data["rates"][i])  # key values
        # here add each row:
        currency = Currency(abbreviation=i, full_name=full_names[i], cost_to_eur=data["rates"][i], date=date)
        db.session.add(currency)

    # set initial counter value
    count = Counter(times=0)
    db.session.add(count)

    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
