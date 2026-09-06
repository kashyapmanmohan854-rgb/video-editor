import streamlit as st
from moviepy.editor import VideoFileClip, vfx
import tempfile
import os

st.set_page_config(page_title="Pro Automated Video Editor", page_icon="🎬", layout="centered")

st.title("🎬 Pro Automated Video Studio")
st.write("100% Free & Powerful Video Editor — Heavy Color Grading & High Quality Export!")

uploaded_file = st.file_uploader("Apni video upload karein", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    
    video = VideoFileClip(tfile.name)
    
    st.success("Video successfully load ho gayi hai!")
    st.video(tfile.name)
    
    st.write("### 🔥 Professional Enhancement Options")
    
    enhance_quality = st.checkbox("💎 Heavy Color & Contrast Boost (Pro Look)", value=True)
    brighten_val = st.slider("☀️ Brightness / Luminosity:", -50.0, 50.0, 15.0)
    contrast_val = st.slider("🎨 Contrast Multiplier:", 0.5, 2.0, 1.3)
    
    rotate_angle = st.selectbox("🔄 Fix Orientation / Rotation:", [0, 90, 180, 270], index=0)
    
    duration = int(video.duration)
    start_time, end_time = st.slider("Trim video duration (seconds):", 0, duration, (0, duration))
    speed_factor = st.selectbox("Overall Speed:", [1.0, 1.25, 1.5, 2.0, 0.5], index=0)
    
    if st.button("🚀 Process Pro Quality Video"):
        with st.spinner("Pro-level rendering aur heavy color grading chal rahi hai... Kripya thoda intezaar karein!"):
            try:
                processed_video = video.subclip(start_time, end_time)
                
                if rotate_angle != 0:
                    processed_video = processed_video.rotate(rotate_angle)
                
                if speed_factor != 1.0:
                    processed_video = processed_video.speedx(speed_factor)
                
                if enhance_quality:
                    processed_video = processed_video.fx(vfx.lum_contrast, lum=brighten_val, contrast=contrast_val)

                output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                processed_video.write_videofile(
                    output_path, 
                    codec='libx264', 
                    audio_codec='aac', 
                    fps=30, 
                    preset='medium',
                    bitrate='5000k'
                )
                
                st.success("🔥 Aapki Pro Quality Video taiyar hai!")
                st.video(output_path)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Pro Edited Video",
                        data=file,
                        file_name="pro_enhanced_video.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Processing error: {e}")
