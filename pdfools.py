from pypdf import PdfReader,PdfWriter
import os
import subprocess

# pdf merger
def merger(a,b):   
 merger = PdfWriter()
 for pdf in [f"{a}.pdf",f"{b}.pdf"]:
     merger.append(pdf)
 
 print("merged sucessfully")
 merger.write("merged-pdf1.pdf")
 merger.close()

# pdf splitter
def splitter(a,b):  
 reader = PdfReader(a)
 writer = PdfWriter()
 for count in range(b):
  writer.add_page(reader.pages[count])
 
 print("pdf splitted succesfully")
 writer.write("splitted-pdf.pdf")
 writer.close()
 reader.close()
 
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

val=0
while(val!=7):
 print("\n---------Enter your Operation-----------")
 print("Enter 1 for merge: ")
 print("Enter 2 for split: ")
 print("Enter 3 for compress: ")
 print("Enter 4 for jpg conversion: ")
 print("Enter 5 for png conversion: ")
 print("Enter 6 for tiff conversion: ")
 print("Enter 7 for exit: ")
  
 op = int(input("\nEnter your operation: "))
 
 match(op):
     case 1:
         file1 = input("Enter first file: ")
         file2 = input("Enter second file: ")
         merger(file1,file2)
     
     case 2:
         file1 = input("Enter file: ")
         file2 = int(input("Enter split end page: "))
         splitter(file1,file2)
     
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
         val=7


