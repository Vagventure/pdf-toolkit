from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import render_template


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/user/<username>")
def hello_user(username):
   return f"<p>Hello, {escape(username)}</p>"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

with app.test_request_context():
    print("---------------------------------")
    print(url_for('projects'))
    print(url_for('about', next='/'))
    print(url_for('hello_user', username='John Doe'))
    print("---------------------------------")