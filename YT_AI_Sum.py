import youtube_transcript_api
import json
import openai
import sys
import tomli

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

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
            chunk = "Analyse and Summarize following text in short sentences: " + chunk
            
            # Call the OpenAI API to generate summary
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=chunk,
                temperature=1,
                max_tokens=maxtoken,
                frequency_penalty=0.2,
                presence_penalty=0.2,
                echo=False,
                stop=["\n"]
            )
            # Print the summary
            print(response["choices"][0]["text"])
       
    except Exception as e:
        print("Error: Unable to generate summary for the paper.")
        print(e)
        sys.exit(1)

#Reading out OpenAI API keys and organization
try:
    with open("openai.toml","rb") as f:
        data = tomli.load(f)
        openai.api_key=data["openai"]["apikey"]
        openai.organization=data["openai"]["organization"]
except:
    print("Error: Unable to read openai.toml file.")
    sys.exit(1)

# Getting max_tokens, video_id from command line
if len(sys.argv) == 1:
    raise Exception("Usage: <video id>")
    sys.exit(1)
try:
    maxtoken = int(sys.argv[1])
    id = sys.argv[2]
except Exception as e:
    print("Error retrieving commandline arguments")
    print(e)
    sys.exit(1)
    
# get YoutTube transcript as text and show summary
text=getTextFromYoutubeTranscript(id)
showTextSummary(text)