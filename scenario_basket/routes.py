import datetime
import os

from flask import Blueprint, request, render_template, current_app, session
from werkzeug.utils import redirect
from access import login_permission_required, login_required
from DB.dbcon import work_with_db, make_update, change_db
from DB.sql_provider import SQL_Provider
from scenario_basket.utils import add_to_basket, clear_basket

basket_app = Blueprint('basket', __name__, template_folder='templates')

provider = SQL_Provider(os.path.join(os.path.dirname(__file__), 'sql'))


@basket_app.route('/choose_client', methods=['GET', 'POST'])
def choose_client():
    if request.method == 'GET':
        items = work_with_db(current_app.config['DB_CONFIG'],
                             provider.get('client_table_name.sql'))
        return render_template('client_menu.html', res=items,
                               name=['Покупатель', 'Дата рождения', 'Бонусные мили'])
    session["C_id"] = request.form.get('C_id')

    return redirect('/basket/')


@basket_app.route('/', methods=['POST', 'GET'])
@login_required
def basket():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        C_id = session.get("C_id", None)
        if not C_id:
            return redirect('/basket/choose_client')
        params = {
            'Airport_out': request.args.get('Airport_out', ''),
            'Airport_in': request.args.get('Airport_in', ''),
            'T_class': request.args.get('T_class', ''),
            'Flight_date': request.args.get('Flight_date', ''),
            'Flight_num': request.args.get('Flight_num', '')
        }
        request_str = "1 = 1"
        for param in params:
            if params[param]:
                request_str += ' and ' + param + " = '" + params[param] + "'"

        sql = provider.get('Ticket_table.sql', req=request_str)
        result = work_with_db(config=db_config, sql=sql)

        current_basket = session.get('basket', [])
        result = [[result[i], 1] for i in range(len(result))]
        sql1 = provider.get('name.sql', C_id=C_id)
        result1 = work_with_db(config=db_config, sql=sql1)

        return render_template('basket_order_list.html', items=result, basket=current_basket, c_name=result1[0])

    T_id = request.form.get('T_id', None)
    ordered_number = request.form.get('ordered_number', None)
    sql = provider.get('order_item.sql', id=T_id)
    items = work_with_db(config=db_config, sql=sql)
    if not items:
        return ''
    add_to_basket([items[0], ordered_number])
    return redirect(request.url)


@basket_app.route('/clear', methods=['POST', 'GET'])
def clear_basket_handler():
    clear_basket()
    return redirect('/basket')


@basket_app.route('/buy', methods=['POST', 'GET'])
def buy_items():
    db_config = current_app.config['DB_CONFIG']
    basket = session.get('basket', [])
    client_id = session.get('C_id')
    for item in basket:
        sql = provider.get('insert_item.sql', **item[0], count=item[1], client_id=client_id)
        sql1 = provider.get('update_customer.sql', **item[0], count=item[1], client_id=client_id)
        result = make_update(db_config, sql)
        result1 = make_update(db_config, sql1)
        if not result:
            return render_template('Error_result.html')
        if not result1:
            return render_template('Error_result.html')

        clear_basket()
    session.pop('C_id')
    return redirect('/basket')


@basket_app.route('/sql_change_1', methods=['GET', 'POST'])
def change_tests():
    if request.method == 'GET':
        return render_template('change_client_table.html')
    else:
        value1 = request.form.get('value1', None)
        value2 = request.form.get('value2', None)
        value3 = request.form.get('value3', None)
        print(value1, value2, value3)
        if value1 and value2:
            sql = provider.get('insert_new_client.sql', gener1=value1, gener2=value2, gener3=value3)
            print(sql)
            if not change_db(current_app.config['DB_CONFIG'], sql):
                return 'Error input'
            return redirect('/basket/choose_client')
        else:
            return 'Not found value'


@basket_app.route('/delete', methods=['GET', 'POST'])
def delete():
    print(1)
    client_id = request.form.get('C_id')
    print(client_id)
    sql = provider.get('delete_client.sql', C_id=client_id)
    print(sql)
    key = change_db(current_app.config['DB_CONFIG'], sql)
    if key:
        return redirect('/basket/choose_client')
    return 'Error input'
