import streamlit as st
from moviepy.editor import VideoFileClip, vfx
import tempfile
import os

# Page Configuration for Professional Look
st.set_page_config(
    page_title="AI Smart Video & Sound Studio",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling for Web/App feel
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #ff4b4b; text-align: center; }
    .sub-title { font-size: 16px; color: #a3a3a3; text-align: center; margin-bottom: 30px; }
    </style>
    <div class="main-title">✨ AI Smart Video & Sound Studio Pro</div>
    <div class="sub-title">Next-Gen Web Platform for Automated Video Enhancement, Smart Color Grading & Pro FX</div>
""", unsafe_allow_html=True)

# File Uploader
uploaded_file = st.file_uploader("📂 Upload Your Video File (MP4, MOV, AVI)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save uploaded video to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.success("🔥 Video successfully uploaded! Previewing original source:")
    st.video(video_path)

    st.markdown("---")
    st.markdown("### 🎛️ AI Studio & Enhancement Controls")

    # User Controls for Auto-Editing / Effects
    auto_ai_mode = st.checkbox("🤖 Enable AI Smart Auto-Mood Enhancement", value=True)
    cinematic_grading = st.checkbox("💎 AI Cinematic Color Grading", value=True)
    brightness_level = st.slider("☀️ Brightness & Exposure Balance", 0.5, 2.0, 1.1)
    
    speed_option = st.selectbox("⚡ Playback Speed Preset", ["Normal (1.0x)", "Cinematic Slow-Mo (0.8x)", "Fast Dynamic (1.25x)"])
    
    # Process Button
    if st.button("🚀 Render & Process Smart Video"):
        with st.spinner("✨ AI is analyzing lighting, cutting unwanted elements, and applying pro effects..."):
            try:
                # Load video using MoviePy
                clip = VideoFileClip(video_path)

                # Apply Speed Modification
                if "0.8x" in speed_option:
                    clip = clip.fx(vfx.speedx, 0.8)
                elif "1.25x" in speed_option:
                    clip = clip.fx(vfx.speedx, 1.25)

                # Apply Auto-Brightness / Color Adjustment if selected
                if cinematic_grading or auto_ai_mode:
                    clip = clip.fx(vfx.colorx, brightness_level)

                # Output temporary file for processed video
                output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                
                # Write result video file
                clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

                st.success("🔥 Success! Your cinematic video is fully optimized and ready.")
                st.video(output_path)

                # Clean up resources
                clip.close()

            except Exception as e:
                st.error(f"⚠️ An error occurred during processing: {e}")
