from flask import blueprints, session, render_template, request
from utils import getter, setter
from data import accounts, accountInfo, typingLevels

pages = blueprints.Blueprint("pages", __name__, url_prefix="/")




@pages.route("/logout")
def logout():
    """
    ! modifier
    """
    session["username"] = None

    return "you are now logged out"

@pages.route('/signup', methods=['POST', "GET"])
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
    
    #! modifier from this point on 
    accounts[name] = hash(password)
    accountInfo[name] = {}
    accountInfo[name]["wpms"] = session.get("wpms")
    accountInfo[name]["levelUpTo"] = session.get("levelUpTo")
    session["username"] = name
    
    #wipe all session fields
    session["wpms"] = None
    session["levelUpTo"] = None

    return main()

@pages.route('/login', methods=['POST', "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    name = request.form.get("name", type=str)
    password = request.form.get("password", type=str)
    
    if not name in accounts:
        return "this username does not exist"
    
    if accounts[name] != hash(password):
        return "wrong username or password"
    
    #! modifier from this point on 
    
    session["username"] = name

    return main()


    
@pages.route('/')
def main():
    wpms, levelUpTo = getter(session, "wpms", "levelUpTo")

    #! modifier from this point on 
    if not wpms:
        setter(session, "wpms", 0)
    if levelUpTo == None:
        setter(session, "levelUpTo", 0)
        levelUpTo = 0
    return render_template("main.html", sentence=typingLevels[levelUpTo], level=levelUpTo)


@pages.route('/payForSentenceGenerationPermission')
def payForSentenceGenerationPermission():
    session["canGenerateSentence"] = True
    return "you now have access to the sentence generation feature"



@pages.route("/showLevels")
def showLevels():
    username = session.get("username")
    [allLevelsWithWpms] = getter(session, "wpms")
    #! modifier from this point on 
    if not allLevelsWithWpms:
        setter(session, "wpms", [0 for _ in range(100)])
        allLevelsWithWpms = [0 for _ in range(100)]

    return render_template("displayLevels.html", allLevels=allLevelsWithWpms, username=username)

@pages.route("/gotoLevel/<int:level>")
def gotoLevel(level: int):
    setter(session, "levelUpTo", level)
    return render_template("main.html", sentence=typingLevels[level], level=level)


@pages.route('/loadNextLevel/<int:level>')
def loadNextLevel(level: int):
    wpm = request.args.get("wpm", type=int)
    assert isinstance(wpm, int)
    [wpms] = getter(session, "wpms")
    if wpms == None:
        setter(session, "wpms", [0 for _ in range(100)])
        wpms = [0 for _ in range(100)]
    wpms[level-1] = wpm
    level+=1
    setter(session, "levelUpTo", level)
    return {"sentence": typingLevels[level], "level": level}
