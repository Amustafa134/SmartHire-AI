# 🚀 SmartHire AI – HR Automation System

SmartHire AI is an AI-powered hiring automation platform that handles the entire recruitment pipeline:

- Parse CVs (PDF/DOCX → JSON)

- Match candidates to job descriptions

- Generate adaptive interview questions

- Score candidate answers with AI

- Rank candidates automatically

This project is built using FastAPI, OpenAI embeddings, and a modular architecture designed for future scaling.

# 📌 Features

## ✅ 1. CV Parsing

Extracts:

- Skills

- Experience

- Education

- Contact info

- Summary

Output: Structured JSON

## ✅ 2. Job Matching

 Uses OpenAI text-embedding-3-large to calculate similarity between:

- Candidate CV

- Job Description

Ranking is based on cosine similarity.

## ✅ 3. Adaptive Interview System

- Begins with easy questions

- Moves to harder levels if the candidate answers correctly

- Uses LLMs to generate role-specific questions

## ✅ 4. AI-Based Answer Scoring

Scores candidate answers based on:

- Technical accuracy

- Clarity

- Relevance

- Depth of knowledge

Returns a score from 0–10.


# 🧑‍💻 Setup & Installation

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)

2) Clone Repository
```bash 
$ git clone https://github.com/YOUR_USERNAME/smarthire-ai.git
cd smarthire-ai
```
3) Activate the environment:
```bash
$ conda activate smarthire-ai
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Install the required packages
```bash
$ pip install -r requirements.txt
```