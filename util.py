import uuid
import hashlib
from fpdf import FPDF
import os
import io
from flask import send_file

#portrait layout, mm unit of measurement, and letter format (short bp)
pdf = FPDF('P', 'mm', 'Letter')


def generateUUID(input:str)->str:
    final_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, input)).replace("-", "")
    return final_id


def hashMD5(input:str):
    hashed =  hashlib.md5(input.encode())

    return str(hashed.hexdigest())

def createPDF(leasingID:str):
    #portrait layout, mm unit of measurement, and letter format (short bp)
    pdf = FPDF('P', 'mm', 'Letter')
    pdf.add_page()
    
    #regular helvetica and 16 font-size
    pdf.set_font('helvetica','',16)

    #one line is cell, multi-line is multi_cell
    #width = 0 (sets the width to the entire page)
    #width 40, length 10, content of cell
    pdf.cell(40,10,'Hello World!')

    directory = f"static\\{leasingID}"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = generateUUID(leasingID)
    pdf.output(f"static\\{leasingID}\{filename}_contract.pdf")
    return filename

def convertPDFasBlob(file_path:str, leasing_doc_name:str):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        # Create an in-memory file object
        file_object = io.BytesIO(file.read())

    # Return the file as a blob
    return send_file(file_object, attachment_filename=leasing_doc_name, as_attachment=True)
