import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
analysis_prompt = os.environ.get('ANALYSIS_PROMPT')
def insights(file):
    data = pd.read_csv(file).to_string()
    analysis_prompt = os.environ.get('ANALYSIS_PROMPT')

    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
# Choose a model that's appropriate for your use case.
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""{data}
    {analysis_prompt}
    """

    response = model.generate_content(prompt)
    if response.text:
        analysis_text = response.text
    return analysis_text




    