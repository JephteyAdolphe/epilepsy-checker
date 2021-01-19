from flask import Flask, render_template, request
import algo
# test = algo.Algo()
# print(test.analyze())

app = Flask(__name__, static_folder="templates/static")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analysis/", methods=['GET', 'POST'])
def analysis():
    start = (int(request.form["startMin"]) * 60) + int(request.form["startSec"])
    end = (int(request.form["endMin"]) * 60) + int(request.form["endSec"])

    epCheck = algo.Algo(request.form["url"], start, end)
    results = epCheck.analyze()

    return render_template("analysis.html", frames=results[0], fps=results[1], flashes=results[2], risk=results[3])


if __name__ == "__main__":
    app.run()
