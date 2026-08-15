#colours for sage pallet
#green = rgb(94, 142, 39)
#gray = rgb(122, 121, 121)


import fitz  # PyMuPDF

colGRAY = (122/255, 121/255, 121/255)
colGREEN = (94/255, 142/255, 39/255)


# extracts the instruction from the csv format
def parse_instruction(cell_text):
    return cell_text.split('|+|')

def find_pdf_in_csv(file_name):
    with open('fileRecords.csv', 'r') as csv_file:
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
        fontsize=14, 
        color=colour # can also be words, but restricted to on obv ones
    )



def open_and_write(file_name, patient_dict):
    
    #try finding sinstructions in the csv file, if not raise error
    try:
        instructions = find_pdf_in_csv(file_name)
    except ValueError as e:
        print(e)
        return


    doc = fitz.open(f"origonalPDFs/{file_name}")

    
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

    doc.save("outputfromtestprogram.pdf") # NEEDS TO BE CHANGES TO SAVE INTO A DUMP FOLDER, ALSO TO BE DELETED AFTER PRINTING. 
    doc.close()
    print(f"Saved: {"outputfromtestprogram.pdf"}")
        
        
    
        

    


def main():

    patient_data = {
    "NAME": "John Smith",
    "DOB": "01/01/1990",
    "POSTCODE": "SO14 3AB",
    "ADDRESS1": "14 Elm Grove, Southampton, SO15 2JA",
    "ADDRESS2": "",
    "ADDRESS3": "",
    "GP": "Dr Patel",
    "SURGERY_DATE": "15/08/2026",
    # ... whatever else your 11 fields are
}

    open_and_write("Botox consent form 2025.pdf", patient_data)  # Replace "example_file_name" with the actual file name you want to process


if __name__ == "__main__":
    main()