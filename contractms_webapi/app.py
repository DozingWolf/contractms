from flask import Flask

app = Flask(__name__)

@app.route('/Goodjob')
def index():
    return "Hello!World!GoodJob！"

@app.route('/')
def mainpage():
    return "This is a main page"

if __name__ == '__main__':
    app.run(debug=True)