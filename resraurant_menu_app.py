from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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
    user_name = request.form['username']
    password = request.form['password']
    password_veified = request.form['password_veified']
    app.logger.debug(f"user name is {user_name}.\t password is {password}.\t varified password {password_veified}")
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
