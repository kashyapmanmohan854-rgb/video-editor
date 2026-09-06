import streamlit as st

st.title("🎬 Video Editor App")
st.success("Aapka video editor ab permanent live ho chuka hai!")

uploaded_file = st.file_uploader("Apni video upload karein", type=["mp4", "mov"])
if uploaded_file is not None:
    st.video(uploaded_file)
