from flask import blueprints, session, render_template, request
from utils import getter, setter, valiedPayment, secure
from data import accountInfo, typingLevels
from dataBaseConnect import giveAccess, userHasAccess, matching, createUser, userExists

pages = blueprints.Blueprint("pages", __name__, url_prefix="")




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

    if userExists(name):
        return "this username already exists"
    
    if not secure(password):
        return "this password is not secure please create another one"
    
    
    createUser(name, hash(password))
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
    
    if not userExists(name):
        return "this user does not exist"
    
    if not matching(name, hash(password)):
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


@pages.route('/payForSentenceGenerationPermission', methods=["POST", "GET"])
def payForSentenceGenerationPermission():
    if request.method == "GET":
        return render_template("payForSentenceGenerationPermission.html")
    
    print(f"{request.form = }")

    cardNumber = request.form.get("cardNumber", type=int)
    cvv = request.form.get("cvv", type=int)
    paymentAmount = request.form.get("paymentAmount", type=int)
    if not cardNumber:
        return "card number is required"
    if not cvv:
        return "cvv is required"
    if not paymentAmount:
        return "payment amount is required"
    if valiedPayment(cardNumber, cvv, paymentAmount):
        giveAccess(session.get("username"))
        return "payment was successful"
    
    return "payment was unsuccessful"



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
    if not 0 < level < len(typingLevels):
        return "invalid level"
    setter(session, "levelUpTo", level)
    return render_template("main.html", sentence=typingLevels[level], level=level)


@pages.route('/loadNextLevel/<int:level>')
def loadNextLevel(level: int):
    wpm = request.args.get("wpm", type=int)
    assert isinstance(wpm, int)
    [wpms] = getter(session, "wpms")
    if not isinstance(wpms, list):
        setter(session, "wpms", [0 for _ in range(100)])
        wpms = [0 for _ in range(100)]
    wpms[level-1] = wpm
    level+=1
    setter(session, "levelUpTo", level)
    return {"sentence": typingLevels[level], "level": level}


