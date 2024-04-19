from flask import blueprints, session
from sentence_maker.tree_maker import get_best_sentence
from dataBaseConnect import userHasAccess

bp = blueprints.Blueprint("api", __name__, url_prefix="/api")

@bp.route('/generateSentence/<string:topFiveLetters>', methods=['GET'])
def sentenceGenerator(topFiveLetters):
    print(f"{topFiveLetters = }")
    username = session.get("username")
    if not username:
        return "you are not logged in"
    if userHasAccess(username):
        print("user has access to the sentence generation feature")
        return {"sentence": get_best_sentence(topFiveLetters)}
    print("user does not have access to the sentence generation feature")
    return "you do not have access to the sentence generation feature"
