from flask import Flask, render_template, session, request


app = Flask(__name__)
app.secret_key = b'\xfd\xec\x82\x96\x94\xa2\xb0\xd3\xb7\x15\xe0\x8e\xd3\x1c\xb7\x1a'


@app.route('/')
def main():
    print(f"{session}")
    if not session.get("wpms"):
        session["wpms"] = [0 for i in range(100)]
    levelUpTo = session.get("levelUpTo", 0)
    return render_template("main.html", sentence=typingLevels[levelUpTo], level=levelUpTo)

@app.route("/showLevels")
def showLevels():
    allLevels = session.get("wpms")
    if not allLevels:
        session["wpms"] = [0 for i in range(100)]

    print(f"{allLevels = }")
    return render_template("displayLevels.html", allLevels=allLevels)

@app.route("/gotoLevel/<int:level>")
def gotoLevel(level: int):
    print(f"got to level {level}")
    print(f"{session = }")
    session["levelUpTo"] = level
    return render_template("main.html", sentence=typingLevels[level], level=level)


@app.route('/loadNextLevel/<int:level>')
def loadNextLevel(level: int):
    print(f"load level after {level}")
    wpm = request.args.get("wpm", type=int)
    assert isinstance(wpm, int)
    session["wpms"][level-1] = wpm
    level+=1
    print(f"level updated to = {level}")
    session["levelUpTo"] = level
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

if __name__ == '__main__':
    app.run(debug=True)