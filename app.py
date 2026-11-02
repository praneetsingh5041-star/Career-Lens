import streamlit as st
import pandas as pd
import plotly.express as px
from analyzer import analyze_resume, extract_text_from_pdf, extract_text_from_docx, demo_resume, demo_job
from storage import init_db, save_analysis, get_history, delete_history, export_history_csv

st.set_page_config(page_title="CareerLens | Resume Intelligence", page_icon="🎯", layout="wide")
init_db()

# ---------- Style ----------
st.markdown("""
<style>
:root { --ink:#172554; --muted:#64748b; --line:#e5eaf3; }
.block-container {padding-top:1.3rem; max-width:1380px;}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#f5f7ff,#eef2ff);}
.hero {background:linear-gradient(115deg,#172554,#4338ca 65%,#7c3aed); color:white;
       padding:2rem 2.2rem; border-radius:22px; margin-bottom:1.25rem;}
.hero h1 {font-size:2.15rem; margin:0; color:white;}
.hero p {opacity:.9; margin:.55rem 0 0 0; font-size:1.05rem;}
.metric-card {background:white;border:1px solid #e6eaf2;border-radius:16px;padding:1rem 1.15rem;
              box-shadow:0 4px 14px rgba(15,23,42,.035);}
.metric-label {color:#64748b;font-size:.82rem;font-weight:600;}
.metric-value {color:#172554;font-size:1.75rem;font-weight:800;margin-top:.25rem;}
.section-title {color:#172554;font-weight:800;font-size:1.15rem;margin:.4rem 0 .8rem;}
.small-note {color:#64748b;font-size:.85rem;}
</style>
""", unsafe_allow_html=True)

def metric(label, value, hint=""):
    st.markdown(f"""<div class="metric-card"><div class="metric-label">{label}</div>
    <div class="metric-value">{value}</div><div class="small-note">{hint}</div></div>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎯 CareerLens")
    st.caption("Resume intelligence & career matching")
    page = st.radio("Navigate", ["Overview", "Analyze Resume", "Analysis History", "About Project"])
    st.divider()
    st.markdown("**Quick tips**")
    st.caption("• Use a text-based PDF or DOCX resume")
    st.caption("• Paste a job description for meaningful matching")
    st.caption("• Demo mode works without uploading a file")
    st.divider()
    st.caption("Python • Streamlit • NLP • SQLite")

if page == "Overview":
    st.markdown("""<div class="hero"><h1>CareerLens</h1>
    <p>Turn your resume into a clearer career direction. Analyze skills, compare a job description,
    and discover practical next steps.</p></div>""", unsafe_allow_html=True)
    hist = get_history()
    total = len(hist)
    avg = round(pd.to_numeric(hist["match_score"], errors="coerce").mean(),1) if total else 0
    c1,c2,c3 = st.columns(3)
    with c1: metric("Saved analyses", total, "Your locally stored analysis history")
    with c2: metric("Average match score", f"{avg}%", "Across saved analyses")
    with c3: metric("Analysis engine", "NLP", "Keyword & skill taxonomy matching")
    st.markdown('<div class="section-title">How it works</div>', unsafe_allow_html=True)
    a,b,c = st.columns(3)
    with a:
        st.markdown("### ① Upload")
        st.write("Provide a PDF/DOCX resume or paste resume text.")
    with b:
        st.markdown("### ② Compare")
        st.write("Compare detected skills with a job description.")
    with c:
        st.markdown("### ③ Improve")
        st.write("Review the score, missing skills, and tailored suggestions.")
    st.info("This project uses transparent rule-based NLP/keyword matching. It does not make hiring decisions or guarantee job outcomes.")
    if st.button("Try a sample analysis", type="primary"):
        st.session_state["load_demo"] = True
        st.session_state["page_from_demo"] = True
        st.rerun()

elif page == "Analyze Resume":
    st.markdown("""<div class="hero"><h1>Resume Analyzer</h1>
    <p>Upload a resume and compare it with a target role.</p></div>""", unsafe_allow_html=True)
    mode = st.radio("Input method", ["Upload resume", "Paste resume text", "Try demo"], horizontal=True)
    resume_text = ""
    if mode == "Upload resume":
        uploaded = st.file_uploader("Upload PDF or DOCX", type=["pdf","docx"])
        if uploaded:
            try:
                resume_text = extract_text_from_pdf(uploaded) if uploaded.name.lower().endswith(".pdf") else extract_text_from_docx(uploaded)
                st.success(f"Read {len(resume_text.split())} words from {uploaded.name}")
            except Exception as e:
                st.error(f"Could not read the file: {e}")
    elif mode == "Paste resume text":
        resume_text = st.text_area("Resume text", height=220, placeholder="Paste your resume content here...")
    else:
        resume_text = demo_resume()
        st.success("Demo resume loaded. You can edit it below.")
        resume_text = st.text_area("Demo resume text", value=resume_text, height=220)

    if mode != "Paste resume text" and mode != "Try demo":
        if resume_text:
            with st.expander("Preview extracted text"):
                st.text(resume_text[:2500])

    job_description = st.text_area("Target job description", value=demo_job() if mode=="Try demo" else "",
                                  height=190, placeholder="Paste the job description you want to compare against...")
    candidate_label = st.text_input("Analysis label (optional)", placeholder="e.g., Data Analyst Internship")
    analyze = st.button("Analyze resume", type="primary", use_container_width=True)

    if analyze:
        if len(resume_text.strip()) < 30:
            st.error("Please provide a resume with at least 30 characters.")
        elif len(job_description.strip()) < 30:
            st.error("Please paste a job description with at least 30 characters.")
        else:
            result = analyze_resume(resume_text, job_description)
            saved_id = save_analysis(candidate_label or "Resume analysis", result)
            st.session_state["last_result"] = result
            st.session_state["last_id"] = saved_id

    result = st.session_state.get("last_result")
    if result:
        st.divider()
        st.markdown('<div class="section-title">Analysis results</div>', unsafe_allow_html=True)
        x1,x2,x3,x4 = st.columns(4)
        with x1: metric("Match score", f'{result["match_score"]}%', "Skill overlap with job description")
        with x2: metric("Skills found", len(result["resume_skills"]), "Recognized in resume")
        with x3: metric("Skills matched", len(result["matched_skills"]), "Also required by job")
        with x4: metric("Skills to develop", len(result["missing_skills"]), "Found in job description only")
        g1,g2 = st.columns([1,1])
        with g1:
            st.markdown("### Skill coverage")
            chart = pd.DataFrame({"Category":["Matched","Missing"],"Count":[len(result["matched_skills"]),len(result["missing_skills"])]})
            st.plotly_chart(px.pie(chart, names="Category", values="Count", hole=.55,
                                   color_discrete_sequence=["#4f46e5","#c4b5fd"]), use_container_width=True)
        with g2:
            st.markdown("### Skills found in resume")
            if result["resume_skills"]:
                st.write(", ".join(result["resume_skills"]))
            else:
                st.warning("No skills from the built-in skill list were detected.")
            st.markdown("### Matching skills")
            st.success(", ".join(result["matched_skills"]) if result["matched_skills"] else "No matching skills detected yet.")
        st.markdown("### Skills to develop")
        if result["missing_skills"]:
            st.write(", ".join(result["missing_skills"]))
        else:
            st.success("All detected job skills also appear in the resume.")
        st.markdown("### Improvement suggestions")
        for item in result["suggestions"]:
            st.markdown(f"- {item}")
        st.markdown("### Career role suggestions")
        st.write(", ".join(result["career_recommendations"]) or "Add more skills to receive role suggestions.")
        report = pd.DataFrame([{
            "match_score":result["match_score"],
            "resume_skills":", ".join(result["resume_skills"]),
            "matched_skills":", ".join(result["matched_skills"]),
            "missing_skills":", ".join(result["missing_skills"]),
            "suggestions":" | ".join(result["suggestions"])
        }])
        st.download_button("Download analysis as CSV", report.to_csv(index=False).encode("utf-8"),
                         "careerlens_analysis.csv", "text/csv")

elif page == "Analysis History":
    st.markdown("""<div class="hero"><h1>Analysis History</h1>
    <p>Review your previous local analyses.</p></div>""", unsafe_allow_html=True)
    hist = get_history()
    if hist.empty:
        st.info("No analyses saved yet. Go to Analyze Resume to create one.")
    else:
        st.dataframe(hist, use_container_width=True, hide_index=True)
        st.download_button("Export history CSV", export_history_csv(), "careerlens_history.csv", "text/csv")
        selected = st.selectbox("Select an analysis ID to delete", hist["id"].tolist())
        if st.button("Delete selected analysis"):
            delete_history(int(selected))
            st.success("Analysis deleted.")
            st.rerun()

elif page == "About Project":
    st.markdown("""<div class="hero"><h1>About CareerLens</h1>
    <p>A student-built resume analysis and career matching web application.</p></div>""", unsafe_allow_html=True)
    st.markdown("### Technology stack")
    st.markdown("""
    - **Python** — core programming language
    - **Streamlit** — web interface and interactive dashboard
    - **pandas** — tabular data handling
    - **Plotly** — charts and visual analytics
    - **SQLite** — local analysis history
    - **PyMuPDF / python-docx** — PDF and DOCX text extraction
    """)
    st.markdown("### Scope and limitations")
    st.write("The system detects skills using a curated dictionary and computes a transparent overlap score. It is a learning and career-planning aid, not an ATS certification, hiring recommendation, or substitute for a recruiter.")
    st.markdown("### Privacy")
    st.write("Uploaded resume text is processed locally by the application. Analysis history is stored in a local SQLite database. Do not upload sensitive personal information to a public deployment.")
