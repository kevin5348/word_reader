# AI Word Reader  
> An adaptive reading assistant and Chrome extension that helps users learn English through word translation and personalized difficulty modeling.

---

## Overview

**AI Word Reader** combines a **Flask backend**, **PostgreSQL database**, and **Chrome extension** to create a dynamic language-learning environment.  
It identifies words above a user’s English level on the web using the Chrome extension, then translates them into their native language directly on the page and tracks reading behavior to adapt difficulty over time.

The system improves user language modeling accuracy with every session, using **Logistic Moddling**, **Gradient Descent**, and a **custom regression word difficulty model** built from linguistic features.

---

## Key Features

- **In-Page Translation** – Translates difficult words using a free translation API.  
- **Adaptive Difficulty Model** – Updates each user’s proficiency level using a logistic model in real time based on which words they struggle with or understand  
- **Smart Caching** – Stores the 20,000 most common translated words; automatically purges least-used words after 7 days for speed.  
- **Secure Token Auth** – Chrome extension stores encrypted login tokens locally; backend decrypts tokens to identify user sessions and validate requests.  
- **Continuous Learning** – Every click or ignore refines the user’s English proficiency curve using the update model.  
- **Custom Word Regression Model** – Estimates word difficulty using linguistic features (frequency, syllables, length, etc.).  
- **Multi-Language Roadmap** – Designed to support English learning for all native languages.

---

## Languages & Technologies Used

**Backend:** Python, Flask, SQLAlchemy  
**Database:** PostgreSQL  
**Frontend/Extension:** JavaScript (Chrome Extension, Manifest v3), HTML, CSS  
**Authentication:** Token-based auth (stored in Chrome local storage, verified in Flask)  
**APIs:** Free translation API  
**Modeling:** logistic modeling gradient-based optimization for updating level and a regression model (linguistic features: frequency, syllables, length, etc.) for word difficulty  
**Caching:** Custom 20k-word cache system (auto-purges least-used entries every 7 days)  
**Tools:** Git

---

## Next Steps

- **Fix word difficulty model** — Improve and retrain the regression model for word difficulty; current accuracy is low.  
- **Add initial level assessment** — Create a website flow for users to take an initial placement test (e.g., CEFR) to set a starting level.  
- **Polish UI/UX** — Make the frontend visually appealing, increase translation speed, enable the difficulty model to recognize new words and assign levels, and add a popup for suggesting similar words of lower difficulty.  
- **Deploy** — Use Docker to containerize services for testing and production deployment.

---

## Demo

Demo coming soon.

---

