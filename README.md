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

<img width="904" height="583" alt="Ekran görüntüsü 2026-03-10 110225" src="https://github.com/user-attachments/assets/e27da401-82fb-4e23-829c-e2424e8221d8" />

# Information Solver: Two-Tier Memory Extraction Pipeline

A local, AI-powered PDF analysis and summarization tool built with Python, Streamlit, and **Ollama**. This project serves as a cognitive memory extraction module (originally designed for the DEUS agentic architecture). 

It processes complex documents using custom-tuned local LLMs (`qwen3:4b`) to extract semantic essence, keywords, and deep summaries, ultimately storing them in a structured, two-tier JSON memory bank.

## 🚀 Key Features

* **100% Local AI Processing:** Complete data privacy and zero API costs using local Ollama models.
* **Custom Model Pipeline:** Utilizes distinct, task-specific `Modelfiles` with strict deterministic parameters (e.g., Temperature 0.0) to ensure reliable JSON outputs and prevent hallucination.
* **Two-Tier Cognitive Memory:** Automatically generates a Master Memory Map for each document:
  * **Shallow Layer:** Contains semantic essence and exact keywords (Optimized for fast Vector DB / ChromaDB searches).
  * **Deep Layer:** Contains structured, bulleted summaries for deep conceptual reading.
* **Automated Chunking:** Handles large PDF files effortlessly by chunking text (1500 words) and synthesizing the pieces incrementally.
* **Streamlit Interface:** A clean, user-friendly GUI to upload PDFs and track the multi-stage analysis progress in real-time.

## 📂 Project Structure & Modelfiles

The system employs a multi-agent approach where different instances of the model handle specific extraction tasks:
* `information_solver.py`: The core Streamlit application and pipeline orchestrator.
* `ModelFile_infosolver`: Synthesizes multiple text chunks into a highly coherent English summary.
* `ModelFile_complex`: Understands core concepts and synthesizes deep, bulleted conclusions.
* `ModelFile_json` & `ModelFile`: Strictly outputs machine-readable JSON formats (`name`, `essence`, `keywords`) without conversational filler.

## 🛠️ Prerequisites

* Python 3.8+
* [Ollama](https://ollama.ai/) installed on your local machine.
* `qwen3:4b` model pulled via Ollama (`ollama pull qwen3:4b`).
