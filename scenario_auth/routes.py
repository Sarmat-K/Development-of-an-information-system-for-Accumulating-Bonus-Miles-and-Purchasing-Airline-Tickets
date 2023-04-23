from flask import Blueprint, render_template, session, request, current_app, redirect
from DB.sql_provider import SQL_Provider
from DB.dbcon import change_db, work_with_db
import os

auth_app = Blueprint('auth_app', __name__, template_folder='templates')
provider = SQL_Provider(os.path.join(os.path.dirname(__file__), 'sql'))


@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')
        sql = provider.get('auth.sql', log=login, pas=password)
        name_group = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not name_group:
            return render_template("index3.html")
        session['group_name'] = name_group[0]['user_group']
        return render_template("index_process.html")
