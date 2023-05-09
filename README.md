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
  <li>Run the script with the command <code>python YT_AI_Sum.py --lang English --videoid <i>youtube videoid</i></code>.</li>
  <li>The summary will be printed in the console.</li>
</ol>

<h2>Notes</h2>
<ul>
  <li>It will use the OpenAI's <code>gpt-3.5-turbo</code> model to generate summary</li>
</ul>

<h2>Limitations</h2>
<ul>
  <li>This script uses OpenAI API to generate summary which has usage limit based on the plan you have subscribed to.</li>
</ul>

</body>
</html>