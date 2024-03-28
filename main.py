from flask import Flask, render_template, session, request


app = Flask(__name__)
app.secret_key = b'\xfd\xec\x82\x96\x94\xa2\xb0\xd3\xb7\x15\xe0\x8e\xd3\x1c\xb7\x1a'

def secure(password: str) -> bool:
    return len(password) < 8



@app.route('/signup')
def signup():
    name = request.args.get("name", type=str)
    password = request.args.get("password", type=str)
    
    if name in accounts:
        return "this username already exists"
    
    if not secure(password):
        return "this password is not secure please create another one"
    
    accounts[name] = password
    accountInfo[name]["wpms"] = session.get("wpms")
    accountInfo[name]["levelUpTo"] = session.get("levelUpTo")
    del session["wpms"]
    del session["levelUpTo"]
    session["username"] = name

    
def getter(session, *attrs) -> list:
    """
    funcType = (non decorator) wrapper
    takes in a session and attributes that a 
    user wants to get either from accountInfo or session
    """
    username = session.get("username")
    if username:
        return [accountInfo[username][attr] for attr in attrs]
    return [session.get(attr) for attr in attrs]

def setter(session, attr, value) -> list:
    """
    funcType = (non decorator) wrapper
    takes in a session and one attribute that the
    user wants to set either into accountInfo or session
    """
    username = session.get("username")
    if username:
        accountInfo[username][attr] = value
    session[attr] = value




@app.route('/')
def main():
    print(f"{session}")
    wpms, levelUpTo = getter(session, "wpms", "levelUpTo")
    if not wpms:
        setter(session, "wpms", 0)
    return render_template("main.html", sentence=typingLevels[levelUpTo], level=levelUpTo)

@app.route("/showLevels")
def showLevels():
    [allLevelsWithWpms] = getter(session, "wpms")
    if not allLevelsWithWpms:
        setter(session, "wpms", [0 for _ in range(100)])

    print(f"{allLevelsWithWpms = }")
    return render_template("displayLevels.html", allLevels=allLevelsWithWpms)

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
    print(f"{wpms}")
    wpms[level-1] = wpm
    level+=1
    print(f"level updated to = {level}")
    setter(session, "levelUpTo", level)
    return {"sentence": typingLevels[level], "level": level}



typingLevels = [
    'f',
    "The Project Gutenberg EBook of The Complete Works of William Shakespear This eBook is for the use of anyone anywhere at no cost and with",
    "almost no restrictions whatsoever, you may use it for any purpose,",
    "including commercial purposes, all without asking permission.",
    "In no case will you be held liable for any damages",
    "arising from the use of this eBook or any part of it.",
    "Moreover, any derivative works, translations,",
    "By William Shakespeare",
    "revisions, and modifications of this work will also be free",
    "from any restriction.  The Project Gutenberg License includes",
    "waiver of copyright and publicity rights in connection",
    "with this work, as well as a waiver of all other rights.",
    "This eBook is for the use of anyone anywhere at no cost and with",
    "almost no restrictions whatsoever.  You may copy it, give it away or",
    "re-use it under the terms of the Project Gutenberg License included",
    "with this eBook or online at www.gutenberg.org",
    "Title: The Complete Works of William Shakespeare",
    "Author: William Shakespeare",
    "Release Date: November 27, 2008 [EBook #3812]",
    "Language: English",
    "*** START OF THIS PROJECT GUTENBERG EBOOK THE COMPLETE WORKS OF WILLIAM SHAKESPEARE ***",
]

accounts = {

}

accountInfo = {

}

if __name__ == '__main__':
    app.run(debug=True)