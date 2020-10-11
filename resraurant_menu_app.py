from flask import Flask, render_template, request, redirect

from database_lib.sql_database_operations import SqlDatabaseOperations
from database_lib.tables.user import table as user_table

app = Flask(__name__)

sql_operator = SqlDatabaseOperations()
sql_operator.create_database("users.db", user_table)

@app.route('/')
@app.route('/login')
def log_in():
    return render_template("login.html")

@app.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")

@app.route('/login_validation', methods=['POST'])
def login_validation():
        user_name = request.form['username']
        password = request.form['password']
        app.logger.debug(f"user name is {user_name}\n password is {password}")
        return redirect('/')

@app.route('/add_signup', methods = ['POST'])
def add_signup():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        password_veified = request.form['password_veified']
        if (password == password_veified) and password != "" and password_veified != "":
            app.logger.debug(f"user name is {user_name}.\t password is  same as {password}.")
            return redirect('/')
        else:
            app.logger.debug(f"user name is {user_name}.\t password is different {password} and varified password {password_veified}")
            return render_template('sign_up.html', not_valid = "password is not same in varification")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
