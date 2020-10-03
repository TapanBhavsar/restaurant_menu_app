from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/login')
def log_in():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
