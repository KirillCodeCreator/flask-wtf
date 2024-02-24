import json
import os

from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class GalleryForm(FlaskForm):
    photo = FileField('Добавить картинку', validators=[DataRequired()])
    submit = SubmitField('Загрузить')


@app.route('/', defaults={'title': 'MarsOne'})
@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('index.html', title=title)


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
