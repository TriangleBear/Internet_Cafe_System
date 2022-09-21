from flask import Flask, render_template, flash, request, session, redirect, url_for
from flask_mysqldb import MySQL


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

@app.route('/payment-2',methods=['POST','GET'])
def payment2():
    return render_template('/Payment/payment-pc2.html')

@app.route('/payment-3',methods=['POST','GET'])
def payment3():
    return render_template('/Payment/payment-pc3.html')

@app.route('/payment-4',methods=['POST','GET'])
def payment4():
    return render_template('/Payment/payment-pc4.html')

@app.route('/payment-5',methods=['POST','GET'])
def payment5():
    return render_template('/Payment/payment-pc5.html')

@app.route('/payment-6',methods=['POST','GET'])
def payment6():
    return render_template('/Payment/payment-pc6.html')

@app.route('/payment-7',methods=['POST','GET'])
def payment7():
    return render_template('/Payment/payment-pc7.html')

@app.route('/payment-8',methods=['POST','GET'])
def payment8():
    return render_template('/Payment/payment-pc8.html')

@app.route('/payment-9',methods=['POST','GET'])
def payment9():
    return render_template('/Payment/payment-pc9.html')

@app.route('/payment-10',methods=['POST','GET'])
def payment10():
    return render_template('/Payment/payment-pc10.html')

@app.route('/payment-11',methods=['POST','GET'])
def payment11():
    return render_template('/Payment/payment-pc11.html')

@app.route('/payment-12',methods=['POST','GET'])
def payment12():
    return render_template('/Payment/payment-pc12.html')




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

@app.route('/terminal2',methods=['POST','GET'])
def terminal2():
    return render_template('/Terminal/terminal-pc2.html')

@app.route('/terminal3',methods=['POST','GET'])
def terminal3():
    return render_template('/Terminal/terminal-pc3.html')

@app.route('/terminal4',methods=['POST','GET'])
def terminal4():
    return render_template('/Terminal/terminal-pc4.html')

@app.route('/terminal5',methods=['POST','GET'])
def terminal5():
    return render_template('/Terminal/terminal-pc5.html')

@app.route('/terminal6',methods=['POST','GET'])
def terminal6():
    return render_template('/Terminal/terminal-pc6.html')

@app.route('/terminal7',methods=['POST','GET'])
def terminal7():
    return render_template('/Terminal/terminal-pc7.html')

@app.route('/terminal8',methods=['POST','GET'])
def terminal8():
    return render_template('/Terminal/terminal-pc8.html')

@app.route('/terminal9',methods=['POST','GET'])
def terminal9():
    return render_template('/Terminal/terminal-pc9.html')

@app.route('/terminal10',methods=['POST','GET'])
def terminal10():
    return render_template('/Terminal/terminal-pc10.html')

@app.route('/terminal11',methods=['POST','GET'])
def terminal11():
    return render_template('/Terminal/terminal-pc11.html')

@app.route('/terminal12',methods=['POST','GET'])
def terminal12():
    return render_template('/Terminal/terminal12.html')



@app.route('/message',methods=['POST','GET'])
def message():
    return render_template('/Message/message.html')



@app.route('/logout',methods=['POST','GET'])
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = 'debugPhaseTotallyAccurateSecretKey69'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
    