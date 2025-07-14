from deep_translator import GoogleTranslator
import time
from functools import lru_cache
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading

# Expanded dictionary for 100 words
DICTIONARY = {
    'abstract': 'abstracto', 'abundant': 'abundante', 'accelerate': 'acelerar',
    'accessible': 'accesible', 'accomplish': 'lograr', 'accumulate': 'acumular',
    'accurate': 'preciso', 'achieve': 'lograr', 'acquire': 'adquirir',
    'adequate': 'adecuado', 'adjacent': 'adyacente', 'adolescent': 'adolescente',
    'advocate': 'abogar', 'aesthetic': 'estético', 'affection': 'afecto',
    'aggressive': 'agresivo', 'agriculture': 'agricultura', 'ambiguous': 'ambiguo',
    'ambitious': 'ambicioso', 'analyze': 'analizar', 'ancient': 'antiguo',
    'anniversary': 'aniversario', 'anonymous': 'anónimo', 'anticipate': 'anticipar',
    'anxiety': 'ansiedad', 'apparent': 'aparente', 'appreciate': 'apreciar',
    'appropriate': 'apropiado', 'arbitrary': 'arbitrario', 'architecture': 'arquitectura',
    'articulate': 'articular', 'artificial': 'artificial', 'associate': 'asociar',
    'assume': 'asumir', 'astonish': 'asombrar', 'atmosphere': 'atmósfera',
    'attentive': 'atento', 'attribute': 'atributo', 'audience': 'audiencia',
    'authentic': 'auténtico', 'authority': 'autoridad', 'automatic': 'automático',
    'available': 'disponible', 'average': 'promedio', 'background': 'fondo',
    'behavior': 'comportamiento', 'beneficial': 'beneficioso', 'biography': 'biografía',
    'brilliant': 'brillante', 'calculate': 'calcular', 'candidate': 'candidato',
    'capacity': 'capacidad', 'category': 'categoría', 'celebrate': 'celebrar',
    'ceremony': 'ceremonia', 'challenge': 'desafío', 'character': 'personaje',
    'characteristic': 'característica', 'chemical': 'químico', 'circumstance': 'circunstancia',
    'citizen': 'ciudadano', 'civilization': 'civilización', 'classify': 'clasificar',
    'climate': 'clima', 'colleague': 'colega', 'collection': 'colección',
    'combination': 'combinación', 'comfortable': 'cómodo', 'command': 'comando',
    'comment': 'comentario', 'commercial': 'comercial', 'commission': 'comisión',
    'commitment': 'compromiso', 'communicate': 'comunicar', 'community': 'comunidad',
    'comparable': 'comparable', 'compete': 'competir', 'competent': 'competente',
    'complex': 'complejo', 'component': 'componente', 'comprehensive': 'comprensivo',
    'concentrate': 'concentrar', 'concept': 'concepto', 'conclusion': 'conclusión',
    'condition': 'condición', 'conference': 'conferencia', 'confidence': 'confianza',
    'conflict': 'conflicto', 'confusion': 'confusión', 'consequence': 'consecuencia',
    'conservative': 'conservador', 'considerable': 'considerable', 'consistent': 'consistente',
    'construct': 'construir', 'contemporary': 'contemporáneo', 'content': 'contenido',
    'context': 'contexto', 'continent': 'continente', 'contract': 'contrato',
    'contribute': 'contribuir', 'controversial': 'controvertido', 'convenient': 'conveniente',
    'conventional': 'convencional', 'conversation': 'conversación', 'coordinate': 'coordinar',
    'corporate': 'corporativo', 'correspond': 'corresponder', 'corrupt': 'corrupto',
    'creative': 'creativo', 'creature': 'criatura', 'criminal': 'criminal',
    'crisis': 'crisis', 'criterion': 'criterio', 'critical': 'crítico',
    'cultural': 'cultural', 'currency': 'moneda', 'current': 'actual',
    'curriculum': 'currículum', 'database': 'base de datos', 'debate': 'debate'
}

# Test words - first 100 keys from dictionary
test_words = list(DICTIONARY.keys())[:100]

print(f"Testing with {len(test_words)} words")
print("=" * 60)

# 1. INDIVIDUAL API TRANSLATION
class IndividualTranslator:
    def __init__(self, source='auto', target='es'):
        self.source = source
        self.target = target
    
    def translate_words(self, words):
        results = {}
        times = []
        
        for word in words:
            try:
                start_time = time.perf_counter()
                translator = GoogleTranslator(source=self.source, target=self.target)
                translation = translator.translate(word)
                end_time = time.perf_counter()
                
                duration = end_time - start_time
                times.append(duration)
                results[word] = translation
                
            except Exception as e:
                print(f"Error translating '{word}': {e}")
                results[word] = word
        
        return results, times

# 2. BATCH TRANSLATION
class BatchTranslator:
    def __init__(self, source='auto', target='es', batch_size=10):
        self.source = source
        self.target = target
        self.batch_size = batch_size
    
    def translate_words(self, words):
        results = {}
        times = []
        translator = GoogleTranslator(source=self.source, target=self.target)
        
        word_list = list(words)
        
        for i in range(0, len(word_list), self.batch_size):
            batch = word_list[i:i+self.batch_size]
            
            try:
                start_time = time.perf_counter()
                batch_text = " ||||| ".join(batch)
                batch_translation = translator.translate(batch_text)
                translations = batch_translation.split(" ||||| ")
                end_time = time.perf_counter()
                
                duration = end_time - start_time
                times.append(duration)
                
                for j, word in enumerate(batch):
                    if j < len(translations):
                        results[word] = translations[j].strip()
                    else:
                        results[word] = word
                        
            except Exception as e:
                print(f"Batch translation error: {e}")
                for word in batch:
                    results[word] = word
        
        return results, times

# 3. CACHED TRANSLATION
class CachedTranslator:
    def __init__(self, source='auto', target='es'):
        self.source = source
        self.target = target
        self.translator = GoogleTranslator(source=source, target=target)
    
    @lru_cache(maxsize=1000)
    def translate_cached(self, word):
        try:
            return self.translator.translate(word)
        except Exception as e:
            print(f"Error translating '{word}': {e}")
            return word
    
    def translate_words(self, words):
        results = {}
        times = []
        
        for word in words:
            start_time = time.perf_counter()
            translation = self.translate_cached(word)
            end_time = time.perf_counter()
            
            duration = end_time - start_time
            times.append(duration)
            results[word] = translation
        
        return results, times

# 4. ASYNC TRANSLATION
class AsyncTranslator:
    def __init__(self, source='auto', target='es', max_workers=3):
        self.source = source
        self.target = target
        self.max_workers = max_workers
    
    def translate_single(self, word):
        try:
            translator = GoogleTranslator(source=self.source, target=self.target)
            return word, translator.translate(word)
        except Exception as e:
            return word, word
    
    async def translate_words(self, words):
        results = {}
        start_time = time.perf_counter()
        
        loop = asyncio.get_event_loop()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            tasks = [
                loop.run_in_executor(executor, self.translate_single, word)
                for word in words
            ]
            
            results_list = await asyncio.gather(*tasks)
            
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        for word, translation in results_list:
            results[word] = translation
        
        return results, [total_time]

# 5. HYBRID TRANSLATION
class HybridTranslator:
    def __init__(self, source='auto', target='es'):
        self.source = source
        self.target = target
        self.translator = GoogleTranslator(source=source, target=target)
        self.dictionary = DICTIONARY
    
    def translate_words(self, words):
        results = {}
        times = []
        
        # Step 1: Dictionary lookup
        start_time = time.perf_counter()
        dict_results = {}
        api_words = []
        
        for word in words:
            if word.lower() in self.dictionary:
                dict_results[word] = self.dictionary[word.lower()]
            else:
                api_words.append(word)
        
        dict_time = time.perf_counter() - start_time
        times.append(dict_time)
        
        # Step 2: API for remaining words
        if api_words:
            start_time = time.perf_counter()
            try:
                batch_text = " ||||| ".join(api_words)
                batch_translation = self.translator.translate(batch_text)
                translations = batch_translation.split(" ||||| ")
                
                api_results = {}
                for i, word in enumerate(api_words):
                    if i < len(translations):
                        api_results[word] = translations[i].strip()
                    else:
                        api_results[word] = word
                        
            except Exception as e:
                print(f"API batch error: {e}")
                api_results = {word: word for word in api_words}
            
            api_time = time.perf_counter() - start_time
            times.append(api_time)
        
        # Combine results
        results = {**dict_results, **api_results}
        
        return results, times

# 6. DICTIONARY ONLY
class DictionaryTranslator:
    def __init__(self):
        self.dictionary = DICTIONARY
    
    def translate_words(self, words):
        results = {}
        times = []
        
        for word in words:
            start_time = time.perf_counter()
            translation = self.dictionary.get(word.lower(), word)
            end_time = time.perf_counter()
            
            duration = end_time - start_time
            times.append(duration)
            results[word] = translation
        
        return results, times

# Testing function
def test_translator(translator, name, words, show_sample=5):
    print(f"\n=== {name} ===")
    
    if name == "Async Translation":
        # Handle async separately
        async def run_async():
            return await translator.translate_words(words)
        
        results, times = asyncio.run(run_async())
    else:
        results, times = translator.translate_words(words)
    
    total_time = sum(times)
    avg_time = total_time / len(times) if times else 0
    
    # Show sample results
    print(f"Sample translations (first {show_sample}):")
    for i, (word, translation) in enumerate(list(results.items())[:show_sample]):
        print(f"  '{word}' → '{translation}'")
    
    print(f"\nResults:")
    print(f"  Total time: {total_time:.3f}s")
    print(f"  Average time per batch: {avg_time:.3f}s")
    print(f"  Words translated: {len(results)}")
    print(f"  Rate: {len(results)/total_time:.1f} words/second")
    
    return total_time, len(results)

# Run all tests
print("🚀 COMPREHENSIVE TRANSLATION SPEED TEST")
print(f"Testing {len(test_words)} words with each method")
print("=" * 60)

# Dictionary only (baseline)
dict_translator = DictionaryTranslator()
dict_time, dict_count = test_translator(dict_translator, "Dictionary Only", test_words)

# Individual API (no optimization - 100 words)
individual_translator = IndividualTranslator()
individual_time, individual_count = test_translator(individual_translator, "Individual API (No Optimization)", test_words)

# Batch API
batch_translator = BatchTranslator(batch_size=10)
batch_time, batch_count = test_translator(batch_translator, "Batch API Translation", test_words)

# Cached API
cached_translator = CachedTranslator()
cached_time, cached_count = test_translator(cached_translator, "Cached API Translation", test_words)

# Async API
async_translator = AsyncTranslator(max_workers=3)
async_time, async_count = test_translator(async_translator, "Async Translation", test_words)

# Hybrid approach
hybrid_translator = HybridTranslator()
hybrid_time, hybrid_count = test_translator(hybrid_translator, "Hybrid Translation", test_words)

# Final comparison
print("\n" + "=" * 60)
print("📊 FINAL COMPARISON")
print("=" * 60)

results = [
    ("Dictionary Only", dict_time, dict_count),
    ("Individual API (No Optimization)", individual_time, individual_count),
    ("Batch API", batch_time, batch_count),
    ("Cached API", cached_time, cached_count),
    ("Async API", async_time, async_count),
    ("Hybrid", hybrid_time, hybrid_count)
]

# Sort by time
results.sort(key=lambda x: x[1])

print(f"{'Method':<20} {'Time (s)':<12} {'Rate (w/s)':<12} {'Speed vs Dict':<15}")
print("-" * 65)

for method, time_taken, word_count in results:
    rate = word_count / time_taken if time_taken > 0 else 0
    speed_vs_dict = dict_time / time_taken if time_taken > 0 else 0
    print(f"{method:<20} {time_taken:<12.3f} {rate:<12.1f} {speed_vs_dict:<15.1f}x")

print("\n🏆 Winner: Fastest method is", results[0][0])
print("💡 Best for production: Hybrid (speed + flexibility)")
print("🔧 Best for development: Dictionary Only (instant + offline)")

# DETAILED EXPLANATION OF ASYNC TRANSLATION
print("\n" + "=" * 80)
print("📚 ASYNC TRANSLATION EXPLANATION")
print("=" * 80)

print("""
🔍 HOW ASYNC TRANSLATION WORKS:

1. PROBLEM WITH SEQUENTIAL TRANSLATION:
   - Individual API calls one by one: Word1 → Word2 → Word3 → ...
   - Each API call takes ~0.3-0.5 seconds
   - 100 words = 30-50 seconds total (blocking)
   - CPU sits idle waiting for network responses

2. ASYNC SOLUTION - CONCURRENT EXECUTION:
   - Multiple API calls happen simultaneously
   - Uses ThreadPoolExecutor to manage worker threads
   - Each thread handles one translation independently
   - Total time ≈ slowest single request (not sum of all)

3. TECHNICAL IMPLEMENTATION:

   class AsyncTranslator:
       def __init__(self, max_workers=3):
           self.max_workers = 3  # Number of concurrent threads
       
       def translate_single(self, word):
           # This runs in a separate thread
           translator = GoogleTranslator(source='auto', target='es')
           return word, translator.translate(word)
       
       async def translate_words(self, words):
           # Create event loop and thread pool
           loop = asyncio.get_event_loop()
           
           with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
               # Create tasks for all words at once
               tasks = [
                   loop.run_in_executor(executor, self.translate_single, word)
                   for word in words
               ]
               
               # Wait for ALL tasks to complete
               results_list = await asyncio.gather(*tasks)
           
           return results

4. EXECUTION FLOW:
   
   Sequential (Individual):     Async (Concurrent):
   ┌─────────────────────┐     ┌─────────────────────┐
   │ Word1 → 0.3s        │     │ Word1 ─┐            │
   │ Word2 → 0.3s        │     │ Word2 ─┤ → 0.3s     │
   │ Word3 → 0.3s        │     │ Word3 ─┘            │
   │ ...                 │     │ ...                 │
   │ Total: 30s          │     │ Total: ~10s         │
   └─────────────────────┘     └─────────────────────┘

5. WHY IT'S FASTER:
   - Network I/O is the bottleneck (not CPU)
   - While one request waits for response, others can start
   - Limited by max_workers (3) to avoid overwhelming API
   - Reduces total time from O(n) to O(n/workers)

6. TRADE-OFFS:
   ✅ Pros:
   - Much faster than sequential
   - Scales well with more words
   - Uses system resources efficiently
   
   ❌ Cons:
   - More complex code
   - May hit API rate limits
   - Memory usage increases with concurrent requests
   - Harder to debug errors

7. PRODUCTION CONSIDERATIONS:
   - Set max_workers based on API limits
   - Add retry logic for failed requests
   - Monitor memory usage with large word lists
   - Consider implementing exponential backoff

8. BROWSER EXTENSION CONTEXT:
   - For 1000+ words on a webpage
   - Async reduces user wait time significantly
   - Must balance speed vs API costs
   - Hybrid approach (dictionary + async) is optimal
""")

print("\n" + "=" * 80)
print("🧪 ASYNC VS SEQUENTIAL COMPARISON")
print("=" * 80)
print(f"Sequential (Individual): ~{individual_time:.1f}s for {individual_count} words")
print(f"Async (Concurrent):      ~{async_time:.1f}s for {async_count} words")
print(f"Speed improvement:       {individual_time/async_time:.1f}x faster")
print(f"Time saved:              {individual_time - async_time:.1f} seconds")
print("\n💡 Async is particularly effective for I/O-bound operations like API calls!")
