# 🏡 Real Estate Multi-AI Agent Assistant

Welcome to **Real Estate Multi-AI Agent** — a powerful, multi-agent AI assistant built to simplify property management and support tenants, owners, and real estate professionals with intelligent, real-time insights. 🧠🏘️⚖️

---

## ✨ What Can It Do?

### 🔍 Issue Detection & Troubleshooting
📸 **AI-Powered Image Analysis** – Upload property images and detect potential issues in seconds  
🛠️ **Smart Issue Detection** – Spot water damage, mold, cracks, and more using computer vision  
💡 **Detailed Troubleshooting** – Get step-by-step repair suggestions & professional recommendations  
💰 **Cost Estimation** – Compare DIY vs professional solutions with estimated costs  

### 📜 Tenancy Rights & Regulations Assistant
🧾 **AI Legal Expert** – Answers complex tenancy questions with confidence  
🌍 **Region-Aware Guidance** – Get insights based on local laws and regulations  
⚡ **Quick Access Presets** – One-tap responses to common tenancy queries  
👩‍⚖️ **Backed by Real Regulations** – AI trained on verified tenancy frameworks

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.8 or higher 🐍
- pip (Python package manager) 📦
- Virtual environment (recommended) 🧪
- OpenAI API Key 🔐

---

### 📦 Installation Steps

1. **Clone the repository**:
```bash
git clone https://github.com/vijayshreepathak/Real-Estate-Multi-AI-Agent.git
cd Real-Estate-Multi-AI-Agent
```

2. **Set up a virtual environment**:
```bash
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Or activate on macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Configuration

### Step 1: Get your OpenAI API key  
🔗 [OpenAI API Console](https://platform.openai.com/)

1. Log in to your account
2. Go to your API keys dashboard
3. Click “Create new secret key”

### Step 2: Add to your environment
1. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_api_key_here
```

2. Code to load the key:
```python
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
```

---

## 💻 Running the App

To launch the Streamlit application:

```bash
streamlit run app.py
```

🖥️ Navigate to your browser:  
`http://localhost:8501`

---

## ⚙️ Tech Stack

| Layer       | Tool/Library                              |
|-------------|--------------------------------------------|
| 💻 Frontend | Streamlit + Custom CSS                     |
| 🧠 AI Models| OpenAI GPT-3.5 Turbo, CLIP (Hugging Face) |
| 🐍 Backend  | Python                                     |
| 🧩 Deps     | `transformers`, `torch`, `pillow`, `pandas`, `openai`, `python-dotenv` |

---

## 📸 Feature Walkthrough

### 🔧 Issue Detection
1. Go to **Issue Detection & Troubleshooting**  
2. Upload a property image (supports JPG, PNG)  
3. Optionally describe the issue  
4. Hit **Analyze Image** to receive:
   - ⚠️ Detected issues with confidence levels
   - 🛠️ Troubleshooting suggestions
   - 💰 Cost breakdown
   - 🧑‍🔧 When to seek expert help

---

### 📚 Tenancy Legal Support
1. Open **Tenancy FAQ**  
2. Choose a preset or type your question  
3. Provide location (optional)  
4. Click **Get Answer** to see:
   - 🧾 Legal insights tailored to your region
   - ⚖️ Regional laws and disclaimers
   - 🔗 Helpful resources and next steps

---

## 🎨 UI Highlights

✨ Responsive Design – Seamless across devices  
🎞️ Animated Elements – Smooth transitions and feedback  
🃏 Interactive Cards – Visual, clickable insights  
📊 Color-Coded Scores – Instantly understand AI confidence  
➕ Expandable Sections – Dive deeper when needed

---

## 🤝 Contributing

Contributions welcome! 🙌  
If you'd like to improve this project, feel free to fork it or submit a pull request.

---

## 📝 License

MIT License – see the [LICENSE](LICENSE) file for full terms.

---

## 👩‍💻 Developed By

**Vijayshree Vaibhav**  
🌐 GitHub: [@vijayshreepathak](https://github.com/vijayshreepathak)  
📫 Email: support@realestatexxxx-ai.com

---

## 🙏 Acknowledgments

Special thanks to:

- 💡 [OpenAI](https://openai.com/)
- 🤗 [Hugging Face](https://huggingface.co/)
- ⚡ [Streamlit](https://streamlit.io/)

---

Made with ❤️ to revolutionize the real estate world.
```
