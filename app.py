import matplotlib.pyplot as plt
from sqlalchemy import func
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
    return render_template('index.html', colors=colors)


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

    return render_template('thanku.html')


@app.route('/statistics')
def stats():
    all_info = {}

    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()

    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]

    all_info['total_count'] = User.query.count()

    qu1_purple_count = db.session.query(Answers.qu1).filter(Answers.qu1 == 'purple').count()
    qu1_pink_count = db.session.query(Answers.qu1).filter(Answers.qu1 == 'pink').count()
    if qu1_purple_count > qu1_pink_count:
        all_info['qu1_answer'] = [qu1_purple_count, 'фиолетовый']
    elif qu1_pink_count > qu1_purple_count:
        all_info['qu1_answer'] = [qu1_pink_count, 'розовый']
    else:
        all_info['qu1_answer'] = 'мнения разделились'

    qu2_green_count = db.session.query(Answers.qu2).filter(Answers.qu2 == 'green').count()
    qu2_yellow_count = db.session.query(Answers.qu2).filter(Answers.qu2 == 'yellow').count()
    if qu2_green_count > qu2_yellow_count:
        all_info['qu2_answer'] = [qu2_green_count, 'зеленый']
    elif qu2_yellow_count > qu2_green_count:
        all_info['qu2_answer'] = [qu2_yellow_count, 'желтый']
    else:
        all_info['qu2_answer'] = 'мнения разделились'

    qu3_blue_count = db.session.query(Answers.qu3).filter(Answers.qu3 == 'blue').count()
    qu3_purple_count = db.session.query(Answers.qu3).filter(Answers.qu3 == 'purple').count()
    if qu3_blue_count > qu3_purple_count:
        all_info['qu3_answer'] = [qu3_blue_count, 'синий']
    elif qu3_purple_count > qu3_blue_count:
        all_info['qu3_answer'] = [qu3_purple_count, 'фиолетовый']
    else:
        all_info['qu3_answer'] = 'мнения разделились'

    qu4_lightblue_count = db.session.query(Answers.qu4).filter(Answers.qu4 == 'light-blue').count()
    qu4_green_count = db.session.query(Answers.qu4).filter(Answers.qu4 == 'green').count()
    if qu4_lightblue_count > qu4_green_count:
        all_info['qu4_answer'] = [qu4_lightblue_count, 'голубой']
    elif qu4_green_count > qu4_lightblue_count:
        all_info['qu4_answer'] = [qu4_green_count, 'зеленый']
    else:
        all_info['qu4_answer'] = 'мнения разделились'

    colors = Questions.query.all()

    return render_template('statistics.html', all_info=all_info, colors=colors)


if __name__ == "__main__":
    app.run(debug=True)
