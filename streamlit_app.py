import streamlit as st
from moviepy.editor import VideoFileClip, vfx
import tempfile
import os

st.title("🎬 Smart Fully-Automated Video Editor")
st.write("Aap sirf video dijiye — color enhance aur rotation control ke sath video taiyar hai!")

uploaded_file = st.file_uploader("Apni video upload karein", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    
    video = VideoFileClip(tfile.name)
    
    st.success("Video successfully load ho gayi hai!")
    st.video(tfile.name)
    
    st.write("### 🤖 Smart Auto-Editing & Rotation Options")
    
    auto_color = st.checkbox("✨ Auto-Enhance Colors (Brightness & Contrast)", value=True)
    rotate_angle = st.selectbox("🔄 Fix Rotation (Agar video tedhi ho):", [0, 90, 180, 270], index=0)
    
    duration = int(video.duration)
    start_time, end_time = st.slider("Trim video duration (seconds):", 0, duration, (0, duration))
    speed_factor = st.selectbox("Overall Speed:", [1.0, 1.25, 1.5, 2.0, 0.5], index=0)
    
    if st.button("🚀 Process Automated Video"):
        with st.spinner("Smart processing aur rotation fix ho rahi hai..."):
            try:
                processed_video = video.subclip(start_time, end_time)
                
                if rotate_angle != 0:
                    processed_video = processed_video.rotate(rotate_angle)
                
                if speed_factor != 1.0:
                    processed_video = processed_video.speedx(speed_factor)
                    
                if auto_color:
                    processed_video = processed_video.fx(vfx.colorx, 1.2)

                output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                processed_video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)
                
                st.success("Aapki video bilkul sahi hokar taiyar hai!")
                st.video(output_path)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Smart Edited Video",
                        data=file,
                        file_name="smart_edited_video.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Processing ke dauran error aaya: {e}")
