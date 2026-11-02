# Deployment & submission guide

## Option A — Run on your laptop
Follow the local setup in README.md. The application URL is usually `http://localhost:8501`.

## Option B — Publish a live web app
Streamlit Community Cloud can host this app from a GitHub repository:
1. Sign in to GitHub and create a repository.
2. Add the files in this folder to the repository.
3. Keep `requirements.txt` and `app.py` at the repository root.
4. Sign in at https://share.streamlit.io/ using GitHub.
5. Create app → select repository and branch → set main file to `app.py`.
6. Deploy. After the build completes, copy the generated public URL.

## Before public deployment
- Remove real personal resumes, private datasets, and local SQLite database files.
- Explain that uploads are processed by the running app and that demo hosting may be public.
- Never upload your `.venv` directory.
- The project currently stores analysis history in local SQLite. On hosted deployments, ephemeral storage may reset and is not intended as durable multi-user storage.

## Share your project ZIP on Google Drive
1. Open https://drive.google.com/
2. New → File upload → select `CareerLens_Dashboard.zip`.
3. Right-click the uploaded file → Share.
4. General access → Anyone with the link → Viewer.
5. Copy the link and submit it to your faculty.

## Suggested submission details
Project: CareerLens — AI Resume Analyzer & Career Matcher
Language: Python
Framework: Streamlit
Storage: SQLite
Libraries: pandas, Plotly, PyMuPDF, python-docx
