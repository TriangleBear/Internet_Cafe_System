from logging import WARNING, FileHandler
import os
from flask import Flask, render_template, flash, request, session, redirect, url_for
from datetime import datetime
import mysql.connector

app = Flask(__name__)
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="internet_cafe_system"
)


@app.route('/')
def index():
    return redirect(url_for('login'), code=302)


@app.route('/login', methods=['POST', 'GET'])
def login():
    status = True
    cur = mydb.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = 'admin'
        cur.execute("select * from user where username=%s and password=%s and user_type=%s",
                    (username, password, user_type))
        data = cur.fetchone()
        if data:
            session['logged_in'] = True
            session['username'] = data[1]
            print('Login Successful!')
            return redirect('/home')
        else:
            print('username, password or user type invalid')
    return render_template("/Login/login.html")


@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('/Home/home.html')


@app.route('/payment', methods=['POST', 'GET'])
def payment():
    return render_template('/Payment/payment.html')


@app.route('/payment-1', methods=['POST', 'GET'])
def payment1():
    cur = mydb.cursor()
    if request.method == 'POST' and 'username' in request.form and 'time-in' in request.form and 'time-out' in request.form:
        username = request.form['username']
        balance = request.form['balance']
        timeIn = request.form['time-in']
        timeOut = request.form['time-out']
        duration = request.form['duration']
        rate = 15
        if not username:
            print('No Username in Field')
        else:
            cur.execute("""
                        INSERT INTO timeslot VALUES(
                            NULL,
                            (SELECT rg_id FROM report_generator JOIN user ON user.user_id=report_generator.user_id WHERE user.username=%s),
                            (SELECT user_id from user WHERE username=%s),
                            NULL,
                            NULL,
                            %s,
                            %s,
                            NULL
                        )
                        """, (username, username, timeIn, timeOut, duration, timeIn, timeOut))
            cur.execute("""
                        UPDATE timeslot
                        SET
                        tmsl_durtn = (SELECT TIMESTAMPDIFF(HOURS, tmslt_in, tmslt_out) FROM timeslot)
                        """)
            mydb.commit()
    return render_template('/Payment/payment-pc1.html')


@app.route('/account', methods=['POST', 'GET'])
def account():
    cur = mydb.cursor()
    cur.execute("""
                SELECT user.username, contact.mobile_num, contact.email, contact.address
                FROM user JOIN contact
                ON user.user_id = contact.user_id
                """)
    dataAcc = cur.fetchall()
    print(dataAcc)
    return render_template('/Account/account.html', data=dataAcc)


@app.route('/new-account', methods=['POST', 'GET'])
def new_account():
    msg = ''
    cur = mydb.cursor()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        mobile = request.form['mobile']
        email = request.form['e-mail']
        address = request.form['address']
        if not username or not password:
            msg = 'Please fill out the form!'
        else:
            cur.execute("""
                        INSERT INTO user VALUES(
                            NULL,
                            %s,
                            %s,
                            %s
                        )
                       """, (username, password, user_type))
            cur.execute("""
                        INSERT INTO contact VALUES(
                            NULL,
                            (SELECT user_id from user WHERE username=%s),
                            %s,
                            %s,
                            %s
                        )
                        """, (username, mobile, email, address,))
            mydb.commit()
    cur.execute("""
                SELECT user.username, contact.mobile_num, contact.email, contact.address
                FROM user JOIN contact
                ON user.user_id = contact.user_id
                """)
    dataAcc = cur.fetchall()
    print(dataAcc)
    return render_template('/Account/acc_new.html', user=dataAcc)


@app.route('/edit-account', methods=['POST', 'GET'])
def edit_account():
    cur = mydb.cursor()
    userID = cur.fetchone()
    if request.method == 'POST' and 'user_id' in request.form and 'username' in request.form and 'mobile_num' in request.form and 'email' in request.form and 'address' in request.form:
        name = request.form['username']
        mobile = request.form['mobile_num']
        email = request.form['email']
        address = request.form['address']
        edi = request.form['user_id']
        cur.execute("""SELECT user.username, contact.mobile_num, contact.email, contact.address
                    FROM user JOIN contact ON user.user_id = contact.user_id
                    WHERE user_id = % s""", (edi))
        if not name:
            print('name must contain only characters and numbers !')
        else:
            cur.execute("""UPDATE user 
                        SET  
                        username =% s, 
                        mobile_num =%s, 
                        email =%s, 
                        address =%s 
                        WHERE user_id =%s""", (name, mobile, email, address, edi))
            mydb.commit()
            print('User updated !')
            return render_template('/Account/acc_edit.html', user=userID)
    else:
        print('Please fill out the form !')# Above is ignore for debug reason
    return render_template('/Account/acc_edit.html', user=userID)

@app.route('/recharge-account', methods=['POST', 'GET'])
def recharge_account():
    cur = mydb.cursor()
    cur.execute("""
                SELECT user.username, payment.bill_num
                FROM user JOIN payment
                ON user.user_id = payment.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Account/acc_recharge.html', user=ucp)


@app.route('/submit-recharge', methods=['POST', 'GET'])
def recharge_account_submit():
    cur = mydb.cursor()
    if request.method == 'POST':
        username = request.form['username']
        recharge = request.form['balance']
        if not username:
            print('Account recognized')
        else:
            cur.execute("""INSERT INTO report_generator VALUES(
                            NULL,
                            (SELECT user_id from user WHERE username=%s),
                            "Customer Recharge",
                            "%s Credits added!"
                            )""", (username, recharge,))

            cur.execute("""INSERT INTO payment VALUES(
                            NULL,
                            (SELECT user_id from user WHERE username=%s),
                            (SELECT rg_id FROM report_generator JOIN user ON user.user_id=report_generator.user_id WHERE user.username=%s),
                            %s
                        )""", (username, username, recharge))
            mydb.commit()
    cur.execute("""
                SELECT user.username, payment.bill_num
                FROM user JOIN payment
                ON user.user_id = payment.user_id
                """)
    rech = cur.fetchall()
    return render_template('/Account/acc_recharge.html', user=rech)


@app.route('/history-account', methods=['POST', 'GET'])
def history_account():
    cur = mydb.cursor()
    cur.execute("""
                SELECT user.username, report_generator.rg_desc, report_generator.rg_desc
                FROM user JOIN report_generator
                ON user.user_id = report_generator.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Account/acc_history.html', user=ucp)

@app.route('/disable-account/', methods=['POST', 'GET'])
def disable_account():
    cur = mydb.cursor()
    cur.execute("""
                SELECT user.username, contact.mobile_num, contact.email, contact.address
                FROM user JOIN contact
                ON user.user_id = contact.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Account/acc_disable.html', user=ucp)


@app.route('/report', methods=['POST', 'GET'])
def report():
    cur = mydb.cursor()
    cur.execute("""
                SELECT user.username, contact.mobile_num, contact.email, contact.address
                FROM user JOIN contact
                ON user.user_id = contact.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Reports/reports.html', user=ucp)


@app.route('/submit-report', methods=['POST', 'GET'])
def submit_report():
    fromData = request.form['from']
    toData = request.form['to']
    cur = mydb.cursor()
    cur.execute("""
                SELECT * FROM timeslot
                WHERE tmslt_in=%s AND
                tmslt_out=%s
                """, (fromData, toData))
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Reports/reports.html', user=ucp)


@app.route('/terminal', methods=['POST', 'GET'])
def terminal():
    return render_template('/Terminal/terminal.html')


@app.route('/submit-terminal', methods=['POST', 'GET'])
def submit_terminal():
    cur = mydb.cursor()
    cur.execute("""
                SELECT user.username, contact.mobile_num, contact.email, contact.address
                FROM user JOIN contact
                ON user.user_id = contact.user_id
                """)
    terminaltime = cur.fetchall()
    print(terminaltime)
    cur.close()
    return render_template('/Terminal/terminal-pc1.html', user=terminaltime)


@app.route('/terminal1', methods=['POST', 'GET'])
def terminal1():
    return render_template('/Terminal/terminal-pc1.html')


@app.route('/message', methods=['POST', 'GET'])
def message():
    return render_template('/Message/message.html')


@app.route('/message1', methods=['POST', 'GET'])
def message1():
    return render_template('/Message/message-pc1.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
