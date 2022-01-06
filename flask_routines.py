from flask import Flask
from flask import request
from flask import render_template

from db_interface import read_all, add_item
from pseudo_database import PseudoDatabase

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('template1.html', db_str=read_db() if request.args.get("read") is not None else None)


@app.route('/add_category_label', methods=['POST'])
def add_category_label():
    try:
        add_item(request.form['category'], request.form['label'])
        return read_all()
    except PseudoDatabase.ItemInCategory:
        return "item in category"


def read_db():
    return read_all()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
