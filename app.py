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
    return render_template('/Reports/reports.html')

@app.route('/terminal',methods=['POST','GET'])
def terminal():
    return render_template('/Terminal/terminal.html')

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
    