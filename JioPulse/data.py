"""Sample data + metrics for the JioPulse demo.

Swap get_data() for your real face-recognition + database backend later —
the rest of the app only depends on these DataFrames and helper functions.
"""
from __future__ import annotations
import datetime as dt
import numpy as np
import pandas as pd
import streamlit as st

_FIRST = ["Aarav","Vivaan","Aditya","Vihaan","Arjun","Sai","Reyansh","Ishaan","Kabir","Krishna",
          "Ananya","Diya","Aadhya","Saanvi","Myra","Aarohi","Anika","Navya","Riya","Prisha",
          "Rohan","Dev","Yuvraj","Aryan","Ira","Kiara","Zara","Meera","Tara","Neel",
          "Ved","Ojas","Parth","Rudra","Ishita","Nitya","Pari","Sara","Kyra","Advait","Reeva","Aman"]
_CLASSES = ["CSE-A","CSE-B","AI-DS","ECE"]
_AVATARS = ["🧑‍🎓","👩‍🎓","🧑‍💻","👨‍🎓","👩‍💻"]


@st.cache_data(show_spinner=False)
def get_data(seed: int = 7, n_students: int = 42, days: int = 45):
    rng = np.random.default_rng(seed)
    names, used = [], set()
    for i in range(n_students):
        base = _FIRST[i % len(_FIRST)]
        nm = base if base not in used else f"{base} {chr(65 + i // len(_FIRST))}"
        used.add(nm); names.append(nm)
    students = pd.DataFrame({
        "student_id": [f"JIO{100 + i}" for i in range(n_students)],
        "name": names,
        "klass": [_CLASSES[i % len(_CLASSES)] for i in range(n_students)],
        "avatar": [_AVATARS[i % len(_AVATARS)] for i in range(n_students)],
    })
    reliability = rng.uniform(0.60, 0.99, n_students)
    today = dt.date.today()
    dates = [today - dt.timedelta(days=d) for d in range(days)][::-1]
    rows = []
    for day in dates:
        if day.weekday() >= 5:   # skip weekends
            continue
        for si in range(n_students):
            if rng.random() < reliability[si]:
                late = rng.random() < 0.12
                status = "Late" if late else "Present"
                hh = 9 + (1 if late else 0)
                mm = int(rng.integers(0, 55))
                check = f"{hh:02d}:{mm:02d}"
                method = "Face" if rng.random() < 0.8 else "Voice"
                conf = float(np.clip(rng.normal(0.985 if method == "Face" else 0.94, 0.02), 0.80, 0.999))
            else:
                status, check, method, conf = "Absent", None, None, np.nan
            rows.append((day, students.student_id[si], students.name[si], students.klass[si],
                         status, method, check, conf))
    att = pd.DataFrame(rows, columns=["date", "student_id", "name", "klass",
                                      "status", "method", "check_in", "confidence"])
    att["date"] = pd.to_datetime(att["date"])
    return students, att


def _present(a):
    return a["status"].isin(["Present", "Late"]).astype(int)


def student_summary(att):
    a = att.copy(); a["p"] = _present(a)
    g = a.groupby(["student_id", "name", "klass"], as_index=False).agg(
        present=("p", "sum"), total=("p", "count"))
    g["rate"] = (g["present"] / g["total"] * 100).round(1)
    streaks = {}
    for sid, d in a.sort_values("date").groupby("student_id"):
        s = 0
        for v in reversed(d["p"].tolist()):
            if v:
                s += 1
            else:
                break
        streaks[sid] = s
    g["streak"] = g["student_id"].map(streaks)
    g["status"] = np.where(g["rate"] >= 90, "Excellent",
                           np.where(g["rate"] >= 75, "On track", "At risk"))
    return g.sort_values("rate", ascending=False).reset_index(drop=True)


def daily_series(att):
    a = att.copy(); a["p"] = _present(a)
    d = a.groupby("date", as_index=False).agg(present=("p", "sum"), total=("p", "count"))
    d["rate"] = (d["present"] / d["total"] * 100).round(1)
    return d


def class_summary(att):
    a = att.copy(); a["p"] = _present(a)
    cs = a.groupby("klass", as_index=False).agg(rate=("p", "mean"))
    cs["rate"] = (cs["rate"] * 100).round(1)
    return cs


def today_stats(att):
    day = att["date"].max()
    t = att[att["date"] == day]
    present = int(_present(t).sum()); total = int(len(t))
    rate = round(present / total * 100, 1) if total else 0.0
    conf = round(t["confidence"].dropna().mean() * 100, 1) if t["confidence"].notna().any() else 0.0
    return {"present": present, "total": total, "rate": rate, "conf": conf}
