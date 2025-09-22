# -*- coding: utf-8 -*-

"""
This script paginates a Microsoft Word document.
The pagination style is "x of y", where x is the current page number in the section
and y is the total number of pages for that section.

A new section is created on any page that has the text "Name of Incumbent:".
Each section's page numbering starts from one.

Required packages:
- python-docx
- lxml

Install them using:
pip install python-docx lxml
"""

import argparse
import docx
from docx.shared import Pt
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def create_page_number_field(paragraph, field_name):
    """
    Create a page number field in the given paragraph.
    """
    run = paragraph.add_run()
    fldChar = OxmlElement('w:fldChar')
    fldChar.set(qn('w:fldCharType'), 'begin')
    run._r.append(fldChar)

    run = paragraph.add_run()
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = field_name
    run._r.append(instrText)

    run = paragraph.add_run()
    fldChar = OxmlElement('w:fldChar')
    fldChar.set(qn('w:fldCharType'), 'separate')
    run._r.append(fldChar)

    run = paragraph.add_run()
    # This text can be anything, Word will replace it with the page number
    run.text = '1'

    run = paragraph.add_run()
    fldChar = OxmlElement('w:fldChar')
    fldChar.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar)


def add_pagination_to_section(section):
    """
    Adds "x of y" pagination to the footer of a section.
    """
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False
    footer = section.footer
    paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    paragraph.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

    # Add "Page X of Y"
    create_page_number_field(paragraph, 'PAGE')
    paragraph.add_run(' of ')
    create_page_number_field(paragraph, 'SECTIONPAGES')


def copy_run(run, new_para):
    """Copies a run's properties to a new run in a new paragraph."""
    new_run = new_para.add_run(run.text)
    new_run.bold = run.bold
    new_run.italic = run.italic
    new_run.underline = run.underline
    new_run.font.name = run.font.name
    new_run.font.size = run.font.size
    if run.font.color.rgb:
        new_run.font.color.rgb = run.font.color.rgb

def paginate_document(input_path, output_path):
    """
    Paginates a Word document by creating sections and adding page numbers.
    """
    doc = docx.Document(input_path)
    new_doc = docx.Document()
    # Remove the default paragraph that python-docx adds
    if new_doc.paragraphs:
        p = new_doc.paragraphs[0]._p
        p.getparent().remove(p)

    # Copy content and create sections
    # We start with one section by default
    is_first_paragraph = True
    for para in doc.paragraphs:
        if "Name of Incumbent:" in para.text and not is_first_paragraph:
            new_doc.add_section(WD_SECTION_START.NEW_PAGE)

        # Copy paragraph to the new document
        new_para = new_doc.add_paragraph(style=para.style)
        # Copy paragraph alignment
        new_para.alignment = para.alignment

        for run in para.runs:
            copy_run(run, new_para)

        is_first_paragraph = False

    # Add pagination to each section
    for section in new_doc.sections:
        section.different_first_page_header_footer = False
        add_pagination_to_section(section)

    new_doc.save(output_path)


def main():
    """
    Main function to parse arguments and call the pagination function.
    """
    parser = argparse.ArgumentParser(description='Paginates a Word document.')
    parser.add_argument('input', help='Input Word document path.')
    parser.add_argument('output', help='Output Word document path.')
    args = parser.parse_args()

    paginate_document(args.input, args.output)
    print(f"Document paginated successfully. Output saved to: {args.output}")

if __name__ == '__main__':
    main()
