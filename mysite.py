from flask import Flask , redirect, url_for
from flask import render_template
from flask import request
import sqlite3 as sql
#In order to get the bootstrap stylesheets to work I needed to install bootstrap and import it.
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def cryptic_welcoming():
    return "Your getting closer to your goal."

@app.route('/welcome')
def mysite_page():
    return render_template('mysite.html')

#The below routes have been decommissioned as of 5:06pm 3/18/2021
#@app.route('/Christmas')
#def Christmas_greetings():
#    return "Merry Christmas"

#@app.route('/Easter')
#def Easter_greetings():
#    return "Happy Easter"

#@app.route('/NewYear')
#def NewYear_greetings():
#    return 'Happy New Year!'

#@app.route('/Independence_Day')
#def Independence_Day_greetings():
#    return "Happy Independence Day " + "Don't Tread On Me! -Metallica"

#This is my attempt at building a dynamic website as of 3-18-2021.
@app.route('/greetings')
def greetings_page():
    return ('The website has been provided with insufficient data. Please enter the name of a holiday to obtain results')

@app.route('/greetings/<string:season>') 
def seasons_greetings_page(season):
    if season == 'christmas':
        return 'Merry Christmas'

    if season == 'easter':
        return 'Happy Easter'
    
    if season == 'newyear':
        return 'Happy New Year!'
    
    if season == 'valentines_day':
        return "Happy Valentine's Day! " + "Kiss those you love."

    if season == 'independence_day':
        return "Happy Independence Day " + "Don't Tread On Me! -Metallica"

#Below is a test of the text in the tutorial file under week 8 on canvas.
#@app.route('/blog/<int:postID>')
#def show_blog(postID):
#    return 'Blog Number {0} '.format(postID)

#@app.route('/rev/<float:revNo>')
#def revision(revNo):
#    return 'Revision Number {0} '.format(revNo)

#Below I will create a database for holiday greeting cards at a store.
#def create_database():
#    conn = sql.connect("StoreHolidayCards.db")
#    conn.execute("CREATE TABLE Holiday_Cards (title TEXT, season TEXT, recipientFName TEXT, recipientLName TEXT, price CURRENCY)")
#    conn.close()

#create_database()

#I will now add another database for customer data 3/23/2021
#def create_database():
#    conn = sql.connect("customers.db")
#    conn.execute("CREATE TABLE customers (fname TEXT, lname TEXT, email TEXT, address TEXT, street TEXT, city TEXT, hpnum TEXT)")
#    conn.close()

#create_database()

#I will be using the HTML POST method to pass data to the database to make my website look more professional.
@app.route('/myform')
def addCustomer():
    return render_template('myCustomerForm.html')

@app.route('/customerTable')
def existing_Customers():
    con = sql.connect('customers.db')
    con.row_factory = sql.Row #pulls sql data and assigns it to an internal data structure in the website.
    cur = con.cursor()
    cur.execute('SELECT * FROM customers')

    rows = cur.fetchall()
    return render_template('customerTable.html', rows = rows)

#attempting to code the form to work tuning on 3/29/2021
@app.route('/addcustomer', methods = ["POST"])
def addcustomer():#Remember to check capitalization on these methods Mitchell.
    if request.method == "POST":#4:25 pm 3/29/2021 I imported request and that fixed the issue.
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        address = request.form["address"]
        street = request.form["street"]
        city = request.form["city"]
        hpnum = request.form["hpnum"]

        with sql.connect("customers.db") as con:
            cur = con.cursor()
            cur.execute('INSERT INTO customers (fname, lname, email, address, street, city, hpnum) VALUES (?, ?, ?, ?, ?, ?, ?)', [fname, lname, email, address, street, city, hpnum])
        con.commit()

        return render_template("customerTable.html")

if __name__ == '__main__':
    app.run(debug=True)