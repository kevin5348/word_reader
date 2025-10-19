# AI Word Reader  
> An adaptive AI-powered reading assistant and Chrome extension that helps users learn English through intelligent word translation and personalized difficulty modeling.

---

## 🚀 Overview

**AI Word Reader** combines a **Flask backend**, **PostgreSQL database**, and **Chrome extension** to create a dynamic language-learning environment.  
It identifies words above a user’s English level, translates them into their native language directly on the page, and tracks reading behavior to adapt difficulty over time.

The system improves user language modeling accuracy with every session, using **Rasch modeling**, **Fisher information**, and a **custom regression-based word difficulty engine** built from linguistic features such as frequency, syllable count, and length.

---

## ✨ Key Features

- 🌐 **In-Page Translation** –translates difficult words using a free translation API.  
- 🧩 **Adaptive Difficulty Model** – Updates user level in real time using Rasch, Fisher Information, and gradient-based confidence scaling.  
- 📊 **Smart Caching** – Stores the 20,000 most common translated words; automatically purges least used words after 7 days for speed.  
- 🔐 **Secure Token Auth** – Chrome extension stores encrypted login tokens locally; backend decrypts to identify user sessions,sent as a wrapper with everything send to backend .  
- 📈 **Continuous Learning** – Every click or ignore refines the user’s English proficiency curve using update model.  
- 🔄 **Custom Word Regression Model** – Estimates word difficulty via linguistic statistics (frequency, syllables, length, etc.).  
- 🌍 **Multi-Language Roadmap** – Designed to support English learning *and* reverse-learning (other-language learners).  

---

