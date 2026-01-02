import requests
import json

def translate_hindi_to_english(text):
    """Translate Hindi text to English using Google Translate API"""
    try:
        # Using a direct translation approach with requests
        url = "https://translate.googleapis.com/translate_a/element.js?callback=google.translate.onLoad"
        params = {
            'client': 'gtx',
            'sl': 'hi',
            'tl': 'en',
            'dt': 't',
            'q': text
        }
        
        # Alternative: Use a simpler approach with requests
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
        print(f"Error: {e}")
        return text

# Test the translation
text = "मुझे मशीन लर्निंग पसंद है"
print(f"Original (Hindi): {text}")
print(f"Translated (English): {translate_hindi_to_english(text)}")