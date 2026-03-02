# information-solver
AI supported PDF reading and summarisation. 

It creates 3 level summaries. Uses chunks for summarising tens of pages. Have two folder creatins. One is for JSONs: Memory_Bank, other is for PDFs: PDFs.

It uses qwen3:4b models that is fast and efficient for local uses. No subscription, no cost per token. Just download Ollama and use command prompt to write:
cmd: ollama pull qwen3:4b 

then you can use modelfiles given and cmd prompt:

cmd: ollama create info-solver -f ./ModelFile 

in the folder for creating info-solver model.

Do this for each model in the python file with given modelfiles. And you are set.


First level: Chunks based summary. All chunks summarised.

Second level: Combines chunks summaries gets the essence of all of them. This is saved as pdf in PDFs file

Third level: Outputs a JSON file with name, keywords, essence keys for further data mining operations.

Potential uses: Data mining, AI learning from text, memory creation for AI, self learner enthusiasts can use it to archive summaries of their PDF works.
