from flask import Flask
from flask import render_template
from flask import request

import requests
import random

from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def index():                                    # get запрос
    main_data = {
        "a": "A",
        "b": "B",
        "c": "C",
        "d": "D"
    }
    context = {
        "name": "Vovan",
        "Surname": "Kyzmin",
        "age": 33
    }
    return render_template("index.html", main_data=main_data, **context)


@app.route("/contacts/")
def contacts():
    # Данные
    developer_name = "ХЗ"
    # Контекст name=developer_name - данныеб которые передаём из view в шаблон - Flask
    # Словарь конкекста props={"name": developer_name} - Django
    # context = {"name": developer_name}
    # return render_template("contacts.html", context=context)
    return render_template("contacts.html", name=developer_name, creation_date="26.02.2023")


@app.route("/result/")
def result():

    URL = "https://torg-pc.ru/catalog/igrovye-kompyutery-intel-core-i5/?PAGEN_1=65"

    response = requests.get(URL)
    def parser(url):
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        game_pc = soup.find_all("div", class_="item_info")
        return [c.text for c in game_pc]

    list_of_pc = parser(URL)
    random.shuffle(list_of_pc)
    return render_template("result.html", list_of_pc=list_of_pc)


@app.route("/run/", methods=["POST"])
def run_post():
    # Получать данные формы
    text = request.form["input_text"]
    with open("result.txt", "a") as file:
        file.write(f"{text}\n")
    return render_template("good.html")


@app.route("/run/", methods=["GET"])
def run_get():
    with open("result.txt", "r") as file:
        text = file.read()
    return render_template("form.html", text=text)


if __name__ == "__main__":
    app.run(debug=True)