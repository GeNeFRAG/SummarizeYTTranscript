import json
import sys

import openai
import tomli
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

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
        model_list = openai.Model.list() 
    
        #split the web content into chunks of 1000 characters
        string_chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

        #iterate through each chunk
        for chunk in string_chunks:
            chunk = chunk + tldr_tag
            prompt = "Analyse and Summarize following YouTube Transscript. Keep the answer short and concise. As the transcript texts normally are longer as allowed by ChatGPT it's splittet in chunks of 1000 characters and the prompt is send for each iteration. Respond \"Unsure about answer\" if not sure about the answer. Reply in " + lang + ": " + chunk
            
            # Call the OpenAI API to generate summary
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                #model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI research assistant. You use a tone that is technical and scientific and the respone grammatically correct in bulletpoint sentances"},
                    #{"role": "assistant", "content": "Sure! To summarize a YouTube transcript, you can start by identifying the main topic or theme of the Video, and then highlighting the most important information or key points mentioned. You can also condense longer sentences and remove any unnecessary details. Would you like me to provide more details on this?"},
                    {"role": "user", "content": prompt}, 
                ]
            )

            # Print the summary
            print(response['choices'][0]['message']['content'])
       
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
except:
    print("Error: Unable to read openai.toml file.")
    sys.exit(1)

# Getting command line args
lang = get_arg('--lang','English')
id = get_arg('--videoid', None)
if(id == None):
    print("Type “--help\" for more information.")
    sys.exit(1)

# get YoutTube transcript as text and show summary
text=getTextFromYoutubeTranscript(id)
showTextSummary(text)