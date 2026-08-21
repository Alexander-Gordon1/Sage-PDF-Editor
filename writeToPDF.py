#colours for sage pallet
#green = rgb(94, 142, 39)
#gray = rgb(122, 121, 121)


import os
import fitz  # PyMuPDF
from pathlib import Path

from utils import resource_path, get_output_folder

colGRAY = (122/255, 121/255, 121/255)
colGREEN = (94/255, 142/255, 39/255)


def add_text_to_pdf( ):

    doc = fitz.open(resource_path("GDPR Notice for signature.pdf"))


    try:
        page = doc[0] #page number indexed from 0
    except IndexError:
        raise ValueError("Document has no pages.")

    
    page.insert_text(
        (101, 185), # starts from bottom left and move right. 
        "Alexander Gordon", #text being incerted
        fontsize=12, 
        color=colGRAY # can also be words, but restricted to on obv ones
    )

    output_folder = get_output_folder()
    output_filename = "outputfromtestprogram.pdf"
    output_path = os.path.join(output_folder, output_filename)
    doc.save(output_path)
    doc.close()
    print(f"Saved: {output_path}")


def main():

    add_text_to_pdf()


if __name__ == "__main__":
    main()