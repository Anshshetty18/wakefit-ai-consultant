# Wakefit AI Sleep Consultant 🌙

An AI-powered web application designed for Wakefit. It acts as an expert sleep consultant, recommending the perfect sleep solutions based on user profiles, sleep positions, budgets, and specific needs. Built to combat decision fatigue and build buyer confidence through transparent, explainable AI.

## 🚀 Features
- **Intelligent Profiling**: Captures sleep position, body weight, budget, firmness preferences, and specific sleep issues (like back pain or sleep heat).
- **Explainable AI Recommendations**: Doesn't just suggest a product—it justifies exactly *why* a mattress fits the user's specific profile with simple bullet points.
- **Top 3 Option Overview**: Ranks products systematically (Recommended, Alternative Choice, Budget Option).
- **Smart Cross-Selling**: Contextually recommends relatable companion sleep accessories (like Wakefit ergonomic pillows or waterproof protectors) that perfectly pair with the mattress.

## 🛠️ Setup Instructions

1. **Clone or Navigate to the project directory**:
   ```bash
   cd "Wakefit_AI_Consultant"
   ```

2. **Install Requirements**:
   Ensure you have Python installed, then install the dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **API Key Setup**:
   This app uses Google's Gemini API (gemini-2.5-flash). You need an API key from [Google AI Studio](https://aistudio.google.com/).
   - Copy `.env.example` to `.env`.
   - Open the new `.env` file and replace the placeholder with your actual Google API key.

4. **Run the Application**:
   Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```

5. **View Application**:
   The app will automatically open in your default browser at `http://localhost:8501`.
