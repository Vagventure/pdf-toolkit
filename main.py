from flask import Flask
from markupsafe import escape
from flask import url_for , jsonify
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import send_file
from werkzeug.utils import secure_filename
import zipfile
import os
import subprocess
import platform
from PIL import Image
from flask import after_this_request


app = Flask(__name__)


gs_cmd = 'gswin64c' if platform.system() == 'Windows' else 'gs'


if os.environ.get('RENDER'):  # Custom flag for Render (you can set this in env vars)
    UPLOAD_FOLDER = '/tmp/uploads'
    OUTPUT_FOLDER = '/tmp/output'
else:
    UPLOAD_FOLDER = os.path.abspath('uploads')
    OUTPUT_FOLDER = os.path.abspath('output')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


def empty_dir(path):
    [os.remove(os.path.join(path, f)) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

@app.route("/")
def hello_world():
    empty_dir(UPLOAD_FOLDER)
    empty_dir(OUTPUT_FOLDER)
    return render_template('index.html')


@app.route("/tools/<slug>", methods=['GET','POST'])
def pdf_tool(slug):
    op = escape(slug)
    if request.method == 'GET':
        # pull your “metadata” out of request.args
        img1       = request.args.get('img1')
        img2       = request.args.get('img2')
        caption1   = request.args.get('caption1')
        caption2   = request.args.get('caption2')
        description   = request.args.get('description')
      
        # … same for img2, caption2, description …
        return render_template(
            "tooljinja.html",
            name=op,
            img1=img1,caption1=caption1,
            img2=img2,caption2=caption2,
            description=description)
     
    match(op):
       
       case "Pdf Merger":
           return pdf_merger(op)
        
       case "Images to Pdf":
           return Img_pdf(op)
        
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
  
    # return render_template("tooljinja.html", name=op , operation="splitt pdf")      
         

def pdf_merger(name): 
    if request.method == 'GET':
             return render_template("tooljinja.html", name=name , operation="Merged pdf")

    if request.method == 'POST':
        uploaded_files = request.files.getlist('files[]')
        # Output_path = ""
        if uploaded_files:
           for file in uploaded_files:
             fileName = secure_filename(file.filename)
             Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
             output_fileName = f"Processed_{fileName}"
             Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
             
             file.save(Upload_path)
            
           input_files = [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER)]
   
        #Ghost Command
        command = [
           gs_cmd,
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

def Img_pdf(name): 
    if request.method == 'GET':
        return render_template("tooljinja.html", name=name, operation="Generated pdf")

    if request.method == 'POST':
        uploaded_files = request.files.getlist('files[]')
        output_fileName = "Processed_Pdf.pdf"
        Output_path = os.path.join(OUTPUT_FOLDER, output_fileName)


        if uploaded_files:
            image_list = []
            for file in uploaded_files:
                img = Image.open(file).convert("RGB")
                image_list.append(img)

            
            # Save all images into a single PDF
            image_list[0].save(Output_path, save_all=True, append_images=image_list[1:])

            return send_from_directory(directory=OUTPUT_FOLDER, path=output_fileName, as_attachment=True)

    return jsonify(success=False, error="File upload failed"), 400


def pdf_compress(name):
         if request.method == 'GET':
             return render_template("tooljinja.html", name=name , operation="Compressed pdf")
        
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
                   gs_cmd,
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
                   return send_file(Output_path, as_attachment=True, download_name=output_fileName, max_age=0, conditional=False)

                  
                except subprocess.CalledProcessError as e:
                   print("Compression failed try again : ",e)  
                   return jsonify(success=False, error="Ghostscript processing failed."), 500
                
         return jsonify(success=False, error="File upload failed"), 400  
              
def pdf_splitt(name):
   if request.method == 'GET':
       return render_template("tooljinja.html", name=name , operation="Splitted pdf")
   
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
                 gs_cmd,
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
                  gs_cmd,
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
                  gs_cmd,
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
                  gs_cmd,
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
             return render_template("tooljinja.html", name=name)

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
                  gs_cmd,
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

