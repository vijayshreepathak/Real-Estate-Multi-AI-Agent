
# 🏡 Real Estate Multi AI Agent Properties

A powerful multi-agent AI assistant designed to help property owners, tenants, and real estate professionals with property management and tenancy-related queries.

![Real Estate Multi AI Agent Properties](https://via.placeholder.com/800x400?text=Real+Estate+Multi+AI+Agent+Properties)

---

## 🔍 Features

### 🧠 Issue Detection & Troubleshooting
- **AI-Powered Image Analysis**: Upload property images to detect potential issues.
- **Smart Issue Detection**: Identifies common property problems like water damage, mold, cracks, etc., with confidence scores.
- **Automated Troubleshooting**: Get detailed suggestions for addressing detected issues, including DIY vs professional costs.
- **Professional Guidance**: Know when to contact a professional for help.

### ❓ Tenancy Rights & Regulations Assistant
- **Comprehensive Knowledge**: Get answers to common tenancy-related questions.
- **Location-Aware Responses**: Understand how answers may vary by region.
- **Expert Advice**: AI trained on real estate and tenancy regulations.
- **Quick Access**: Use preset buttons for frequently asked questions.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/real-estate-multi-ai-agent.git
cd real-estate-multi-ai-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Setup

### Step 1: Get Your OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign in to your account
3. Navigate to the API keys section
4. Click **"Create new secret key"**

### Step 2: Set Up Environment Variables
1. Create a `.env` file in the root directory
2. Add your key:
```env
OPENAI_API_KEY=your_api_key_here
```

3. Code for loading the key:
```python
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
```

---

## 🏃 Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

Open your browser and go to:
```
http://localhost:8501
```

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit + custom CSS
- **AI Models**:
  - GPT-3.5 Turbo (OpenAI)
  - CLIP (Contrastive Language-Image Pre-training)
- **Backend**: Python
- **Dependencies**:
  - `transformers`
  - `torch`
  - `pillow`
  - `openai`
  - `pandas`
  - `python-dotenv`

---

## 📸 Usage Guide

### 🔧 Property Issue Detection
1. Navigate to **"Issue Detection & Troubleshooting"**
2. Upload a property image (JPG, JPEG, PNG)
3. Add context in the text area (optional)
4. Click **Analyze Image**

Outputs:
- Issues with confidence scores
- Detailed repair suggestions
- Cost estimates (DIY vs professional)
- Recommendations for expert help

### 🧾 Tenancy Rights & Regulations
1. Go to **"Tenancy FAQ"**
2. Choose or type a question
3. (Optional) Enter your location
4. Click **Get Answer**

Outputs:
- AI-generated, location-aware answers
- Legal and regulatory context
- Disclaimer and resources

---

## 💡 UI Features

- Responsive layout
- Animated transitions
- Interactive cards and hover effects
- Loading indicators
- Color-coded confidence levels
- Expandable sections for more info

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👥 Development

- **Developed by**: Vijayshree Vaibhav
- **Contact**: support@realestatexxxx-ai.com

---

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/)
- [Hugging Face](https://huggingface.co/)
- [Streamlit](https://streamlit.io/)

---

Made with ❤️ for the real estate community.
```

---