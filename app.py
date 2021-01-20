from flask import Flask, render_template, request
import playground

app = Flask(__name__, static_folder="templates/static")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analysis/", methods=['GET', 'POST'])
def analysis():
    if checkValues(request.form["url"], request.form["startMin"], request.form["startSec"], request.form["endMin"], request.form["endSec"]):
        start = (int(request.form["startMin"]) * 60) + int(request.form["startSec"])
        end = (int(request.form["endMin"]) * 60) + int(request.form["endSec"])

        epCheck = playground.Algo(request.form["url"], start, end)
        results = epCheck.analyzeWithout()

        return render_template("analysis.html", frames=results[0], fps=results[1], flashes=results[2], risk=results[3])
    else:
        return render_template("error.html")


def checkValues(url, startMin, startSec, endMin, endSec) -> bool:
    start = (int(startMin) * 60) + int(startSec)
    end = (int(endMin) * 60) + int(endSec)

    if start > end or start + 10 < end or not url:
        return False
    return True


if __name__ == "__main__":
    app.run()
