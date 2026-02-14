import flask_login
from flask import render_template, redirect, Flask, flash
from apps.app.forms import Register, SIGN
from sqlite3 import connect
from apps.config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, LoginManager
from flask_login import UserMixin
from apps.app.Models import User


app = Flask(__name__)
app.config.from_object(Config)

print('START')
print(generate_password_hash('admin'))

db = connect('site.db', check_same_thread=False)
cursor = db.cursor()
login_manager = LoginManager()

cursor.execute(f"UPDATE AU SET PASS = '{generate_password_hash('admin')}' WHERE USERS = 'admin'")

login_manager.init_app(app)
@login_manager.user_loader
def user_loader(user_id):
    return User.id


@app.route('/')
@app.route('/index')
def index():
    cursor.execute('SELECT * FROM AU')
    users = cursor.fetchall()
    for i in users:
        print(i[0])
    return render_template('index.html', title='index')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    reg = Register()
    if reg.validate_on_submit():
        cursor.execute(f"SELECT USERS FROM AU WHERE USERS = '{reg.user}'")
        con = cursor.fetchone()
        if not(con):
            cursor.execute(f"INSERT INTO AU(USERS, FIO, PASS, TYPE) VALUES ('{reg.user.data}','{reg.fio.data}','{generate_password_hash(str(reg.password.data))}', 'std')")
            db.commit()
            return redirect('/index')
        else:
            print(con)
    return render_template('Reg.html', title='Register', form=reg)

@app.route('/in', methods=['GET', 'POST'])
def sign():
    sign = SIGN()
    if sign.validate_on_submit():
        cursor.execute(f"SELECT * FROM AU WHERE USERS = '{sign.user.data}'")
        con = cursor.fetchone()
        if (con):
            if check_password_hash(con[3],sign.password.data):
                user = User(con[1])
                login_user(user=user)
                print()
                match con[4]:
                    case 'std' : return redirect('/stdmain')
            else: flash('Invalid username or password')
            return redirect('/in')
        else:
            flash('Invalid username or password')
            return redirect('/in')
        users = cursor.fetchall()
    return render_template('AUTO.html', title='Register', form=sign)

@app.route('/stdmain')
@flask_login.login_required
def stdmain():
    if usrtypecheck()!='std':
        return render_template('403.html')
    return render_template('stdmain.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')



def usrtypecheck():
    return cursor.execute(f"SELECT TYPE FROM AU WHERE USERS = '{flask_login.current_user}'")




