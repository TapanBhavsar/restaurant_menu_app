from flask import Flask, render_template, request, redirect, url_for, session
import os

from sqlalchemy import exc

from database_lib.sql_database_operations import SqlDatabaseOperations
from database_lib.tables.user import table as user_table
from database_lib.tables.restaurant import table as restaurant_table

from database_lib.tables.user import User
from database_lib.tables.restaurant import Restaurant

from configuration import Configuration

app = Flask(__name__)

sql_operator = SqlDatabaseOperations()
sql_operator.create_database(Configuration.SIGN_UP_DATABASE_NAME, user_table)

restaurant_query_operator = SqlDatabaseOperations()
restaurant_query_operator.create_database(Configuration.RESTAURANT_DATABASE, restaurant_table)


def available_restautant(restaurant_name):
        available_flag = False
        try:
            restaurant_query_operator.add_data(Restaurant(name=restaurant_name))
        except exc.IntegrityError as error:
            available_flag = True
        return available_flag

@app.route('/')
@app.route('/login')
def log_in():
    if session.get('logged_in') == False:
        return render_template("login.html", error = "Entered username or password are invalid.")
    else:
        return render_template("login.html")

@app.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")

@app.route('/login_validation', methods=['POST'])
def login_validation():
    user_name = request.form['username']
    password = request.form['password']
    app.logger.debug(f"user name is {user_name}\npassword is {password}")
    query_data = sql_operator.read_data(table=User, filter=f"user_name='{user_name}'", one=True)
    if query_data.user_name==user_name and query_data.password==password:
        session['logged_in'] = True
        app.logger.debug(f"access granted.")
        return redirect('/query_home')
    else:
        session['logged_in'] = False
        return redirect('/')

@app.route('/add_signup', methods = ['POST'])
def add_signup():
    user_name = request.form['username']
    password = request.form['password']
    password_veified = request.form['password_veified']
    if (password == password_veified) and password != "" and password_veified != "":
        app.logger.debug(f"user name is {user_name}.\t password is  same as {password}.")
        sql_operator.add_data(User(user_name=user_name, password = password))
        return redirect('/')
    else:
        app.logger.debug(f"user name is {user_name}.\t password is different {password} and varified password {password_veified}")
        return render_template('sign_up.html', not_valid = "password is not same in varification")

@app.route('/query_home', methods=['GET'])
def query_home():
    if session.get('logged_in'):
        return render_template('query_home.html')
    else:
        return redirect('/')
    
@app.route('/search', methods=['POST'])
def search():
    if session.get('logged_in'):
        restaurant_name = request.form['restaurant_name']
        if available_restautant(restaurant_name):
            pass # TODO add read all menu items and pass to html_page/update link
        return redirect('/query_home')
    else:
        return redirect('/')

if __name__ == '__main__':
    MAX_USERS = 12
    app.secret_key = os.urandom(MAX_USERS)
    app.run(host="0.0.0.0", port=8080, debug=True)
