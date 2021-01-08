from flask import Flask, render_template, request, redirect, url_for
from models import *
from datetime import datetime
import requests

"""
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="the username from the 'Databases' tab",
    password="the password you set on the 'Databases' tab",
    hostname="the database host address from the 'Databases' tab",
    databasename="the database name you chose, probably yourusername$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
"""

app = Flask(__name__) # this creates flask application to run my code
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Danepereblago1@localhost/currency"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

full_names = {
    "USD": "US Dollar", "EUR": "Euro", "NOK": "Norwegian krone", "UAH": "Ukrainian hryvna", "CNY": "Chinese yuan",
    "GBP": "Pounds sterling"
}


# Trailing slash
# global:
# app.url_map.strict_slashes = False
@app.route("/test", strict_slashes=False)
def test():
    return 'This is a test page <br> '\
           '@app.route("/test", strict_slashes=False)'


# route: get info from db and render index page
@app.route("/")
def index():
    # If DB data is old then update:
    # today's date
    idag = datetime.today().strftime('%Y-%m-%d')

    # get currency from db to be compared to today's date
    curr_in_db = Currency.query.get(1)

    # compare
    if curr_in_db.date != idag:
        # print("Values are outdated, update is required")
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
            curr_in_db.full_name = full_names[i]
            db.session.commit()
        # print("Done")
    # else:
        # print("Values are up to date")

    currency = Currency.query.all()
    any_cur = Currency.query.get(1)
    up_date = any_cur.date
    return render_template("index.html", currency=currency, up_date=up_date)


# calculate rates and display results
@app.route("/result", methods=['POST'])
def result():

    # first and second currency. Which are currency.id
    first_cur = request.form.get("first_cur")  # id
    second_cur = request.form.get("second_cur")  # id

    # get amount to be calculated
    amount = float(request.form.get("amount"))

    # create db instances for first and second currency if not EUR
    if first_cur != "EUR":
        first_cur_db = Currency.query.get(int(first_cur))
        abr_first_cur = first_cur_db.abbreviation
        rate_first_cur = first_cur_db.cost_to_eur
    else:
        abr_first_cur = "EUR"
        rate_first_cur = 1

    if second_cur != "EUR":
        second_cur_db = Currency.query.get(int(second_cur))
        abr_second_cur = second_cur_db.abbreviation
        rate_second_cur = second_cur_db.cost_to_eur
    else:
        abr_second_cur = "EUR"
        rate_second_cur = 1

    # calculated rate
    rate = round((rate_second_cur/rate_first_cur)*amount, 2)

    return render_template("result.html", abr_first_cur=abr_first_cur, full_first_cur=full_names[abr_first_cur],
                           abr_second_cur=abr_second_cur, full_second_cur=full_names[abr_second_cur],
                           amount=amount, rate=rate)


if __name__ == '__main__':
    app.run(debug=True)
