from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"

boggle_game = Boggle()


@app.route("/", methods=["POST", "GET"])
def home():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numPlays = session.get("numPlays", 0)

    return render_template('index.html', board=board, highscore=highscore, numPlays=numPlays)


@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numPlays = session.get("numPlays", 0)

    session['highscore'] = max(score, highscore)
    session['numPlays'] = numPlays + 1

    return jsonify(brokenRecord=score > highscore)
