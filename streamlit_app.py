
import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os

st.title("🎬 Professional Video Editor App")
st.write("Aapka permanent aur powerful video editor!")

uploaded_file = st.file_uploader("Apni video upload karein", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    video = VideoFileClip(tfile.name)
    
    st.success("Video successfully load ho gayi hai!")
    st.video(tfile.name)
    
    st.write("### 🛠️ Editing Options")
    
    duration = int(video.duration)
    start_time, end_time = st.slider("Select start and end time (seconds):", 0, duration, (0, duration))
    
    speed_factor = st.selectbox("Speed select karein:", [1.0, 1.5, 2.0, 0.5], index=0)
    rotate_angle = st.selectbox("Rotation select karein:", [0, 90, 180, 270], index=0)
    
    if st.button("🚀 Process Video"):
        with st.spinner("Video process ho rahi hai..."):
            try:
                processed_video = video.subclip(start_time, end_time)
                
                if speed_factor != 1.0:
                    processed_video = processed_video.speedx(speed_factor)
                    
                if rotate_angle != 0:
                    processed_video = processed_video.rotate(rotate_angle)
                
                output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                processed_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
                
                st.success("Video taiyar hai!")
                st.video(output_path)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Edited Video",
                        data=file,
                        file_name="edited_video.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Kuch error aa gaya: {e}")
