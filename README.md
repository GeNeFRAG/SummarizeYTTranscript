# Summarize YouTube Transcripts Using OpenAI Completion APIs

his script summarizes the text content of a YouTube using the OpenAI Completion API.

## Requirements

* Python 3
* youtube_transcript_api
* openai
* tomli
* tiktoken
* GPTCommons (a custom utility module)

## Usage

To use this script, provide the following command-line arguments:

### Arguments

- `--videoid`: The ID of the YouTube video.
- `--lang`: (Optional) Language of the summary (default: English).
- `--output`: (Optional) Output file name (default: STDOUT).
- `--html`: (Optional) Convert output to HTML (default: False).
- `--detail_level`: (Optional) Detail level of the summary (default: analytical).
- `--max_words`: (Optional) Maximum number of words for the summary (default: 200).

### OpenAI Configuration

The script requires an `openai.toml` file with API key, organization details, model, and maximum tokens per request. The config file should have the following format:

`[openai]`
- `apikey = "your_api_key"`
- `organization = "your_organization"`
- `model = "gpt-4"`
- `maxtokens = "1000"`

### Example

`$ python YT_AI_Sum.py --lang English --videoid 23idx333s --output yourfile.html --html True --detail_level high --max_words 500`