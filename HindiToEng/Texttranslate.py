"""
Hindi to English Translation
Uses transformers library with MarianMT model when available,
falls back to Google Translate API for stability on macOS
"""

import os
import sys

# Disable BLAS threading and MPS to avoid mutex errors on macOS
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'

import requests

def hindi_to_english_api(text):
    """
    Translate Hindi to English using Google Translate API (more stable on macOS)
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

def hindi_to_english_transformers(text):
    """
    Translate Hindi to English using transformers library (MarianMT)
    Note: Has threading issues on macOS, use API version instead
    """
    try:
        # These imports trigger the mutex error on macOS
        import torch
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)
        
        from transformers import MarianMTModel, MarianTokenizer
        
        model_name = "Helsinki-NLP/opus-mt-hi-en"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs, max_length=512)
        return tokenizer.decode(translated[0], skip_special_tokens=True)
        
    except Exception as e:
        print(f"Transformers Error (using API fallback): {e}")
        return hindi_to_english_api(text)

# Use API version by default on macOS for stability
def hindi_to_english(text, use_api=True):
    """
    Translate Hindi text to English
    
    Args:
        text: Hindi text to translate
        use_api: If True, uses Google Translate API (more stable on macOS)
                If False, uses transformers library (may crash on macOS)
    
    Returns:
        Translated English text
    """
    if use_api:
        return hindi_to_english_api(text)
    else:
        return hindi_to_english_transformers(text)

# Example usage
if __name__ == "__main__":
    print("Hindi to English Translator")
    print("=" * 50)
    print("Note: Using API version for macOS stability\n")
    
    hindi_text = "भारत एक महान देश है।"
    print(f"Hindi: {hindi_text}")
    
    # Use API method (stable on macOS)
    result = hindi_to_english(hindi_text, use_api=True)
    print(f"English: {result}")
    
    # Uncomment below to use transformers (may crash on macOS)
    # result = hindi_to_english(hindi_text, use_api=False)
    # print(f"English (Transformers): {result}")