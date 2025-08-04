# YouTube Video SEO Assistant

This repository contains a Python application designed to assist with generating SEO-friendly titles, tags, and summaries for YouTube videos based on their transcripts. The application leverages the OpenAI API to process video transcripts and produce optimized metadata for better visibility and engagement on YouTube.

## Features

- **Transcript Processing**: Fetches video transcripts using the `youtube_transcript_api`.
- **AI-Generated Metadata**: Utilizes OpenAI's API to generate a clickable title, SEO-friendly tags, and a concise summary.
- **Caching System**: Stores processed results in a JSON cache to avoid redundant processing.
- **Environment Configuration**: Uses a `.env` file to manage API keys securely.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube_videos.git
   cd youtube_videos
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your `.env` file with the necessary API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. Run the main script to process a video:
   ```bash
   python main.py
   ```

2. The script will check if the video has already been processed and display cached results if available. Otherwise, it will fetch the transcript, generate metadata using AI, and save the results to the cache.

## File Structure

- `main.py`: The main script to run the application.
- `video_results.json`: Stores cached results of processed videos.
- `.gitignore`: Specifies files and directories to be ignored by git.
- `README.md`: Documentation for the repository.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.