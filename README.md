# Summarize YouTube transcripts using OpenAI Completion APIs
This script retrieves the transcript of a YouTube video and uses the OpenAI APIs to generate a summary of the transcript.

# Requirements
* Python 3
* youtube_transcript_api
* openai
* tomli

# Useage 
To use this script, you need to provide the --lang and the --videoid of the YoutTube video. You will find the videoid in the YouTube video URL.  
For example:  
`$ python YT_AI_Sum.py --lang English --videoid 12345`  
The script also requires an openai.toml file with the API key, organization details for the OpenAI API, model to be used and the maximum number of tokens per request.  
The config file should contain the following information:  
`[openai]`  
`- apikey = "your_api_key"`
`- organization = "your_organization"`
`- model = "gtp-4"`
`- maxtokens = "1000"`
The script will then fetch the transcript of the YouTube video and generates a summary using the OpenAI API. The summary will be printed to the console.
