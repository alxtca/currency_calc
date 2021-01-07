from flask import Flask, render_template, request
from models import *
from datetime import datetime
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Danepereblago1@localhost/currency"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    # today's date
    idag = datetime.today().strftime('%Y-%m-%d')

    # get currency from db to be compared to today's date
    curr_in_db = Currency.query.get(1)

    # compare
    if curr_in_db.date != idag:
        print("Values are outdated, update is required")
        # Update with latest JSON data

        # get JSON
        res = requests.get("http://data.fixer.io/api/latest?access_key=53b9312d9464e65927bc025bdb0700b4"
                           "&base=EUR&symbols=USD,NOK,GBP,UAH,CNY")
        data = res.json()
        date = data["date"]

        # update db rows
        # 1 for loop go through JSON data, extract key and value
        # 2 search in db by abbreviation, update .cost_to_eur and date with new value
        for i in data["rates"]:
            curr_in_db = Currency.query.filter_by(abbreviation=i).first()
            curr_in_db.cost_to_eur = data["rates"][i]
            curr_in_db.date = date
            db.session.commit()
        print("Done")
    else:
        print("Values are up to date")


if __name__ == "__main__":
    with app.app_context():
        main()
