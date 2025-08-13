#importing libraries
import streamlit as st
from helper_func import input_pdf_setup, get_gemini_response, get_gemini_response_keywords
from streamlit_lottie import st_lottie
import requests
import json

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

## Streamlit App

# Page configuration with custom theme
st.set_page_config(
    page_title="ATS Resume Scanner",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 1rem;
        border-radius: 8px;
        background-color: #0A192F;  /* Rich navy background */
    }
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 3em;
        background: linear-gradient(135deg, #6366F1, #4F46E5);  /* Modern indigo gradient */
        color: white;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 3px 15px rgba(99, 102, 241, 0.4);
        background: linear-gradient(135deg, #4F46E5, #4338CA);
    }
    .upload-box {
        border: 2px dashed #6366F1;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        background: rgba(99, 102, 241, 0.1);
        backdrop-filter: blur(5px);
    }
    .match-score {
        padding: 20px;
        border-radius: 16px;
        margin: 15px 0;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    .excellent {
        background: linear-gradient(135deg, #059669, #10B981);  /* Emerald gradient */
        color: white;
    }
    .good {
        background: linear-gradient(135deg, #3B82F6, #60A5FA);  /* Blue gradient */
        color: white;
    }
    .average {
        background: linear-gradient(135deg, #F59E0B, #FBBF24);  /* Amber gradient */
        color: white;
    }
    .below-average {
        background: linear-gradient(135deg, #EF4444, #F87171);  /* Red gradient */
        color: white;
    }
    .match-details {
        margin-top: 15px;
        padding: 20px;
        border-radius: 16px;
        background: linear-gradient(135deg, #1E40AF, #3B82F6);  /* Rich blue gradient */
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    .upload-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px 0 rgba(99, 102, 241, 0.15);
        border: 2px dashed rgba(99, 102, 241, 0.6);
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(99, 102, 241, 0.06));
    }
    .stFileUploader {
        padding: 12px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(99, 102, 241, 0.04));
        border-radius: 12px;
        margin-top: 12px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    .stFileUploader:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(99, 102, 241, 0.06));
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    /* Enhance the upload button appearance */
    .stFileUploader button {
        background: linear-gradient(135deg, #6366F1, #4F46E5) !important;
        color: white !important;
        border: none !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    .stFileUploader button:hover {
        background: linear-gradient(135deg, #4F46E5, #4338CA) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Lottie Animation
lottie_scan = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")

# App Header with Animation
st.title("🤖 Smart ATS Resume Scanner")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div style='background:darkgray; padding: 15px; border-radius: 10px; box-shadow: 0 8px 20px rgba(0,0,0,0.2);'>
        <h4 style='color: black; text-shadow: 0 2px 4px rgba(0,0,0,0.1);'>Upload your resume and get instant AI-powered analysis!</h4>
        <p style='color: black;'>Our advanced ATS scanner will help you understand:</p>
        <ul style='color: black;'>
            <li>Resume-Job Description Match</li>
            <li>Key Skills Analysis</li>
            <li>Improvement Suggestions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st_lottie(lottie_scan, height=200)

# Add spacing
st.markdown("<div style='margin: 2.5em'></div>", unsafe_allow_html=True)

# Job Description Input
st.markdown("""
    <div style='background: linear-gradient(135deg, #1A1F3C, #2E1C4C); 
        padding: 30px; 
        border-radius: 20px; 
        border: 2px solid rgba(147, 112, 219, 0.2); 
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);'>
        <h3 style='color: #E6E6FA; 
            margin-bottom: 10px; 
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            font-size: 24px;'>
            📋 Job Description
        </h3>
        <div style='background: darkgray; 
            padding: 35px; 
            border-radius: 15px; 
            margin-bottom: 20px; 
            text-align: center; 
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 8px 32px 0 rgba(11, 78, 124, 0.37);'>
            <p style='color: black; 
                margin-bottom: 5px; 
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
                font-size: 20px;'>
                <i>Paste the complete job description below for accurate analysis</i> ✨
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

input_text = st.text_area(
    "",  # Removed label since we have it in the markdown
    height=100,
    key="input",
    placeholder="Paste your job description here...",
    help="For best results, include the complete job description with all requirements and qualifications"
)

# Add a visual separator
st.markdown("<hr style='margin: 5px 0; background-color: rgba(129, 181, 234, 0.1); height: 2px; border: none;'>", unsafe_allow_html=True)

# Add visual separator and gap
st.markdown("""
    <div style='
        margin: 20px 0;
        background: linear-gradient(90deg, 
            rgba(99, 102, 241, 0.1), 
            rgba(99, 102, 241, 0.3), 
            rgba(99, 102, 241, 0.1));
        height: 2px;
        border-radius: 1px;
    '></div>
""", unsafe_allow_html=True)

# Resume Upload Section - Refined color harmony
st.markdown("""
    <div style='background: linear-gradient(135deg, #1E293B, #0F172A);
        padding: 15px;
        border-radius: 20px;
        margin: 15px 0;
        border: 2px solid rgba(99, 102, 241, 0.2);
        box-shadow: 0 8px 32px rgba(15, 23, 42, 0.3);'>
        <h3 style='color: #E2E8F0;
            margin-bottom: 20px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            font-size: 24px;
            font-weight: 600;'>
            📤 Upload Resume
        </h3>
        <div class='upload-box' style='
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(99, 102, 241, 0.03));
            border: 2px dashed rgba(99, 102, 241, 0.4);
            padding: 10px;
            border-radius: 16px;
            text-align: center;
            backdrop-filter: blur(8px);
            box-shadow: 0 4px 20px 0 rgba(15, 23, 42, 0.15);
            transition: all 0.3s ease-in-out;'>
            <h4 style='color: #E2E8F0;
                margin: 10px 0;
                font-size: 18px;
                font-weight: 500;'>
                Drag and drop your resume here
            </h4>
            <p style='color: #94A3B8;
                font-size: 14px;
                margin-top: 12px;'>
                Supported format: PDF
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF Uploaded Successfully!")

# Analysis Options
st.markdown("### 🔍 Choose Analysis Type")
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    submit1 = st.button("🎯 Analyze Resume Match")

with col2:
    submit2 = st.button("🔑 Extract Keywords")

with col3:
    submit3 = st.button("📊 Calculate Match Score")

with col4:
    submit4 = st.button("❓ Generate Interview Questions")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
As an expert ATS (Applicant Tracking System) scanner with an in-depth understanding of AI and ATS functionality, 
your task is to evaluate a resume against a provided job description. Please identify the specific skills and keywords 
necessary to maximize the impact of the resume and provide responde in json format as {Technical Skills:[], Analytical Skills:[], Soft Skills:[]}.
Note: Please do not make up the answer only answer from job description provided"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Provide the following information:
1. Calculate the percentage match between the resume and job description
2. Identify missing keywords and skills
3. Provide specific improvement suggestions
4. Give a detailed analysis of the match

Format the percentage as a number without any symbols or text.
"""

input_prompt4 = """
As an experienced Technical Interviewer, analyze the resume and generate relevant interview questions. Please provide:
1. 3-4 Technical questions based on the candidate's skills
2. 2-3 Behavioral questions related to their experience
3. 2 Problem-solving questions relevant to their field
Format the response with clear sections and numbering.
Note: Questions should be specifically tailored to the candidate's background and experience shown in the resume.
"""

if submit1:
    if uploaded_file is not None:
        with st.spinner('Analyzing your resume... Please wait...'):
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt1,pdf_content,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
    else:
        st.error("⚠️ Please upload your resume first!")

elif submit2:
    if uploaded_file is not None:
        with st.spinner('Extracting keywords... Please wait...'):
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response_keywords(input_prompt2,pdf_content,input_text)
            print(response)
            st.subheader("Skills are:")
            if response != None:
                st.write(f"Technical Skills: {', '.join(response['Technical Skills'])}.")
                st.write(f"Analytical Skills: {', '.join(response['Analytical Skills'])}.")
                st.write(f"Soft Skills: {', '.join(response['Soft Skills'])}.")
    else:
        st.error("⚠️ Please upload your resume first!")

elif submit3:
    if uploaded_file is not None:
        with st.spinner('Calculating match score... Please wait...'):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            
            # Extract percentage from response (assuming it's the first line)
            try:
                match_percentage = float(response.split('\n')[0].strip())
            except:
                match_percentage = 0
                
            # Display match score with level indicator
            st.subheader("📊 Resume Match Analysis")
            
            # Determine level and display appropriate message
            if match_percentage >= 90:
                level_color = "excellent"
                level_text = "Excellent Match! 🌟"
                emoji = "🎯"
            elif match_percentage >= 70:
                level_color = "good"
                level_text = "Good Match! 👍"
                emoji = "✨"
            elif match_percentage >= 50:
                level_color = "average"
                level_text = "Average Match 📈"
                emoji = "⚡"
            else:
                level_color = "below-average"
                level_text = "Needs Improvement 🎯"
                emoji = "💪"

            # Display match score with styling
            st.markdown(f"""
                <div class='match-score {level_color}'>
                    <h2>{level_text}</h2>
                    <h1>{match_percentage:.1f}% {emoji}</h1>
                </div>
                """, unsafe_allow_html=True)

            # Create columns for detailed analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div class='match-details'>
                        <h4>📋 Match Level Guide</h4>
                        <ul>
                            <li>90-100%: Excellent Match</li>
                            <li>70-89%: Good Match</li>
                            <li>50-69%: Average Match</li>
                            <li>Below 50%: Needs Improvement</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div class='match-details'>
                        <h4>🎯 What This Means</h4>
                        <ul>
                            <li>Higher scores indicate better alignment with job requirements</li>
                            <li>Consider the missing keywords in the detailed analysis</li>
                            <li>Focus on suggested improvements</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)

            # Display detailed analysis
            st.markdown("### 📝 Detailed Analysis")
            st.markdown(response)
            
            # Add improvement tips based on score
            st.markdown("### 💡 Quick Tips")
            if match_percentage < 70:
                st.warning("""
                To improve your match score:
                - Add more relevant keywords from the job description
                - Highlight specific technical skills
                - Quantify your achievements
                - Tailor your resume to the job requirements
                """)

elif submit4:
    if uploaded_file is not None:
        with st.spinner('Generating interview questions... Please wait...'):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt4, pdf_content, input_text)
            
            st.subheader("🎯 Recommended Interview Questions")
            st.markdown("""
                <div style='background-color: rgba(27, 69, 110, 0.1); padding: 20px; border-radius: 15px; border: 2px solid rgb(2, 16, 17);'>
                    <h4 style='color: rgb(222, 229, 237);'>Questions tailored to the candidate's profile:</h4>
                </div>
            """, unsafe_allow_html=True)
            st.write(response)
    else:
        st.error("⚠️ Please upload your resume first!")





   





