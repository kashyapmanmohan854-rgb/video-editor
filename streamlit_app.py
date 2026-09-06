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
    .main-title {font-size: 32px; font-weight: bold; color: #FF4B4B; text-align: center;}
    .sub-text {font-size: 16px; color: #555; text-align: center; margin-bottom: 30px;}
    .feature-box {background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">✨ AI Smart Video & Sound Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Next-Gen Web Platform for Automated Video Enhancement, Sound Grading & Pro FX!</p>', unsafe_allow_html=True)

# Sidebar with Web Stats & Info (Professional touch)
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/video-editing.png", width=120)
    st.header("💡 Web Platform Stats")
    st.info("⚡ Powered by Advanced Cloud Rendering\n🛡️ Secure & 100% Free Processing\n🔥 High Bitrate HD Output")
    st.markdown("---")
    st.write("**Pro Tips for Users:**")
    st.write("• Upload MP4/MOV files.")
    st.write("• Fix rotation if shot vertically.")
    st.write("• Use color boost for cinematic look.")

uploaded_file = st.file_uploader("📂 Upload Your Video File (MP4, MOV, AVI)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    
    video = VideoFileClip(tfile.name)
    
    st.success("🎉 Video successfully loaded into Cloud Buffer!")
    st.video(tfile.name)
    
    st.markdown("---")
    st.markdown("### 🎛️ AI Studio & Enhancement Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        enhance_color = st.checkbox("💎 AI Cinematic Color Grading", value=True)
        brightness_val = st.slider("☀️ Brightness Level:", 0.5, 2.0, 1.1)
    with col2:
        rotate_angle = st.selectbox("🔄 Smart Rotation Fix:", [0, 90, 180, 270], index=0)
        speed_factor = st.selectbox("⚡ Playback Speed:", [1.0, 1.25, 1.5, 2.0, 0.5], index=0)
    
    duration = int(video.duration)
    start_time, end_time = st.slider("⏱️ Precision Timeline Trimming (seconds):", 0, duration, (0, duration))
    
    st.markdown("---")
    
    if st.button("🚀 Render & Process Smart Video", type="primary", use_container_width=True):
        with st.spinner("✨ AI is analyzing frames, adjusting color balance, and rendering output... Please wait!"):
            try:
                # 1. Trimming
                processed = video.subclip(start_time, end_time)
                
                # 2. Rotation
                if rotate_angle != 0:
                    processed = processed.rotate(rotate_angle)
                
                # 3. Speed
                if speed_factor != 1.0:
                    processed = processed.speedx(speed_factor)
                
                # 4. Color Grading
                if enhance_color:
                    processed = processed.fx(vfx.colorx, brightness_val)

                # Export High Quality Output
                output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                processed.write_videofile(
                    output_path, 
                    codec='libx264', 
                    audio_codec='aac', 
                    fps=30, 
                    preset='medium',
                    bitrate='5000k'
                )
                
                st.success("🔥 Success! Your cinematic video is fully optimized and ready.")
                st.video(output_path)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download HD Processed Video",
                        data=file,
                        file_name="ai_optimized_video.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"⚠️ Processing Error encountered: {e}")
