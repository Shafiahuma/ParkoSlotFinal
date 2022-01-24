from flask import Flask, render_template, request, redirect, jsonify, json
import mysql.connector
from mysql.connector import cursor

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="huma@123",
    database="carparking"
)
mycursor = mydb.cursor()


@app.route('/', methods=['GET', 'POST'])
def homePage():
    print("aubonee")
    user = request.args.get('name')
    print(user)
    return render_template("new-templates/index.html")


@app.route('/admin-dashboard', methods=['GET', 'POST'])
def adminDashboard():
    if request.method == 'POST' and request.form['password'] == "":
        return render_template("adminblank.html")
    else:
        if request.method == 'POST' and request.form['password'] == "admin":
            mycursor.execute("SELECT * FROM car")
            myresult = mycursor.fetchall()
            return render_template("new-templates/admin-dashboard.html", data=myresult)
        else:
            return render_template("invalid.html")


# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("John", "Highway 21")
# mycursor.execute(sql, val)
@app.route('/about', methods=['GET', 'POST'])
def aboutUs():
    # print("aubonee1")
    return render_template("new-templates/aboutus.html")


@app.route('/slot-booking', methods=['GET', 'POST'])
def slotBooking():
    return render_template("new-templates/slotbooking.html")


@app.route('/contact-us', methods=['GET', 'POST'])
def contactUs():
    return render_template("new-templates/contact.html")


@app.route('/admin-panel', methods=['GET', 'POST'])
def adminPanel():
    return render_template("new-templates/adminpanel.html")


@app.route('/booking-done', methods=['GET', 'POST'])
def bookingDone():
    global result
    check = "select count(id) from car;"
    mycursor.execute(check)
    count = mycursor.fetchall()
    x = count[0][0]
    if x < 30:
        if request.method == 'POST' and request.form['name'] != "":
            try:
                sql = "INSERT INTO car(u_name,city_and_c_exte,c_number,phone) VALUES (%s, %s, %s , %s)"
                val = (request.form.get('name'), request.form.get('city_and_c_exte'), request.form.get('carnumber'),
                       request.form.get('phone'),)
                mycursor.execute(sql, val)
                mydb.commit()
                result = request.form
                return render_template("new-templates/bookconfirm.html", result=result)
            except mysql.connector.IntegrityError as ierror:
                return render_template("duplicate.html")
        else:
            return render_template("gap.html")
    else:
        return render_template("book.html")


@app.route('/slot-cancel', methods=['GET', 'POST'])
def slotCancel():
    return render_template("new-templates/slotcancel.html")


@app.route('/p', methods=['GET', 'POST'])
def hello_world61():
    return render_template('paid.html')


@app.route('/booking-cancel', methods=['GET', 'POST'])
def bookingCancel():
    if request.method == 'POST' and request.form['name'] != "":
        # print("GG")
        val = request.form['phone']
        print(type(val))
        try:
            sql = "select TIMESTAMPDIFF(second , (select e_time from car where phone = %s), CURRENT_TIMESTAMP);"
            adr = (val,)
            mycursor.execute(sql, adr)
            myresult = mycursor.fetchall()
            cost = myresult[0][0] * .05
        except Exception:
            print("asdfg")

        #  x=myresult
        # y=x*.05
        #   print(y)

        # for x in myresult:
        #  print(x)

        sql = "DELETE FROM car WHERE phone= %s"
        mycursor.execute(sql, adr)
        mydb.commit()
        return render_template("new-templates/cancelconfirm.html", bill=cost)
    else:
        return render_template("unauthorized.html")


if __name__ == '__main__':
    app.run()
