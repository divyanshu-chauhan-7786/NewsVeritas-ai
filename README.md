# 🧠 TruthLens – AI Powered Fake News Detection Platform
### Detect Fake & Real News Instantly with Explainable Confidence Analysis  
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-black.svg)
![HuggingFace](https://img.shields.io/badge/Model-RoBERTa%20Fine--Tuned-orange.svg)

---

## 📌 Overview
**TruthLens** is a machine-learning-powered fake news detection system designed to identify misinformation using an advanced **Fine-Tuned RoBERTa Transformer Model**.

It provides:
- Real-time analysis  
- Confidence scores  
- Risk-level categorization  
- Full history tracking  
- Feedback learning system  
- Clean & modern UI  

---

## 🚀 Features

### 🔍 Fake News Classification  
- Highly accurate detection using fine-tuned **RoBERTa**  
- Identifies **FAKE** or **REAL** news instantly  

### 📊 Confidence Level Analysis  
Displays detailed interpretations such as:
- **Highly Likely Fake**  
- **Likely Authentic**  
- **Possibly Fake**  
- **Uncertain**  

### 📜 History Tracking  
Automatically stores all previous analyses.

### 📝 User Feedback System  
Users can submit corrections to improve future versions.

### 📈 Dashboard  
Shows:
- Total analyses  
- Fake/Real ratios  
- Average confidence score  

### 🌐 Fully deployable on Render or any cloud platform  

---

## 🤖 Model Details

Model used for classification:  
### 🔗 [Fake-News-RoBERTa on HuggingFace](https://huggingface.co/divyanshu-chauhan-7786/fake-news-roberta)

The model uses:
- **RoBERTa-base architecture**  
- Fine-tuned on a Fake/Real News dataset  
- Saved in **safetensors** format  

---

## 🛠 Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Flask (Python) |
| AI Model | HuggingFace Transformers |
| UI | HTML, CSS, Bootstrap |
| Deployment | Render.com |
| Data Format | JSON, Safetensors |
| Tokenizer | AutoTokenizer (RoBERTa) |

---

## 🔄 Project Workflow

TruthLens follows a clean and efficient end-to-end pipeline for detecting misinformation.

### **1️⃣ User Input**
Users enter:
- News headline (optional)
- Full news article or text (required)

System checks:
- Minimum text length
- Empty input validation

---

### **2️⃣ Preprocessing**
Before model inference:
- Text is tokenized using RoBERTa tokenizer
- Long text is truncated to 512 tokens
- Attention masks and input IDs are generated automatically by the HuggingFace API

---

### **3️⃣ Model Inference**
The system uses the fine-tuned RoBERTa model:

- Model ID: `divyanshu-chauhan-7786/fake-news-roberta`
- Hosted on Hugging Face
- Classification labels:
  - `LABEL_0` → REAL  
  - `LABEL_1` → FAKE  

Model returns:
- Prediction  
- Confidence score (0–100%)

---

### **4️⃣ Confidence Level Categorization**
Based on the confidence, an explanatory label is generated:

| Range | Meaning |
|-------|---------|
| 90–100% | Highly Likely Fake / Highly Authentic |
| 75–89% | Likely Fake / Likely Authentic |
| 60–74% | Possibly Fake / Possibly Authentic |
| 0–59% | Uncertain / Low Reliability |

Each level includes:
- Description  
- Color-coded indicator  
- Risk or reliability message  

---

### **5️⃣ Result Display**
The frontend shows:
- Final prediction (FAKE / REAL)
- Confidence percentage
- Explanation badge
- Highlight color (green/yellow/orange/red)

---

### **6️⃣ History Tracking**
Every analysis is saved inside the session:
- Headline
- Short preview
- Full text
- Prediction
- Confidence score
- Timestamp
- Confidence category

History can be viewed anytime.

---

### **7️⃣ User Feedback**
Optional feedback form allows:
- User corrected label (Real/Fake)
- Additional comments

Stored in `feedback.json` for improving future retraining.

---

### **8️⃣ Dashboard Analytics**
Calculates:
- Total analyses
- Real vs Fake count
- Real/Fake percentages
- Average confidence score

---

## 📬 Contact

### 👤 **Developed By**
**Divyanshu Chauhan**  
AI & Machine Learning Engineer | Python Developer  
+91 8960717110

### 📧 **Email**
**divyanshuchauhan471@gmail.com**

### 🔗 **Connect with Me**
- **LinkedIn:** https://www.linkedin.com/in/divyanshu-chauhan  
- **GitHub:** https://github.com/divyanshu-chauhan-7786
- **HuggingFace:**  [https://github.com/divyanshu-chauhan-7786](https://huggingface.co/divyanshu-chauhan-7786/fake-news-roberta)

---

### ⭐ Support  
If you find this project helpful, please consider giving it a **⭐ star on GitHub**.  
Your support motivates me to build more open-source AI projects!


