
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

                const words = extractWordsFromPage();
                console.log(`Found ${words.length} unique words on page`);

                const difficulties = await getWordDifficulties(words);
                console.log("Difficulty scores received:", difficulties);

                // Make sure we have translations before proceeding
                if (Object.keys(difficulties).length > 0) {
                    languageTranslation(difficulties);
                } else {
                    console.log("No difficult words found");
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
    // Check if difficulties object is valid
    if (!difficulties || typeof difficulties !== 'object' || Object.keys(difficulties).length === 0) {
        console.error("Invalid difficulties object:", difficulties);
        return;
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

    let replacementsMade = 0;

    textNodes.forEach((textNode, index) => {
        let text = textNode.nodeValue;
        let originalText = text;

        if (!text || text.trim().length === 0) {
            return;
        }

        Object.keys(difficulties).forEach(word => {
            const translationData = difficulties[word];
            const translation = translationData?.translation || word;

            // Create regex with word boundaries
            const regex = new RegExp(`\\b${word}\\b`, 'gi');

            // Check if word exists in text
            if (regex.test(text)) {
                const fragment = document.createDocumentFragment();
                let lastIndex = 0;

                text.replace(regex, (match, offset) => {
                    if (offset > lastIndex) {
                        fragment.appendChild(document.createTextNode(text.slice(lastIndex, offset)));
                    }

                    const span = document.createElement("span");
                    span.textContent = translation;
                    span.className = "translated";
                    span.style.backgroundColor = 'red';
                    fragment.appendChild(span);

                    lastIndex = offset + match.length;
                });
                if (lastIndex < TextTrack.length) {
                    fragment.appendChild(document.createTextNode(text.slice(lastIndex)));
                }
                textNode.replaceWith(fragment);
                replacementsMade++;
            }

        });


    });

    if (replacementsMade === 0) {
        console.warn("No replacements made.");

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
        return data
    } catch (error) {
        console.error('Error fetching word difficulties:', error);
        return {};
    }
}

try { translatedWordClicked() }
catch (error) {
    console.error('Error getting clicked words');
}



function translatedWordClicked() {
    const span = document.querySelector('span');
    span.addEventListener('click', () => {
        if (span.className == 'translated') {
            span.style.backgroundColor = 'blue';
            console.log("colour changed");
            return span
        }
        else return;

    });
}