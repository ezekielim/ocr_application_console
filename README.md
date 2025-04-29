# OCR Command-Line Application

A user-friendly command-line OCR (Optical Character Recognition) application that converts images and PDFs to text or PDF format.

## Features

- Support for multiple input formats:
  - PDF files
  - Image files (JPEG, PNG)
- Output options:
  - Text file (.txt)
  - PDF file (.pdf)
- User-friendly command-line interface
- Progress indicators and status messages
- Error handling and validation

## Requirements

- Python 3.11.2 or Python 3.11
- Required Python packages:
  - pytesseract
  - pdf2image
  - Pillow
  - PyPDF2
  - argparse
  - tqdm
  - reportlab

## Installation

1. Install Tesseract OCR engine:
   ```bash
   # For Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # For macOS
   brew install tesseract
   
   # For Windows
   # Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. Set up Python environment:

   **Option 1: Using a virtual environment (Recommended)**
   ```bash
   # Install python3-venv if not already installed
   # For Ubuntu/Debian
   sudo apt-get install python3-venv python3-full

   # Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # or
   .\venv\Scripts\activate  # On Windows
   ```

   **Option 2: Using pipx (Alternative for Debian/Ubuntu)**
   ```bash
   # Install pipx
   sudo apt-get install pipx
   pipx ensurepath
   ```

3. Install Python dependencies:
   ```bash
   # If using virtual environment (Option 1)
   pip install -r requirements.txt

   # If using pipx (Option 2)
   pipx install -r requirements.txt
   ```

   Note: If you encounter "externally-managed-environment" error on Debian/Ubuntu, please use one of the above options instead of installing packages system-wide.

## Usage

The application can be used in two ways:

1. Interactive Mode: 
- Esnure you use the full file path for interactive mode: example /home/user/Documents/file.png (works with Jpeg, txt and PDFs)
   ```bash
   python ocr_app.py
   ```
   Follow the prompts to:
   - Select input file
   - Choose output format
   - Specify output location

2. Command-line Arguments:
   ```bash
   python ocr_app.py --input <input_file> --output <output_file> --format <txt|pdf>
   ```

### Examples

1. Convert an image to text:
   ```bash
   python ocr_app.py --input document.jpg --output result.txt --format txt
   ```

2. Convert a PDF to text:
   ```bash
   python ocr_app.py --input document.pdf --output result.txt --format txt
   ```

3. Convert an image to PDF:
   ```bash
   python ocr_app.py --input document.jpg --output result.pdf --format pdf
   ```

## Error Handling

The application includes error handling for:
- Invalid file formats
- Missing input files
- Permission issues
- OCR processing errors

## Output

- Text files will be saved with UTF-8 encoding
- PDF files will maintain the original layout where possible
- Progress and status messages will be displayed during processing

## License

MIT License 