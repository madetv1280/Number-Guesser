"""
title: number guesser, version: 2.1
author: madetv1280
last change: 01/29/2024
"""

import flask
import random
import yaml
import time


def rand_int(minimum=1, maximum=100):
    random_number = random.randint(minimum, maximum)
    return random_number


def is_prime(n: int):
    for i in range(2, n):
        if (n % i) == 0:
            return False
    return True


def difference(a, b):
    diff = a - b
    return diff


def write_score(path, username: str, tries: int):
    yaml_data = read_yaml(path)

    found_username_in_yaml = False
    scores = []

    for score in yaml_data:
        if score["name"] == username:
            found_username_in_yaml = True
            if score["trys"] > tries:
                score = {
                    "name": username,
                    "time": diff,
                    "trys": tries
                }
        scores.append(score)

    if not found_username_in_yaml:
        new_entry = {
            "name": username,
            "time": diff,
            "trys": tries
        }
        scores.append(new_entry)

    write_yaml(path, scores)


def write_yaml(path, data):
    with open(path, 'w') as file:
        yaml.dump(data, file)
    return


def read_yaml(path):
    with open(path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


def goto(site):
    return flask.redirect(flask.url_for(site))


def is_correct(guessed_number):
    global number
    if guessed_number != number:
        return False

    number = rand_int(1, 100)
    global game_won
    game_won = True
    return True


def guess_valid(guessed_number):
    if guessed_number.isdigit():
        guessed_number = int(guessed_number)
        print(guessed_number)
        if 1 <= guessed_number <= 100 or not guessed_number:
            return True
    return False


def convert_username(string):
    string = string[0:10]
    return string


app = flask.Flask(__name__)

number = rand_int(1, 100)

old_value = None
value = None

tries = 0

prefix = '💡Tip:'

start_time = time.time()

game_won = False


@app.route("/error")
def error():
    return flask.render_template("error.html")


@app.route("/scores")
def scores():
    highscores = read_yaml("templates/highscores.yml")

    return flask.render_template('scores.html', highscores=highscores)


@app.route("/win/")
def win():
    global game_won
    global start_time
    import time
    global diff

    print(f"win: {game_won}")
    if game_won:
        username = flask.request.args.get("username", "")
        print(f"[USER] {username}")

        if username != '':

            global tries
            write_score("templates/highscores.yml", username, tries)

            tries = 0
            username = None
            game_won = False
            start_time = time.time()
            return goto("scores")

        end_time = time.time()

        print(end_time)
        print(start_time)

        diff = int(end_time - start_time)

        return flask.render_template("win.html", trys=tries, time=diff)

    else:
        return goto("error")


@app.route("/")
def index():
    guessed_number = flask.request.args.get("guessed_number", "")
    print(f"[USER] {guessed_number}")

    valid = guess_valid(guessed_number)
    if valid:
        guessed_number = int(guessed_number)

        if is_correct(guessed_number):
            return goto("win")

        tip = generate_tip(guessed_number)
    else:
        tip = "Please enter a valid number!"

    if isinstance(tip, str):
        return flask.render_template('index.html', tip=tip)
    return tip


@app.errorhandler(404)
def internal_error(error):
    print(f"[ERROR] {error}")
    return goto("error")


def generate_tip(guessed_number):
    global prefix
    global tries
    global number

    guessed_number = int(guessed_number)

    tries += 1
    print(f"Tries: {tries}")

    global old_value
    global value

    # prevents tip from getting behind the wheel
    while value == old_value:
        value = rand_int(0, 2)
    old_value = value

    print(f"Number to guess: {number}")

    if value == 0:
        if number > guessed_number:
            return f"{prefix} The number is greater then {guessed_number}"

        if number < guessed_number:
            return f"{prefix} The number is less then {guessed_number}"

    if value == 1:
        if is_prime(number):
            return f"{prefix} The number is a prime number"

        else:
            return f"{prefix} The number is not a prime number"

    if value == 2:
        if number % 2:
            return f"{prefix} The number cannot be divided by 2"

        else:
            return f"{prefix} The number can be divided by 2"


if __name__ == '__main__':
    app.run(debug=True)
