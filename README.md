<!DOCTYPE html>
<html>
<body>
   <h1>YouTube Transcript Summarizer</h1>

<p>This script uses the <a href="https://pypi.org/project/youtube-transcript-api/">youtube_transcript_api</a> library to retrieve the transcript of a YouTube video in English and German, and the <a href="https://pypi.org/project/openai/">openai</a> library to generate a summary of the transcript.</p>

<h2>Requirements</h2>

<ul>
  <li>Python 3</li>
  <li><a href="https://pypi.org/project/youtube-transcript-api/">youtube_transcript_api</a></li>
  <li><a href="https://pypi.org/project/openai/">openai</a></li>
  <li><a href="https://pypi.org/project/tomli/">tomli</a></li>
</ul>

<h2>Usage</h2>

<ol>
  <li>Replace <code>openai.api_key</code> and <code>openai.organization</code> in <code>openai.toml</code> file with your OpenAI API key and organization.</li>
  <li>Run the script with the command <code>python YT_AI_Sum.py &lt;max_tokens&gt; &lt;video_id&gt;</code>.</li>
  <li>The summary will be printed in the console.</li>
</ol>

<h2>Notes</h2>

<ul>
  <li>The <code>youtube_transcript_api</code> library uses the YouTube Data API to retrieve the transcript, so you will need to have a YouTube API key set up.</li>
  <li>The <code>openai</code> library uses the OpenAI API to generate the summary, so you will need to have an OpenAI API key set up.</li>
  <li>The <code>max_tokens</code> argument determines the maximum number of tokens in the summary.</li>
  <li>The <code>video_id</code> argument is the YouTube video ID of the video you want to summarize.</li>
  <li>If an exception is raised, the script will print an error message and exit.</li>
  <li>The tldr tag will be added at the end of each summary</li>
  <li>split the text into chunks of 1000 characters and will iterate through each chunk and generate the summary.</li>
</ul>

</body>
</html>