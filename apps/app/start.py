from flask import render_template, redirect
from apps.app import app
from apps.app.forms import Register
from sqlite3 import connect


print('START')

db = connect('site.db', check_same_thread=False)
cursor = db.cursor()

@app.route('/')
@app.route('/index')
def index():
    cursor.execute('SELECT * FROM au')
    users = cursor.fetchall()
    for i in users:
        print(i)
    return 'LOX'

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    a = ''
    reg = Register()
    if reg.validate_on_submit():

        return redirect('/')
    return render_template('Reg.html', title='Register', form=reg)
