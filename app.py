import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini API
api_key = os.getenv("GOOGLE_API_KEY")

# Fallback for Streamlit Cloud Secrets
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass

if api_key:
    genai.configure(api_key=api_key)

# App Configuration
st.set_page_config(
    page_title="Wakefit AI Sleep Consultant", 
    page_icon="https://www.google.com/s2/favicons?domain=wakefit.co&sz=128", 
    layout="centered"
)

# Include the Wakefit logo and title
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://www.google.com/s2/favicons?domain=wakefit.co&sz=128", width=80)
with col_title:
    st.title("Wakefit AI Consultant")

st.write("Welcome to the Wakefit AI Sleep Consultant! Fill out the questionnaire below, and our AI will recommend the perfect Wakefit mattress and sleep accessories for your exact needs.")

with st.sidebar:
    st.header("How it works")
    st.write("1. Enter your preferences and physical details.")
    st.write("2. Select your budget and any special requirements.")
    st.write("3. Our AI agent evaluates your profile against the ideal mattress characteristics and gives you personalized recommendations.")
    st.markdown("---")
    if not api_key or api_key == "your_google_api_key_here":
        st.warning("Please add your GOOGLE_API_KEY to the .env file to enable AI recommendations.")

# User Input Form
with st.form("mattress_form"):
    st.subheader("Your Sleep Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        sleep_position = st.selectbox("Primary Sleeping Position", ["Side", "Back", "Stomach", "Combination (move around)"])
        body_weight = st.selectbox("Body Weight Category", ["Light (under 130 lbs)", "Average (130 - 230 lbs)", "Heavy (over 230 lbs)"])
    
    with col2:
        budget = st.selectbox("Budget", ["Under ₹10,000", "₹10,000 - ₹15,000", "₹15,000 - ₹20,000", "₹20,000 - ₹30,000", "Over ₹30,000"])
        firmness = st.select_slider("Preferred Firmness", options=["Very Soft", "Soft", "Medium Soft", "Medium", "Medium Firm", "Firm", "Very Firm"], value="Medium")

    st.subheader("Special Requirements")
    special_needs = st.multiselect(
        "Select any specific needs or preferences:",
        ["Cooling / Sleep Hot", "Back Pain Relief", "Motion Isolation (sleep with partner)", "Edge Support", "Organic / Eco-friendly", "Hypoallergenic"]
    )
    
    current_mattress_issue = st.text_area("What do you dislike about your current mattress? (Optional)")
    
    submitted = st.form_submit_button("Find My Perfect Mattress")

if submitted:
    if not api_key or api_key == "your_google_api_key_here":
        st.error("Google API Key not found. Please set GOOGLE_API_KEY in your .env file.")
    else:
        with st.spinner("Analyzing your sleep profile with AI..."):
            try:
                # Prepare the prompt
                prompt = f"""
                You are an expert sleep consultant working for "Wakefit", a leading Indian sleep solutions company. Based on the following user profile, provide personalized mattress recommendations ONLY from Wakefit's product catalog (e.g., Wakefit Orthopedic Memory Foam, Wakefit Dual Comfort, Wakefit Latex, Wakefit Elevate).
                
                User Profile:
                - Primary Sleeping Position: {sleep_position}
                - Body Weight: {body_weight}
                - Budget: {budget}
                - Firmness Preference: {firmness}
                - Special Requirements: {', '.join(special_needs) if special_needs else 'None'}
                - Complaints about current mattress: {current_mattress_issue if current_mattress_issue else 'None specified'}
                
                Please strictly format your response using Markdown exactly following this structure:

                ### Top 3 Options Overview
                (Provide a quick summary of the top 3 Wakefit mattress recommendations like the example below)
                1️⃣ [Wakefit Mattress Name] (Best for [specific reason])
                2️⃣ [Wakefit Mattress Name] (Best for [specific reason])
                3️⃣ [Wakefit Mattress Name] (Best for [specific reason])
                
                ---
                
                ### 🏆 Recommended for you: [Top Wakefit Mattress Name]
                
                #### Why we chose this mattress:
                (Provide 3-4 bullet points using '✔' explaining WHY this mattress matches their specific profile)
                ✔ [Reason related to their sleep position]
                ✔ [Reason related to their body weight/firmness choice]
                ✔ [Reason related to their special requirements/complaints]
                ✔ [Additional benefit]
                
                **Price:** [Estimated Price in ₹ based on their budget]  
                **Rating:** ⭐ [Estimated Rating, e.g., 4.5]  
                **Link:** [Buy on Wakefit](https://www.wakefit.co/search?q=[URL encoded Wakefit+Brand+Model])
                
                ---
                
                ### 🥈 Alternative Choice: [Second Wakefit Mattress Name]
                
                #### Why this suits you:
                ✔ [Reason 1]
                ✔ [Reason 2]
                ✔ [Reason 3]
                
                **Price:** [Estimated Price in ₹]  
                **Rating:** ⭐ [Estimated Rating]  
                **Link:** [Buy on Wakefit](https://www.wakefit.co/search?q=[URL encoded Wakefit+Brand+Model])

                ---
                
                ### 🥉 Budget/Other Option: [Third Wakefit Mattress Name]
                
                #### Why this suits you:
                ✔ [Reason 1]
                ✔ [Reason 2]
                ✔ [Reason 3]
                
                **Price:** [Estimated Price in ₹]  
                **Rating:** ⭐ [Estimated Rating]  
                **Link:** [Buy on Wakefit](https://www.wakefit.co/search?q=[URL encoded Wakefit+Brand+Model])

                ---

                ### 🛍️ Relatable Wakefit Accessories
                Recommend 2-3 extra sleep accessories (e.g., Wakefit pillows, mattress protectors, fitted sheets) that go perfectly with their profile.
                - **[Wakefit Accessory Name]**: Why it helps. [Buy on Wakefit](https://www.wakefit.co/search?q=[URL Encoded Wakefit+Accessory+Name])
                - **[Wakefit Accessory Name]**: Why it helps. [Buy on Wakefit](https://www.wakefit.co/search?q=[URL Encoded Wakefit+Accessory+Name])
                
                ---
                
                ### 🚫 What to Avoid
                (Briefly list 1-2 mattress types or materials they should absolutely avoid based on their profile, e.g., "Avoid ultra-plush if you are a heavy stomach sleeper.")
                """
                
                # Setup model and generate response
                # Using gemini-2.5-flash since it's fast and perfect for text generation
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                
                st.success("Analysis Complete!")
                st.markdown("### 🛏️ Your Personalized Recommendations")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred while generating recommendations: {e}")


