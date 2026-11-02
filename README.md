# CareerLens — AI Resume Analyzer & Career Matcher

A Python web application that compares a resume with a target job description, detects skills, computes a transparent skill-overlap score, identifies missing skills, and suggests career roles and improvement steps.

## Features
- Upload text-based PDF or DOCX resume, paste text, or load demo data
- Detect skills using a curated skill dictionary and aliases
- Calculate match score from skills detected in the job description
- Show matching and missing skills
- Suggest resume improvement actions and potential roles
- Save analysis history locally using SQLite
- Interactive dashboard and CSV exports

## Tech stack
Python, Streamlit, pandas, Plotly, SQLite, PyMuPDF, python-docx.

## Run locally (Windows)
1. Install Python 3.10+ from https://www.python.org/downloads/
2. Extract the ZIP and open this folder in VS Code.
3. Open terminal in the project folder.
4. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```
5. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, run:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```
6. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
7. Launch:
   ```powershell
   streamlit run app.py
   ```
8. Streamlit will open the app in your browser. If not, visit http://localhost:8501.

## Deploy a public demo with Streamlit Community Cloud
1. Create a GitHub account and a new **public** repository.
2. Upload the project files to the repository (do not upload `.venv`, `careerlens.db`, or personal resumes).
3. Visit https://share.streamlit.io/ and sign in with GitHub.
4. Select **Create app**, choose your repository, branch, and `app.py` as the main file.
5. Click **Deploy** and wait for the build to finish.
6. Copy the app URL shown by Streamlit and share it with your instructor.

## Upload ZIP/report to Google Drive
1. Open https://drive.google.com/
2. Click **New → File upload** and upload `CareerLens_Dashboard.zip`.
3. Right-click the uploaded file → **Share**.
4. Under **General access**, choose **Anyone with the link** (if permitted by your account).
5. Set role to **Viewer** and click **Copy link**.

## Project structure
```
CareerLens_Dashboard/
├── app.py
├── analyzer.py
├── storage.py
├── requirements.txt
├── README.md
├── DEPLOYMENT_GUIDE.md
├── PROJECT_REPORT.docx
└── data/
    └── sample_job_description.txt
```

## Scoring method
`match_score = matched skills / skills detected in job description × 100`.
If the job description contains no recognized skills, score is 0. The score is an illustrative skill overlap metric, not a hiring prediction or a professional ATS score.

## Limitations
- Skill detection uses a built-in dictionary and phrase matching, not a trained language model.
- Text extraction can fail on scanned/image-only PDFs; OCR is not included.
- Skill context, proficiency, experience, and synonyms outside the dictionary may be missed.
- The result is for educational career planning only, not a hiring decision.
- Do not upload sensitive resumes to public deployments. Demo deployment is public unless access is configured.

## Troubleshooting
- `streamlit is not recognized`: activate the virtual environment and run `pip install -r requirements.txt`.
- PDF extraction returns no text: use a text-based PDF or paste the resume text.
- Module not found: confirm terminal is opened in this folder and dependencies installed.
