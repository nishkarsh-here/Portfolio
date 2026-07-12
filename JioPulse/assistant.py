"""Ask JioPulse AI — natural-language answers over the attendance data.

Default: a fast local keyword engine that queries the DataFrame (works offline,
no API key). If st.secrets["OPENAI_API_KEY"] is set, it uses OpenAI instead —
this is where your real agentic RAG assistant plugs in.
"""
import streamlit as st
import data as D


def _local(question, students, att):
    q = (question or "").lower()
    summ = D.student_summary(att)
    day = att["date"].max()
    today = att[att["date"] == day]

    def names_of(series, n=10):
        vals = list(series)
        extra = f" (+{len(vals) - n} more)" if len(vals) > n else ""
        return (", ".join(vals[:n]) + extra) if vals else "nobody"

    if "absent" in q:
        ab = today[today.status == "Absent"]
        return (f"**{len(ab)}** students are absent today: {names_of(ab['name'])}.",
                ab[["name", "klass"]].reset_index(drop=True))
    if ("present" in q or "here" in q or "in class" in q) and ("today" in q or q.strip() in ("present", "who is present")):
        pr = today[today.status.isin(["Present", "Late"])]
        rate = round(len(pr) / len(today) * 100) if len(today) else 0
        return (f"**{len(pr)}** of {len(today)} students are present today (**{rate}%**).", None)
    if "at risk" in q or "at-risk" in q or "risk" in q or "failing" in q:
        ar = summ[summ.rate < 75]
        return (f"**{len(ar)}** students are at risk (below 75% attendance).",
                ar[["name", "klass", "rate", "streak"]].reset_index(drop=True))
    if "rate" in q or "overall" in q or "percentage" in q or "average" in q:
        a = att.copy(); a["p"] = a.status.isin(["Present", "Late"]).astype(int)
        return (f"Overall attendance is **{round(a['p'].mean() * 100, 1)}%** "
                f"across {att['date'].nunique()} school days and {students.shape[0]} students.", None)
    if "top" in q or "best" in q or "highest" in q:
        return ("Here are the top students by attendance:",
                summ.head(6)[["name", "klass", "rate", "streak"]].reset_index(drop=True))
    if "streak" in q:
        return ("Longest current streaks:",
                summ.sort_values("streak", ascending=False).head(6)[["name", "streak", "rate"]].reset_index(drop=True))
    if "class" in q or "section" in q:
        return ("Attendance by class:", D.class_summary(att))
    if "late" in q:
        lt = today[today.status == "Late"]
        return (f"**{len(lt)}** students were late today: {names_of(lt['name'])}.", None)
    for nm in students["name"]:
        if nm.lower() in q:
            row = summ[summ.name == nm]
            if len(row):
                r = row.iloc[0]
                return (f"**{nm}** ({r.klass}) — attendance **{r.rate}%**, current streak "
                        f"**{int(r.streak)}** days, status **{r.status}**.", None)
    return ("I can answer questions like *who's absent today*, *overall attendance rate*, "
            "*who is at risk*, *top attendance*, *longest streaks*, *attendance by class*, "
            "*who was late* — or ask about any student by name.", None)


def answer(question, students, att):
    """Returns (markdown_text, optional_dataframe)."""
    key = None
    try:
        key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        key = None
    if key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=key)
            ctx = D.student_summary(att).to_csv(index=False)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.2,
                messages=[
                    {"role": "system", "content": "You are Ask JioPulse AI. Answer concisely about class "
                     "attendance using ONLY the provided CSV. Use markdown."},
                    {"role": "user", "content": f"Attendance summary CSV:\n{ctx}\n\nQuestion: {question}"},
                ],
            )
            return resp.choices[0].message.content, None
        except Exception:
            pass  # fall back to local engine
    return _local(question, students, att)
