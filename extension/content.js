
console.log("👀 content.js loaded");

window.addEventListener("analyze-readability", async () => {
    console.log("📘 Received 'analyze-readability' event in content.js");

    // Step 1: Extract words
    const words = Array.from(document.body.innerText.match(/\b\w+\b/g) || []).slice(0, 100);
    const uniqueWords = [...new Set(words.map(w => w.toLowerCase()))];
    console.log("📦 Words extracted:", uniqueWords.slice(0, 10));

    // Step 2: Send to backend
    const userId = "test-user";  // Can make dynamic later
    const query = new URLSearchParams({
        user_id: userId,
        words: uniqueWords.join(",")
    });

    try {
        const res = await fetch(`http://localhost:5000/get_difficulties?${query}`);
        const difficulties = await res.json();
        console.log("📊 Difficulty scores received:", difficulties);

        // Step 3: Highlight hard words (e.g., difficulty > 0.7)
        const threshold = 0.7;
        const pattern = new RegExp(`\\b(${Object.keys(difficulties).join("|")})\\b`, "gi");

        document.body.innerHTML = document.body.innerHTML.replace(pattern, (match) => {
            const score = difficulties[match.toLowerCase()] || 0.5;
            if (score >= threshold) {
                return `<mark style="background-color: yellow;" title="Difficulty: ${score.toFixed(2)}">${match}</mark>`;
            }
            return match;
        });

        console.log("✅ Highlighting complete.");
    } catch (err) {
        console.error("❌ Fetch failed:", err);
    }
});
