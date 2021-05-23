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
def hello_world():
    print("aubonee")
    user = request.args.get('name')
    print(user)
    return render_template("Home.html")


@app.route('/data', methods=['GET', 'POST'])
def hello_world58():
    if request.method == 'POST' and request.form['password'] == "":
        return render_template("adminblank.html")
    else:
        if request.method == 'POST' and request.form['password'] == "admin":
            mycursor.execute("SELECT * FROM car")
            myresult = mycursor.fetchall()
            return render_template("datashow.html", data=myresult)
        else:
            return render_template("invalid.html")


# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("John", "Highway 21")
# mycursor.execute(sql, val)
@app.route('/a', methods=['GET', 'POST'])
def hello_world20():
    # print("aubonee1")
    return render_template('about.html')


@app.route('/l', methods=['GET', 'POST'])
def hello_world1():
    return render_template('Login.html')


@app.route('/cc', methods=['GET', 'POST'])
def hello_world19():
    return render_template('contact_us.html')


@app.route('/ad', methods=['GET', 'POST'])
def hello_world12():
    return render_template('admin_panel.html')


@app.route('/d', methods=['GET', 'POST'])
def hello_world8():
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
                return render_template('Done.html', result=result)
            except mysql.connector.IntegrityError as ierror:
                return render_template("duplicate.html")
        else:
            return render_template("gap.html")
    else:
        return render_template("book.html")


@app.route('/s', methods=['GET', 'POST'])
def hello_world6():
    return render_template('slotcancel.html')


@app.route('/p', methods=['GET', 'POST'])
def hello_world61():
    return render_template('paid.html')


@app.route('/b', methods=['GET', 'POST'])
def hello_world5():
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
        return render_template('Bill.html', bill=cost)
    else:
        return render_template("unauthorized.html")


if __name__ == '__main__':
    app.run()
