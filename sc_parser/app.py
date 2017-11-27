from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import parser

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     return 'Post ID is ' % post_id

@app.route('/', methods=['GET', 'POST'])
def get_contract():
    text = request.form['text']
    print(text)
    parsable_text = "'"+text+"'"
    print(parsable_text)
    return parser.parse(text)


if __name__ == "__main__":
    app.run(debug=True)
