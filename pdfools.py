from pypdf import PdfReader,PdfWriter
import os
import subprocess
import pdfkit
from docx2pdf import convert
import fitz

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
      print("Pdfs successfully merged : ",output_path)
   except Exception as e:
      print("Merging failed : ",e)   


# pdf splitter
def splitter(input_file, start_page, end_page, output_path="Slpitted.pdf"): 
   gs_exe = "gswin64c"

   #Ghost Command
   command = [
      gs_exe,
      "-sDEVICE=pdfwrite",
      "-dBATCH",
      "-dQUIET",
      "-dNOPAUSE",
      f"-dFirstPage={start_page}",
      f"-dLastPage={end_page}",
      f"-sOutputFile={output_path}",
      input_file
   ] 

   try:
      subprocess.run(command, check=True)
      print("Pdfs successfully splitted : ",output_path)
   except Exception as e:
      print("Splitting failed : ",e)   

 
# Pdf compresser 
def compress_pdf(input_path, output_path, quality='/screen'):
 gs_exe = "gswin64c"

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
   f"{input_path}.pdf"
  ]

 try:
    subprocess.run(command, check=True)
    print(f"Compressed successfully to : {output_path}")
 except subprocess.CalledProcessError as e:
    print("Compression failed : ",e)  


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
    print("Conversion failed: ",e)           

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
    print("Conversion failed: ",e)           

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
    print("Conversion failed: ",e)           

# Pdf encryption
def pdf_encrypt(input_path, output_path, user_pass, owner_pass):
 gs_exe = "gswin64c"

  #Ghostscript command
 command = [
    gs_exe,
    "-sDEVICE=pdfwrite",
    "-dPDFSETTINGS=/default",
    "-dNOPAUSE",
    "-dQUIET",
    "-dBATCH",
    f"-sUserPassword={user_pass}",
    f"-sOwnerPassword={owner_pass}",
    f"-sOutputFile={output_path}.pdf",
    "-dEncrypt128",
   f"{input_path}.pdf"
  ]

 try:
    subprocess.run(command, check=True)
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

    print(f"Pdf successfully locked : {output_path}")
 except subprocess.CalledProcessError as e:
    print("Process failed: ",e)           

# docx to pdf
def docx_pdf(input_path,output_path):
   try:
      convert(f"{input_path}.docx",f"{output_path}.pdf")
      print("Converted successfully to : ",output_path)
   except Exception as e:
      print("Process failed: ",e)   

# text extraction pdf
def pdf_text_extract(input_path,output_path):
   doc = fitz.open(f"{input_path}.pdf")
   with open(f"{output_path}.txt","w", encoding="utf-8") as f:
      for i,page in enumerate(doc):
         text = page.get_text()
         f.write(f"----Page {1+i}----\n{text}\n\n")
   doc.close()
   print(f"Text saved to :{output_path}.txt")
         
   
val=0
while(val!=11):
 print("\n---------Enter your Operation-----------")
 print("Enter 1 for merge: ")
 print("Enter 2 for split: ")
 print("Enter 3 for compress: ")
 print("Enter 4 for jpg conversion: ")
 print("Enter 5 for png conversion: ")
 print("Enter 6 for tiff conversion: ")
 print("Enter 7 for HTML to PDF conversion: ")
 print("Enter 8 to lock Pdf: ")
 print("Enter 9 for docx to PDF conversion: ")
 print("Enter 10 Pdf text extraction: ")
 print("Enter 11 for exit: ")
  
 op = int(input("\nEnter your operation: "))
 
 match(op):
     case 1:
         file1 = input("Enter first file: ")
         file2 = input("Enter second file: ")
         merger([file1,file2])
     
     case 2:
         file1 = input("Enter file: ")
         file2 = input("Enter file: ")
         Spage = int(input("Enter start page : "))
         Lpage = int(input("Enter end page : "))
         splitter(file1,Spage,Lpage,file2)
     
     case 3:
         file1 = input("Enter file: ")
         file2 = input("Enter file: ")
         compress_pdf(file1,file2,)
     
     case 4:
         file1 = input("Enter file: ")
         file2 = input("Enter file: ")
         quality = input("Set quality [1-100] : ")
         dpi = input("Set resolution default[72dpi]: ")
         pdf_To_Jpeg(file1,file2,quality,dpi)
     
     case 5:
         file1 = input("Enter file: ")
         file2 = input("Enter file: ")
         quality = input("DownGrade by factor : ")
         dpi = input("Set resolution default[150dpi]: ")
         pdf_To_Png(file1,file2,quality,dpi)
     
     case 6:
         file1 = input("Enter file: ")
         file2 = input("Enter file: ")
         dpi = input("Set resolution default[150dpi]: ")
         pdf_To_Tiff(file1,file2,dpi)

     case 7:
       file1 = input("Enter file: ")
       file2 = input("Enter file: ")
       options = {'enable-local-file-access': None}
       pdfkit.from_file(file1, file2, options=options)
     
     case 8:
       file1 = input("Enter file: ")
       file2 = input("Enter file: ")
       userpass= input("Set a user password: ")
       ownerpass= input("Set a owner password: ")
       pdf_encrypt(file1, file2, userpass, ownerpass)
     
     case 9:
       file1 = input("Enter file: ")
       file2 = input("Enter file: ")
       docx_pdf(file1, file2)
     
     case 10:
       file1 = input("Enter file: ")
       file2 = input("Enter file: ")
       pdf_text_extract(file1, file2)

     case 11:
         val=11


