from pypdf import PdfReader,PdfWriter
import os

def merger(a,b):   
 merger = PdfWriter()
 for pdf in [f"{a}.pdf",f"{b}.pdf"]:
     merger.append(pdf)
 
 print("merged sucessfully")
 merger.write("merged-pdf1.pdf")
 merger.close()


def splitter(a,b):  
 reader = PdfReader(a)
 writer = PdfWriter()
 for count in range(b):
  writer.add_page(reader.pages[count])
 
 print("pdf splitted succesfully")
 writer.write("splitted-pdf.pdf")
 writer.close()
 reader.close()
 

val=0
while(val!=3):
 print("\n---------Enter your Operation-----------")
 print("Enter 1 for merge: ")
 print("Enter 2 for split: ")
 print("Enter 3 for exit: ")
  
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
       val=3