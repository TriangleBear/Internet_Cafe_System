from flask import Flask, render_template, flash, request, session, redirect, url_for
from flask_mysqldb import MySQL
import mysql.connector


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'internet_cafe_system'


mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('login'),code=302)

@app.route('/login',methods=['POST','GET'])
def login():
    status=True
    cur=mysql.connection.cursor()
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user_type='admin'
        cur.execute("select * from user where username=%s and password=%s and user_type=%s",(username,password,user_type))
        data=cur.fetchone()
        if data:
            session['logged_in']=True
            session['username']=data[1]
            print('Login Successful!')
            mysql.connection.close()
            return redirect('home')
        else:
            print('username, password or user type invalid')
    cur.close()
    return render_template("/Login/login.html")

@app.route('/home',methods=['POST','GET'])
def home():
    return render_template('/Home/home.html')

@app.route('/payment',methods=['POST','GET'])
def payment():
    return render_template('/Payment/payment.html')

@app.route('/payment-1',methods=['POST','GET'])
def payment1():
    return render_template('/Payment/payment-pc1.html')


@app.route('/account',methods=['POST','GET'])
def account():
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * FROM user
                INNER JOIN contact
                ON user.user_id = contact.user_id
                INNER JOIN payment
                ON user.user_id = payment.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Account/account.html', user = ucp)

@app.route('/new-account',methods=['POST','GET'])
def new_account():
    msg=''
    cur = mysql.connection.cursor()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        mobile = request.form['mobile']
        email = request.form['e-mail']
        address = request.form['address']
        cur.execute("""
                SELECT * FROM user
                WHERE username = %s
                """, (username,))
        ucp = cur.fetchone()
        if ucp:
            mSG='Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg='Username must contain only character ad number!'
        elif not username or not password:
            msg='Please fill out the form!'
        else:
            cur.execute("""
                        INSERT INTO user VALUES(
                            NULL,
                            %s,
                            %s,
                            %s
                        )
                        """,(username,password,user_type))
            mysql.connection.commit()
            cur.execute("""
                        INSERT INTO contact VALUES(
                            NULL,
                            (SELECT user_id from user WHERE username=%s),
                            %s,
                            %s,
                            %s
                        )
                        """,(username, mobile,email,address,))
            mysql.connection.commit()
    elif request.method == 'POST':
        print('Please fill out the form')
    cur.execute("""
                SELECT * FROM user
                INNER JOIN contact
                ON user.user_id = contact.user_id
                INNER JOIN payment
                ON user.user_id = payment.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    return render_template('/Account/acc_new.html', user=ucp)


@app.route('/edit-account',methods=['POST','GET'])
def edit_account():
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * FROM user
                INNER JOIN contact
                ON user.user_id = contact.user_id
                INNER JOIN payment
                ON user.user_id = payment.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Account/acc_edit.html', user = ucp)

@app.route('/recharge-account',methods=['POST','GET'])
def recharge_account():
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * FROM user
                INNER JOIN contact
                ON user.user_id = contact.user_id
                INNER JOIN payment
                ON user.user_id = payment.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Account/acc_recharge.html', user = ucp)

@app.route('/submit-recharge',methods=['POST','GET'])
def recharge_account_submit():
    cur=mysql.connection.cursor()
    if request.method =='POST':
        username=request.form['username']
        rechargeAm=request.form['balance']
        cur.execute("""
                    SELECT SUM(balance + %i) 
                    FROM payment
                    GROUP BY user_id
                    """,(rechargeAM))
        ucp = cur.fetchall()
        return render_template('/Account/acc_recharge.html', user = ucp)


@app.route('/history-account',methods=['POST','GET'])
def history_account():
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * FROM user
                INNER JOIN contact
                ON user.user_id = contact.user_id
                INNER JOIN payment
                ON user.user_id = payment.user_id
                INNER JOIN timeslot
                ON user.user_id = timeslot.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Account/acc_history.html', user = ucp)

@app.route('/disable-account',methods=['POST','GET'])
def disable_account():
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * FROM user
                INNER JOIN contact
                ON user.user_id = contact.user_id
                INNER JOIN payment
                ON user.user_id = payment.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Account/acc_disable.html', user = ucp)



@app.route('/report',methods=['POST','GET'])
def report():
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * FROM user
                INNER JOIN payment
                ON user.user_id = payment.user_id
                INNER JOIN timeslot
                ON user.user_id = timeslot.user_id
                """)
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Reports/reports.html', user=ucp)


@app.route('/submit-report',methods=['POST','GET'])
def submit_report():
    fromData=request.form['from']
    toData=request.form['to']
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * FROM timeslot
                WHERE tmslt_in=%s AND
                tmslt_out=%s
                """,(fromData,toData))
    ucp = cur.fetchall()
    print(ucp)
    cur.close()
    return render_template('/Reports/reports.html', user=ucp)


@app.route('/terminal',methods=['POST','GET'])
def terminal():
    return render_template('/Terminal/terminal.html')

@app.route('/submit-terminal',methods=['POST','GET'])
def submit_terminal():
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * FROM user
                INNER JOIN payment
                ON user.user_id = payment.user_id
                INNER JOIN timeslot
                ON user.user_id = timeslot.user_id
                """)
    terminaltime = cur.fetchall()
    print(terminaltime)
    cur.close()
    return render_template('/Terminal/terminal-pc1.html', user =terminaltime)

@app.route('/terminal1',methods=['POST','GET'])
def terminal1():
    return render_template('/Terminal/terminal-pc1.html')



@app.route('/message',methods=['POST','GET'])
def message():
    return render_template('/Message/message.html')

@app.route('/message1',methods=['POST','GET'])
def message1():
    return render_template('/Message/message-pc1.html')



@app.route('/logout',methods=['POST','GET'])
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = 'debugPhaseTotallyAccurateSecretKey69'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
    