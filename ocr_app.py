#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
from typing import Union, Optional
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfWriter, PdfReader
from tqdm import tqdm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import re

class OCRApp:
    def __init__(self):
        self.supported_image_formats = ['.jpg', '.jpeg', '.png']
        self.supported_pdf_formats = ['.pdf']
        self.supported_output_formats = ['.txt', '.pdf']

    def validate_input_file(self, input_file: str) -> bool:
        """Validate if the input file exists and has a supported format."""
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' does not exist.")
            return False

        file_ext = os.path.splitext(input_file)[1].lower()
        if file_ext not in self.supported_image_formats + self.supported_pdf_formats:
            print(f"Error: Unsupported input file format. Supported formats are: "
                  f"{', '.join(self.supported_image_formats + self.supported_pdf_formats)}")
            return False
        return True

    def validate_output_file(self, output_file: str) -> bool:
        """Validate if the output file has a supported format."""
        file_ext = os.path.splitext(output_file)[1].lower()
        if file_ext not in self.supported_output_formats:
            print(f"Error: Unsupported output file format. Supported formats are: "
                  f"{', '.join(self.supported_output_formats)}")
            return False
        return True

    def process_image(self, image_path: str) -> str:
        """Process an image file and return the extracted text."""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return ""

    def process_pdf(self, pdf_path: str) -> str:
        """Process a PDF file and return the extracted text."""
        try:
            # Get total number of pages
            pdf = PdfReader(pdf_path)
            total_pages = len(pdf.pages)
            print(f"\nTotal pages in PDF: {total_pages}")

            # Convert PDF to images with progress tracking
            print("\nConverting PDF to images...")
            images = convert_from_path(pdf_path)
            
            text = ""
            # Process each page with detailed progress
            for i, image in enumerate(tqdm(images, desc="Processing PDF pages", total=total_pages)):
                print(f"\nProcessing page {i+1} of {total_pages}")
                page_text = pytesseract.image_to_string(image)
                if page_text.strip():  # Only add non-empty pages
                    text += f"\n{'='*50}\nPage {i+1}\n{'='*50}\n{page_text}\n"
                else:
                    print(f"Warning: No text extracted from page {i+1}")
            
            if not text.strip():
                print("Warning: No text could be extracted from any page of the PDF")
            return text
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return ""

    def save_text(self, text: str, output_file: str) -> bool:
        """Save extracted text to a file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        except Exception as e:
            print(f"Error saving text file: {str(e)}")
            return False

    def clean_text_for_pdf(self, text: str) -> str:
        """Clean text for PDF generation by removing special characters and formatting."""
        # Replace special characters that might cause issues
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        # Remove any other potentially problematic characters
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        return text

    def save_pdf(self, text: str, output_file: str) -> bool:
        """Save extracted text as a PDF file."""
        try:
            # Create custom styles
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(
                name='CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                leading=14,
                alignment=TA_LEFT
            ))
            styles.add(ParagraphStyle(
                name='CustomHeading',
                parent=styles['Heading1'],
                fontSize=14,
                leading=18,
                alignment=TA_LEFT
            ))

            # Create the PDF document
            doc = SimpleDocTemplate(
                output_file,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            # Prepare the content
            story = []
            pages = text.split('='*50)
            
            for page in pages:
                if not page.strip():
                    continue
                
                # Split page into lines and process each line
                lines = page.split('\n')
                for i, line in enumerate(lines):
                    if not line.strip():
                        continue
                    
                    # Clean the line text
                    clean_line = self.clean_text_for_pdf(line.strip())
                    
                    if i == 0 and "Page" in line:  # Page number
                        story.append(Paragraph(clean_line, styles['CustomHeading']))
                        story.append(Spacer(1, 12))
                    else:  # Regular text
                        story.append(Paragraph(clean_line, styles['CustomNormal']))
                        story.append(Spacer(1, 6))
                
                story.append(PageBreak())
            
            # Build the PDF
            doc.build(story)
            return True
        except Exception as e:
            print(f"Error saving PDF file: {str(e)}")
            return False

    def process_file(self, input_file: str, output_file: str) -> bool:
        """Process the input file and save the output."""
        if not self.validate_input_file(input_file) or not self.validate_output_file(output_file):
            return False

        # Determine file type and process accordingly
        file_ext = os.path.splitext(input_file)[1].lower()
        if file_ext in self.supported_image_formats:
            text = self.process_image(input_file)
        elif file_ext in self.supported_pdf_formats:
            text = self.process_pdf(input_file)
        else:
            return False

        if not text:
            print("Error: No text could be extracted from the file.")
            return False

        # Save the output
        output_ext = os.path.splitext(output_file)[1].lower()
        if output_ext == '.txt':
            return self.save_text(text, output_file)
        elif output_ext == '.pdf':
            return self.save_pdf(text, output_file)
        return False

    def interactive_mode(self):
        """Run the application in interactive mode."""
        print("\nOCR Command-Line Application")
        print("===========================")
        
        # Get input file
        while True:
            input_file = input("\nEnter the path to your input file (PDF or image): ").strip()
            if self.validate_input_file(input_file):
                break

        # Get output format
        while True:
            print("\nSelect output format:")
            print("1. Text file (.txt)")
            print("2. PDF file (.pdf)")
            choice = input("Enter your choice (1 or 2): ").strip()
            
            if choice == "1":
                output_ext = ".txt"
                break
            elif choice == "2":
                output_ext = ".pdf"
                break
            else:
                print("Invalid choice. Please try again.")

        # Get output file path
        while True:
            output_file = input(f"\nEnter the output file path (with {output_ext} extension): ").strip()
            if self.validate_output_file(output_file):
                break

        # Process the file
        print("\nProcessing file...")
        if self.process_file(input_file, output_file):
            print(f"\nSuccess! Output saved to: {output_file}")
        else:
            print("\nFailed to process the file.")

def main():
    parser = argparse.ArgumentParser(description="OCR Command-Line Application")
    parser.add_argument("--input", help="Input file path (PDF or image)")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--format", choices=["txt", "pdf"], help="Output format (txt or pdf)")
    
    args = parser.parse_args()
    app = OCRApp()

    if args.input and args.output and args.format:
        # Command-line mode
        output_file = args.output if args.output.endswith(f".{args.format}") else f"{args.output}.{args.format}"
        if app.process_file(args.input, output_file):
            print(f"Success! Output saved to: {output_file}")
        else:
            print("Failed to process the file.")
    else:
        # Interactive mode
        app.interactive_mode()

if __name__ == "__main__":
    main() 