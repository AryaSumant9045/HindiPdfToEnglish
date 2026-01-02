"""
Hindi PDF to English Translation
Extracts text from Hindi PDF and translates to English
Uses Google Translate API for stability on macOS
"""

import os
import sys
import re

# Disable BLAS threading and MPS to avoid mutex errors on macOS
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'

import requests

def extract_text_from_pdf(pdf_file):
    """
    Extract text from PDF file.
    Tries pdfplumber first (better for complex PDFs), then falls back to PyPDF2
    """
    try:
        import pdfplumber
        print(f"✓ Using pdfplumber for PDF extraction")
        
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            total_pages = len(pdf.pages)
            print(f"  Found {total_pages} pages\n")
            
            for i, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                print(f"  Extracted text from page {i}/{total_pages}")
        
        return text
        
    except ImportError:
        print("⚠ pdfplumber not found. Trying PyPDF2...")
        try:
            import PyPDF2
            
            text = ""
            with open(pdf_file, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                total_pages = len(pdf_reader.pages)
                print(f"  Found {total_pages} pages\n")
                
                for i, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    print(f"  Extracted text from page {i}/{total_pages}")
            
            return text
            
        except ImportError:
            print("✗ Neither pdfplumber nor PyPDF2 found!")
            print("  Installing required packages...")
            os.system("pip install pdfplumber PyPDF2")
            return extract_text_from_pdf(pdf_file)
        except Exception as e:
            print(f"Error extracting PDF with PyPDF2: {e}")
            return None

def split_sentences(text):
    """
    Split text into complete sentences.
    Hindi sentences end with: । (Devanagari danda), ॥ (Double danda), ! or ?
    """
    sentences = re.split(r'([।॥!?]+)', text)
    
    complete_sentences = []
    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i].strip()
        punctuation = sentences[i + 1] if i + 1 < len(sentences) else ''
        
        if sentence:
            complete_sentences.append(sentence + punctuation)
    
    if sentences[-1].strip():
        complete_sentences.append(sentences[-1].strip())
    
    return complete_sentences

def hindi_to_english(text):
    """
    Translate Hindi text to English using Google Translate API
    """
    try:
        url = 'https://translate.googleapis.com/translate_a/single'
        headers = {'User-Agent': 'Mozilla/5.0'}
        params = {
            'client': 'gtx',
            'sl': 'hi',
            'tl': 'en',
            'dt': 't',
            'q': text
        }
        response = requests.get(url, params=params, headers=headers, timeout=5)
        result = response.json()
        return result[0][0][0] if result and result[0] else text
    except Exception as e:
        print(f"API Error: {e}")
        return text

def translate_pdf(pdf_file, output_file="English.txt"):
    """
    Extract text from Hindi PDF and translate to English
    """
    try:
        print("=" * 70)
        print("PDF to English Translator")
        print("=" * 70 + "\n")
        
        # Extract text from PDF
        print(f"Extracting text from: {pdf_file}\n")
        hindi_text = extract_text_from_pdf(pdf_file)
        
        if not hindi_text:
            print("Error: Could not extract text from PDF")
            return
        
        print(f"\n✓ Extracted {len(hindi_text)} characters from PDF\n")
        
        # Split into sentences
        sentences = split_sentences(hindi_text)
        print(f"✓ Found {len(sentences)} complete sentences\n")
        
        # Translate sentences
        print(f"Translating sentences...\n")
        with open(output_file, "w", encoding="utf-8") as out:
            for i, sentence in enumerate(sentences, 1):
                sentence = sentence.strip()
                if sentence:
                    translated = hindi_to_english(sentence)
                    out.write(translated + " ")
                    print(f"Sentence {i}: Translated")
                    if len(sentence) > 70:
                        print(f"  Hindi: {sentence[:70]}...")
                        print(f"  English: {translated[:70]}...\n")
                    else:
                        print(f"  Hindi: {sentence}")
                        print(f"  English: {translated}\n")
        
        print(f"✓ Translation complete!")
        print(f"✓ Output saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"✗ Error: PDF file '{pdf_file}' not found")
    except Exception as e:
        print(f"✗ Error: {e}")

# Main execution
if __name__ == "__main__":
    import glob
    
    # Find Hindi PDF files in current directory
    pdf_files = glob.glob("*.pdf")
    
    if not pdf_files:
        print("Error: No PDF files found in current directory!")
        print("Please place a Hindi PDF file in the current directory.")
        sys.exit(1)
    
    # Use the first PDF file found
    pdf_file = pdf_files[0]
    print(f"\nFound PDF file: {pdf_file}\n")
    
    translate_pdf(pdf_file, "English.txt")
