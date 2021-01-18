from flask import Flask, render_template
import algo
# test = algo.Algo()
# print(test.analyze())

app = Flask(__name__, static_folder="templates/static")


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
