import streamlit as st
from transformers import pipeline
import arabic_reshaper
from bidi.algorithm import get_display

# إعداد نموذج التلخيص
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # الجهاز -1 لضمان استخدام CPU
except Exception as e:
    st.error(f"Error loading summarizer: {e}")

# عنوان التطبيق
st.title("📚 تطبيق المخططات الهيكلية")
st.write("تلخيص النصوص، استخراج الأفكار الرئيسية، وتصميم المخططات الهيكلية.")

# تحميل النص من المستخدم
uploaded_file = st.file_uploader("📝 اختر ملف نصي (TXT):", type=["txt"])

if uploaded_file is not None:
    # قراءة النصوص من الملف
    text = uploaded_file.read().decode("utf-8")
    st.write("### النص الأصلي:")
    st.text_area("النص:", value=text, height=200)
    
    # تلخيص النص
    if st.button("📜 تلخيص النص"):
        with st.spinner("جاري التلخيص..."):
            summary = summarizer(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            
            # تجهيز النص العربي
            reshaped_summary = arabic_reshaper.reshape(summary)
            display_summary = get_display(reshaped_summary)
            
            st.write("### النص الملخص:")
            st.success(display_summary)
    
    # استخراج الأفكار الرئيسية (كمثال: الجمل الطويلة)
    if st.button("🧠 استخراج الأفكار"):
        with st.spinner("جاري استخراج الأفكار..."):
            ideas = [sentence for sentence in text.split('.') if len(sentence.strip()) > 50]
            st.write("### الأفكار الرئيسية:")
            for i, idea in enumerate(ideas, start=1):
                st.write(f"{i}. {idea.strip()}")
