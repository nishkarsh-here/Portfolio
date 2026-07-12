"""Premium dark theme (CSS injection) + Plotly styling for JioPulse."""
import streamlit as st

ACCENT = "#5EEAD4"
INK = "#F4F6FB"
DIM = "#AAB2C0"
BG = "#05060A"
CARD = "#0C0F16"
LINE = "rgba(244,246,251,.10)"


def inject():
    st.markdown(
        f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, p, span, div {{ font-family:'Inter',sans-serif; }}
h1,h2,h3,h4 {{ font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.02em; }}
.stApp {{ background: radial-gradient(1100px 560px at 82% -12%, rgba(94,234,212,.07), transparent 60%), {BG}; }}
#MainMenu, footer {{ visibility:hidden; }}
[data-testid="stToolbar"] {{ right:12px; }}
section[data-testid="stSidebar"] {{ background:{CARD}; border-right:1px solid {LINE}; }}
section[data-testid="stSidebar"] .stButton>button {{ width:100%; }}

/* KPI cards */
.kpi {{ background:linear-gradient(160deg, rgba(94,234,212,.06), {CARD}); border:1px solid {LINE};
  border-radius:16px; padding:16px 18px; height:100%; }}
.kpi .l {{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:.14em;
  text-transform:uppercase; color:{DIM}; }}
.kpi .v {{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:30px; color:{INK};
  line-height:1.1; margin-top:4px; }}
.kpi .d {{ font-size:12.5px; color:{DIM}; margin-top:4px; }}
.accent {{ color:{ACCENT}; }}
.pill {{ display:inline-block; font-family:'JetBrains Mono',monospace; font-size:11px;
  padding:5px 11px; border:1px solid {LINE}; border-radius:100px; color:{DIM}; margin:2px 2px 2px 0; }}
.brandwrap {{ display:flex; align-items:center; gap:10px; }}
.dot {{ width:9px; height:9px; border-radius:50%; background:{ACCENT}; box-shadow:0 0 14px {ACCENT}; }}

.stButton>button {{ border-radius:10px; border:1px solid {LINE}; transition:.2s; }}
.stButton>button:hover {{ border-color:{ACCENT}; color:{ACCENT}; }}
.stTabs [data-baseweb="tab-list"] {{ gap:4px; }}
.stTabs [data-baseweb="tab"] {{ border-radius:10px 10px 0 0; }}
[data-testid="stMetricValue"] {{ font-family:'Space Grotesk',sans-serif; }}
a {{ color:{ACCENT}; }}
</style>""",
        unsafe_allow_html=True,
    )


def kpi(label, value, delta=""):
    st.markdown(
        f"<div class='kpi'><div class='l'>{label}</div><div class='v'>{value}</div>"
        f"<div class='d'>{delta}</div></div>",
        unsafe_allow_html=True,
    )


_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=DIM, family="Inter"),
    margin=dict(l=8, r=8, t=24, b=8),
    xaxis=dict(gridcolor="rgba(244,246,251,.06)", zeroline=False),
    yaxis=dict(gridcolor="rgba(244,246,251,.06)", zeroline=False),
    colorway=["#5EEAD4", "#7DD3FC", "#C084FC", "#FDBA74", "#FB7185"],
    height=300,
)


def style_fig(fig, height=300):
    lay = dict(_LAYOUT); lay["height"] = height
    fig.update_layout(**lay)
    return fig
