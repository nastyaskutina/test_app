from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/HP/PycharmProjects/hw5.1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'informants'  # имя таблицы
    id = db.Column(db.Integer, primary_key=True) # имя колонки = специальный тип (тип данных, первичный ключ)
    gender = db.Column(db.Text)
    age = db.Column(db.Integer)
    city = db.Column(db.Text)
    language = db.Column(db.Text)
    education = db.Column(db.Text)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)

class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    qu1 = db.Column(db.Integer)
    qu2 = db.Column(db.Integer)
    qu3 = db.Column(db.Integer)
    qu4 = db.Column(db.Integer)

@app.route('/')
def question_page():
    colors = Questions.query.all()
    return render_template('index.html',
        colors=colors
    )


@app.route('/process', methods=['get'])
def answer_process():
    # если пустой запрос, то отправить проходить анкету
    if not request.args:
        return redirect(url_for('question_page'))

    # получаем значения ответов
    gender = request.args.get('gender')
    education = request.args.get('edu')
    age = request.args.get('age')
    language = request.args.get('language')
    city = request.args.get('city')

    # записываем в базу
    user = User(
        age=age,
        gender=gender,
        education=education,
        language=language,
        city=city

    )
    db.session.add(user)
    db.session.commit()

    # обновляем user'a, чтобы его ответ записать с таким же id
    db.session.refresh(user)

    # это же делаем с ответом
    qu1 = request.args.get('qu1')
    qu2 = request.args.get('qu2')
    qu3 = request.args.get('qu3')
    qu4 = request.args.get('qu4')
    answer = Answers(
        id=user.id,
        qu1=qu1,
        qu2=qu2,
        qu3=qu3,
        qu4=qu4
    )
    db.session.add(answer)
    db.session.commit()

    return 'Ok'

@app.route("/statistics")
def statistics():
    return render_template('statistics.html')

if __name__ == "__main__":
    app.run(debug=True)
