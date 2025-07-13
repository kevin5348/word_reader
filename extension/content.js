
// Run immediately when script loads
(async function () {
    console.log("Content script loaded");

    // Wait a bit for Chrome APIs to be available
    await new Promise(resolve => setTimeout(resolve, 100));

    if (typeof chrome === 'undefined' || !chrome.storage || !chrome.storage.local) {
        console.error('Chrome storage API not available');
        return;
    }

    try {
        const result = await chrome.storage.local.get(['auth_token']);
        if (result.auth_token) {
            console.log("Word Reader: Starting page processing...");

            const words = extractWordsFromPage();
            console.log(`Found ${words.length} unique words on page`);

            const difficulties = await getWordDifficulties(words);
            console.log("Difficulty scores received:", difficulties);

        } else {
            console.log("No auth token found, user not logged in.");
        }
    } catch (error) {
        console.error('Error in content script:', error);
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
            method: 'GET', // Changed from POST
            headers: {
                'Authorization': `Bearer ${result.auth_token}`, // Added auth
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching word difficulties:', error);
        return {};
    }
}