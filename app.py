import streamlit as st
import yt_dlp
import base64
from io import BytesIO

# Video Quality Options
VIDEO_QUALITIES = ["144p", "240p", "360p", "480p", "720p", "1080p"]

def download_video(url, quality):
    """Downloads a YouTube video in the selected quality without merging."""
    try:
        ydl_opts = {
            'format': f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': 'video.mp4',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'merge_output_format': 'mp4',  # Ensure MP4 output (No ffmpeg needed)
            'postprocessors': [],  # Disable ffmpeg merging
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.youtube.com/',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)  # Validate video
            ydl.download([url])

        # Read video file into memory
        with open("video.mp4", "rb") as f:
            video_data = BytesIO(f.read())

        return video_data, "video.mp4"

    except yt_dlp.utils.DownloadError as e:
        return None, f"Download Error: {e}"
    except yt_dlp.utils.ExtractorError as e:
        return None, f"Extractor Error: {e}"
    except Exception as e:
        return None, f"Unexpected Error: {e}"

def get_download_link(file_data, filename):
    """Generates a download link for the video file."""
    encoded_data = base64.b64encode(file_data.getvalue()).decode()
    href = f'<a href="data:video/mp4;base64,{encoded_data}" download="{filename}">Click here to download</a>'
    return href

def main():
    st.title("🎬 YouTube Video Downloader")
    url = st.text_input("🔗 Enter YouTube video URL:")
    quality = st.selectbox("🎥 Select video quality:", VIDEO_QUALITIES, index=4)  # Default: 720p

    if st.button("📥 Download"):
        if url:
            st.info("⏳ Downloading... Please wait.")
            file_data, filename = download_video(url, quality)

            if file_data:
                st.success(f"✅ Downloaded: {filename}")
                st.markdown(get_download_link(file_data, filename), unsafe_allow_html=True)
            else:
                st.error(f"❌ {filename}")  # Display error message
        else:
            st.warning("⚠️ Please enter a valid YouTube URL.")

    if st.button("▶️ View Video"):
        if url:
            st.video(url)
        else:
            st.warning("⚠️ Enter a valid YouTube URL to preview.")

if __name__ == "__main__":
    main()
