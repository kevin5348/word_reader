# AI Word Reader  
> An adaptive reading assistant and Chrome extension that helps users learn English through word translation and personalized difficulty modeling.

---

##  Overview

**AI Word Reader** combines a **Flask backend**, **PostgreSQL database**, and **Chrome extension** to create a dynamic language-learning environment.  
It identifies words above a user’s English level on the web using the chrome extension then translates them into their native language directly on the page and tracks reading behavior to adapt difficulty over time.

The system improves user language modeling accuracy with every session, using **Rasch modeling**, **Fisher information**, and a **custom regression word difficulty model ** built from linguistic features such as frequency, syllable count, and length.

---

##  Key Features

-  **In-Page Translation** –translates difficult words using a free translation API.  
-  **Adaptive Difficulty Model** – Updates user level in real time using Rasch, Fisher Information, and gradient-based confidence scaling.  
-  **Smart Caching** – Stores the 20,000 most common translated words; automatically purges least used words after 7 days for speed.  
-  **Secure Token Auth** – Chrome extension stores encrypted login tokens locally; backend decrypts to identify user sessions,sent as a wrapper with everything send to backend .  
-  **Continuous Learning** – Every click or ignore refines the user’s English proficiency curve using update model.  
-  **Custom Word Regression Model** – Estimates word difficulty using linguistic features (frequency, syllables, length, etc).  
-  **Multi-Language Roadmap** – Designed to support English learning for all languages.

---
##  Languages & Technologies Used

**Backend:** Python, Flask, SQLAlchemy  
**Database:** PostgreSQL  
**Frontend/Extension:** JavaScript (Chrome Extension, Manifest v3), HTML, CSS 
**Authentication:** Token-based auth (stored in Chrome local storage, verified in Flask)  
**APIs:** Free translation API  
**Modeling:** regression model (Rasch and Fisher information) for updating level and regession model (linguistic features (frequency, syllables, length, etc)) for word diffculty  
**Caching:** Custom 20k-word cache system (auto-purges least-used entries every 7 days)  
**Tools:** VS Code, Git, Docker (for testing and deployment)

---

## Next Steps
-  
-  **Plan to fix word difficulty level model** Need to fix ression model for word diffiucluty as accuracy is low
-  **Add intial level system** Need website for users to get tested on initial level using the Common European Framework of Reference for Languages
-  **Polish** Make frontend visualy appealing increase translate speed. Add abilty for word difficulty model to reconise new words and give a level to them. Add popup for similar word of less difficulty/desciption of words.Fix refesh token. 
-  **Deploy** Using docker to containerize for testing  

---

##Demo coming soon

---

