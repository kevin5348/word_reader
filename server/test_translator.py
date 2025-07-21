import asyncio
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator

class Translator:
    def __init__(self, source='auto', target='es', max_workers=5):
        self.source = source
        self.target = target
        self.max_workers = max_workers    
        
    def translate_word(self, word):
        try:
            translator = GoogleTranslator(source=self.source, target=self.target)
            translation = translator.translate(word)
            return word, translation
        except Exception as e: 
            print(f"Translation error for '{word}': {e}")
            return word, word
    
    async def translate_words(self, words):
        if not words:
            return {}
            
        loop = asyncio.get_event_loop()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            tasks = [
                loop.run_in_executor(executor, self.translate_word, word)
                for word in words
            ]
            
            results = await asyncio.gather(*tasks)
            return dict(results)

# Test the translator directly
def test_translator():
    try:
        translator = Translator(source='auto', target='es', max_workers=3)
        
        test_words = ["hello", "world", "test"]
        
        async def run_translation():
            return await translator.translate_words(test_words)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            translations = loop.run_until_complete(run_translation())
            print("Success! Translations:", translations)
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error in translator test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_translator()
