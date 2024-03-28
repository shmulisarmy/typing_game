from flask import Flask, render_template, session, request
from utils import getter, setter, secure, hash
from data import accounts, accountInfo, typingLevels

app = Flask(__name__)
app.secret_key = b'\xfd\xec\x82\x96\x94\xa2\xb0\xd3\xb7\x15\xe0\x8e\xd3\x1c\xb7\x1a'

@app.route("/logout")
def logout():
    session["username"] = None

    return "you are now logged out"

@app.route('/signup', methods=['POST', "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    """places all data previously in session into accountInfo"""
    name = request.form.get("name", type=str)
    password = request.form.get("password", type=str)
    
    if name in accounts:
        return "this username already exists"
    
    if not secure(password):
        return "this password is not secure please create another one"
    
    accounts[name] = hash(password)
    accountInfo[name] = {}
    accountInfo[name]["wpms"] = session.get("wpms")
    accountInfo[name]["levelUpTo"] = session.get("levelUpTo")
    print(f"{accountInfo = }")
    session["wpms"] = None
    session["levelUpTo"] = None
    session["username"] = name

    return main()

@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    name = request.form.get("name", type=str)
    password = request.form.get("password", type=str)
    
    if not name in accounts:
        return "this username does not exist"
    
    if accounts[name] != hash(password):
        return "wrong username or password"
    session["username"] = name

    return main()


    
@app.route('/')
def main():
    print(f"{session}")
    wpms, levelUpTo = getter(session, "wpms", "levelUpTo")
    if not wpms:
        setter(session, "wpms", 0)
    if levelUpTo == None:
        setter(session, "levelUpTo", 0)
        levelUpTo = 0
    return render_template("main.html", sentence=typingLevels[levelUpTo], level=levelUpTo)

@app.route("/showLevels")
def showLevels():
    [allLevelsWithWpms] = getter(session, "wpms")
    if not allLevelsWithWpms:
        setter(session, "wpms", [0 for _ in range(100)])

    username = session.get("username")

    print(f"{allLevelsWithWpms = }")
    return render_template("displayLevels.html", allLevels=allLevelsWithWpms, username=username)

@app.route("/gotoLevel/<int:level>")
def gotoLevel(level: int):
    print(f"go to level {level}")
    print(f"{session = }")
    setter(session, "levelUpTo", level)
    return render_template("main.html", sentence=typingLevels[level], level=level)


@app.route('/loadNextLevel/<int:level>')
def loadNextLevel(level: int):
    print(f"load level after {level}")
    wpm = request.args.get("wpm", type=int)
    assert isinstance(wpm, int)
    [wpms] = getter(session, "wpms")
    print(f"{wpms = }")
    if wpms == None:
        setter(session, "wpms", [0 for _ in range(100)])
        wpms = [0 for _ in range(100)]
    wpms[level-1] = wpm
    level+=1
    print(f"level updated to = {level}")
    setter(session, "levelUpTo", level)
    return {"sentence": typingLevels[level], "level": level}


if __name__ == '__main__':
    app.run(debug=True)