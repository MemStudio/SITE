#-*-coding: utf-8-*-
import csv
import flask_login
from flask import render_template, redirect, Flask, flash, request, send_file
from apps.app.forms import *
from sqlite3 import connect
from apps.config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from flask_login import UserMixin
from apps.app.Models import User



app = Flask(__name__)
app.config.from_object(Config)
app.json.ensure_ascii = False

date = ''

print('START')
print(generate_password_hash('admin'))

db = connect('site.db', check_same_thread=False)

cursor = db.cursor()
login_manager = LoginManager()

cursor.execute(f"UPDATE AU SET PASS = '{generate_password_hash('admin')}' WHERE USERS = 'admin'")

login_manager.init_app(app)
@login_manager.user_loader
def user_loader(user_id):
    return User(user_id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='index')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated:
        match usrtypecheck():
            case 'std' : return redirect('/stdmain')
    reg = Register()
    if reg.validate_on_submit():
        cursor.execute(f"SELECT USERS FROM AU WHERE USERS = '{reg.user.data}'")
        con = cursor.fetchone()
        print(con)
        if not(con):
            cursor.execute(f"INSERT INTO AU(USERS, FIO, PASS, TYPE) VALUES ('{reg.user.data}','{reg.fio.data}','{generate_password_hash(str(reg.password.data))}', 'std')")
            db.commit()
            return redirect('/index')
        else:
            flash(f"Пользователь {con[0]} Уже СУЩЕСТВУЕТ")

    return render_template('Reg.html', title='Register', form=reg)

@app.route('/in', methods=['GET', 'POST'])
def sign():
    if current_user.is_authenticated:
        match usrtypecheck():
            case 'std' : return redirect('/stdmain')
            case 'admin' : return redirect('/admin')
            case 'cook' : return redirect('/cook')
    sign = SIGN()
    if sign.validate_on_submit():
        cursor.execute(f"SELECT * FROM AU WHERE USERS = '{sign.user.data}'")
        con = cursor.fetchone()
        if (con):
            if check_password_hash(con[3],sign.password.data):
                user = User(con[1])
                login_user(user=user)
                print(flask_login.current_user)
                print('SUCCES')
                match con[4]:
                    case 'std' : return redirect('/stdmain')
                    case 'admin' : return redirect('/admin')
                    case 'ck' : return redirect('/control')
                    case _ : return 403
            else: flash('Invalid username or password')
            return redirect('/in')
        else:
            flash('Invalid username or password')
            return redirect('/in')
        users = cursor.fetchall()
    return render_template('AUTO.html', title='Register', form=sign)
@app.route('/du')
@login_required
def du():
    if usrtypecheck()!='admin':
        return render_template('403.html')
    cursor.execute('SELECT USER, FIO, TYPE FROM AU')
    data = cursor.fetchall()
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Write header
        writer.writerows(data)
    return send_file('output.csv', as_attachment=True)
@app.route('/dpl')
@login_required
def dpl():
    if usrtypecheck()!='admin':
        return render_template('403.html')
    cursor.execute('SELECT USER, TYPE, COUNT FROM PLAT')
    data = cursor.fetchall()
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Write header
        writer.writerows(data)
    return send_file('output.csv', as_attachment=True)
@app.route('/ds')
@login_required
def ds():
    if usrtypecheck()!='admin':
        return render_template('403.html')
    cursor.execute('SELECT * FROM STD')
    data = cursor.fetchall()
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Write header
        writer.writerows(data)
    return send_file('output.csv', as_attachment=True)
@app.route('/dpb')
@login_required
def dpb():
    if usrtypecheck()!='admin':
        return render_template('403.html')
    cursor.execute('SELECT * FROM NEED')
    data = cursor.fetchall()
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Write header
        writer.writerows(data)
    return send_file('output.csv', as_attachment=True)
@app.route('/dp')
@login_required
def dp():
    if usrtypecheck()!='admin':
        return render_template('403.html')
    cursor.execute('SELECT * FROM INGREDIENT')
    data = cursor.fetchall()
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Write header
        writer.writerows(data)
    return send_file('output.csv', as_attachment=True)
@app.route('/dz')
@login_required
def dz():
    if usrtypecheck()!='admin':
        return render_template('403.html')
    cursor.execute('SELECT * FROM ORDERS')
    data = cursor.fetchall()
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Write header
        writer.writerows(data)
    return send_file('output.csv', as_attachment=True)
@app.route('/dm')
@login_required
def dm():
    if usrtypecheck()!='admin':
        return render_template('403.html')
    cursor.execute('SELECT * FROM MENU')
    data = cursor.fetchall()
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Write header
        writer.writerows(data)
    return send_file('output.csv', as_attachment=True)

@app.route('/cooker', methods=["GET", "POST"])
@login_required
def cooker():
    if usrtypecheck()!='admin':
        return render_template('403.html')
    cursor.execute("SELECT USERS,FIO FROM AU WHERE TYPE = 'cook'")
    cook = cursor.fetchall()
    reg = Register()
    if reg.validate_on_submit():
        cursor.execute(f"SELECT USERS FROM AU WHERE USERS = '{reg.user.data}'")
        con = cursor.fetchone()
        print(con)
        if not (con):
            cursor.execute(
                f"INSERT INTO AU(USERS, FIO, PASS, TYPE) VALUES ('{reg.user.data}','{reg.fio.data}','{generate_password_hash(str(reg.password.data))}', 'cook')")
            db.commit()
            return redirect('/cooker')
        else:
            flash(f"Пользователь {con[0]} Уже СУЩЕСТВУЕТ")
    elif request.method == 'POST' and 'submit' not in request.form:
        print(request.form)
        gets = [i[0] for i in request.form.items() if i[1] == 'Удалить']
        get = gets[0]
        print('ssaa',gets)
        cursor.execute(f"DELETE FROM AU WHERE USERS = '{get}'")
        return redirect('/cooker')

    return render_template('cu.html', user=current_user.id, form=reg, als=cook)

@app.route('/stdmain', methods=['GET', 'POST'])
@login_required
def stdmain():
    initab()
    if usrtypecheck()!='std':
        return render_template('403.html')
    cursor.execute(f"SELECT FIO FROM AU WHERE USERS = '{current_user.id}'")
    FIO = cursor.fetchone()[0]
    cursor.execute(f"SELECT MONEY, ABONEMENT FROM STD WHERE USERS = '{current_user.id}'")
    data = cursor.fetchone()
    cursor.execute(f"SELECT ALLERGY FROM STD WHERE USERS = '{current_user.id}'")
    als = str(cursor.fetchone()[0]).split(',')
    print(als)
    if '' in als:
        als.remove('')
    print(als)
    atal = Allergy()
    if atal.validate_on_submit():
        print(request.form)
        cursor.execute(f"SELECT ALLERGY FROM STD WHERE USERS = '{current_user.id}'")
        old = str(cursor.fetchone()[0])
        old += f'{atal.aller.data},'
        cursor.execute(f"UPDATE STD SET ALLERGY = '{old}'")
        db.commit()
        return redirect('/stdmain')
    elif request.method == 'POST' and 'submit' not in request.form:
        print(request.form)
        gets = [i[1] for i in request.form.items() if i[1] =='Удалить']
        get = gets[0]
        cursor.execute(f"SELECT ALLERGY FROM STD WHERE USERS = '{current_user.id}'")
        old = str(cursor.fetchone()[0])
        old = old.replace(f'{get},' ,'')
        cursor.execute(f"UPDATE STD SET ALLERGY = '{old}' WHERE USERS = '{current_user.id}'")
        db.commit()
        return redirect('/stdmain')
    print(request.form)

    return render_template('stdmain.html', user=current_user.id, FIO=FIO, als=als, count=data[0],abon=data[1], form=atal)
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')
def usrtypecheck():
    print(current_user.id)
    cursor.execute(f"SELECT TYPE FROM AU WHERE USERS = '{flask_login.current_user.id}'")
    return cursor.fetchone()[0]

@app.route('/order',methods=['GET', 'POST'])
@login_required
def order():
    if usrtypecheck()!='std':
        return render_template('403.html')
    cursor.execute(f"SELECT * FROM ORDERS WHERE USERS = '{flask_login.current_user.id}'")
    orders = cursor.fetchall()
    if request.method == 'POST':
        print(request.form)
        gets = [i[0] for i in request.form.items() if i[1] == 'Отменить заказ']
        get = gets[0].split('/')
        cursor.execute(f"DELETE FROM ORDERS WHERE USERS = '{current_user.id}' AND DATE = '{get[1]}' AND TYPE = '{get[0]}'")
        cursor.execute(f"SELECT MONEY FROM STD WHERE USERS = '{current_user.id}'")
        balance = cursor.fetchone()[0]
        cursor.execute(f"SELECT COST FROM MENU WHERE (DATE, TYPE) == ('{get[1]}', '{get[0]}')")
        cost = int(cursor.fetchone()[0])
        cursor.execute(f"UPDATE STD SET MONEY = {int(balance) + cost} WHERE USERS = '{current_user.id}'")
        cursor.execute(f"INSERT INTO PLAT(TYPE, USER, COUNT) VALUES( 'Отмена Заказа','{current_user.id}', {cost})")
        db.commit()
        return redirect('/order')
    return render_template('order.html',user=current_user.id, ords=orders)


@app.route('/menu',  methods=['GET', 'POST'])
@login_required
def menu():
    if usrtypecheck()!='std':
        return render_template('403.html')
    cursor.execute(f"SELECT * FROM MENU WHERE ((DATE, TYPE) NOT IN (SELECT DATE, TYPE FROM ORDERS WHERE USERS = '{current_user.id}')) ")
    orders = cursor.fetchall()
    print(orders)
    print('orders')
    if request.method == 'POST' :
        print(request.form)
        gets = [i[0] for i in request.form.items() if i[1] == 'Заказать']
        get = gets[0].split('/')
        print(get)
        cursor.execute(f"SELECT MONEY FROM STD WHERE USERS = '{current_user.id}'" )
        balance = cursor.fetchone()[0]
        cursor.execute(f"SELECT COST FROM MENU WHERE (DATE, TYPE) == ('{get[1]}', '{get[0]}')")
        cost = int(cursor.fetchone()[0])
        if int(balance) >= cost:
            cursor.execute(f"SELECT FOOD FROM MENU WHERE (DATE, TYPE) = ('{get[1]}', '{get[0]}')")
            food = cursor.fetchone()[0]
            cursor.execute(f"SELECT FIO FROM AU WHERE USERS = '{current_user.id}'")
            fio = cursor.fetchone()[0]
            cursor.execute(f"INSERT INTO ORDERS(USERS, TYPE, DATE, FOOD, CONTROL, AB, FIO) VALUES ('{current_user.id}', '{get[0]}', '{get[1]}', '{food}' , 0, 0, '{fio}')" )
            cursor.execute(f"UPDATE STD SET MONEY = {int(balance) - cost} WHERE USERS = '{current_user.id}'")
            cursor.execute(f"INSERT INTO PLAT(TYPE, USER, COUNT) VALUES( 'Заказ','{current_user.id}', {cost})")
            db.commit()
            return redirect('/menu')
        else:
            flash("Недостаточно средств")
            return redirect('/menu')
        return redirect('/menu')
    return render_template('menu.html', user=current_user.id, ords=orders)
@app.route('/admin')
@login_required
def admin():
    if usrtypecheck()!='admin':
        return render_template('403.html')
    cursor.execute("SELECT USERS, FIO FROM AU WHERE TYPE = 'cook'")
    cook = cursor.fetchall()
    return render_template('admin.html', user=current_user.id, als=cook)


@app.route('/chng', methods=['GET', 'POST'])
@login_required
def chng():
    if usrtypecheck() != 'admin':
        return render_template('403.html')

    cp = CHGPASS()
    if cp.validate_on_submit():
        print('dd', cp.passw.data)
        cursor.execute(f"UPDATE AU SET PASS = '{generate_password_hash(cp.passw.data)}' WHERE USERS = '{current_user.id}'")
        db.commit()
        return redirect('/admin')
    return render_template('CHPASS.html', form=cp)

@app.route('/cook',  methods=['GET', 'POST'])
@login_required
def cook():
    if usrtypecheck()!='cook':
        return render_template('403.html')
    cursor.execute("SELECT* FROM INGREDIENT")
    ing = cursor.fetchall()
    form = ING()
    if form.validate_on_submit():
        cursor.execute(f"INSERT INTO INGREDIENT(ING, COUNT, COST) VALUES ('{form.ingr.data}', 0.0, {form.count.data})")
        db.commit()
        return redirect('/cook')
    elif request.method == 'POST' and 'submit' not in request.form:
        print(request.form)
        gets = [i[1] for i in request.form.items()]
        gets2=[i[0] for i in request.form.items()]
        print(gets2)
        get = gets[0]
        get2 = gets2[0]
        cursor.execute(f"SELECT COST FROM INGREDIENT WHERE ING = '{get2}'")
        cost = cursor.fetchone()[0]
        cursor.execute(f"INSERT INTO NEED(ING, COST, NEED, TYPE) VALUES('{get2}', {float(get)}, {cost}, 0)")
        db.commit()
    return render_template('cook.html',user=current_user.id, als=ing, form=form)

@app.route('/menuop',  methods=['GET', 'POST'])
@login_required
def menuop():
    if usrtypecheck()!='cook':
        return render_template('403.html')
    cursor.execute('SELECT * FROM MENU')
    m = cursor.fetchall()
    food = FOOD()
    if food.validate_on_submit():
        cursor.execute(f"INSERT INTO MENU(TYPE, DATE, FOOD, COST) VALUES ('{food.type.data}','{food.date.data}','{food.food.data}',{food.cost.data})")
        db.commit()
        return redirect('/menuop')
    elif request.method == 'POST' and 'submit' not in request.form:
        gets = [i[0] for i in request.form.items() if i[1] == 'Удалить']
        get = gets[0].split('/')

        cursor.execute(f"DELETE FROM MENU WHERE (TYPE, DATE) = ('{get[0]}', '{get[1]}')")
        return redirect('/menuop')

    return render_template('menuop.html', form=food, als=m)

@app.route('/work',  methods=['GET', 'POST'])
@login_required
def work():
    if usrtypecheck()!='cook':
        return render_template('403.html')

    cursor.execute('SELECT USERS, TYPE, DATE, FIO FROM ORDERS WHERE (DATE, CONTROL) = (date("now"), 0)')
    ord = cursor.fetchall()
    if request.method == 'POST' and 'submit' not in request.form:
        print(request.form)
        gets = [i[1] for i in request.form.items() if i[1] == 'Выдать']
        if gets:
            get = gets[0].split('/')
            cursor.execute(f"UPDATE ORDERS SET CONTROL = 1 WHERE (USERS, TYPE, DATE) = ('{get[0]}', '{get[1]}', '{get[2]}')")
            db.commit()
            return redirect('/work')
        else:
            cursor.execute(f"UPDATE ORDERS SET CONTROL = 2 WHERE (DATE, CONTROL) = (date('now'), 0)")
            db.commit()
            return redirect('/zp')
    return render_template('sm.html', user=current_user.id, als=ord)


@app.route('/ost')
@login_required
def ost():
    if usrtypecheck()!='cook':
        return render_template('403.html')
    return 'ost'

@app.route('/ba', methods = ['GET','POST'])
@login_required
def ba():
    if usrtypecheck()!='std':
        return render_template('403.html')
    cursor.execute(f"SELECT ABONEMENT FROM STD WHERE USERS = '{current_user.id}'")
    ab = cursor.fetchone()
    if ab[0]:
        print('ab', ab)
        return redirect('/stdmain')
    cursor.execute("SELECT COST FROM AB")
    abon = cursor.fetchone()[0]
    if request.method == 'POST':
        print(request.form.keys())
        if 'order' in request.form.keys():
            cursor.execute(f"UPDATE STD SET ABONEMENT = date('now', '+14 days')")
            cursor.execute(f"SELECT MONEY FROM STD WHERE USERS = '{current_user.id}'" )
            balance = cursor.fetchone()[0]
            cursor.execute(f"UPDATE STD SET MONEY = {int(balance) - abon} WHERE USERS = '{current_user.id}'")
            cursor.execute(f"INSERT INTO PLAT(TYPE, USER, COUNT) VALUES( 'Абонемент','{current_user.id}', {abon})")
            db.commit()
            return redirect('/ba')
    return render_template('ab.html', abon=abon)

@app.route('/br', methods=['GET', 'POST'])
@login_required
def br():
    if usrtypecheck()!='std':
        return render_template('403.html')
    pay = Pay()
    if pay.validate_on_submit():
        cursor.execute(f"SELECT MONEY FROM STD WHERE USERS = '{current_user.id}'")
        old = cursor.fetchone()[0]
        cursor.execute(f"UPDATE STD SET MONEY = {old + pay.count.data}")
        cursor.execute(f"INSERT INTO PLAT(TYPE, USER, COUNT) VALUES( 'Пополнение','{current_user.id}', {pay.count.data})")
        db.commit()
        return redirect('/stdmain')
    return render_template('balance.html', form=pay)


def initab():
    cursor.execute(f"SELECT ABONEMENT FROM STD WHERE USERS = '{current_user.id}'")
    ab = cursor.fetchone()
    if ab:
        ab = ab[0]
        print(ab)
    cursor.execute(f"SELECT DATE FROM ORDERS WHERE USERS = '{current_user.id}' AND AB = 1 ")
    now = cursor.fetchall()
    print(ab)
    print('now', now)
    for i in range(0, 15):
        cursor.execute(f"SELECT FOOD FROM MENU WHERE (TYPE, DATE) = ('Завтрак', date('{ab}', '-{i} days'))")
        zav = cursor.fetchone()
        if zav:
            zav = zav[0]
        cursor.execute(f"SELECT FOOD FROM MENU WHERE (TYPE, DATE) = ('Обед', date('{ab}', '-{i} days'))")
        ob = cursor.fetchone()
        cursor.execute(f"SELECT FIO FROM AU WHERE USERS = '{current_user.id}'")
        fio = cursor.fetchone()[0]
        print(fio)
        if ob:
            ob = ob[0]
        print(ob)
        if zav != None:
            cursor.execute(f"INSERT INTO ORDERS (USERS, TYPE, DATE, FOOD, CONTROL, AB, FIO) VALUES ('{current_user.id}', 'Завтрак',  date('{ab}','-{i} days'),'{zav}', 0, 1, '{fio}')")
        if ob != None:
            cursor.execute(f"INSERT INTO ORDERS (USERS, TYPE, DATE, FOOD, CONTROL, AB, FIO) VALUES ('{current_user.id}', 'Обед',  date('{ab}','-{i} days'), '{ob}', 0, 1, '{fio}')")
    cursor.execute('DELETE FROM ORDERS WHERE rowid NOT IN (SELECT MIN(rowid) FROM ORDERS GROUP BY DATE, TYPE)')
    db.commit()


