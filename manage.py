from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql
#sql is an alias for sqlite3
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/Index')
def Index_page():
    return render_template('Index.html')

@app.route("/boot")
def boot_page():
    return render_template("boot.html")

@app.route("/page/<message>")
def page_message(message):
    return "you entered {0}".format(message)

@app.route("/number/<int:num>")
def number_num(num):
    return "you entered {0}".format(num)

@app.route("/user/<username>")
def user_page(username):
    if username == "admin":
        return "welcome admin"
    else:
        return "Welcome users"

#passing name address and city to the database
@app.route("/save/<string:name>/<string:address>/<string:city>")
def save_data(name, address, city):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute('INSERT INTO students (name, address, city) VALUES (?, ?, ?)', [name, address, city])
    con.commit()

    return "record successfully added {0} {1} {2}".format(name, address, city)

@app.route("/list")
def list_data():
    con = sql.connect("database.db")
    con.row_factory = sql.Row #pulls sql data and assigns it to an internal data structure
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    
    rows = cur.fetchall()
    return render_template("list.html", rows = rows)

@app.route("/student")
def new_student():
    return render_template("student.html")

@app.route("/addRecord", methods=["POST"])
def addRecord():
    if request.method == "POST":
        name = request.form["nm"]#parse the data if the used method on the page is post
        addr = request.form["add"]
        city = request.form["city"]

        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('INSERT INTO students (name, address, city) VALUES (?, ?, ?)', [name, addr, city])
        con.commit()

        return render_template("list.html")

# def create_database():
#     conn = sql.connect("database.db")
#     conn.execute("CREATE TABLE students (name TEXT, address TEXT, city TEXT)")
#     conn.close()

# create_database()

if __name__ == '__main__':
    app.run(debug=True)