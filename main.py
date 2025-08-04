from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import os
import json
from datetime import datetime
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_results_cache(cache_file="video_results.json"):
    """Load existing results from JSON file"""
    try:
        with open(cache_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_results_cache(cache, cache_file="video_results.json"):
    """Save results to JSON file"""
    with open(cache_file, 'w') as f:
        json.dump(cache, f, indent=2)

def parse_ai_response(response_text):
    """Parse the AI response into separate title, tags, and summary"""
    title_match = re.search(r'Title:\s*["\']?([^"\'\n]+)', response_text)
    tags_match = re.search(r'Tags:\s*\[([^\]]+)\]', response_text)
    summary_match = re.search(r'Summary:\s*["\']?([^"\'\n]+)', response_text)
    
    title = title_match.group(1).strip() if title_match else "No title found"
    
    # Parse tags and clean them up
    if tags_match:
        tags_text = tags_match.group(1)
        tags = [tag.strip().strip("'\"") for tag in tags_text.split(',')]
    else:
        tags = []
    
    summary = summary_match.group(1).strip() if summary_match else "No summary found"
    
    return {
        "title": title,
        "tags": tags,
        "summary": summary
    }

def generate_tags_and_title(transcript: str):
    prompt = f"""
                You are a YouTube SEO assistant. A user gave you the transcript of a video. Your job is to:

                1. Suggest a **clickable title** (max 60 characters)
                2. Suggest **5-10 SEO-friendly tags** (single words or short phrases)
                3. Provide a **1-line TLDR summary**

                Transcript:
                \"\"\"
                {transcript[:4000]}
                \"\"\"

                Output format:
                Title: <...>
                Tags: [tag1, tag2, ...]
                Summary: <...>
                """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def check_cache_and_display(video_id, results_cache):
    """Check if video is in cache and display results if found"""
    if video_id in results_cache:
        print(f"✓ Video {video_id} already processed. Loading from cache...")
        cached_result = results_cache[video_id]
        print(f"Processed on: {cached_result['processed_date']}")
        display_results(cached_result)
        return True
    return False

def get_video_transcript(video_id):
    """Get transcript for given video ID"""
    yt_api = YouTubeTranscriptApi()
    transcript = yt_api.fetch(video_id)
    return transcript

def process_video_with_ai(transcript):
    """Process transcript with AI and parse the response"""
    ai_response = generate_tags_and_title(transcript)
    parsed_response = parse_ai_response(ai_response)
    return parsed_response, ai_response

def display_results(result_data):
    """Display the title, tags, and summary"""
    print(f"Title: {result_data['title']}")
    print(f"Tags: {result_data['tags']}")
    print(f"Summary: {result_data['summary']}")

def save_to_cache(video_id, transcript, parsed_response, ai_response, results_cache, cache_file):
    """Save results to cache"""
    results_cache[video_id] = {
        "processed_date": datetime.now().isoformat(),
        "transcript_length": len(transcript),
        "title": parsed_response['title'],
        "tags": parsed_response['tags'],
        "summary": parsed_response['summary'],
        "raw_ai_response": ai_response
    }
    
    save_results_cache(results_cache, cache_file)
    print(f"\n✓ Results saved to {cache_file}")

def main():
    video_id = "H6gmux1z6Zk"  # Get this from the URL
    cache_file = "video_results.json"
    
    # Load existing results
    results_cache = load_results_cache(cache_file)
    
    # Check if video was already processed
    if check_cache_and_display(video_id, results_cache):
        return
    
    print(f"Processing new video: {video_id}")
    
    # Get transcript
    transcript = get_video_transcript(video_id)
    
    # Generate AI summary and parse response
    parsed_response, ai_response = process_video_with_ai(transcript)
    
    # Display results
    display_results(parsed_response)
    
    # Save to cache
    save_to_cache(video_id, transcript, parsed_response, ai_response, results_cache, cache_file)

if __name__ == "__main__":
    main()

