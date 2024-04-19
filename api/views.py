from flask import blueprints, session, request
from sentence_maker.tree_maker import get_best_sentence
from dataBaseConnect import userHasAccess
from utils import getter, setter

bp = blueprints.Blueprint("api", __name__, url_prefix="/api")

@bp.route('/generateSentence/<string:topFiveLetters>', methods=['GET'])
def sentenceGenerator(topFiveLetters):
    #! modifier
    wpm = request.args.get("wpm")
    levelUpTo = int(request.args.get("levelUpTo"))
    [wpms] = getter(session, "wpms")
    if not isinstance(wpms, list):
        setter(session, "wpms", [0 for _ in range(100)])
        wpms = [0 for _ in range(100)]
    print(f"{wpms = }")
    wpms[levelUpTo-1] = wpm
    print(f"{topFiveLetters = }")
    username = session.get("username")
    if not username:
        return {
            "message":  "you are not logged in",
                        "didGnereatedSentence": False,
        
            }
    if userHasAccess(username):
        print("user has access to the sentence generation feature")
        generatedSentence = get_best_sentence(topFiveLetters)
        print(f"{generatedSentence = }")
        return {"sentence": generatedSentence,
                "message":  "this is an ai generated sentence",
                "didGnereatedSentence": True}
    print("user does not have access to the sentence generation feature")
    return {
        "message":  "you do not have access to the sentence generation feature",
                    "didGnereatedSentence": False
                    }
