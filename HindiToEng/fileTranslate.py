import requests
import json
import re

def translate_hindi_to_english(text):
    """
    Translate Hindi text to English using Google Translate API
    This approach avoids PyTorch/TensorFlow issues on macOS
    """
    try:
        url = 'https://translate.googleapis.com/translate_a/single'
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        params = {
            'client': 'gtx',
            'sl': 'hi',
            'tl': 'en',
            'dt': 't',
            'q': text
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        result = response.json()
        
        # Extract translated text from response
        translated_text = result[0][0][0] if result and result[0] else text
        return translated_text
        
    except Exception as e:
        print(f"Error translating: {e}")
        return text

def split_sentences(text):
    """
    Split text into complete sentences.
    Hindi sentences end with:
    - । (Devanagari danda - full stop)
    - ॥ (Double danda)
    - ! or ? (English punctuation sometimes used in Hindi)
    """
    # Split by Hindi punctuation marks
    sentences = re.split(r'([।॥!?]+)', text)
    
    complete_sentences = []
    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i].strip()
        punctuation = sentences[i + 1] if i + 1 < len(sentences) else ''
        
        if sentence:  # Only add non-empty sentences
            complete_sentences.append(sentence + punctuation)
    
    # Add the last part if it exists and doesn't end with punctuation
    if sentences[-1].strip():
        complete_sentences.append(sentences[-1].strip())
    
    return complete_sentences

def translate_file(input_file, output_file):
    """
    Translate sentences from Hindi file to English.
    Waits for complete sentences (ending with पूर्णविराम) before translating.
    """
    try:
        # Read entire file
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"File loaded. Total content length: {len(content)} characters\n")
        
        # Split into complete sentences
        sentences = split_sentences(content)
        
        print(f"Found {len(sentences)} complete sentences\n")
        
        # Translate each complete sentence
        with open(output_file, "w", encoding="utf-8") as out:
            for i, sentence in enumerate(sentences, 1):
                sentence = sentence.strip()
                if sentence:
                    translated = translate_hindi_to_english(sentence)
                    out.write(translated + " ")
                    print(f"Sentence {i}: Translated")
                    print(f"  Hindi: {sentence[:80]}{'...' if len(sentence) > 80 else ''}")
                    print(f"  English: {translated[:80]}{'...' if len(translated) > 80 else ''}\n")
        
        print(f"\n✓ Translation complete! Output saved to '{output_file}'")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except Exception as e:
        print(f"Error during file translation: {e}")

# Run the translation
if __name__ == "__main__":
    print("=" * 70)
    print("Hindi to English Sentence-based Translator")
    print("=" * 70)
    print("Note: Translates complete sentences ending with पूर्णविराम (।)\n")
    
    translate_file("Hindi.txt", "english.txt")