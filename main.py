from flask import Flask
from markupsafe import escape
from flask import url_for , jsonify
from flask import render_template
from flask import request
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
import subprocess


app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath("uploads")
OUTPUT_FOLDER = os.path.abspath("output")

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/tools/<slug>", methods=['GET','POST'])
def pdf_tool(slug):
    if request.method == 'GET':
        return render_template("tooljinja.html", name=escape(slug) , operation="compress pdf")
   
    if request.method == 'POST':
        file = request.files['file']
        if file:
           fileName = secure_filename(file.filename)
           Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
           output_fileName = f"Processed_{fileName}"
           Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
         
           file.save(Upload_path)

         # Pdf compresser 
     
           command = [
              "gswin64c",
              "-sDEVICE=pdfwrite",
              "-dCompatibilityLevel=1.4",
              "-dPDFSETTINGS=/screen",
              "-dNOPAUSE",
              "-dQUIET",
              "-dBATCH",
              f"-sOutputFile={Output_path}",
             Upload_path
            ]
           
           try:
              subprocess.run(command, check=True)
              print(f"Pdf successfully compressed to : {output_fileName}")
              return send_from_directory(directory=OUTPUT_FOLDER, path=output_fileName, as_attachment= True)
           except subprocess.CalledProcessError as e:
              print("Compression failed try again : ",e)  
              return jsonify(success=False, error="Ghostscript processing failed."), 500
        
        return jsonify(success=False, error="File upload failed"), 400
    return render_template("tooljinja.html", name=escape(slug) , operation="compress pdf")

# @app.route('/tools/<slug>')
# def template(slug):
    
#     return render_template("tooljinja.html", name=escape(slug) , operation="compress pdf")


# @app.route('/tools', methods=['POST'])
# def upload_file():
#         file = request.files['file']
#         file.save(f"uploads/{secure_filename(file.filename)}")
#         return render_template('tools.html')



# @app.route("/user/<username>")
# def hello_user(username):
#    return f"<p>Hello, {escape(username)}</p>"

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return f'Post {post_id}'

# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return f'Subpath {escape(subpath)}'

# @app.route('/projects/')
# def projects():
#     return 'The project page'

# @app.route('/about')
# def about():
#     return 'The about page'

# with app.test_request_context():
#     print("---------------------------------")
#     print(url_for('projects'))
#     print(url_for('about', next='/'))
#     print(url_for('hello_user', username='John Doe'))
#     print("---------------------------------")