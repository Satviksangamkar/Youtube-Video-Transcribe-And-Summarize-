import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables (ensure you have GOOGLE_API_KEY in your .env file)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define a more comprehensive prompt for the model
prompt = """You are a YouTube video summarizer. Your task is to analyze the 
following transcript text and provide a concise summary within 250 words. 
Highlight the key points, main arguments, and any important conclusions 
presented in the video. 
Transcript: """

# Function to extract transcript text 
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Efficiently join transcript segments
        transcript = " ".join([item["text"] for item in transcript_list])

        return transcript
    except Exception as e:
        st.error(f"Error processing transcript: {e}") 
        return None  # Return None to signal failure

# Function to generate summary using Gemini Pro (replace with actual model)
def generate_gemini_content(transcript_text, prompt):
    # Replace with the actual code to interact with Gemini Pro
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text) 
    return response.text


# Streamlit UI
st.title("YouTube Video Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    # Extract video ID and display thumbnail (error handling included)
    try:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except IndexError:
        st.warning("Invalid YouTube link format. Please make sure it's a valid video URL.")

# Columns for buttons
col1, col2 = st.columns(2)

# Button to get the summary
with col1:
    if st.button("Summarize"):
        if youtube_link:  # Check if a link was provided
            transcript_text = extract_transcript_details(youtube_link)
            if transcript_text:  # Check if transcript extraction was successful
                with st.spinner("Summarizing..."):
                    summary = generate_gemini_content(transcript_text, prompt)
                    st.subheader("Summary:")
                    st.write(summary)
        else:
            st.warning("Please enter a YouTube video link first.")

# Button to get the full transcript
with col2:
    if st.button("Show Full Transcript"):
        if youtube_link:
            transcript_text = extract_transcript_details(youtube_link)
            if transcript_text:
                st.subheader("Full Transcript:")
                st.text_area("", value=transcript_text, height=300) 
        else:
            st.warning("Please enter a YouTube video link first.")