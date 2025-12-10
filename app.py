import streamlit as st
import pdfplumber
import google.generativeai as genai
import json
import re
import os
import pandas as pd


st.set_page_config(page_title="AI Legal Auditor", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
    div.stButton > button:first-child { background-color: #004d99; color: white; }
    .legal-clause { background-color: #f9f9f9; padding: 15px; border-left: 5px solid #004d99; margin-bottom: 10px; border-radius: 5px; }
    .risk-box { padding: 10px; border-radius: 5px; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)


def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        return None
    return text

def run_rule_engine(text):
    flags = []
    text_lower = text.lower()
    
    # Rule 1: Possession Date
    date_pattern = r"\d{1,2}[-/thstndrd]+\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{2,4}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}"
    if len(re.findall(date_pattern, text, re.IGNORECASE)) < 1:
        flags.append({"risk": "Possession Date Missing", "severity": "HIGH", "advice": "Ensure a specific date (e.g., 12-Dec-2025) is written."})

    # Rule 2: Indemnity
    if "indemni" not in text_lower:
        flags.append({"risk": "Missing Indemnity Clause", "severity": "HIGH", "advice": "Seller must explicitly indemnify buyer against title defects."})

    # Rule 3: Dispute Resolution
    if "arbitration" not in text_lower and "court" not in text_lower:
        flags.append({"risk": "No Dispute Resolution", "severity": "MEDIUM", "advice": "Add an Arbitration clause to avoid lengthy court battles."})

    return flags

def run_gemini_analysis(text, rule_flags, api_key):
    system_prompt = f"""
    You are an AI Legal Auditor for Indian Property Transactions.
    
    INPUT:
    1. AUTOMATED RULE FLAGS: {json.dumps(rule_flags)}
    2. DOCUMENT TEXT: (Below)
    
    TASK:
    1. Summarize the deal.
    2. Explain every clause in simple English.
    3. Analyze Risks (verify the Rule Flags).
    
    OUTPUT JSON:
    {{
      "executive_summary": {{
        "parties": "Seller: [Name] | Buyer: [Name]",
        "property_details": "[Address, Survey No]",
        "financial_terms": "[Price & Payment Mode]"
      }},
      "section_analysis": [
        {{
          "section_title": "e.g. Indemnity Clause",
          "legal_summary": "Technical summary...",
          "simple_explanation": "Simple one-sentence explanation for a layman."
        }}
      ],
      "risk_report": [
        {{ "issue": "...", "severity": "High/Medium/Low", "advice": "..." }}
      ],
      "final_verdict": "NORMAL / SUSPICIOUS / FRAUD-LIKE"
    }}
    """
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest', system_instruction=system_prompt)
        response = model.generate_content(
            text,
            generation_config=genai.types.GenerationConfig(temperature=0.2, response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620542.png", width=50)
    st.title("AI Legal Auditor")
    
    api_key = st.text_input("Gemini API Key", type="password")
    st.caption("Get key: aistudio.google.com")
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Sale Deed (PDF)", type=['pdf'])

if uploaded_file and api_key:
    with st.spinner("🔍 Reading Document & Running Rules..."):
        text = extract_text_from_pdf(uploaded_file)
        
    if text:
        with st.spinner("🧠 performing Deep Legal Analysis..."):
            rule_flags = run_rule_engine(text)
            report = run_gemini_analysis(text, rule_flags, api_key)
        
        if "error" in report:
            st.error(f"Analysis Failed: {report['error']}")
        else:
            st.title("📄 Audit Report")
            
            col1, col2, col3 = st.columns(3)
            verdict = report.get("final_verdict", "UNKNOWN")
            
            v_color = "red" if "FRAUD" in verdict else "orange" if "SUSPICIOUS" in verdict else "green"
            
            col1.markdown(f"### Verdict: :{v_color}[{verdict}]")
            col2.metric("Risks Found", len(report.get("risk_report", [])))
            col3.metric("Rule Flags", len(rule_flags))
            
            st.markdown("---")
            
            tab1, tab2, tab3 = st.tabs(["📊 Summary", "⚠️ Risks", "📖 Clause Explainer"])
            
            with tab1:
                summ = report.get("executive_summary", {})
                st.info(f"**👤 Parties:** {summ.get('parties', 'N/A')}")
                st.write(f"**🏠 Property:** {summ.get('property_details', 'N/A')}")
                st.write(f"**💰 Financials:** {summ.get('financial_terms', 'N/A')}")
                
            with tab2:
                if not report.get("risk_report"):
                    st.success("✅ No high-priority risks detected.")
                for risk in report.get("risk_report", []):
                    sev = risk.get('severity', 'Low')
                    icon = "🔴" if sev == "High" else "🟠" if sev == "Medium" else "🟢"
                    with st.expander(f"{icon} {sev}: {risk.get('issue')}"):
                        st.write(f"**Advice:** {risk.get('advice')}")
                        
            with tab3:
                for sec in report.get("section_analysis", []):
                    st.markdown(
                        f"""
                        <div class="legal-clause">
                            <b>🔹 {sec['section_title']}</b><br>
                            <small style="color:#555">⚖️ {sec['legal_summary']}</small><br><br>
                            <span style="color:#004d99">💡 <b>Simple English:</b> {sec['simple_explanation']}</span>
                        </div>
                        """, unsafe_allow_html=True
                    )

elif not api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar.")
elif not uploaded_file:
    st.info("👈 Please upload a PDF to start.")