import os

from flask import Blueprint, request, render_template, current_app, session
from werkzeug.utils import redirect
from DB.dbcon import work_with_db
from access import login_required
from DB.sql_provider import SQL_Provider

app_Purch = Blueprint('Purchased_tickets', __name__, template_folder='templates')
provider = SQL_Provider(os.path.join(os.path.dirname(__file__), 'sql'))


@app_Purch.route('/choose_client', methods=['GET', 'POST'])
def choose_client():
    if request.method == 'GET':
        items = work_with_db(current_app.config['DB_CONFIG'],
                             provider.get('client_name_1.sql'))
        return render_template('client_menu_purch.html', res=items,
                               name=['Покупатель', 'Дата рождения', 'Бонусные мили'])
    session["C_id"] = request.form.get('C_id')

    return redirect('/Purch/')


@app_Purch.route('/', methods=['POST', 'GET'])
@login_required
def purch():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        C_id = session.get("C_id", None)
        if not C_id:
            return redirect('/Purch/choose_client')
        current_basket = session.get('basket', [])
        sql = provider.get('sql_purch_1.sql', C_id=C_id)
        result = work_with_db(config=db_config, sql=sql)
        result = [[result[i], 1] for i in range(len(result))]
        sql1 = provider.get('name.sql', C_id=C_id)
        result1 = work_with_db(config=db_config, sql=sql1)
        session.pop('C_id')
        return render_template('Purch_ticket.html', items=result, basket=current_basket, c_name=result1[0],
                               name=['Аэропорт вылета', 'Аэропорт прилета', 'Класс билета',
                                     'Номер рейса', 'Дата покупки рейса', 'Цена',
                                     'Бонусные мили'])

