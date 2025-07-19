# ScouseAI: AI-Powered Due Diligence Platform

**ScouseAI is a full-stack web application that automates corporate due diligence by analyzing real-time public data to identify and classify potential financial, legal, and reputational risks.**

---

### ► Project Overview

Traditional due diligence is a manual, time-consuming, and expensive process. ScouseAI was engineered to solve this problem by leveraging modern software architecture and machine learning. The platform allows a user to input any entity (e.g., a company name) and receive an immediate, article-level risk analysis based on the latest news from multiple sources.

The project is built with a production-mindset, featuring a complete MLOps pipeline where user feedback is used to continuously retrain and improve the underlying AI model over time.

---

### ► Technical Architecture

The application is designed as a robust, multi-component system:

1.  **React Frontend:** A responsive user interface for submitting analysis requests and viewing results.
2.  **FastAPI Backend:** A high-performance Python backend that serves the AI models and manages the database.
3.  **Multi-Source Scraping Engine:** A resilient data ingestion module that scrapes and aggregates news from multiple sources like DuckDuckGo and Bing.
4.  **AI/ML Service:** A sophisticated pipeline featuring a custom-trained financial NLP model for risk classification.
5.  **PostgreSQL Database:** A persistent data store for capturing user feedback to enable model retraining.
6.  **MLOps Retraining Pipeline:** A set of scripts that form a "Human-in-the-Loop" system to continuously improve the AI model's accuracy.

---

### ► Key Features

* **Article-Level Risk Analysis:** Instead of a single summary, the platform provides a detailed breakdown of individual news articles, each with its own risk classification (LOW, MEDIUM, HIGH) and confidence score.
* **State-of-the-Art Financial NLP Model:** Utilizes a **`FinBERT`** model, pre-trained on a massive corpus of financial text, which was then fine-tuned on a custom-built dataset of over 2,000 examples for the specific task of risk assessment.
* **Human-in-the-Loop Feedback System:** A complete, full-stack feedback mechanism that allows users to validate or correct the AI's predictions. This feedback is persisted to a **PostgreSQL** database, turning user interaction into valuable training data.
* **Automated Model Retraining Pipeline:** Includes a Python script that automatically queries the feedback database, combines new data with the original dataset, and retrains a new, improved version of the model, which can then be pushed to the Hugging Face Hub.
* **KPI Analytics Dashboard:** A dedicated dashboard page built with **Recharts** that visualizes the distribution of risk levels from user feedback, providing key insights into the model's performance and trends.
* **Resilient Multi-Source Data Ingestion:** The web scraping engine pulls data from multiple sources simultaneously and includes robust error handling, ensuring the application remains functional even if one source is unavailable.

---

### ► Tech Stack

| Category      | Technologies                                                                          |
|---------------|---------------------------------------------------------------------------------------|
| **Backend** | Python, FastAPI, SQLAlchemy, PostgreSQL, Psycopg2                                     |
| **Frontend** | React.js, JavaScript, HTML/CSS, Recharts                                              |
| **AI/ML** | Hugging Face (Transformers, Datasets, Evaluate), PyTorch, FinBERT, spaCy, Scikit-learn |
| **Data Tools**| Pandas, NumPy, BeautifulSoup, Programmatic Data Augmentation                          |

---

### ► Local Setup & Installation

To run this project locally, follow these steps:

**Prerequisites:**
* Python 3.10+
* Node.js and npm
* PostgreSQL server running locally

### 1. Clone the Repository
```bash
git clone [https://github.com/Bats107/ScouseAI.git](https://github.com/Bats107/ScouseAI.git)
cd ScouseAI
```

### 2. Setup the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set up your PostgreSQL database and user, then run the one-time table creation script
python create_db_tables.py
# Start the server (use the second command if the first one fails)
uvicorn app.main:app --reload
# OR for specific environments:
venv/bin/python -m uvicorn app.main:app --reload
```

### 3. Setup the Frontend
*(In a new terminal)*
```bash
cd frontend
npm install
npm start
```
The application will be available at `http://localhost:3000`.
