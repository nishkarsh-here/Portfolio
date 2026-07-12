# JioPulse — Intelligent AI Attendance (redesign)

A premium, dark-themed Streamlit redesign of JioPulse: face + voice check-in, role-based dashboards, an **Ask JioPulse AI** assistant, and a **guided onboarding tour**. It runs on realistic sample data out of the box and is structured so you can drop in your real dlib + RAG + database backend.

![theme: phosphor teal on void black](https://img.shields.io/badge/theme-phosphor%20teal%20on%20void-5EEAD4)

## Features

- **Guided tour** — a multi-step walkthrough that auto-opens for first-time users (re-openable from the sidebar).
- **Teacher view** — KPIs (present today, rate, at-risk, avg confidence), attendance trend, per-class breakdown, today's check-ins with confidence bars, at-risk alerts, searchable student table, CSV export.
- **Student view** — attendance %, current streak, badges, personal history chart, progress-to-goal, and a **face/voice check-in** demo.
- **Ask JioPulse AI** — chat that answers natural-language questions (*who's absent today?*, *who is at risk?*, *attendance by class?*) directly from the data. Local engine by default; OpenAI-ready.

## Run locally

```bash
cd JioPulse
python3 -m venv .venv && source .venv/bin/activate      # optional
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501.

## Structure

```
JioPulse/
├── app.py            # UI, layout, tour, role views
├── data.py           # sample data + metrics  ← swap for your DB
├── assistant.py      # NL query engine        ← swap for your RAG / add OpenAI key
├── theme.py          # dark theme CSS + Plotly styling
├── requirements.txt
└── .streamlit/config.toml   # base dark theme
```

## Wire in your real backend

- **Attendance data:** replace `data.get_data()` with a query to your database (Supabase/Postgres). Keep the same columns (`date, student_id, name, klass, status, method, check_in, confidence`) and every dashboard keeps working.
- **Face / voice recognition:** in `app.py → check_in()`, replace the camera/voice demo with your dlib pipeline; write the result to your DB.
- **Real AI assistant:** add your key to `.streamlit/secrets.toml` and the assistant automatically uses OpenAI instead of the local engine:
  ```toml
  # .streamlit/secrets.toml
  OPENAI_API_KEY = "sk-..."
  ```
  For full agentic RAG, extend `assistant.answer()`.

## Deploy to Streamlit Community Cloud (free)

1. Push this folder to a GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → pick the repo, branch, and `app.py`.
3. Add your `OPENAI_API_KEY` under **Advanced settings → Secrets** (optional).
4. Deploy — you get a public `*.streamlit.app` URL.

## Notes

- The theme matches the portfolio: phosphor teal (`#5EEAD4`) on void black, Space Grotesk + Inter + JetBrains Mono.
- Sample data is deterministic (seeded), so the numbers are stable between runs.
