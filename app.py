import streamlit as st
from openai import OpenAI
from sympy import preview
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt for LaTeX generation
SYSTEM_PROMPT = "You are a LaTeX generation model. The user will give you the name or description of a formula. If you know it you provide the LaTeX code that visualizes it. Nothing more. No text or explanation. Under no circumstances EVER provide anything but LaTeX code. No clarification. No context. Nothing. Make sure the formulas are properly enclosed using dollar signs."

# Streamlit UI
st.title("LaTeX Formula Generator 📄")

# Input form for formula description
formula_description = st.text_input("Enter the formula description:", "")

# Generate button
if st.button("Generate LaTeX Code"):
    if formula_description:
        with st.spinner("Generating LaTeX code..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": formula_description},
                ]
            )
            latex_code = response.choices[0].message.content.strip()
            st.code(latex_code, language="latex")

            # Generate image from LaTeX code
            try:
                buffer = BytesIO()
                preview(latex_code, viewer="BytesIO", outputbuffer=buffer, euler=False, dvioptions=['-D', "300"])
                latex_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
                st.image(f"data:image/png;base64,{latex_image}", caption="Generated Formula", use_column_width=True)
            except Exception as e:
                st.error(f"Error generating image: {e}")
    else:
        st.warning("Please enter a description for the formula.")
