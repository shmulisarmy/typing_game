from flask import blueprints, session
from sentence_maker.tree_maker import get_best_sentence
from utils import getter, setter

bp = blueprints.Blueprint("api", __name__, url_prefix="/api")


@bp.route("/yo")
def hello():
    return "hello"


@bp.route('/generateSentence/<string:topFiveLetters>', methods=['GET'])
def sentenceGenerator(topFiveLetters):
    print(f"{topFiveLetters = }")
    
    if getter(session, "canGenerateSentence")[0] == True:
        return {"sentence": get_best_sentence(topFiveLetters)}
    return "you do not have access to the sentence generation feature"
