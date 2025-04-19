import streamlit as st
import os
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import openai
from dotenv import load_dotenv
import time
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize OpenAI client properly - NEVER hardcode API keys
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="Real Estate Multi AI Agent Properties",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced custom CSS with fixes for visibility and additional styling
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary-color: #3a86ff;
        --secondary-color: #8338ec;
        --accent-color: #ff006e;
        --background-color: #f8f9fa;
        --text-color: #212529;
        --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(58, 134, 255, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(58, 134, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(58, 134, 255, 0); }
    }
    
    /* General Styling */
    .main-header {
        font-size: 2.8rem !important;
        color: white !important; /* Ensure visibility on dark backgrounds */
        text-shadow: 0px 2px 4px rgba(0,0,0,0.3);
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-out;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    
    /* Fix for browsers that don't support gradient text */
    @supports not (background-clip: text) {
        .main-header {
            background: transparent;
            -webkit-text-fill-color: white;
        }
    }
    
    .sub-header {
        font-size: 1.8rem; 
        color: var(--primary-color) !important; /* Ensure visibility */
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 0.5rem;
        animation: fadeIn 1s ease-out;
    }
    
    .sidebar-content {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f1f3f5;
    }
    
    .sidebar-title {
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        color: var(--secondary-color);
    }
    
    .team-info {
        font-size: 1rem;
        font-style: italic;
        text-align: right;
        margin-top: 1rem;
        color: white;
        text-shadow: 0px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: var(--card-shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button:active {
        transform: translateY(1px);
    }
    
    /* Card Styling */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        border-left: 5px solid var(--primary-color);
        box-shadow: var(--card-shadow);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 0.8s ease-out;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    .results-card {
        border-left: 5px solid var(--accent-color);
    }
    
    /* Other Elements */
    .stFileUploader > div {
        border-radius: 8px;
        border: 2px dashed var(--primary-color);
        padding: 1rem;
    }
    
    .stTextArea > div > div {
        border-radius: 8px;
        border-color: #ced4da;
    }
    
    /* Table Styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        border: none !important;
    }
    
    .dataframe thead th {
        background-color: var(--primary-color) !important;
        color: white !important;
        text-align: center !important;
        font-weight: 600 !important;
        padding: 8px !important;
    }
    
    .dataframe tbody tr:nth-child(odd) {
        background-color: rgba(58, 134, 255, 0.05) !important;
    }
    
    /* Footer Styling - Enhanced for visibility */
    .footer {
        background-color: #f1f3f5;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 2rem;
        text-align: center;
    }
    
    .footer-section {
        background-color: #4470bd;
        padding: 0.8rem;
        border-radius: 5px;
        margin: 0.25rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .footer-text {
        color: white !important; 
        font-weight: bold;
    }
    
    .footer-subtext {
        color: #e0e0e0 !important;
        font-size: 0.9rem;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.375rem;
        background-color: var(--accent-color);
        color: white;
        margin-left: 0.5rem;
    }
    
    /* Progress Bar Animation */
    .stProgress > div > div > div {
        background-color: var(--primary-color);
    }
    
    /* Loading Spinner */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    
    /* Custom Toggle Button */
    .toggle-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 1rem;
    }
    
    /* Improved UI for Sidebar Radio Buttons */
    div.row-widget.stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    div.row-widget.stRadio > div [role="radiogroup"] {
        flex-direction: column;
        gap: 0.5rem;
    }
    
    div.row-widget.stRadio > div [role="radio"] {
        padding: 0.8rem;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    div.row-widget.stRadio > div [data-baseweb="radio"] {
        margin-right: 0.5rem;
    }
    
    div.row-widget.stRadio > div [role="radio"]:hover {
        background-color: #f8f9fa;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .logo-text {
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 1.2rem;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Tips and notification styling */
    .tip-box {
        background-color: rgba(255, 243, 205, 0.5);
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .highlight-text {
        color: var(--accent-color);
        font-weight: bold;
    }
    
    /* Developer attribution */
    .developer-credit {
        font-style: italic;
        color: white;
        text-shadow: 0px 1px 2px rgba(0,0,0,0.2);
        text-align: center;
        margin-top: 0.5rem;
        animation: fadeIn 1s ease-out;
    }
    
    /* Improved header container for better visibility */
    .header-container {
        background: linear-gradient(135deg, #3a86ff, #8338ec);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize CLIP model for image analysis
@st.cache_resource
def load_clip_model():
    try:
        model_name = "openai/clip-vit-base-patch32"
        model = CLIPModel.from_pretrained(model_name)
        processor = CLIPProcessor.from_pretrained(model_name)
        return model, processor, True
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None, False

model, processor, model_loaded = load_clip_model()

# Property issue categories with icons
PROPERTY_ISSUES = [
    ("water damage", "💧"), 
    ("mold", "🧫"), 
    ("cracks", "🧱"), 
    ("poor lighting", "💡"), 
    ("broken fixtures", "🔨"),
    ("peeling paint", "🖌️"), 
    ("leak", "💦"), 
    ("structural damage", "🏚️"), 
    ("electrical issues", "⚡"),
    ("plumbing problems", "🚿"),
    ("pest infestation", "🐜"), 
    ("roof damage", "🏠")
]

def analyze_image(image):
    """Analyze property image for issues using CLIP"""
    issue_names = [issue[0] for issue in PROPERTY_ISSUES]
    
    # Process image
    image_inputs = processor(
        images=image,
        return_tensors="pt",
        padding=True
    )
    
    # Process text descriptions
    text_inputs = processor(
        text=issue_names,
        return_tensors="pt",
        padding=True
    )
    
    # Get image and text features
    with torch.no_grad():
        # Get image features
        image_features = model.get_image_features(**image_inputs)
        
        # Get text features
        text_features = model.get_text_features(**text_inputs)
        
        # Normalize features
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        # Calculate similarity scores
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        scores = similarity[0].tolist()
    
    # Get top 3 issues with their icons
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]
    top_issues = [(PROPERTY_ISSUES[i][0], PROPERTY_ISSUES[i][1], scores[i]) for i in top_indices]
    return top_issues

def get_troubleshooting_suggestions(issues):
    """Get troubleshooting suggestions using OpenAI"""
    try:
        prompt = f"""Based on the following property issues, provide specific troubleshooting suggestions:
        {', '.join([issue[0] for issue in issues])}
        
        Please provide:
        1. A brief description of each issue
        2. Recommended actions for homeowners or tenants
        3. When to contact a professional
        4. Estimated costs for DIY fixes vs professional help
        
        Format the response with clear headers and bullet points for easy reading.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error generating suggestions: {str(e)}\n\nPlease try again or contact support."

def handle_tenancy_question(question):
    """Handle tenancy-related questions using OpenAI"""
    try:
        prompt = f"""You are a knowledgeable real estate agent specializing in tenancy laws and regulations.
        Please answer the following question about tenancy:
        
        {question}
        
        If the answer depends on location, please:
        1. Provide general information applicable in most places
        2. Note which aspects vary by location
        3. Explain major regional differences (e.g., US vs UK, or state-by-state variations)
        
        Format your answer with clear headings, bullet points where appropriate, and highlight key points.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error processing question: {str(e)}\n\nPlease try again or contact support."

# Create a custom logo for the app header with better visibility
def create_logo():
    st.markdown("""
    <div class="header-container">
        <div style="display: flex; align-items: center; justify-content: center;">
            <div style="background: white; width: 60px; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                <span style="font-size: 30px;">🏡</span>
            </div>
            <div>
                <h1 class='main-header'>Real Estate Multi AI Agent Properties</h1>
                <div class='team-info'>Developed by Vijayshree | <span class="badge">v1.0</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# App Header with Custom Logo
create_logo()

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown("<div class='sidebar-title'>AI-Powered Services</div>", 
                unsafe_allow_html=True)
    
    # Add sidebar image with gradient background and developer credit
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3a86ff, #8338ec); 
                border-radius: 12px; padding: 20px; 
                display: flex; justify-content: center; align-items: center;
                margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <span style="font-size: 40px;">🏡</span>
        <span style="color: white; font-weight: bold; font-size: 18px; margin-left: 10px;">
            REAL ESTATE<br>MULTI AI AGENT<br><span style="font-size: 12px;">by Vijayshree</span>
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    agent = st.radio(
        "Choose a service",
        ["Issue Detection & Troubleshooting", "Tenancy FAQ"],
        key="agent_selection",
        index=0
    )
    
    with st.expander("📝 About This App", expanded=False):
        st.markdown("""
        <div style="font-size: 0.9rem;">
        This AI-powered assistant helps with:
        
        * 📸 Detecting property issues from images
        * 🔍 Providing customized troubleshooting advice
        * ❓ Answering tenancy questions with legal insights
        * 💰 Estimating repair costs
        
        <div class="tip-box">
        <strong>TIP:</strong> For best results when uploading photos, ensure good lighting and a clear view of the issue.
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add contact info in sidebar
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.9rem;">
    <strong>Need help?</strong><br>
    Contact: support@realestate-ai.com<br>
    Phone: (555) 123-4567
    </div>
    """, unsafe_allow_html=True)

# Main content area with tabs
if agent == "Issue Detection & Troubleshooting":
    st.markdown("<h2 class='sub-header'>🔍 Property Issue Detection & Analysis</h2>", 
                unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; align-items: center;">
            <div style="flex: 3;">
                <strong style="font-size: 1.2rem;">How It Works:</strong> 
                <ol style="margin-top: 0.5rem;">
                    <li>Upload a clear photo of the property issue</li>
                    <li>Our AI will analyze the image and detect potential problems</li>
                    <li>Review the troubleshooting recommendations</li>
                </ol>
            </div>
            <div style="flex: 1; text-align: center;">
                <span style="font-size: 3rem;">🔎→🧠→🛠️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Create two columns for upload and context
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload a property image", 
            type=["jpg", "jpeg", "png"],
            help="Supported formats: JPG, JPEG, PNG. For best results, ensure good lighting."
        )
    
    with col2:
        text_context = st.text_area(
            "Additional context (optional)", 
            placeholder="e.g., 'Dark spots on bathroom ceiling' or 'Noise from pipes when flushing'",
            height=120
        )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            analyze_button = st.button("🔍 Analyze Image", use_container_width=True)
            
            if analyze_button:
                if not model_loaded:
                    st.error("Model failed to load. Please try again later.")
                else:
                    # Add a progress bar for visual feedback
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Image analysis
                    status_text.text("Processing image...")
                    for i in range(50):
                        progress_bar.progress(i)
                        time.sleep(0.01)
                    
                    issues = analyze_image(image)
                    
                    # Step 2: Generating recommendations
                    status_text.text("Detecting issues...")
                    for i in range(50, 80):
                        progress_bar.progress(i)
                        time.sleep(0.01)
                    
                    # Display detected issues in an attractive card
                    st.markdown("<div class='card results-card'>", unsafe_allow_html=True)
                    st.markdown("### 🔎 Detected Issues")
                    
                    # Create a table for detected issues with icons
                    issue_data = {"Issue": [], "Confidence": []}
                    for issue_name, issue_icon, score in issues:
                        issue_data["Issue"].append(f"{issue_icon} {issue_name.title()}")
                        # Format confidence as percentage with color coding
                        confidence_level = round(score * 100, 1)
                        if confidence_level > 50:
                            color = "green"
                        elif confidence_level > 30:
                            color = "orange"
                        else:
                            color = "gray"
                        issue_data["Confidence"].append(f"<span style='color:{color};font-weight:bold;'>{confidence_level}%</span>")
                    
                    # Convert to DataFrame and display
                    df = pd.DataFrame(issue_data)
                    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
                    
                    # Add context from user if provided
                    if text_context:
                        st.markdown(f"""
                        <div style='margin-top:1rem;'>
                            <strong>Additional context provided:</strong>
                            <blockquote style='font-style:italic;color:#555;'>{text_context}</blockquote>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Step 3: Generating troubleshooting advice
                    status_text.text("Generating recommendations...")
                    for i in range(80, 100):
                        progress_bar.progress(i)
                        time.sleep(0.01)
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    
                    suggestions = get_troubleshooting_suggestions(issues)
                    
                    st.markdown("<div class='card results-card'>", unsafe_allow_html=True)
                    st.markdown("### 🛠️ Troubleshooting Recommendations")
                    st.markdown(suggestions)
                    
                    # Add a disclaimer
                    st.markdown("""
                    <div style='font-size:0.8rem;margin-top:1rem;padding:0.5rem;background-color:#f8f9fa;border-radius:5px;'>
                        <strong>Note:</strong> These recommendations are AI-generated based on image analysis. 
                        For serious structural or safety issues, always consult with a qualified professional.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Add a "print report" button
                    if st.button("📄 Generate PDF Report", key="print_report"):
                        st.success("Report generation feature coming soon!")

else:  # Tenancy FAQ
    st.markdown("<h2 class='sub-header'>❓ Tenancy Rights & Regulations Assistant</h2>", 
                unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; align-items: center;">
            <div style="flex: 3;">
                <strong style="font-size: 1.2rem;">How It Works:</strong>
                <p style="margin-top: 0.5rem;">
                Ask any question about tenant or landlord rights, rental agreements, deposits, 
                maintenance responsibilities, or other tenancy matters. Our AI assistant will provide 
                detailed information to help you navigate your situation.
                </p>
            </div>
            <div style="flex: 1; text-align: center;">
                <span style="font-size: 3rem;">❓→🤖→📝</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Add common tenancy questions as quick buttons
    st.markdown("<strong>Common Questions:</strong>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        q1 = st.button("Security deposit rights", key="q1", use_container_width=True)
    with col2:
        q2 = st.button("Landlord entry notice", key="q2", use_container_width=True)
    with col3:
        q3 = st.button("Repairs responsibility", key="q3", use_container_width=True)
    
    # Set preset questions if buttons are clicked
    preset_question = ""
    if q1:
        preset_question = "What are my rights regarding security deposits? When can a landlord withhold a deposit?"
    elif q2:
        preset_question = "How much notice must a landlord give before entering a rental property?"
    elif q3:
        preset_question = "Who is responsible for repairs in a rental property - the tenant or the landlord?"
    
    # Create a form for the question
    with st.form(key="question_form"):
        question = st.text_area(
            "Ask your tenancy-related question", 
            value=preset_question,
            placeholder="Example: What are my rights as a tenant if my landlord wants to increase the rent?",
            height=100
        )
        
        # Add location information for more specific answers
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("Location (optional)", 
                                     placeholder="e.g., California, New York, UK, etc.")
        
        # Submit button in center column
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button(label="🔍 Get Answer", use_container_width=True)
    
    if submit_button and question:
        # Add location to the question if provided
        if location:
            full_question = f"{question} (Location: {location})"
        else:
            full_question = question
            
        with st.spinner("Finding your answer..."):
            # Add progress bar for visual feedback
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.01)
            
            answer = handle_tenancy_question(full_question)
            
            st.markdown("<div class='card results-card'>", unsafe_allow_html=True)
            st.markdown("### 📝 Answer")
            
            # If location was provided, add a note
            if location:
                st.markdown(f"<p><em>Answer specific to: <strong>{location}</strong></em></p>", 
                            unsafe_allow_html=True)
            
            st.markdown(answer)
            
            # Add disclaimer
            st.markdown("""
            <div style='font-size:0.8rem;margin-top:1rem;padding:0.5rem;background-color:#f8f9fa;border-radius:5px;'>
                <strong>Disclaimer:</strong> This information is provided for general guidance only and 
                should not be considered legal advice. Laws and regulations vary by location and change over time. 
                For specific legal concerns, please consult with a qualified attorney.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Add helpful resources
            with st.expander("📚 Additional Resources"):
                st.markdown("""
                - [HUD.gov](https://www.hud.gov/topics/rental_assistance) - U.S. Department of Housing and Urban Development
                - [Tenant.org](https://www.tenant.org) - National tenant rights information
                - [LawHelp.org](https://www.lawhelp.org) - Free legal aid information
                """)

# Improved Footer with enhanced visibility for dark backgrounds
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div class="footer-section">
            <span class="footer-text">Real Estate Multi AI Agent Properties</span><br>
            <span class="footer-subtext">Contact: support@realestate-ai.com</span>
        </div>
        <div class="footer-section">
            <span class="footer-text">© 2025 Real Estate AI Assistant</span><br>
            <span class="footer-subtext">All rights reserved</span>
        </div>
        <div class="footer-section">
            <span class="footer-text">Developed by Vijayshree</span><br>
            <span style="font-size: 1.5rem; color: white;">
                📱 💬 📧
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
