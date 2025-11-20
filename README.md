# 🚀 SmartHire AI – HR Automation System

SmartHire AI is an AI-powered hiring automation platform that handles the entire recruitment pipeline:

- Parse CVs (PDF/DOCX → JSON)

- Match candidates to job descriptions

- Generate adaptive interview questions

- Score candidate answers with AI

- Rank candidates automatically

This project is built using FastAPI, OpenAI embeddings, and a modular architecture designed for future scaling.

# 📌 Features

✅ 1. CV Parsing

Extracts:

- Skills

- Experience

- Education

- Contact info

- Summary

Output: Structured JSON

✅ 2. Job Matching

 Uses OpenAI text-embedding-3-large to calculate similarity between:

- Candidate CV

- Job Description

Ranking is based on cosine similarity.