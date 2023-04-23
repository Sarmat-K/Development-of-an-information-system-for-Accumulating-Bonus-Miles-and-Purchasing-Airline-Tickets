from flask import Flask, render_template, session
from Select_sql.routes import app_sql
from scenario_auth.routes import auth_app
from scenario_basket.routes import basket_app
from Purchased_tickets.routes import app_Purch
import json

app = Flask(__name__, static_folder='templates/index_files', static_url_path='/index_files')

app.config['DB_CONFIG'] = json.load(open('configs/config.json'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))
app.config['SECRET_KEY'] = 'super secret key'

app.register_blueprint(app_sql, url_prefix='/Bonus')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(basket_app, url_prefix='/basket')
app.register_blueprint(app_Purch, url_prefix='/Purch')


@app.route("/")
def index():
    return render_template('index_begin.html')


@app.route("/process")
def process():
    return render_template('index_process.html')


@app.route('/clear_session')
def clear_session():
    session.clear()
    return render_template('index_begin.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4200)
