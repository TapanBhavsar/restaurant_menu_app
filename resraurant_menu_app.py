from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
import os

from sqlalchemy.orm.exc import NoResultFound

from database_lib.sql_database_operations import SqlDatabaseOperations
from database_lib.tables.user import table as user_table
from database_lib.tables.menu_item import table as menu_item_table

from database_lib.tables.user import User
from database_lib.tables.restaurant import Restaurant
from database_lib.tables.menu_item import MenuItem

from configuration import Configuration

app = Flask(__name__)

sql_operator = SqlDatabaseOperations()
sql_operator.create_database(Configuration.SIGN_UP_DATABASE_NAME, user_table)

restaurant_query_operator = SqlDatabaseOperations()
restaurant_query_operator.create_database(Configuration.RESTAURANT_DATABASE, menu_item_table)

def available_restautant(restaurant_name):
        available_flag = True
        try:
            restaurant_availability = restaurant_query_operator.read_data(Restaurant, f"name='{restaurant_name}'", True)
        except NoResultFound:
            available_flag = False
        return available_flag

def get_menu_item_dict(menu_item):
    return {
        "name":menu_item.name,
        "description": menu_item.description,
        "course": menu_item.course,
        "price": menu_item.price,
    }

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
        req = request.get_json()
        restaurant_name = req.get("restaurant_name")
        if available_restautant(restaurant_name):
            restaurant_menu_items = restaurant_query_operator.read_data(table=MenuItem,
                                                                        filter=f"restaurant_name='{restaurant_name}'")
            menu_item_response = list(map(get_menu_item_dict, restaurant_menu_items))
            res = make_response(jsonify({"message": "OK", "result": menu_item_response}), 200)
        else:
            restaurant_query_operator.add_data(Restaurant(name=restaurant_name))
            res = make_response(jsonify({"message": "NOT OK"}), 200)
        return res
    else:
        return redirect('/')

@app.route('/new_item', methods=['POST'])
def new_item():
    if session.get('logged_in'):
        try:
            request_json = request.get_json()
            app.logger.debug(f"response : {request_json}")
            menu_item = MenuItem(name = request_json.get("item_name"),
                                description = request_json.get("description"),
                                course = request_json.get("course"),
                                price = request_json.get("price"),
                                restaurant_name = request_json.get("restaurant_name"),
                                )            
            restaurant_query_operator.add_data(menu_item)
            response = make_response(jsonify({"message": "done"}), 200)
        except:
            response = make_response(jsonify({"message":"Server error"}), 500)
        finally:
            return response
    else:
        return redirect('/')

@app.route('/update_item', methods=["POST"])
def update_item():
    request_json = request.get_json()
    updated_item = restaurant_query_operator.read_data(MenuItem,
                                                       filter=f"name='{request_json.get('item_name')}', restaurant_name='{request_json.get('restaurant_name')}'",
                                                       one=True)
    updated_item.name = request_json.get("item_name")
    updated_item.description = request_json.get("description")
    updated_item.course = request_json.get("course")
    updated_item.price = request_json.get("price")
    updated_item.restaurant_name = request_json.get("restaurant_name")
    restaurant_query_operator.add_data(updated_item)
    return make_response(jsonify({"message": "done"}), 200)

@app.route('/delete_item', methods=['POST'])
def delete_item():
    request_json = request.get_json()
    data = restaurant_query_operator.read_data(MenuItem,
                                               filter=f"name='{request_json.get('item_name')}', restaurant_name='{request_json.get('restaurant_name')}'",
                                               one=True)
    restaurant_query_operator.delete_data(data)
    return make_response(jsonify({"message": "done"}), 200)

if __name__ == '__main__':
    MAX_USERS = 12
    app.secret_key = os.urandom(MAX_USERS)
    app.run(host="0.0.0.0", port=8080, debug=True)
