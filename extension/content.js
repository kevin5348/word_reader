console.log("📦 content.js injected");

// === CONFIG ===
const USER_ID = "test-user";
const DIFFICULTY_THRESHOLD = 0.4;
const MAX_WORDS = 1000;

// === STEP 1: Extract words from page ===
function extractWordsFromPage(limit = MAX_WORDS) {
    const text = document.body.innerText;
    const words = text
        .toLowerCase()
        .match(/\b[a-z]{3,}\b/g)  // 3+ letter words only
        ?.slice(0, limit) || [];

    const uniqueWords = [...new Set(words)];
    console.log("🧠 Words extracted:", uniqueWords);
    return uniqueWords;
}

// === STEP 2: Fetch difficulty scores from Flask ===
async function fetchDifficulties(words) {
    const query = new URLSearchParams({
        user_id: USER_ID,
        words: words.join(","),
    });

    const url = `http://localhost:5000/get_difficulties?${query}`;
    console.log("🌐 Fetching:", url);

    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);

    const data = await res.json();
    console.log("✅ Difficulty scores received:", data);
    return data;
}

// === STEP 3: Safely highlight words in DOM ===
function highlightWords(difficulties, threshold = DIFFICULTY_THRESHOLD) {
    const wordsToHighlight = Object.entries(difficulties)
        .filter(([_, score]) => score >= threshold)
        .map(([word]) => word.toLowerCase());

    if (wordsToHighlight.length === 0) {
        console.log("⚠️ No words to highlight");
        return;
    }

    console.log("🟨 Highlighting words:", wordsToHighlight);

    const regex = new RegExp(`\\b(${wordsToHighlight.join('|')})\\b`, "gi");
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);

    while (walker.nextNode()) {
        const node = walker.currentNode;

        // skip non-visible or unsafe nodes
        if (!node.nodeValue.trim()) continue;
        if (node.parentNode.closest("script, style, noscript, iframe")) continue;

        const text = node.nodeValue;
        const matches = [...text.matchAll(regex)];
        if (matches.length === 0) continue;

        const fragment = document.createDocumentFragment();
        let lastIndex = 0;

        for (const match of matches) {
            const start = match.index;
            const end = start + match[0].length;

            fragment.appendChild(document.createTextNode(text.slice(lastIndex, start)));

            const mark = document.createElement("mark");
            mark.className = "highlighted-word";
            mark.textContent = match[0];
            fragment.appendChild(mark);

            lastIndex = end;
        }

        fragment.appendChild(document.createTextNode(text.slice(lastIndex)));
        node.parentNode.replaceChild(fragment, node);
    }

    console.log("✅ Highlighting complete.");
}

// === STEP 4: Inject highlight styles ===
(function injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
    .highlighted-word {
      background: yellow;
      font-weight: bold;
      padding: 0 2px;
    }
  `;
    document.head.appendChild(style);
})();

// === STEP 5: Run the pipeline ===
(async function () {
    try {
        const words = extractWordsFromPage();
        const difficulties = await fetchDifficulties(words);
        highlightWords(difficulties);
    } catch (err) {
        console.error("❌ Extension error:", err);
    }
})();



