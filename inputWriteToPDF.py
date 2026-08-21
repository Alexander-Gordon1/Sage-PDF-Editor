#colours for sage pallet
#green = rgb(94, 142, 39)
#gray = rgb(122, 121, 121)


import os
import fitz  # PyMuPDF
import time
from pathlib import Path

from utils import resource_path, get_output_folder

colGREY = (166/255, 166/255, 166/255)
colGREEN = (94/255, 142/255, 39/255)
colBLACK = (0, 0, 0)
colRED = (192/255, 0, 0)

# extracts the instruction from the csv format
def parse_instruction(cell_text):
    return cell_text.split('|+|')

def find_pdf_in_csv(file_name):
    with open(resource_path('fileRecords.csv'), 'r') as csv_file:
        for line in csv_file:
            print(line)
            parts = line.strip().split(',')
            if parts[0] == file_name:
                # Everything after the filename, minus any empty trailing cells
                return [cell for cell in parts[1:] if cell.strip()]
    raise ValueError(f"File name '{file_name}' not found in CSV.")



def add_text_to_pdf(doc, pageNumber, xPos, yPos, colour, textToInsert):

    
    #try and open the 
    try:
        page = doc[pageNumber] #page number indexed from 0
    except IndexError:
        raise ValueError("Document has no pages.")

    
    page.insert_text(
        (xPos, yPos), # starts from bottom left and move right. 
        textToInsert, #text being incerted
        fontsize=12, 
        color=colour # can also be words, but restricted to on obv ones
    )



def open_and_write(file_name, patient_dict):
    
    #try finding sinstructions in the csv file, if not raise error
    try:
        instructions = find_pdf_in_csv(file_name)
    except ValueError as e:
        print(e)
        return


    doc = fitz.open(resource_path(os.path.join("origonalPDFs", file_name)))

    
    for instruction in instructions:
        pageNumber, xPos, yPos, colour, textToInsert = parse_instruction(instruction)

        try:
            pageNumber = int(pageNumber)
            xPos = float(xPos)
            yPos = float(yPos)
            colour = eval(colour)  # Convert string to actual color tuple
            text = patient_dict[textToInsert]  # Assuming textToInsert is a key in patient_dict
        except ValueError as e:
            print(f"Error parsing instruction '{instruction}': {e}") # will need to abort program if this happens as it will invalidate the documet. 
            continue  # Skip this instruction and move to the next

        try:
            add_text_to_pdf(doc, pageNumber, xPos, yPos, colour, text)
        except Exception as e:
            print(f"Error adding text {text} to PDF: {e}")

    output_folder = get_output_folder()
    output_filename = f"{Path(file_name).stem}_{int(time.time())}.pdf"
    output_path = os.path.join(output_folder, output_filename)
    doc.save(output_path)
    doc.close()
    print(f"Saved: {output_path}")
        
        
    
        

    


def main():

    patient_data = {
    "NAME": "John Smith",
    "DOB": "01/01/1990",
    "POSTCODE": "SO14 3AB",
    "ADDRESS1": "14 Elm Grove, Southampton, SO15 2JA",
    "ADDRESS2": "",
    "ADDRESS3": "",
    "DATE_OF_APPOINTMENT": "15/08/2026",
    "PREFERRED_GP": "Dr Patel",
    "SURGERY": "15/08/2026",
    "BOTOX_BATCH": "NO_1781617",
    "BOTOX_EXPIRY_DATE": "15/08/2026",
    "IN_NORMAL_SALINE": "15/08/2026",
    "NOK_NAME": "John Doe",
    "NOK_RELATIONSHIP": "Brother",
    "NOK_PHONE": "0123456789",
    "CONTACT_DETAILS": "idk im sure you have them all now",
    "PHONE_NUMBER": "0123456789",
    "EMAIL_ADDRESS": "john.smith@example.com",
    "GENDER": "Male",
    "AGE": "36",

    }

    open_and_write("Sage MS Consent Form V 1.pdf", patient_data)  # Replace "example_file_name" with the actual file name you want to process


if __name__ == "__main__":
    main()