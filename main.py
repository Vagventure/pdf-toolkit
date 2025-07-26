from flask import Flask
from markupsafe import escape
from flask import url_for , jsonify
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import send_file
from werkzeug.utils import secure_filename
from pypdf import PdfWriter,PdfReader
import fitz
import zipfile
import time
import os
import shutil
import io
import subprocess
import platform
from PIL import Image
from flask import after_this_request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color, black



app = Flask(__name__)


gs_cmd = 'gswin64c' if platform.system() == 'Windows' else 'gs'


if os.environ.get('RENDER'):  # Custom flag for Render (you can set this in env vars)
    UPLOAD_FOLDER = '/tmp/uploads'
    OUTPUT_FOLDER = '/tmp/output'
    PREVIEW_FOLDER = '/tmp/previews'
else:
    UPLOAD_FOLDER = os.path.abspath('uploads')
    OUTPUT_FOLDER = os.path.abspath('output')
    PREVIEW_FOLDER = os.path.abspath('previews')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(PREVIEW_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['PREVIEW_FOLDER'] = PREVIEW_FOLDER


def empty_dir(path):
    [os.remove(os.path.join(path, f)) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def create_watermark(text, output="./uploads/watermark.pdf"):
    os.makedirs(os.path.dirname(output), exist_ok=True)

    c = canvas.Canvas(output, pagesize=A4)
    c.setFont("Helvetica", 100)
    c.setFillColor(Color(0.5, 0.5, 0.5, alpha=0.6))
    c.saveState()
    c.translate(300, 400)
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()
    return output 

@app.route("/")
def hello_world():
    empty_dir(UPLOAD_FOLDER)
    empty_dir(OUTPUT_FOLDER)
    empty_dir(PREVIEW_FOLDER)
    return render_template('index.html')

# @app.route('/preview-list')
# def preview_list():
#     previews = os.listdir('previews')
#     return jsonify(previews)

# @app.route('/previews/<filename>')
# def get_preview(filename):
#     return send_from_directory('previews', filename)

@app.route('/previews/<filename>')
def serve_preview(filename):
    return send_from_directory(PREVIEW_FOLDER, filename)

@app.route('/previews')
def list_previews():
    files = os.listdir(PREVIEW_FOLDER)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    return jsonify(image_files)

@app.route('/reorder-previews', methods=['POST'])
def reorder_previews():
    data = request.json
    order = data.get('order', [])

    temp_folder = 'Preview_temp'

    os.makedirs(temp_folder, exist_ok=True)

    # Move files to temp in the new order
    for i, filename in enumerate(order):
        src = os.path.join(PREVIEW_FOLDER, filename)
        dst = os.path.join(temp_folder, f"{i:03d}_{filename}")
       
        if os.path.exists(src):
            shutil.move(src, dst)

    # Clear old previews and move temp back
    for f in os.listdir(PREVIEW_FOLDER):
        os.remove(os.path.join(PREVIEW_FOLDER, f))

    for f in os.listdir(temp_folder):
        shutil.move(os.path.join(temp_folder, f), os.path.join(PREVIEW_FOLDER, f))

    os.rmdir(temp_folder)
    pdf_path = os.path.join(OUTPUT_FOLDER, "Reordered_pdf.pdf")
    doc = fitz.open()

    for filename in sorted(os.listdir(PREVIEW_FOLDER)):
        filepath = os.path.join(PREVIEW_FOLDER, filename)
        img = fitz.Pixmap(filepath)

        if img.alpha:  # If image has transparency
            img = fitz.Pixmap(fitz.csRGB, img)

        rect = fitz.Rect(0, 0, img.width, img.height)
        page = doc.new_page(width=img.width, height=img.height)
        page.insert_image(rect, pixmap=img)
        img = None  # free memory

    doc.save(pdf_path)
    doc.close()

    return send_from_directory(directory=OUTPUT_FOLDER, path="Reordered_pdf.pdf", as_attachment= True)




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
       
       case "Pdf Decryptor":
           return pdf_unlocker(op)
       
       case "Pdf Rotator":
           return pdf_rotator(op)
       
       case "Text Extractor":
           return pdf_textext(op)
        
       case "Pdf Watermarker":
           return pdf_Wmark(op)
      
       case "Pdf Reorderer":
           return pdf_reorder(op)
  
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

def pdf_unlocker(name):
    if request.method == 'GET':
             return render_template("tooljinja.html", name=name)

    if request.method == 'POST':
            uploaded_files = request.files.getlist('files[]')
            if uploaded_files:
               for file in uploaded_files:
                 fileName = secure_filename(file.filename)
                 Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
                 output_fileName = f"Unlocked_{fileName}"
                 Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
                 
                 file.save(Upload_path)
                
               user_pass = request.form.get("code")

          #Ghostscript command
               command = [
                  gs_cmd,
                  "-sDEVICE=pdfwrite",
                  "-dCompatibilityLevel=1.4",
                  "-dPDFSETTINGS=/default",
                  "-dNOPAUSE",
                  "-dBATCH",
                  "-dQUIET",
                  f"-sPDFPassword={user_pass}",
                  f"-sOutputFile={Output_path}",
                  Upload_path
                ]
              
               try:
                 subprocess.run(command, check=True)
                 print(f"Pdf is successfully Unlocked : {output_fileName}")
                 print("Output path: ",Output_path)
                 print("Input Filename ",fileName)
                 return send_from_directory(directory=OUTPUT_FOLDER, path=output_fileName, as_attachment= True)

                 
               except subprocess.CalledProcessError as e:
                 print("Process failed try again: ",e)           
                 return jsonify(success=False, error="Ghostscript processing failed."), 500
                 
    return jsonify(success=False, error="File upload failed"), 400


def pdf_rotator(name):
    if request.method == 'GET':
             return render_template("tooljinja.html", name=name)

    if request.method == 'POST':
            uploaded_files = request.files.getlist('files[]')
            if uploaded_files:
               for file in uploaded_files:
                 fileName = secure_filename(file.filename)
                 Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
                 output_fileName = f"Rotated_{fileName}"
                 Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
                 
                 file.save(Upload_path)
                
               angle = int(request.form.get("value", 90))

          #Ghostscript command
            Writer = PdfWriter()
            Reader = PdfReader(Upload_path)
            try:
                for page in Reader.pages:
                 page.rotate(angle)
                 Writer.add_page(page)

                with open(Output_path, "wb") as f :
                    Writer.write(f)
                return send_from_directory(directory=OUTPUT_FOLDER, path=output_fileName, as_attachment= True)

                 
            except subprocess.CalledProcessError as e:
                 print("Process failed try again: ",e)           
                 return jsonify(success=False, error="Ghostscript processing failed."), 500
                 
    return jsonify(success=False, error="File upload failed"), 400

def pdf_textext(name):
    if request.method == 'GET':
             return render_template("tooljinja.html", name=name)

    if request.method == 'POST':
            uploaded_files = request.files.getlist('files[]')
            if uploaded_files:
               for file in uploaded_files:
                 fileName = secure_filename(file.filename)
                 Upload_path = os.path.join(UPLOAD_FOLDER,fileName)
                 output_fileName = "Text_file.txt"
                 Output_path = os.path.join(OUTPUT_FOLDER,output_fileName)
                 
                 file.save(Upload_path)                          

          #PyuPDf command
            try:
              doc = fitz.open(Upload_path)
              with open(Output_path, "w", encoding="utf-8") as f:
               for i, page in enumerate(doc):
                  text = page.get_text()
                  f.write(f"----Page {i+1}----\n{text}\n\n")
              doc.close()
              print(f"Text saved to: {Output_path}")
              return send_from_directory(directory=OUTPUT_FOLDER, path=output_fileName, as_attachment= True)
            except Exception as e:
             print("Extraction failed:", e)
             return  jsonify(success=False, error="Ghostscript processing failed."), 500
                 
    return jsonify(success=False, error="File upload failed"), 400


def pdf_Wmark(name):
    if request.method == 'GET':
        return render_template("tooljinja.html", name=name)

    if request.method == 'POST':
        uploaded_files = request.files.getlist('files[]')
        if not uploaded_files:
            return jsonify(success=False, error="No files uploaded"), 400

        for file in uploaded_files:
         fileName = secure_filename(file.filename)
         Upload_path = os.path.join(UPLOAD_FOLDER, fileName)
         output_fileName = f"Watermarked_{fileName}"
         Output_path = os.path.join(OUTPUT_FOLDER, output_fileName)
     
         file.save(Upload_path)
         file.stream.seek(0)
     
         if os.path.getsize(Upload_path) == 0:
             print(f"❌ File {fileName} is empty after saving.")
             continue  # Skip this file
     
         # Proceed only if saved properly
         watermark_pdf_bytes = create_watermark("Confidential")
         time.sleep(1)
         input_pdf = PdfReader(Upload_path)
         watermark_pdf = PdfReader(watermark_pdf_bytes)
         watermark_page = watermark_pdf.pages[0]
     
         writer = PdfWriter()
     
         for page in input_pdf.pages:
             page.merge_page(watermark_page)
             writer.add_page(page)
     
         with open(Output_path, "wb") as f_out:
             writer.write(f_out)
     
         print(f"✅ Watermarked PDF generated: {output_fileName}")
         return send_from_directory(OUTPUT_FOLDER, output_fileName, as_attachment=True)


    return jsonify(success=False, error="Invalid method"), 400

def pdf_reorder(name):
    if request.method == 'GET':
        return render_template("tooljinja.html", name=name)

    if request.method == 'POST':
        uploaded_files = request.files.getlist('files[]')
        if not uploaded_files:
            return jsonify(success=False, error="No files uploaded"), 400
        previews = []
        for file in uploaded_files:
           fileName = secure_filename(file.filename)
           Upload_path = os.path.join(UPLOAD_FOLDER, fileName)
           output_fileName = f"Watermarked_{fileName}"
           Output_path = os.path.join(OUTPUT_FOLDER, output_fileName)
       
           file.save(Upload_path)

           doc = fitz.open(Upload_path)
           for i in range(len(doc)):
               page = doc[i]
               pix  = page.get_pixmap(matrix=fitz.Matrix(2,2))
               img_bytes = io.BytesIO(pix.tobytes("png"))

               preview_filename = f"{fileName}_page_{i}.png"
               preview_path = os.path.join(PREVIEW_FOLDER, preview_filename)
               with open(preview_path,"wb") as img_file:
                   img_file.write(img_bytes.getvalue())

               previews.append({
                   "page": i,
                   "preview_url": f"/preview/{preview_filename}"
               })

        return jsonify(success=True)
         
    return jsonify(success=False, error="Invalid method"), 400
