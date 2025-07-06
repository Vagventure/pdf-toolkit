from pypdf import PdfReader,PdfWriter
import os
import subprocess
import pdfkit
from docx2pdf import convert
import fitz
import tkinter as tk
from tkinter import filedialog

# pdf merger
def merger(input_files, output_path="merged.pdf"): 
   gs_exe = "gswin64c"

   #Ghost Command
   command = [
      gs_exe,
      "-sDEVICE=pdfwrite",
      "-dBATCH",
      "-dQUIET",
      "-dNOPAUSE",
      f"-sOutputFile={output_path}"
   ] + input_files

   try:
      subprocess.run(command, check=True)
      print("Pdfs are successfully merged : ",output_path)
   except Exception as e:
      print("Merging failed try again : ",e)   


# pdf splitter
def splitter(input_file,output_path, start_page, end_page): 
   gs_exe = "gswin64c"

   #Ghost Command
   command = [
      gs_exe,
      "-sDEVICE=pdfwrite",
      "-dCompatibilityLevel=1.4",
      "-dBATCH",
      "-dQUIET",
      "-dNOPAUSE",
      f"-dFirstPage={start_page}",
      f"-dLastPage={end_page}",
      f"-sOutputFile={output_path}.pdf",
      input_file
   ] 

   try:
      subprocess.run(command, check=True)
      print(f"Pdf successfully splitted from {start_page}-{end_page} : ",output_path)
   except Exception as e:
      print("Splitting failed try again : ",e)   

 
# Pdf compresser 
def compress_pdf(input_path, output_path, quality):
 gs_exe = "gswin64c"

 match(quality):
    case 1:
       quality = '/prepares'
    case 2: 
       quality = '/printer'
    case 3: 
       quality = '/default'
    case 4: 
       quality = '/ebook'
    case 5: 
       quality = '/screen'
 
  #Ghostscript command
 command = [
    gs_exe,
    "-sDEVICE=pdfwrite",
    "-dCompatibilityLevel=1.4",
    f"-dPDFSETTINGS={quality}",
    "-dNOPAUSE",
    "-dQUIET",
    "-dBATCH",
    f"-sOutputFile={output_path}.pdf",
   input_path
  ]

 try:
    subprocess.run(command, check=True)
    print(f"Pdf successfully compressed to : {output_path}")
 except subprocess.CalledProcessError as e:
    print("Compression failed try again : ",e)  


# Pdf to jpeg images 
def pdf_To_Jpeg(input_path, output_path, quality, dpi=150):
 gs_exe = "gswin64c"

  #Ghostscript command
 command = [
    gs_exe,
    "-sDEVICE=jpeg",
    f"-r{dpi}"
    f"-dJPEGQ={quality}",
    "-dNOPAUSE",
    "-dQUIET",
    "-dBATCH",
    f"-sOutputFile={output_path}%03d.jpg",
   f"{input_path}.pdf"
  ]

 try:
    subprocess.run(command, check=True)
    print(f"Jpeg successfully created at : {output_path}")
 except subprocess.CalledProcessError as e:
    print("Conversion failed try again: ",e)           

# Pdf to png images 
def pdf_To_Png(input_path, output_path, quality, dpi=150):
 gs_exe = "gswin64c"

  #Ghostscript command
 command = [
    gs_exe,
    "-sDEVICE=png16m",
    f"-r{dpi}"
    f"-dDownScaleFactor={quality}",
    "-dNOPAUSE",
    "-dQUIET",
    "-dBATCH",
    f"-sOutputFile={output_path}%03d.png",
    f"{input_path}.pdf"
  ]

 try:
    subprocess.run(command, check=True)
    print(f"Png successfully created at : {output_path}")
 except subprocess.CalledProcessError as e:
    print("Conversion failed try again: ",e)           

# Pdf to tiff images 
def pdf_To_Tiff(input_path, output_path, dpi=150):
 gs_exe = "gswin64c"

  #Ghostscript command
 command = [
    gs_exe,
    "-sDEVICE=tiff24nc",
    f"-r{dpi}"
    "-dNOPAUSE",
    "-dQUIET",
    "-dBATCH",
    f"-sOutputFile={output_path}%03d.tiff",
   f"{input_path}.pdf"
  ]

 try:
    subprocess.run(command, check=True)
    print(f"Tiff successfully created at : {output_path}")
 except subprocess.CalledProcessError as e:
    print("Conversion failed try again : ",e)           

# Pdf encryption
def pdf_encrypt(input_path, output_path, user_pass, owner_pass):
 gs_exe = "gswin64c"

  #Ghostscript command
 command = [
    gs_exe,
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
    f"-sOutputFile={output_path}.pdf",
    input_path
  ]

 try:
    subprocess.run(command, check=True)
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

    print(f"Pdf is successfully locked : {output_path}")
 except subprocess.CalledProcessError as e:
    print("Process failed try again: ",e)           

# docx to pdf
def docx_pdf(input_path,output_path):
   try:
      convert(f"{input_path}.docx",f"{output_path}.pdf")
      print("Pdf successfully created at : ",output_path)
   except Exception as e:
      print("Process failed try again: ",e)   

# text extraction pdf
def pdf_text_extract(input_path,output_path):
   try:
      doc = fitz.open(f"{input_path}.pdf")
      with open(f"{output_path}.txt","w", encoding="utf-8") as f:
         for i,page in enumerate(doc):
            text = page.get_text()
            f.write(f"----Page {1+i}----\n{text}\n\n")
      doc.close()
      print(f"Text saved to :{output_path}.txt")
   except:
      print("Extraction failed try again : ")

# file browser
def browse_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    return file_path

# main   
val=0
while(val!=11):
 print("\n---------Enter your Operation-----------")
 print("Enter 1 for merge: ")
 print("Enter 2 for split: ")
 print("Enter 3 for compress: ")
 print("Enter 4 to Lock a PDF: ")
 print("Enter 5 for PDF to png conversion: ")
 print("Enter 6 for PDF to tiff conversion: ")
 print("Enter 7 for HTML to PDF conversion: ")
 print("Enter 8 for PDF to jpg conversion: ")
 print("Enter 9 for docx to PDF conversion: ")
 print("Enter 10 for Pdf text extraction: ")
 print("Enter 11 for exit: ")
  
 op = int(input("\nEnter your operation: "))
 
 match(op):
     case 1:
         file1 = input("Enter first file: ")
         file2 = input("Output file name: ")
         merger([file1,file2])
     
     case 2:
         file1 = browse_file()
         print("Input file : ",file1)
         file2 = input("Output file name: ")
         Spage = int(input("Enter start page : "))
         Lpage = int(input("Enter end page : "))
         splitter(file1,file2,Spage,Lpage)
     
     case 3:
         file1 = browse_file()
         print("Input file : ",file1)
         file2 = input("Output file name: ")
         quality = int(input("Compression intensity [1-5] : "))
         compress_pdf(file1,file2,quality)
     
     case 4:
         file1 = browse_file()
         print("Input file : ",file1)
         file2 = input("Output file name: ")
         userpass= input("Set a user password: ")
         ownerpass= input("Set a owner password: ")
         pdf_encrypt(file1, file2, userpass, ownerpass)
     
     case 5:
         file1 = browse_file()
         print("Input file : ",file1)
         file2 = input("Output file name: ")
         quality = input("DownGrade by factor : ")
         dpi = input("Set resolution default[150dpi]: ")
         pdf_To_Png(file1,file2,quality,dpi)
     
     case 6:
         file1 = browse_file()
         print("Input file : ",file1)
         file2 = input("Output file name: ")
         dpi = input("Set resolution default[150dpi]: ")
         pdf_To_Tiff(file1,file2,dpi)

     case 7:
         file1 = browse_file()
         print("Input file : ",file1)
         file2 = input("Output file name: ")
         options = {'enable-local-file-access': None}
         pdfkit.from_file(file1, file2, options=options)
     
     case 8:
         file1 = browse_file()
         print("Input file : ",file1)
         file2 = input("Output file name: ")
         quality = input("Set quality [1-100] : ")
         dpi = input("Set resolution default[72dpi]: ")
         pdf_To_Jpeg(file1,file2,quality,dpi)
    
     case 9:
         file1 = browse_file()
         print("Input file : ",file1)
         file2 = input("Output file name: ")
         docx_pdf(file1, file2)
     
     case 10:
         file1 = browse_file()
         print("Input file : ",file1)
         file2 = input("Output file name: ")
         pdf_text_extract(file1, file2)

     case 11:
         val=11


