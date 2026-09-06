import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, vfx
import tempfile
import os

st.title("🎬 Smart Automated Video Editor")
st.write("Ek click mein video ko automatically enhance karein aur music jodein!")

uploaded_file = st.file_uploader("Apni video upload karein", type=["mp4", "mov", "avi"])
background_music = st.file_uploader("Background Music (Optional - MP3 upload karein)", type=["mp3", "wav"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    video = VideoFileClip(tfile.name)
    
    st.success("Video successfully load ho gayi hai!")
    st.video(tfile.name)
    
    st.write("### 🤖 Smart Auto-Editing Options")
    
    auto_color = st.checkbox("✨ Auto-Enhance Colors (Brightness & Contrast)", value=True)
    auto_slowmo_intro = st.checkbox("🎬 Cinematic Slow-mo Effect on Start", value=False)
    
    duration = int(video.duration)
    start_time, end_time = st.slider("Trim video duration (seconds):", 0, duration, (0, duration))
    
    speed_factor = st.selectbox("Overall Speed:", [1.0, 1.25, 1.5, 2.0, 0.5], index=0)
    rotate_angle = st.selectbox("Rotation:", [0, 90, 180, 270], index=0)
    
    if st.button("🚀 Process Automated Video"):
        with st.spinner("Smart processing aur rendering ho rahi hai, kripya intezaar karein..."):
            try:
                processed_video = video.subclip(start_time, end_time)
                
                if speed_factor != 1.0:
                    processed_video = processed_video.speedx(speed_factor)
                    
                if rotate_angle != 0:
                    processed_video = processed_video.rotate(rotate_angle)
                
                if auto_color:
                    processed_video = processed_video.fx(vfx.colorx, 1.2)
                
                if background_music is not None:
                    music_tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                    music_tfile.write(background_music.read())
                    
                    audio_clip = AudioFileClip(music_tfile.name)
                    
                    if audio_clip.duration > processed_video.duration:
                        audio_clip = audio_clip.subclip(0, processed_video.duration)
                        
                    processed_video = processed_video.set_audio(audio_clip)

                output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                processed_video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)
                
                st.success("Aapki smart edited video taiyar hai!")
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
