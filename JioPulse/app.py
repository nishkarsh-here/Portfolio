"""JioPulse — Intelligent AI Attendance (redesign).

Run:  streamlit run app.py
Demo on sample data; swap data.py / assistant.py for your real
face-recognition + RAG + database backend.
"""
import time
import plotly.express as px
import streamlit as st

import data as D
import theme as T
import assistant as A

st.set_page_config(page_title="JioPulse — Intelligent Attendance",
                   page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
T.inject()

students, att = D.get_data()
summ = D.student_summary(att)
TODAY = att["date"].max()

ss = st.session_state
ss.setdefault("role", "Teacher")
ss.setdefault("student_id", students["student_id"].iloc[0])
ss.setdefault("tour_open", False)
ss.setdefault("tour_step", 0)
ss.setdefault("first_seen", True)
ss.setdefault("chat", [])

# ----------------------------------------------------------------- TOUR
TOUR = [
    ("Welcome to JioPulse 👋",
     "JioPulse is an AI attendance system — students check in by **face or voice**, and you can "
     "ask questions about the data in plain English. This 30-second tour shows you around."),
    ("Switch roles anytime",
     "Use the **sidebar** to flip between the **Teacher** and **Student** views. Teachers get analytics "
     "and alerts; students get streaks, badges and one-tap check-in."),
    ("The live overview",
     "The **Overview** tab shows today's attendance, the trend over time, a per-class breakdown and "
     "at-risk alerts — all computed live from the data."),
    ("Check in by face or voice",
     "In the **Check In** tab a student is recognised by face (or voice) with a confidence score and "
     "marked present instantly. Your real dlib pipeline plugs in right here."),
    ("Ask JioPulse AI",
     "The **Ask AI** tab answers natural-language questions like *who's absent today?* or *who is at "
     "risk?* straight from the attendance data."),
    ("You're all set ✦",
     "That's the tour. Explore freely — and try the **Student → Check In** tab to see recognition in action."),
]


@st.dialog("JioPulse · guided tour")
def tour_dialog():
    i = ss.tour_step
    title, body = TOUR[i]
    st.markdown(f"<span class='pill'>Step {i + 1} / {len(TOUR)}</span>", unsafe_allow_html=True)
    st.subheader(title)
    st.write(body)
    st.progress((i + 1) / len(TOUR))
    c1, c2, c3 = st.columns(3)
    if c1.button("‹ Back", disabled=(i == 0), use_container_width=True):
        ss.tour_step = max(0, i - 1); st.rerun()
    if c2.button("Skip", use_container_width=True):
        ss.tour_open = False; ss.tour_step = 0; st.rerun()
    if i < len(TOUR) - 1:
        if c3.button("Next ›", type="primary", use_container_width=True):
            ss.tour_step = i + 1; st.rerun()
    elif c3.button("Finish ✦", type="primary", use_container_width=True):
        ss.tour_open = False; ss.tour_step = 0; st.rerun()


if ss.first_seen:
    ss.first_seen = False
    ss.tour_open = True
if ss.tour_open:
    tour_dialog()

# ----------------------------------------------------------------- SIDEBAR
with st.sidebar:
    st.markdown(
        "<div class='brandwrap'><span class='dot'></span>"
        "<b style='font-family:Space Grotesk;font-size:19px'>JioPulse</b></div>",
        unsafe_allow_html=True)
    st.caption("Intelligent attendance · face + voice")
    st.divider()
    ss.role = st.radio("View as", ["Teacher", "Student"], horizontal=True)
    if ss.role == "Student":
        sel = st.selectbox("Student", students["name"].tolist(), index=0)
        ss.student_id = students.loc[students.name == sel, "student_id"].iloc[0]
    st.divider()
    if st.button("▶  Take the tour", use_container_width=True):
        ss.tour_open = True; ss.tour_step = 0; st.rerun()
    st.divider()
    a = att.copy(); a["p"] = a.status.isin(["Present", "Late"]).astype(int)
    st.markdown(
        f"<span class='pill'>{students.shape[0]} students</span>"
        f"<span class='pill'>{att['date'].nunique()} days</span>"
        f"<span class='pill'>{round(a['p'].mean() * 100, 1)}% overall</span>",
        unsafe_allow_html=True)

# ----------------------------------------------------------------- HEADER
st.markdown(
    "<h1 style='margin-bottom:0'>Jio<span class='accent'>Pulse</span></h1>"
    "<p style='color:#AAB2C0;margin-top:2px;font-size:16px'>Attendance that recognises you — by face "
    "and by voice — then answers questions about itself.</p>",
    unsafe_allow_html=True)
st.write("")


def trend_fig():
    d = D.daily_series(att)
    fig = px.area(d, x="date", y="rate", markers=False)
    fig.update_traces(line_color=T.ACCENT, fillcolor="rgba(94,234,212,.12)")
    fig.update_yaxes(range=[0, 100], title=""); fig.update_xaxes(title="")
    return T.style_fig(fig)


def class_fig():
    cs = D.class_summary(att)
    fig = px.bar(cs, x="klass", y="rate", text="rate")
    fig.update_traces(marker_color=T.ACCENT, textposition="outside")
    fig.update_yaxes(range=[0, 108], title=""); fig.update_xaxes(title="")
    return T.style_fig(fig)


def ask_ai(scope=""):
    st.markdown("#### Ask JioPulse AI")
    st.caption("Natural-language questions over the attendance data. Try a chip or type your own.")
    chips = ["Who's absent today?", "Overall attendance rate", "Who is at risk?",
             "Top attendance", "Attendance by class"]
    cols = st.columns(len(chips))
    clicked = None
    for i, ch in enumerate(chips):
        if cols[i].button(ch, key=f"chip-{scope}-{i}", use_container_width=True):
            clicked = ch
    for m in ss.chat:
        with st.chat_message(m["role"], avatar="🧑" if m["role"] == "user" else "🤖"):
            st.markdown(m["content"])
            if m.get("table") is not None:
                st.dataframe(m["table"], use_container_width=True, hide_index=True)
    prompt = clicked or st.chat_input("Ask about attendance…")
    if prompt:
        ss.chat.append({"role": "user", "content": prompt})
        text, table = A.answer(prompt, students, att)
        ss.chat.append({"role": "assistant", "content": text, "table": table})
        st.rerun()


# ----------------------------------------------------------------- TEACHER
def teacher_view():
    tabs = st.tabs(["📊  Overview", "👥  Students", "💬  Ask AI"])
    with tabs[0]:
        ts = D.today_stats(att)
        c = st.columns(4)
        with c[0]: T.kpi("Present today", ts["present"], f"of {ts['total']} · {ts['rate']}%")
        with c[1]: T.kpi("Attendance rate", f"{ts['rate']}%", "today")
        with c[2]: T.kpi("At risk", int((summ.rate < 75).sum()), "below 75%")
        with c[3]: T.kpi("Avg confidence", f"{ts['conf']}%", "face + voice")
        st.write("")
        left, right = st.columns([2, 1])
        with left:
            st.markdown("**Attendance trend**")
            st.plotly_chart(trend_fig(), use_container_width=True)
        with right:
            st.markdown("**By class**")
            st.plotly_chart(class_fig(), use_container_width=True)
        ar = summ[summ.rate < 75]
        if len(ar):
            st.warning(f"⚠️  {len(ar)} students below 75% — " + ", ".join(ar["name"].head(6)) +
                       (" …" if len(ar) > 6 else ""))
        st.markdown("**Today's check-ins**")
        tdf = att[att.date == TODAY]
        show = tdf[tdf.status != "Absent"].sort_values("check_in")[
            ["check_in", "name", "klass", "method", "confidence", "status"]]
        st.dataframe(
            show, use_container_width=True, hide_index=True,
            column_config={
                "check_in": "time",
                "confidence": st.column_config.ProgressColumn("confidence", format="%.2f",
                                                              min_value=0.0, max_value=1.0)},
        )
    with tabs[1]:
        q = st.text_input("Search students", placeholder="Type a name…")
        view = summ if not q else summ[summ.name.str.contains(q, case=False, na=False)]
        st.dataframe(
            view[["name", "klass", "rate", "streak", "present", "total", "status"]],
            use_container_width=True, hide_index=True,
            column_config={"rate": st.column_config.ProgressColumn("rate %", format="%.0f",
                                                                   min_value=0, max_value=100)},
        )
        st.download_button("⬇  Export summary (CSV)", summ.to_csv(index=False),
                           "jiopulse_attendance_summary.csv", "text/csv")
    with tabs[2]:
        ask_ai("teacher")


# ----------------------------------------------------------------- STUDENT
def student_view():
    me = students.loc[students.student_id == ss.student_id].iloc[0]
    my = att[att.student_id == ss.student_id]
    r = summ.loc[summ.student_id == ss.student_id].iloc[0]
    tabs = st.tabs(["🎯  My attendance", "📷  Check in", "💬  Ask AI"])
    with tabs[0]:
        st.markdown(f"### {me['avatar']}  {me['name']} &nbsp; <span class='pill'>{me['klass']}</span>",
                    unsafe_allow_html=True)
        c = st.columns(4)
        with c[0]: T.kpi("Attendance", f"{r.rate}%", me["klass"])
        with c[1]: T.kpi("Current streak", f"{int(r.streak)} 🔥", "days in a row")
        with c[2]: T.kpi("Days present", int(r.present), f"of {int(r.total)}")
        with c[3]: T.kpi("Status", r.status, "keep it up")
        st.write("")
        badges = []
        if r.streak >= 5: badges.append("🔥 5-day streak")
        if r.rate >= 90: badges.append("🏆 90%+ club")
        if r.rate >= 95: badges.append("⭐ Near-perfect")
        if int(r.present) >= 20: badges.append("💎 20+ days")
        st.markdown("**Badges**")
        st.markdown(" ".join(f"<span class='pill'>{b}</span>" for b in badges)
                    or "<span class='pill'>Attend to earn your first badge</span>", unsafe_allow_html=True)
        st.write("")
        st.markdown("**My attendance over time**")
        m = my.copy(); m["p"] = m.status.isin(["Present", "Late"]).astype(int)
        fig = px.bar(m, x="date", y="p")
        fig.update_traces(marker_color=[T.ACCENT if v else "rgba(244,246,251,.14)" for v in m["p"]])
        fig.update_yaxes(visible=False, range=[0, 1.1]); fig.update_xaxes(title="")
        st.plotly_chart(T.style_fig(fig, height=180), use_container_width=True)
        goal = 90
        st.markdown(f"**Progress to {goal}% goal**")
        st.progress(min(1.0, r.rate / goal))
    with tabs[1]:
        check_in(me)
    with tabs[2]:
        ask_ai("student")


def check_in(me):
    st.markdown("#### Check in for today")
    st.caption("Face-recognition demo — your real dlib + voice pipeline plugs in here.")
    left, right = st.columns(2)
    with left:
        img = st.camera_input("Look at the camera")
        if img is not None:
            with st.spinner("Recognising face…"):
                time.sleep(1.0)
            st.success(f"✅  Recognised **{me['name']}** · confidence **98%**")
            st.caption("Marked present via Face at " + time.strftime("%H:%M"))
            st.balloons()
    with right:
        st.markdown("Prefer voice?")
        st.caption("Say the passphrase to check in hands-free.")
        if st.button("🎙️  Simulate voice check-in", use_container_width=True):
            with st.spinner("Listening…"):
                time.sleep(1.1)
            st.success(f"✅  Voice matched **{me['name']}** · confidence **94%**")
            st.toast("Marked present 🎉")
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("In production this writes to your database (Supabase) and updates the dashboards live.")


if ss.role == "Teacher":
    teacher_view()
else:
    student_view()

st.divider()
st.caption("JioPulse redesign · demo on sample data · face + voice recognition + agentic RAG, ready to wire in.")
