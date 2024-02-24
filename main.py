from flask import render_template, Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/index/<title>')
def index(title):
    return render_template("index.html", title=title)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    return render_template('table.html', gender=sex, age=age)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
