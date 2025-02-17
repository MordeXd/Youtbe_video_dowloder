import streamlit as st
import yt_dlp
import os
import shutil

# Video Quality Options
VIDEO_QUALITIES = ["144p", "240p", "360p", "480p", "720p", "1080p"]

def download_video(url, quality):
    """Downloads video and audio separately and merges them into one MP4 file."""
    try:
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_id = info_dict['id']  # Get unique video ID
            ydl.download([url])

        # Get file names
        video_file = next((f for f in os.listdir(output_dir) if f.startswith(video_id) and f.endswith(".mp4")), None)
        audio_file = next((f for f in os.listdir(output_dir) if f.startswith(video_id) and f.endswith(".m4a")), None)

        # Merge manually if needed
        final_file = f"{output_dir}/{video_id}_merged.mp4"
        if video_file and audio_file:
            with open(final_file, "wb") as merged:
                with open(f"{output_dir}/{video_file}", "rb") as vf, open(f"{output_dir}/{audio_file}", "rb") as af:
                    merged.write(vf.read())  # Write video
                    merged.write(af.read())  # Append audio

            os.remove(f"{output_dir}/{video_file}")  # Remove original chunks
            os.remove(f"{output_dir}/{audio_file}")

        return final_file

    except Exception as e:
        return f"Error: {e}"

def main():
    st.title("🎬 YouTube Video Downloader")
    url = st.text_input("🔗 Enter YouTube video URL:")
    quality = st.selectbox("🎥 Select video quality:", VIDEO_QUALITIES, index=4)  # Default: 720p

    if st.button("📥 Download"):
        if url:
            st.info("⏳ Downloading... Please wait.")
            file_path = download_video(url, quality)

            if os.path.exists(file_path):
                st.success("✅ Download Complete!")
                st.markdown(f"📥 [Download Video]({file_path})", unsafe_allow_html=True)
            else:
                st.error("❌ Download Failed.")
        else:
            st.warning("⚠️ Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()