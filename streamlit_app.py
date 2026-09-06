import streamlit as st
from moviepy.editor import VideoFileClip, vfx
import tempfile
import os

st.set_page_config(page_title="Pro Automated Video Editor", page_icon="🎬", layout="centered")

st.title("🎬 Pro Automated Video Studio")
st.write("Ekdum powerful aur high-quality processing — automatic filters aur rotation ke sath!")

uploaded_file = st.file_uploader("Apni video upload karein", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    
    video = VideoFileClip(tfile.name)
    
    st.success("Video successfully load ho gayi hai!")
    st.video(tfile.name)
    
    st.write("### 🔥 Professional Enhancement Options")
    
    enhance_quality = st.checkbox("💎 Heavy Color & Sharpness Boost (Pro Look)", value=True)
    brighten = st.slider("☀️ Brightness Adjustment:", 0.8, 1.5, 1.1)
    contrast_val = st.slider("🎨 Contrast Boost:", 0.8, 1.5, 1.2)
    
    rotate_angle = st.selectbox("🔄 Fix Orientation / Rotation:", [0, 90, 180, 270], index=0)
    
    duration = int(video.duration)
    start_time, end_time = st.slider("Trim video duration (seconds):", 0, duration, (0, duration))
    speed_factor = st.selectbox("Overall Speed:", [1.0, 1.25, 1.5, 2.0, 0.5], index=0)
    
    if st.button("🚀 Process Pro Quality Video"):
        with st.spinner("Pro-level rendering aur quality enhancement chal rahi hai... Kripya intezaar karein!"):
            try:
                processed_video = video.subclip(start_time, end_time)
                
                if rotate_angle != 0:
                    processed_video = processed_video.rotate(rotate_angle)
                
                if speed_factor != 1.0:
                    processed_video = processed_video.speedx(speed_factor)
                
                if enhance_quality:
                    processed_video = processed_video.fx(vfx.colorx, contrast_val)
                    processed_video = processed_video.fx(vfx.lum_contrast, lum=0.1, contrast=contrast_val, g=brighten)

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
