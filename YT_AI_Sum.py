import json
import sys

import openai
import tomli
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

def get_completion(prompt, model, temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def optimize_text_for_api(text, max_tokens):
    text = text.replace('\r', ' ').replace('\n', ' ')
    tokenized_text = text.split()  # Tokenize the text by splitting on spaces
    if len(tokenized_text) > max_tokens:
        tokenized_text = tokenized_text[:max_tokens]  # Truncate the text to fit within the token limit
        optimized_text = ' '.join(tokenized_text)  # Join the tokens back into a string
        print("Text has been optimized to fit within the token limit.")
        return optimized_text
    else:
        return text

def get_arg(arg_name, default=None):
    """
    Safely reads a command line argument by name.
    :param arg_name: the name of the argument to read.
    :param default: the default value to return if the argument is not found.
    :return: the value of the argument if found, or the default value.
    """
    if "--help" in sys.argv:
        print("Usage: python Web_AI_Sum.py [--help] [--lang] [--videoid]")
        print("Arguments:")
        print("\t--help\t\tHelp\t\tNone")
        print("\t--lang\t\tLanguage\tEnglish")
        print("\t--videoid\tYoutube VideoID\tNone")
        # Add more argument descriptions here as needed
        sys.exit(0)
    try:
        arg_value = sys.argv[sys.argv.index(arg_name) + 1]
        return arg_value
    except (IndexError, ValueError):
        return default

# This function attempts to retrieve the transcript of a YouTube video with the given ID in both English and German. If an exception is raised, an error message is printed and the program exits. The text segments of the transcript are concatenated together and returned as a string.
def getTextFromYoutubeTranscript(id):
    # Attempt to retrieve the transcript of the video in English and German
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id, languages=['en','de'])
    # If an exception is raised, print an error message and exit the program
    except Exception as e:
        print("Error: Unable to retrieve YouTube transcript.")
        print(e)
        sys.exit(1)
    # Concatenate all of the text segments of the transcript together
    transcript_text = ""
    for x in transcript:
        transcript_text += "-"
        transcript_text += x["text"]
    # Return the full transcript as a string
    return transcript_text

# This function takes a text as an argument and prints a summary of the text. It first checks if the text is None, and if it is, it returns. Otherwise, it creates a list of models using openai.Model.list(), splits the web content into chunks of 1000 characters, iterates through each chunk and calls the OpenAI API to generate summary for each chunk. Finally, it prints the summary for each chunk with a tldr tag at the end.
def showTextSummary(text):
    if text is None:
        return
    try:
        # tldr tag to be added at the end of each summary
        tldr_tag = "\n tl;dr:"

        #split the web content into chunks of 1000 characters
        string_chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

        #iterate through each chunk
        responses = ""
        for chunk in string_chunks:
            chunk = chunk + tldr_tag
            prompt = f"""You will be provided with text chunks of a YouTube Transscript delimited by triple backtips.\
                        Your task is to summarize the chunks in an executive summary style. \
                        Provide the answer in at most 5 bulletpoint sentences and at most 100 words. \
                        Respond \"Unsure about answer\" if not sure about the answer. \
                        Reply in Language {lang}.\
                        ```{chunk}```
                        """
            
            # Call the OpenAI API to generate summary
            response = get_completion(prompt, gptmodel)

            # Store the summary
            responses = responses + response
            
        responses = optimize_text_for_api(responses, maxtokens)

        prompt = f"""Your task is to remove duplicate or similar information in provided text delimited by triple backtips. \
                Your task is to create smooth transitions between each bulletpoint.
        ```{responses}```
                """
        response = get_completion(prompt, gptmodel)
        print(response)

    except Exception as e:
        print("Error: Unable to generate summary for the paper.")
        print(e)
        return None

#Reading out OpenAI API keys and organization
try:
    with open("openai.toml","rb") as f:
        data = tomli.load(f)
        openai.api_key=data["openai"]["apikey"]
        openai.organization=data["openai"]["organization"]
        gptmodel=data["openai"]["model"]
        maxtokens = int(data["openai"]["maxtokens"])
except:
    print("Error: Unable to read openai.toml file.")
    sys.exit(1)

# Getting command line args
lang = get_arg('--lang','English')
id = get_arg('--videoid', None)
if(id == None):
    print("Type “--help\" for more information.")
    sys.exit(1)

# Get YoutTube transcript as text and show summary
text=getTextFromYoutubeTranscript(id)
showTextSummary(text)