from flask import Flask

from api.views import bp
from pages.views import pages


app = Flask(__name__, template_folder = "templates")
app.register_blueprint(bp)
app.register_blueprint(pages)
app.secret_key = b'\xfd\xec\x82\x96\x94\xa2\xb0\xd3\xb7\x15\xe0\x8e\xd3\x1c\xb7\x1a'


if __name__ == '__main__':
    app.run(debug=True, port=5050)