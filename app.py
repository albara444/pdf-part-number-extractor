import streamlit as st
import openai
import fitz
import re

openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ''
    for page in pdf_document:
        text += page.get_text()
    return text

def get_part_numbers(text):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "قم باستخراج أرقام الـ Part Numbers فقط من النص وحدد نوعها (داخلي أو خارجي). إذا كانت البيانات غير مؤكدة وضح ذلك."},
            {"role": "user", "content": text[:3000]}  # للحد من طول النص
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()

st.title("استخراج أرقام Parts (أجهزة باناسونيك)")

uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file:
    with st.spinner("جارٍ استخراج البيانات..."):
        text = extract_text_from_pdf(uploaded_file)
        result = get_part_numbers(text)
        st.success("تم استخراج البيانات بنجاح!")
        st.text_area("النتيجة", value=result, height=300)
