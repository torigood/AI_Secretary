from googletrans import Translator

def translate_to_korean(text):
    translator = Translator()
    try:
        translated = translator.translate(text, src='en', dest='ko')
        return translated.text
    except Exception as e:
        print(f"번역 오류: {e}")
        return text
    
def translate_to_english(text):
    translator = Translator()
    try:
        translated = translator.translate(text, src='ko', dest='en')
        return translated.text
    except Exception as e:
        print(f"영어 번역 오류: {e}")
        return text  # 실패 시 원문 그대로 반환