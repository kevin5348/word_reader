console.log("✅ popup.js loaded");

document.getElementById("analyze").addEventListener("click", async () => {
    console.log("🚀 Analyze Page button clicked");

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => {
            console.log("📦 Script injected into tab");
            window.dispatchEvent(new CustomEvent("analyze-readability"));
        }
    });
});
