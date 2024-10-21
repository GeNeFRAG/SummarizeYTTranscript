import sys
from youtube_transcript_api import YouTubeTranscriptApi
from GPTCommons import GPTCommons

def get_text_yt_transcript(id):
    """
    Retrieves the transcript of a YouTube video in English and German languages (if available).

    Args:
    id (str): The YouTube video ID for which to retrieve the transcript.

    Returns:
    str: The concatenated transcript text.

    Example:
    >>> video_id = "abc123"
    >>> transcript_text = get_text_yt_transcript(video_id)
    >>> print(transcript_text)
    'This is the transcript of the video...'
    """
    print(f"Attempting to retrieve the transcript for video ID: {id}...")
    try:
        # Attempt to retrieve the transcript of the video in English and German
        transcript = YouTubeTranscriptApi.get_transcript(id, languages=['en', 'en-US', 'de'])
        print("Transcript successfully retrieved.")
    except Exception as e:
        # If an exception is raised, print an error message and exit the program
        print("Error: Unable to retrieve YouTube transcript.")
        print(f"{e}")
        sys.exit(1)

    # Concatenate all of the text segments of the transcript together
    transcript_text = []
    for x in transcript:
        transcript_text.append(x["text"])

    # Join the list at the end
    transcript_text = "-".join(transcript_text)

    # Return the full transcript as a string
    return transcript_text

def show_text_summary(text, output_file=None, to_html=False,detail_level='analytical', max_words=200):
    """
    Generates a text summary of a given input text, removes duplicate or redundant information, and prints the result.
    If an output file is specified, writes the summary to the file instead of printing it.

    Args:
    text (str): The input text to be summarized and cleaned.
    output_file (str, optional): The path to the file where the summary should be written. Defaults to None.

    Returns:
    None

    Example:
    >>> web_content = "This is a long piece of text with multiple paragraphs. It contains information about various topics."
    >>> show_text_summary(web_content)
    [Summary of the text]
    [Cleaned text with duplicate/redundant information removed]

    Note:
    The function relies on the 'split_into_chunks' and 'get_completion' functions, and it uses a specific model ('gptmodel') and language ('lang') for text generation.
    """
    if text is None:
        print("No text found to summarize.")
        return
    try:
        # Split the transcript into chunks to fit into the ChatGPT API limits
        print("Splitting the transcript into manageable chunks...")
        string_chunks = commons.split_into_chunks(text, commons.get_maxtokens(), 0.5)

        # Iterate through each chunk
        print(f"Summarizing transcript using OpenAI completion API with model {commons.get_gptmodel()}. Detail level {detail_level}, max. words {max_words}...")  
        responses = [
                    commons.get_chat_completion(
                            f"""Extract the key points and main ideas from the following text in an {detail_level} style. 
                            Focus on the most important information and key statements. Reply in {lang}.
                            Text: ```{chunk}```"""
                         ) 
                        for chunk in string_chunks
                    ]
        
        complete_response_str = "\n".join(responses)
        complete_response_str = commons.clean_text(complete_response_str)

        # Reduce the text to the maximum number of tokens
        print("Reducing the text to the maximum number of tokens...")
        complete_response_str = commons.reduce_to_max_tokens(complete_response_str)

        # Remove duplicate and redundant information
        print(f"Removing duplicate or redundant information using OpenAI completion API with model {commons.get_gptmodel()}...") 
        prompt = f"""Remove duplicate or redundant information from the text below, keeping the tone consistent. Provide the answer in bullet points, and a maximum of {max_words} words.
                    Text: ```{complete_response_str}```"""
        response = commons.get_chat_completion(prompt)
        
        commons.write_summary_to_file(response, output_file, to_html)

    except Exception as e:
        print("Error: Unable to generate summary for the transcript.")
        print(f"{e}")
        return None

# Initialize Utility class
print("Initializing GPTCommons utility class...")
commons = GPTCommons.initialize_gpt_commons("openai.toml")

arg_descriptions = {
    "--help": "Help",
    "--lang": "Language (default: English)",
    "--videoid": "YouTube Video ID",
    "--output": "Output file name",
    "--html": "Convert output to HTML format (default: False)",
    "--detail_level": "Detail level (default: analytical)",
    "--max_words": "Maximum number of words of the summary (default: 200)"
}

# Getting command line args
print("Retrieving command-line arguments...")
lang = commons.get_arg('--lang', arg_descriptions, 'English')
id = commons.get_arg('--videoid', arg_descriptions, None)
if id is None:
    print("Error: YouTube Video ID not provided. Type '--help' for more information.")
    sys.exit(1)
output_file = commons.get_arg('--output', arg_descriptions, None)
to_html = commons.get_arg('--html', arg_descriptions, 'False').lower() == 'true'
detail_level = commons.get_arg('--detail_level', arg_descriptions, 'analytical')
# Parse max_length with error handling
try:
    max_words = int(commons.get_arg('--max_words', arg_descriptions, 200))
except ValueError:
    print("Error: Invalid value for --max_words. It must be an integer. Using default value of 200.")
    max_words = 200

print(f"Downloading YouTube transcript for video ID: {id}...")

# Get YouTube transcript as text and show summary
show_text_summary(get_text_yt_transcript(id), output_file, to_html, detail_level, max_words)