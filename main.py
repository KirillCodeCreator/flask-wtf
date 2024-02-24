import json
import os

from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, StringField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username_astro = StringField('Id астронавта', validators=[DataRequired()])
    password_astro = PasswordField('Пароль астронавта', validators=[DataRequired()])
    username_cap = StringField('Id капитана', validators=[DataRequired()])
    password_cap = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')


class GalleryForm(FlaskForm):
    photo = FileField('Добавить картинку', validators=[DataRequired()])
    submit = SubmitField('Загрузить')


@app.route('/', defaults={'title': 'MarsOne'})
@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('index.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/table/<sex>/<int:age>')
def table(sex: str, age: int):
    return render_template('table.html', gender=sex, age=age)


def get_image_paths(base_path):
    # пути относительно static
    return [f"images/gallery/{i}" for i in os.listdir(base_path)]


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    image_base_path = 'static/images/gallery'
    if request.method == 'GET':
        form = GalleryForm()
        image_paths = get_image_paths(image_base_path)
        return render_template('gallery.html', image_paths=image_paths, form=form)
    elif request.method == 'POST':
        file = request.files['photo']
        with open(os.path.join(image_base_path, file.filename), 'wb') as f:
            f.write(file.stream.read())
        return redirect('/gallery')


@app.route('/member')
def member():
    with open('templates/members.json', 'r', encoding='utf8') as f:
        members = json.load(f)['members']
    return render_template('member.html', members=members)


if __name__ == '__main__':
    app.run("", 8080)
