from flask import Blueprint, render_template, request, current_app
from access import login_permission_required, login_required
from DB.sql_provider import SQL_Provider
from DB.dbcon import change_db, work_with_db
import os

app_sql = Blueprint('Select_sql', __name__, template_folder='templates')
provider = SQL_Provider(os.path.join(os.path.dirname(__file__), 'sql'))


@app_sql.route("/")
@login_required
def query_list():
    return render_template('select_menu_new.html')


@app_sql.route('/tsk1', methods=['GET', 'POST'])
@login_permission_required
def sql1():
    if request.method == 'GET':
        return render_template('user_input_tsk1.html')
    else:
        XX = request.form.get('XX')
        print(XX)
        if XX != "":
            sql = provider.get('1.sql', number=XX)
            print(sql)
            result = work_with_db(current_app.config['DB_CONFIG'], sql=sql)
            print(result)
            if not result:
                return render_template('Error_result.html')
            else:
                stroka = result
                res_keys = result[0].keys()
        else:
            return render_template('Error_result.html')
        keyList = ['Ф.И.О', 'Дата рождения', 'Бонус', 'Рейс', 'Цена']
        context = {'itemList': stroka, 'keys': res_keys, 'k_list': keyList}
        return render_template('result_1.html', **context)


@app_sql.route('/tsk2', methods=['GET', 'POST'])
@login_permission_required
def sql2():
    if request.method == 'GET':
        return render_template('user_input_tsk2.html')
    else:
        month = request.form.get('month')
        year = request.form.get('year')
        if month != "" and year != "":
            sql = provider.get('2.sql', month=month, year=year)
            result = work_with_db(current_app.config['DB_CONFIG'], sql=sql)
            if not result:
                return render_template('Error_result.html')
            else:
                stroka = result
                res_keys = result[0].keys()
        else:
            return render_template('Error_result.html')
        keyList = ['Номер клиента', 'Ф.И.О', 'Дата рождения']
        context = {'itemList': stroka, 'keys': res_keys, 'k_list': keyList}
        return render_template('result_2.html', **context)


@app_sql.route('/tsk3', methods=['GET', 'POST'])
@login_permission_required
def sql3():
    if request.method == 'GET':
        return render_template('user_input_tsk3.html')
    else:
        year = request.form.get('year')
        if year != "":
            sql = provider.get('3.sql', year=year)
            result = work_with_db(current_app.config['DB_CONFIG'], sql=sql)
            if not result:
                return render_template('Error_result.html')
            else:
                stroka = result
                res_keys = result[0].keys()
        else:
            return render_template('Error_result.html')
        keyList = ['Ф.И.О', 'Насичление бонусов']
        context = {'itemList': stroka, 'keys': res_keys, 'k_list': keyList}
        return render_template('result_3.html', **context)


