from flask import Flask
from markupsafe import escape
from flask import url_for , jsonify
from flask import render_template
from flask import request
from flask import send_from_directory
from werkzeug.utils import secure_filename
import zipfile
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
    op = escape(slug)
   
    match(op):
       
       case "Pdf Merger":
           return pdf_merger(op)
        
       case "Pdf Compresser":
           return pdf_compress(op)
       
       case "Pdf Splitter":
           return pdf_splitt(op)
      
       case "Pdf to PNG":
           return pdf_PNG(op)
      
       case "Pdf to JPG":
           return pdf_JPG(op)
      
       case "Pdf to TIFF":
           return pdf_TIFF(op)
       
       case "Pdf Encryptor":
           return pdf_Locker(op)
  
    return render_template("tooljinja.html", name=op , operation="splitt pdf")      
         

def pdf_merger(name): 
    if request.method == 'GET':
             return render_template("tooljinja.html", name=name , operation="compress pdf")

    if request.method == 'POST':
            uploaded_files = request.files.getlist('files[]')
            if uploaded_files:
               for file in uploaded_files:
                 fileName = secure_filename(file.filename)
                 Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
                 output_fileName = f"Processed_{fileName}"
                 Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
                 
                 file.save(Upload_path)
                
            input_files = os.listdir(UPLOAD_FOLDER)
            #Ghost Command
            command = [
               "gswin64c",
               "-sDEVICE=pdfwrite",
               "-dBATCH",
               "-dQUIET",
               "-dNOPAUSE",
               f"-sOutputFile={Output_path}"
            ] + input_files
            
            try:
               subprocess.run(command, check=True)
               print("Pdfs are successfully merged : ",output_fileName)
               return send_from_directory(directory=OUTPUT_FOLDER, path=output_fileName, as_attachment= True)

            except Exception as e:
               print("Merging failed try again : ",e) 
               return jsonify(success=False, error="Ghostscript processing failed."), 500

    return jsonify(success=False, error="File upload failed"), 400  
    


def pdf_compress(name):
         if request.method == 'GET':
             return render_template("tooljinja.html", name=name , operation="compress pdf")
        
         if request.method == 'POST':
             uploaded_files = request.files.getlist('files[]')
             if uploaded_files:
                for file in uploaded_files:
                 fileName = secure_filename(file.filename)
                 Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
                 output_fileName = f"Processed_{fileName}"
                 Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
                 
                 file.save(Upload_path)

                quality = request.form.get('value') 
               
              # Pdf compresser 
          
                command = [
                   "gswin64c",
                   "-sDEVICE=pdfwrite",
                   "-dCompatibilityLevel=1.4",
                   f"-dPDFSETTINGS={quality}",
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
              
def pdf_splitt(name):
   if request.method == 'GET':
       return render_template("tooljinja.html", name=name , operation="splitt pdf")
   
   if request.method == 'POST':
             uploaded_files = request.files.getlist('files[]')
             if uploaded_files:
                for file in uploaded_files:
                 fileName = secure_filename(file.filename)
                 Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
                 output_fileName = f"Processed_{fileName}"
                 Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
                 Start_page = request.form.get("start-page")
                 End_page = request.form.get("end-page")
                 
                 file.save(Upload_path)

                 command = [
                 "gswin64c",
                 "-sDEVICE=pdfwrite",
                 "-dCompatibilityLevel=1.4",
                 "-dBATCH",
                 "-dQUIET",
                 "-dNOPAUSE",
                 f"-dFirstPage={Start_page}",
                 f"-dLastPage={End_page}",
                 f"-sOutputFile={Output_path}",
                 Upload_path
                ] 
                 
                try:
                   subprocess.run(command, check=True)
                   print(f"Pdf successfully splitted from {Start_page}-{End_page} : ",output_fileName)
                   return send_from_directory(directory=OUTPUT_FOLDER, path=output_fileName, as_attachment= True)
                except subprocess.CalledProcessError as e:
                   print("Splitting failed try again : ",e)  
                   return jsonify(success=False, error="Ghostscript processing failed."), 500


  
def pdf_PNG(name):
    if request.method == 'GET':
             return render_template("tooljinja.html", name=name , operation="Pdf to PNG")

    if request.method == 'POST':
            uploaded_files = request.files.getlist('files[]')
            if uploaded_files:
               for file in uploaded_files:
                 fileName = secure_filename(file.filename)
                 Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
                 output_fileName = "img"
                 Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
                 
                 file.save(Upload_path)
                
          #Ghostscript command
               command = [
                  "gswin64c",
                  "-sDEVICE=png16m",
                  f"-r150",
                  f"-dDownScaleFactor=2",
                  "-dNOPAUSE",
                  "-dQUIET",
                  "-dBATCH",
                  f"-sOutputFile={Output_path}%03d.png",
                  Upload_path
                ]
              
               try:
                  subprocess.run(command, check=True)
                  zip_path = os.path.join(OUTPUT_FOLDER,"photos.zip")
                  with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                      for image in os.listdir(OUTPUT_FOLDER):
                          if image.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                              full_path = os.path.join(OUTPUT_FOLDER,image)
                              zipf.write(full_path, arcname=image)
                  print(f"Photos zipped into: {output_fileName}")
                  return send_from_directory(directory=OUTPUT_FOLDER, path="photos.zip", as_attachment= True)

               except subprocess.CalledProcessError as e:
                  print("Conversion failed try again: ",e)    

def pdf_JPG(name):
    if request.method == 'GET':
             return render_template("tooljinja.html", name=name , operation="Pdf to JPG")

    if request.method == 'POST':
            uploaded_files = request.files.getlist('files[]')
            if uploaded_files:
               for file in uploaded_files:
                 fileName = secure_filename(file.filename)
                 Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
                 output_fileName = "img"
                 Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
                 
                 file.save(Upload_path)
                
          #Ghostscript command
               command = [
                  "gswin64c",
                  "-sDEVICE=jpeg",
                  f"-r150",
                  f"-dDownScaleFactor=2",
                  "-dNOPAUSE",
                  "-dQUIET",
                  "-dBATCH",
                  f"-sOutputFile={Output_path}%03d.JPG",
                  Upload_path
                ]
              
               try:
                  subprocess.run(command, check=True)
                  zip_path = os.path.join(OUTPUT_FOLDER,"photos.zip")
                  with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                      for image in os.listdir(OUTPUT_FOLDER):
                          if image.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                              full_path = os.path.join(OUTPUT_FOLDER,image)
                              zipf.write(full_path, arcname=image)
                  print(f"Photos zipped into: {output_fileName}")
                  return send_from_directory(directory=OUTPUT_FOLDER, path="photos.zip", as_attachment= True)

               except subprocess.CalledProcessError as e:
                  print("Conversion failed try again: ",e)    

def pdf_TIFF(name):
    if request.method == 'GET':
             return render_template("tooljinja.html", name=name , operation="Pdf to TIFF")

    if request.method == 'POST':
            uploaded_files = request.files.getlist('files[]')
            if uploaded_files:
               for file in uploaded_files:
                 fileName = secure_filename(file.filename)
                 Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
                 output_fileName = "img"
                 Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
                 
                 file.save(Upload_path)
                
          #Ghostscript command
               command = [
                  "gswin64c",
                  "-sDEVICE=tiff24nc",
                  "-r150",
                  "-dNOPAUSE",
                  "-dQUIET",
                  "-dBATCH",
                  f"-sOutputFile={Output_path}%03d.tiff",
                  Upload_path
                ]
              
               try:
                  subprocess.run(command, check=True)
                  zip_path = os.path.join(OUTPUT_FOLDER,"photos.zip")
                  with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                      for image in os.listdir(OUTPUT_FOLDER):
                          if image.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                              full_path = os.path.join(OUTPUT_FOLDER,image)
                              zipf.write(full_path, arcname=image)
                  print(f"Photos zipped into: {output_fileName}")
                  return send_from_directory(directory=OUTPUT_FOLDER, path="photos.zip", as_attachment= True)

               except subprocess.CalledProcessError as e:
                  print("Conversion failed try again: ",e)    

            return jsonify(success=False, error="File upload failed"), 400

def pdf_Locker(name):
    if request.method == 'GET':
             return render_template("tooljinja.html", name=name , operation="Pdf Locker")

    if request.method == 'POST':
            uploaded_files = request.files.getlist('files[]')
            if uploaded_files:
               for file in uploaded_files:
                 fileName = secure_filename(file.filename)
                 Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
                 output_fileName = f"Locked_{fileName}"
                 Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
                 
                 file.save(Upload_path)
                
               user_pass = request.form.get("code")
               owner_pass = f"{user_pass}@135"
          #Ghostscript command
               command = [
                  "gswin64c",
                  "-sDEVICE=pdfwrite",
                  "-dCompatibilityLevel=1.4",
                  "-dPDFSETTINGS=/default",
                  "-dNOPAUSE",
                  "-dBATCH",
                  "-dQUIET",
                  "-dEncryptionR=3",         # Encryption settings:       
                  "-dKeyLength=128",
                  f"-sUserPassword={user_pass}",
                  f"-sOwnerPassword={owner_pass}",
                  "-dPermissions=-4",
                  f"-sOutputFile={Output_path}",
                  Upload_path
                ]
              
               try:
                 subprocess.run(command, check=True)
                 print(f"Pdf is successfully locked : {output_fileName}")
                 print("Output path: ",Output_path)
                 print("Input Filename ",fileName)
                 return send_from_directory(directory=OUTPUT_FOLDER, path=output_fileName, as_attachment= True)
                 
               except subprocess.CalledProcessError as e:
                 print("Process failed try again: ",e)           
                 return jsonify(success=False, error="Ghostscript processing failed."), 500
                 
    return jsonify(success=False, error="File upload failed"), 400


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