# 🛡️ PhishGuard: Phishing Website Detection System Using Machine Learning

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Academic Level](https://img.shields.io/badge/Academic%20Level-B.Tech%20CSE%203rd%20Year-orange.svg)](#)
[![Dataset](https://img.shields.io/badge/UCI%20Repo-ID%20327-red.svg)](https://archive.ics.uci.edu/dataset/327/phishing+websites)

**Author:** Saransh  
**Course:** B.Tech Computer Science and Engineering (3rd Year)  
**Academic Submission:** College Mini-Project  
**Environment:** Python 3 | Jupyter Notebook | Scikit-Learn  

---

## 📌 1. Project Overview

**PhishGuard** is a machine learning-powered cybersecurity detection system designed to identify fraudulent phishing websites. Phishing remains the leading initial attack vector for enterprise data breaches, credential harvesting, and financial fraud. 

Traditional static blacklists (e.g., Google Safe Browsing, PhishTank) are reactive and leave users vulnerable to newly minted zero-day phishing sites during the first 6 to 12 hours of their lifespan. PhishGuard solves this problem by using supervised machine learning algorithms to learn the structural, cryptographic, and behavioral patterns that distinguish malicious web pages from legitimate ones.

PhishGuard features a **dual-track architecture**:
1. **Track A (Trained Machine Learning Pipeline):** Evaluates 30 extracted website telemetry features (SSL certificate validity, anchor tag distributions, DNS parameters, web traffic) using baseline and ensemble classifiers (`DummyClassifier`, `LogisticRegression`, and `RandomForestClassifier`).
2. **Track B (Transparent Rule-Based URL Analyzer):** A standalone, zero-dependency Python function (`analyze_url`) that safely evaluates raw URL strings offline without making external HTTP requests.

---

## ✨ 2. Key Features

* **Empirical Academic Rigor:** Trained on the benchmark UCI Phishing Websites Dataset (11,055 instances, 30 features) with strict zero-leakage stratified 80/20 train-test splitting.
* **Top-Tier Classification Performance:**
  * **Random Forest Classifier:** **97.01% Accuracy**, **97.41% Precision**, **95.82% Recall**, **96.60% F1-Score**, and **0.9968 ROC-AUC**.
  * Out of 980 phishing websites in the unseen test set, Random Forest intercepted **939 attacks**, missing only 41.
* **Cybersecurity Metric Education:** Demonstrates why raw accuracy is misleading in security (e.g., the naive baseline achieves 55.68% accuracy while missing 100% of phishing sites).
* **Feature Importance Insights:** Uncovers that SSL certificate state (`sslfinal_state`, 33.5%) and external anchor link ratios (`url_of_anchor`, 26.6%) are the dominant discriminators of phishing websites.
* **Safe Lexical URL Inspector:** Standalone `analyze_url(url)` checks IP hostnames, excessive length, credential keywords, embedded `@` symbols, excessive subdomains, missing HTTPS, and punycode.
* **Viva Voce Ready:** Includes an integrated viva preparation guide with common 3rd-year defense questions and answers.

---

## 🎯 3. Project Objectives

1. Develop an end-to-end reproducible machine learning pipeline in Jupyter Notebook for phishing website classification.
2. Benchmark a naive baseline against linear (`Logistic Regression`) and non-linear ensemble (`Random Forest`) models.
3. Quantify performance using confusion matrices, precision, recall, F1-scores, and ROC curves.
4. Bridge the gap between multi-feature ML models and raw URL string analysis with transparent heuristics.
5. Create professional, college-submission-ready deliverables including an executable notebook and Microsoft Word report.

---

## 🛠️ 4. Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3.10 / 3.12** | Core programming language |
| **NumPy & Pandas** | High-performance numerical computing and tabular data manipulation |
| **Scikit-Learn** | Stratified splitting, DummyClassifier, LogisticRegression, RandomForestClassifier, and metrics |
| **Matplotlib & Seaborn** | Publication-quality visualizations, confusion matrices, and ROC curves |
| **ucimlrepo** | Official programmatic client for the UCI Machine Learning Repository |
| **python-docx** | Document generation engine for Microsoft Word report automation |
| **Jupyter Notebook / nbconvert** | Interactive coding environment and complete cell execution |

---

## 📊 5. Official Dataset Citation & Schema

* **Repository:** UCI Machine Learning Repository (Dataset ID: `327`)
* **Title:** *Phishing Websites Dataset*
* **Citation:** Mohammad, R., Thabtah, F., and McCluskey, L. (2012). *An Assessment of Features Related to Phishing Websites Using an Automated Technique.*
* **Dataset DOI:** [https://doi.org/10.24432/C51W2X](https://doi.org/10.24432/C51W2X)
* **Dataset URL:** [https://archive.ics.uci.edu/dataset/327/phishing+websites](https://archive.ics.uci.edu/dataset/327/phishing+websites)

### Dataset Properties
* **Total Instances:** 11,055
* **Features:** 30 discrete attributes (taking values `-1`, `0`, or `1`)
* **Missing Values:** 0
* **Class Distribution:**
  * Original encoding: `1` = Legitimate (6,157 instances, 55.69%), `-1` = Phishing (4,898 instances, 44.31%).
  * Cybersecurity recoding: `1` = Phishing (Malicious / Alert), `0` = Legitimate (Safe).

---

## 🚀 6. Installation & Environment Setup

These instructions are tested and verified for **Windows** (PowerShell / Command Prompt) as well as **macOS / Linux**.

### Step 1: Clone or Navigate to the Workspace
```powershell
# Open terminal in the project directory
cd d:\S\projects\cybersecurity_project
```

### Step 2: Ensure Python 3.10+ is Installed
Check your Python version:
```powershell
python --version
```

### Step 3: (Recommended) Create and Activate a Virtual Environment
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
# python3 -m venv venv
# source venv/bin/activate
```

### Step 4: Install Required Dependencies
Install all packages from `requirements.txt`:
```powershell
python -m pip install -r requirements.txt
```

> **Windows PowerShell Tip:** If your environment displays an Application Control or script execution warning, unblock the local site-packages binaries:
> ```powershell
> Get-ChildItem -Path ".\venv\Lib\site-packages" -Recurse -Include *.pyd,*.dll | Unblock-File
> ```

---

## 💻 7. Steps to Launch & Run the Project

### Option A: Launching Jupyter Notebook (Interactive Mode)
To explore, edit, and demonstrate the project interactively:
```powershell
python -m notebook
```
or
```powershell
python -m jupyter notebook
```
1. Your web browser will open automatically showing the dashboard.
2. Click on **`Saransh_PhishGuard.ipynb`**.
3. In the top navigation bar, click **Kernel** ➡️ **Restart & Run All Cells**.
4. Observe each section executing sequentially: from data ingestion to model training, charts, and live URL analysis.

### Option B: Running the Pipeline Headlessly via Command Line
To run the automated pipeline and recompute all metrics and charts without opening a browser:
```powershell
python run_experiments.py
```

To re-execute the notebook in-place via `nbconvert`:
```powershell
python -m nbconvert --to notebook --execute --inplace Saransh_PhishGuard.ipynb
```

---

## 🧪 8. Using the Rule-Based URL Analyzer

The `analyze_url(url)` function runs directly in Python without requiring internet access or dangerous network calls:

```python
from build_notebook import analyze_url  # Or defined directly in the notebook

# Test a legitimate website
legit_result = analyze_url("https://www.google.com")
print(legit_result)
# Output: {'url': 'https://www.google.com', 'risk_score': 0, 'risk_level': 'Low Risk (Looks Benign Based on Lexical Checks)', ...}

# Test a suspicious phishing URL
phish_result = analyze_url("http://192.168.1.100/secure-login/bank-account-update/verify.php?user=test@domain.com")
print(f"Risk Score: {phish_result['risk_score']}/100")
print(f"Category:   {phish_result['risk_level']}")
for ind in phish_result['triggered_indicators']:
    print(f"  • {ind}")
```

### Expected Output for the Phishing URL:
```text
Risk Score: 100/100
Category:   Severe Risk (High Probability of Phishing)
Triggered Indicators:
  • IP address hostname detected instead of a registered domain name (Penalty: +30).
  • Unusually long URL (82 characters > 75 threshold) (Penalty: +20).
  • Presence of '@' character: Browsers ignore text before '@' (Penalty: +25).
  • Missing HTTPS encryption: Site uses insecure plain HTTP (Penalty: +15).
  • Suspicious credential/security keywords detected: ['login', 'verify', 'update', 'account', 'secure'] (Penalty: +25).
```

---

## 📈 9. Real Measured Evaluation Results

Evaluated on 2,211 unseen test records (Stratified 80/20 split, `random_state=42`):

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Caught Phishing (TP / Total) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dummy (Baseline)** | 55.68% | 0.00% | 0.00% | 0.00% | 0.5000 | 0 / 980 (100% Missed) |
| **Logistic Regression** | 92.76% | 93.43% | 90.00% | 91.68% | 0.9784 | 882 / 980 (90.0% Caught) |
| **Random Forest (Champion)** | **97.01%** | **97.41%** | **95.82%** | **96.60%** | **0.9968** | **939 / 980 (95.8% Caught)** |

---

## 📁 10. Project Directory Layout

```text
cybersecurity_project/
│
├── Saransh_PhishGuard.ipynb      # [Mandatory] Complete executable Jupyter Notebook
├── Saransh_ProjectReport.docx    # [Mandatory] Professional Word Project Report
├── requirements.txt              # [Mandatory] External Python dependencies
├── README.md                     # [Mandatory] Project documentation & setup instructions
│
├── run_experiments.py            # Standalone ML training and evaluation script
├── build_notebook.py             # Programmatic builder for Saransh_PhishGuard.ipynb
├── build_report.py               # Programmatic builder for Saransh_ProjectReport.docx
├── generate_diagram.py           # Architecture diagram generator
├── experiment_results.json       # Exact JSON dump of empirical metrics and importances
│
├── data/
│   └── phishing_websites_uci_327.csv  # Local cached copy of UCI Dataset #327
│
└── charts/
    ├── architecture_diagram.png       # Dual-engine system workflow diagram
    ├── class_distribution.png         # Dataset target class distribution
    ├── confusion_matrices.png         # 3-model confusion matrix heatmaps
    ├── model_comparison.png           # Accuracy, Precision, Recall, F1 comparison bar chart
    ├── roc_curves.png                 # Receiver Operating Characteristic curves
    └── feature_importance.png         # Random Forest Gini feature importances
```

---

## ⚠️ 11. Limitations & Future Scope

### Limitations
1. **Feature Extraction Overhead:** In production, extracting 30 features (DNS queries, certificate validation, HTML DOM parsing) takes 200–800ms per webpage before classification can occur.
2. **Adversarial Adaptation:** Attackers continually adapt by acquiring legitimate SSL certificates (e.g., Let's Encrypt) or structuring anchor links to point back to authentic brand servers.
3. **Lexical Scope:** Standalone lexical URL inspection evaluates syntax offline; it cannot detect a compromised, authentic web page serving malicious forms.

### Future Scope
* **Browser Extension:** Package the Random Forest inference engine into a Chrome/Firefox extension for real-time DOM checking prior to form submission.
* **Deep Learning on Raw URLs:** Train a Character-level CNN or BiLSTM to classify raw URLs without manual feature engineering.
* **Computer Vision Phishing Detection:** Use perceptual hashing (pHash) or Vision Transformers to compare screenshot layouts against legitimate banking brand logos.

---

## 📚 12. References & Acknowledgements

1. Mohammad, R. M., Thabtah, F., & McCluskey, L. (2012). *An Assessment of Features Related to Phishing Websites Using an Automated Technique.* DOI: [10.24432/C51W2X](https://doi.org/10.24432/C51W2X).
2. UCI Machine Learning Repository: [Phishing Websites Dataset (ID: 327)](https://archive.ics.uci.edu/dataset/327/phishing+websites).
3. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python.* Journal of Machine Learning Research.
4. Anti-Phishing Working Group (APWG). (2024). *Phishing Activity Trends Report.*

---
*Created for academic submission — Saransh (B.Tech CSE, 3rd Year)*
