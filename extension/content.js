
// Run immediately when script loads
(async function () {
    console.log("Content script loaded");

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', startProcessing);
    } else {
        startProcessing();
    }

    async function startProcessing() {
        try {
            const result = await chrome.storage.local.get(['auth_token']);
            if (result.auth_token) {
                console.log("Word Reader: Starting page processing...");

                const words = extractWordsFromPage();
                console.log(`Found ${words.length} unique words on page`);

                const difficulties = await getWordDifficulties(words);
                console.log("Difficulty scores received:", difficulties);
                
                // Make sure we have translations before proceeding
                if (Object.keys(difficulties).length > 0) {
                    languageTranslation(difficulties);
                    console.log("Language translation applied");
                } else {
                    console.log("No difficult words found or translation failed");
                }

            } else {
                console.log("No auth token found, user not logged in.");
            }
        } catch (error) {
            console.error('Error in content script:', error);
        }
    }
})();

function extractWordsFromPage() {
    const bodyText = document.body.innerText;

    if (!bodyText) {
        console.warn("No text content found in the body.");
        return [];

    }

    // Use a regex to match words, including contractions not numbers and just whole words
    const words = bodyText.match(/\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b/g);
    if (!words) {
        console.warn("No words found in the body text.");
        return [];
    }
    // Convert to lowercase and remove duplicates
    const lowerWords = words.map(word => word.toLowerCase());
    return Array.from(new Set(lowerWords));
}

function languageTranslation(difficulties) {
    console.log("🔄 Starting translation with difficulties:", difficulties);
    
    // Check if difficulties object is valid
    if (!difficulties || typeof difficulties !== 'object' || Object.keys(difficulties).length === 0) {
        console.error("❌ Invalid difficulties object:", difficulties);
        return;
    }
    
    // Debug: Show what words we're trying to translate
    const wordsToTranslate = Object.keys(difficulties);
    console.log(`📝 Words to translate: [${wordsToTranslate.join(', ')}]`);
    
    // Debug: Show translations
    wordsToTranslate.forEach(word => {
        const translation = difficulties[word]?.translation;
        console.log(`📖 "${word}" -> "${translation}"`);
    });
    
    // Simple test first - replace ALL instances of "the" with "LA" to verify DOM manipulation works
    console.log("🧪 Testing basic DOM manipulation...");
    const allText = document.body.innerText;
    if (allText.includes('the')) {
        console.log("Found 'the' in page text - DOM manipulation should work");
    }
    
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        (node) => {
            // Skip script and style tags
            const parent = node.parentNode;
            if (parent && (parent.tagName === 'SCRIPT' || parent.tagName === 'STYLE')) {
                return NodeFilter.FILTER_REJECT;
            }
            return NodeFilter.FILTER_ACCEPT;
        },
        false
    );

    const textNodes = [];
    let node;

    while ((node = walker.nextNode())) {
        textNodes.push(node);
    }

    console.log(`🔍 Found ${textNodes.length} text nodes`);

    let replacementsMade = 0;

    textNodes.forEach((textNode, index) => {
        let text = textNode.nodeValue;
        let originalText = text;

        // Skip empty or whitespace-only text nodes
        if (!text || text.trim().length === 0) {
            return;
        }

        // Debug: Log first few text nodes
        if (index < 5) {
            console.log(`📄 Text node ${index}: "${text.substring(0, 50)}${text.length > 50 ? '...' : ''}"`);
        }

        Object.keys(difficulties).forEach(word => {
            const translationData = difficulties[word];
            const translation = translationData?.translation || word;
            
            // Create regex with word boundaries
            const regex = new RegExp(`\\b${word}\\b`, 'gi');
            
            // Check if word exists in text
            if (regex.test(text)) {
                console.log(`✅ Found "${word}" in text node, replacing with "${translation}"`);
                text = text.replace(regex, translation);
            }
        });

        // Apply changes if text was modified
        if (text !== originalText) {
            console.log(`🔄 REPLACING text node ${index}:`);
            console.log(`   FROM: "${originalText}"`);
            console.log(`   TO:   "${text}"`);
            textNode.nodeValue = text;
            replacementsMade++;
        }
    });

    console.log(`✨ Translation completed. Made ${replacementsMade} replacements.`);
    
    if (replacementsMade === 0) {
        console.warn("⚠️ No replacements made. This could be because:");
        console.warn("   1. Words are not found in text (case sensitivity)");
        console.warn("   2. Words are in different DOM structure");
        console.warn("   3. API didn't return expected translations");
    }
}





async function getWordDifficulties(words) {
    try {
        // Get auth token from storage
        const result = await chrome.storage.local.get(['auth_token']);
        if (!result.auth_token) {
            throw new Error('No auth token found');
        }
        // make the array a string of words separated by commas
        const wordsParam = words.join(',');

        const response = await fetch(`http://localhost:5000/get_difficulties?words=${wordsParam}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${result.auth_token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error status: ${response.status}`);
        }
        const data = await response.json();
        console.log("🔍 Raw API response:", data);
        console.log("🔍 Response type:", typeof data);
        console.log("🔍 Response keys:", Object.keys(data));
        return data
    } catch (error) {
        console.error('Error fetching word difficulties:', error);
        return {};
    }
}