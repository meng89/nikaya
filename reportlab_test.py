#!/usr/bin/env python3

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Define the file name
file_name = "document_a4.pdf"

# Create a SimpleDocTemplate object with A4 page size
doc = SimpleDocTemplate(file_name, pagesize=A4)

# Get some styles
styles = getSampleStyleSheet()
normal_style = styles["Normal"]

# Build the story (list of flowables)
story = list()
story.append(Paragraph("This is a document using the A4 page size.", normal_style))
story.append(Paragraph("It uses the high-level Platypus API.", normal_style))

# Build the PDF document
doc.build(story)
