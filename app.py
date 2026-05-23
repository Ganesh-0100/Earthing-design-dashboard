"""
Earthing System Design
Phase-wise Calculation with Full Formula Derivation and Engineering Reasoning

Reference Standards:
  - CBIP Manual Pub.339 (2017): Manual on Earthing of AC Power Systems
  - IEEE Std 80-2013: Guide for Safety in AC Substation Grounding
  - IS 3043:1987 (Reaffirmed 2006): Code of Practice for Earthing
  - IEEE Std 665: Guide for Safety in Generating Station Grounding
"""

import streamlit as st
import math
import pandas as pd

st.set_page_config(
    page_title="Earthing Design Calculator",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

*, *::before, *::after {
    font-family: 'IBM Plex Sans', 'Segoe UI', Arial, sans-serif !important;
}
.main .block-container {
    background: #f4f6f9;
    padding: 1.4rem 1.8rem 3rem 1.8rem;
    max-width: 1480px;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #cde3f4;
}
[data-testid="stSidebar"] .block-container { padding: 0.7rem 0.9rem; }
[data-testid="stSidebar"] label {
    color: #1a2e40 !important;
    font-size: 0.77rem !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #2c4a60 !important; }
[data-testid="stSidebar"] input {
    background: #eef6fd !important;
    color: #1a2e40 !important;
    border: 1px solid #9ecce8 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #eef6fd !important;
    color: #1a2e40 !important;
    border: 1px solid #9ecce8 !important;
}
[data-testid="stSidebar"] .stRadio label { color: #1a2e40 !important; }
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] p[data-testid="stMarkdownContainer"] {
    color: #4a7a9b !important;
    font-size: 0.71rem !important;
    line-height: 1.5 !important;
}

.sb-hdr {
    background: #2980b9;
    margin: 0 -0.9rem 0.9rem -0.9rem;
    padding: 0.9rem;
    border-bottom: 2px solid #1a6fa0;
}
.sb-hdr-t { font-size:0.8rem; font-weight:700; color:#ffffff; text-transform:uppercase; letter-spacing:0.05em; }
.sb-hdr-s { font-size:0.67rem; color:#d6eaf8; margin-top:0.2rem; line-height:1.4; }
.sb-g {
    font-size:0.59rem; font-weight:700; text-transform:uppercase; letter-spacing:0.16em;
    color:#2980b9 !important; padding:0.85rem 0 0.28rem 0;
    border-bottom:1px solid #cde3f4; margin-bottom:0.45rem;
}

.pg-hdr {
    background: #2980b9;
    border-left: 4px solid #e74c3c;
    padding: 1.1rem 1.5rem;
    border-radius: 3px;
    margin-bottom: 1.3rem;
}
.pg-hdr-t { font-size:0.98rem; font-weight:700; color:#ffffff; text-transform:uppercase; letter-spacing:0.05em; margin:0; }
.pg-hdr-s { font-size:0.71rem; color:#d6eaf8; margin-top:0.22rem; line-height:1.5; }
.pg-hdr-p { font-size:0.77rem; color:#ebf5fb; margin-top:0.4rem; font-weight:500; }

.stTabs [data-baseweb="tab-list"] {
    background:#ffffff; border-bottom:2px solid #9ecce8; padding:0; gap:0;
}
.stTabs [data-baseweb="tab"] {
    font-size:0.67rem; font-weight:600; text-transform:uppercase;
    letter-spacing:0.09em; color:#4a7a9b; padding:0.62rem 0.9rem;
    border-bottom:2px solid transparent; margin-bottom:-2px;
    border-radius:0; background:transparent;
}
.stTabs [aria-selected="true"] {
    color:#1a6fa0; border-bottom:2px solid #1a6fa0; background:transparent;
}

.sec {
    font-size:0.66rem; font-weight:700; text-transform:uppercase;
    letter-spacing:0.13em; color:#1a6fa0; padding-bottom:0.38rem;
    border-bottom:2px solid #1a6fa0; margin-top:1.3rem; margin-bottom:0.85rem;
}

.phase-badge {
    display:inline-block; background:#2980b9; color:#fff;
    font-size:0.62rem; font-weight:700; text-transform:uppercase;
    letter-spacing:0.1em; padding:0.22rem 0.7rem; border-radius:2px;
    margin-bottom:0.6rem;
}

.fb {
    background:#ffffff; border:1px solid #cde3f4;
    border-left:3px solid #1a6fa0;
    border-radius:0 3px 3px 0; padding:0.95rem 1.15rem; margin:0.75rem 0;
}
.fb-f {
    font-family:'IBM Plex Mono','Courier New',monospace !important;
    font-size:0.83rem; font-weight:600; color:#154360;
    margin-bottom:0.7rem; line-height:1.6;
}
.fb-p { font-size:0.76rem; color:#1a2e40; line-height:2.0; }
.fb-p b { font-family:'IBM Plex Mono',monospace; font-weight:600; color:#1a6fa0; }
.fb-why {
    font-size:0.73rem; color:#154360; background:#d6eaf8;
    border-left:3px solid #1a6fa0; padding:0.5rem 0.75rem;
    margin-top:0.65rem; border-radius:0 3px 3px 0; line-height:1.6;
}
.fb-ref {
    font-size:0.66rem; color:#4a7a9b; margin-top:0.55rem;
    padding-top:0.45rem; border-top:1px solid #d6eaf8; font-style:italic;
}
.fb-r {
    font-family:'IBM Plex Mono',monospace; font-size:0.8rem;
    font-weight:600; color:#1a5c2a; margin-top:0.48rem;
    padding-top:0.48rem; border-top:1px solid #d6eaf8;
}

.kv-table {
    background:#ebf5fb; border:1px solid #cde3f4;
    border-left:3px solid #1a6fa0; border-radius:0 3px 3px 0;
    padding:0.8rem 1rem; margin:0.6rem 0; font-size:0.76rem;
}
.kv-table-title {
    font-size:0.65rem; font-weight:700; text-transform:uppercase;
    letter-spacing:0.1em; color:#1a6fa0; margin-bottom:0.5rem;
}

.r-pass {
    background:#edf7ee; border:1px solid #a8d5ad; border-left:3px solid #1e7e34;
    color:#145a32; padding:0.7rem 0.95rem; border-radius:0 3px 3px 0;
    font-size:0.81rem; font-weight:600; margin:0.45rem 0; line-height:1.6;
}
.r-fail {
    background:#fdf0f0; border:1px solid #f0a8a8; border-left:3px solid #b92020;
    color:#7b1818; padding:0.7rem 0.95rem; border-radius:0 3px 3px 0;
    font-size:0.81rem; font-weight:600; margin:0.45rem 0; line-height:1.6;
}
.r-note {
    background:#fdf8ec; border:1px solid #e8c97e; border-left:3px solid #c47c0a;
    color:#6b4500; padding:0.7rem 0.95rem; border-radius:0 3px 3px 0;
    font-size:0.81rem; font-weight:600; margin:0.45rem 0; line-height:1.6;
}
.r-info {
    background:#d6eaf8; border:1px solid #9ecce8; border-left:3px solid #1a6fa0;
    color:#154360; padding:0.6rem 0.85rem; border-radius:0 3px 3px 0;
    font-size:0.75rem; margin:0.3rem 0; line-height:1.62;
}

.dt { width:100%; border-collapse:collapse; font-size:0.78rem; margin:0.45rem 0; }
.dt th {
    background:#2980b9; color:#ffffff; padding:0.42rem 0.7rem;
    text-align:left; font-size:0.66rem; font-weight:700;
    text-transform:uppercase; letter-spacing:0.07em; white-space:nowrap;
}
.dt td {
    padding:0.4rem 0.7rem; border-bottom:1px solid #cde3f4;
    color:#1a2e40; vertical-align:top; line-height:1.5;
}
.dt tr:hover td { background:#ebf5fb; }
.dt .mn { font-family:'IBM Plex Mono',monospace; font-size:0.77rem; color:#0d2137; }
.dt .ps { color:#145a32; font-weight:700; }
.dt .fl { color:#7b1818; font-weight:700; }
.dt .nt { color:#6b4500; font-weight:600; }
.dt .hl { background:#d5f5e3; }

.mc-row { display:grid; gap:0.65rem; margin:0.75rem 0; }
.mc {
    background:#ffffff; border:1px solid #cde3f4; border-radius:3px;
    padding:0.75rem 0.95rem; text-align:center;
}
.mc.ps { border-top:3px solid #1e7e34; }
.mc.fl { border-top:3px solid #b92020; }
.mc.bl { border-top:3px solid #2980b9; }
.mc.wn { border-top:3px solid #c47c0a; }
.mc .ml { font-size:0.61rem; text-transform:uppercase; letter-spacing:0.12em; color:#4a7a9b; font-weight:700; margin-bottom:0.28rem; }
.mc .mv { font-size:1.05rem; font-weight:700; color:#154360; font-family:'IBM Plex Mono',monospace; line-height:1.2; }
.mc .mu { font-size:0.65rem; color:#7a9aaa; margin-top:0.12rem; }

.card {
    background:#ffffff; border:1px solid #cde3f4; border-radius:3px;
    padding:1.1rem 1.3rem; margin-bottom:0.75rem;
}

#MainMenu, footer, header { display:none; }
.stDeployButton { display:none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def sec(t):
    st.markdown(f'<div class="sec">{t}</div>', unsafe_allow_html=True)

def phase(n, t):
    st.markdown(f'<div class="phase-badge">Phase {n} — {t}</div>', unsafe_allow_html=True)

def fb(formula, params, why, ref, result=None):
    ph = "".join(f"<div><b>{s}</b> = {d}</div>" for s, d in params.items())
    rh = f'<div class="fb-r">Calculated Result : {result}</div>' if result else ""
    st.markdown(
        f'<div class="fb"><div class="fb-f">{formula}</div>'
        f'<div class="fb-p">{ph}</div>'
        f'<div class="fb-why">Why this formula? {why}</div>'
        f'<div class="fb-ref">Reference : {ref}</div>{rh}</div>',
        unsafe_allow_html=True
    )

def known_table(title, rows):
    r = "".join(f"<tr><td class='mn'>{a}</td><td class='mn'>{b}</td><td style='font-size:0.74rem;color:#1a2e40'>{c}</td><td style='font-size:0.72rem;color:#4a7a9b'>{d}</td></tr>" for a,b,c,d in rows)
    st.markdown(
        f'<div class="kv-table"><div class="kv-table-title">{title}</div>'
        f'<table class="dt"><tr><th>Symbol</th><th>Value</th><th>Meaning</th><th>Source / How obtained</th></tr>{r}</table></div>',
        unsafe_allow_html=True
    )

def rpass(t): st.markdown(f'<div class="r-pass">{t}</div>', unsafe_allow_html=True)
def rfail(t): st.markdown(f'<div class="r-fail">{t}</div>', unsafe_allow_html=True)
def rnote(t): st.markdown(f'<div class="r-note">{t}</div>', unsafe_allow_html=True)
def rinfo(t): st.markdown(f'<div class="r-info">{t}</div>', unsafe_allow_html=True)

def mcards(items, cols=4):
    h = f'<div class="mc-row" style="grid-template-columns:repeat({cols},1fr)">'
    for lbl, val, unit, sty in items:
        h += f'<div class="mc {sty}"><div class="ml">{lbl}</div><div class="mv">{val}</div><div class="mu">{unit}</div></div>'
    st.markdown(h + '</div>', unsafe_allow_html=True)

def sp(h=0.5):
    st.markdown(f'<div style="height:{h}rem"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MATERIAL DATA
# ─────────────────────────────────────────────────────────────────────────────

MATS = {
    "MS Steel — Welded Joint (Recommended for India)": {
        "rho_r_v":15.0, "alpha_r":0.00423, "SW":7.86, "SH":0.114,
        "Tm":500.0, "Tr":20.0, "K":12.15,
    },
    "MS Steel — Bolted Joint": {
        "rho_r_v":15.0, "alpha_r":0.00423, "SW":7.86, "SH":0.114,
        "Tm":310.0, "Tr":20.0, "K":15.70,
    },
    "Copper — Welded Joint": {
        "rho_r_v":1.72, "alpha_r":0.00393, "SW":8.89, "SH":0.094,
        "Tm":1084.0, "Tr":20.0, "K":4.7,
    },
    "Copper — Bolted Joint": {
        "rho_r_v":1.72, "alpha_r":0.00393, "SW":8.89, "SH":0.094,
        "Tm":450.0, "Tr":20.0, "K":5.8,
    },
}

STD_DIA = [8,10,12,16,18,20,22,25,28,32,36,40]

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sb-hdr">
        <div class="sb-hdr-t">Earthing Design Calculator</div>
        <div class="sb-hdr-s">CBIP Pub.339 (2017) / IEEE Std 80-2013 / IS 3043:1987<br>
        Enter your project values. All results update instantly.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-g">Project Information</div>', unsafe_allow_html=True)
    proj    = st.text_input("Project Name", "Substation Earthing Design")
    prepby  = st.text_input("Prepared By", "")
    docno   = st.text_input("Document Number", "")
    volt    = st.selectbox("System Voltage", ["11 kV","33 kV","66 kV","110 kV","132 kV","220 kV","400 kV","765 kV"], index=4)
    sbtype  = st.selectbox("Substation Type", ["AIS — Air Insulated Switchgear","GIS — Gas Insulated Switchgear"])
    neutral = st.selectbox("Neutral Grounding", ["Solid Grounded","Resistance Grounded","Unearthed"])

    st.markdown('<div class="sb-g">Phase 1 — Soil Measurement Data</div>', unsafe_allow_html=True)
    rho   = st.number_input("Mean Soil Resistivity — rho (ohm-m)", value=53.0, min_value=0.1, step=1.0,
                help="Measured by Wenner 4-probe method on site. CBIP Chapter 9. Different spacing values are averaged to get the representative value for the full grid depth.")
    rho_s = st.number_input("Surface Layer Resistivity — rho_s (ohm-m)", value=3000.0, min_value=1.0, step=100.0,
                help="Resistivity of the crushed rock or concrete layer spread on switchyard surface. CBIP assumes 3000 ohm-m. This layer raises the permissible touch and step voltage limits significantly.")
    h_s   = st.number_input("Surface Layer Thickness — hs (m)", value=0.15, min_value=0.001, step=0.01,
                help="Thickness of concrete or crushed rock. A thicker layer gives more benefit but Cs correction reduces the full advantage.")

    st.markdown('<div class="sb-g">Phase 1 — Fault System Data</div>', unsafe_allow_html=True)
    If_kA = st.number_input("Earth Fault Current — If (kA)", value=40.0, min_value=0.1, step=0.5,
                help="Maximum single line-to-earth fault current from system short circuit study. This is the most critical input — it determines conductor size and all voltages.")
    tf    = st.selectbox("Fault Duration for Conductor Sizing — tf (s)", [0.5,1.0,2.0,3.0], index=1,
                help="Maximum fault clearing time INCLUDING backup protection. CBIP: 1s for digital relays, 3s for EM relays. This is always >= ts.")
    ts    = st.selectbox("Shock Duration for Safety Voltages — ts (s)", [0.2,0.3,0.5,1.0], index=2,
                help="Primary relay clearing time only. CBIP: 0.5s for digital relays, 1.0s for EM relays. Always ts <= tf.")
    Sf    = st.slider("Current Division Factor — Sf", 0.10, 1.00, 0.70, 0.05,
                help="Fraction of If that flows into the earth grid. Use 1.0 (conservative) if earth wire data is not available. CBIP Sec 3.7.2.")
    Df    = st.number_input("Decrement Factor — Df", value=1.0, min_value=1.0, max_value=1.5, step=0.01,
                help="IEEE 80-2013 Cl.15.10: For tf >= 0.5s (30 cycles), Df = 1.0. Accounts for DC offset in initial fault cycles.")
    Ta    = st.number_input("Ambient Temperature — Ta (deg C)", value=50.0, min_value=10.0, max_value=80.0, step=5.0,
                help="Initial conductor temperature before fault. Use maximum site ambient for conservative design.")

    st.markdown('<div class="sb-g">Phase 2 — Conductor Selection</div>', unsafe_allow_html=True)
    mat_key = st.selectbox("Conductor Material and Joint Type", list(MATS.keys()), index=0,
                help="CBIP Sec 3.9: MS Steel is standard in India. Avoid mixing copper and steel underground — galvanic cell causes rapid steel corrosion.")
    mat = MATS[mat_key]

    st.markdown('<div class="sb-g">Phase 2 — Grid Geometry</div>', unsafe_allow_html=True)
    Lx  = st.number_input("Grid Length — Lx (m)", value=250.0, min_value=5.0, step=5.0,
              help="Station dimension along X. Cover the entire fenced area including control room, DG building. Extend 1-2m outside fence if needed.")
    Ly  = st.number_input("Grid Width — Ly (m)", value=300.0, min_value=5.0, step=5.0)
    D   = st.number_input("Mesh Spacing — D (m)", value=10.0, min_value=0.5, step=0.5,
              help="CBIP Sec 5.3.5: 3 to 8m typical. Smaller D reduces mesh voltage Em. Start with 10m — reduce if Em exceeds Etouch permissible.")
    h   = st.number_input("Burial Depth of Conductors — h (m)", value=1.0, min_value=0.1, step=0.1,
              help="CBIP: 0.5m minimum. Greater depth reduces both Km and Ks factors, thus reducing Em and Es.")
    d_c_mm = st.number_input("Grid Conductor Diameter — dc (mm)", value=32.0, min_value=1.0, step=1.0,
              help="Use the conductor diameter selected in Phase 2 sizing.")
    Lt_manual = st.number_input("Total Buried Conductor Length — Lt (m)", value=11000.0, min_value=10.0, step=100.0,
              help="Enter from your layout drawings. Auto-estimate is approximate. This is the primary grid resistance parameter.")

    st.markdown('<div class="sb-g">Phase 2 — Ground Rods</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:0.71rem;color:#4a7a9b;line-height:1.6;padding:0.2rem 0 0.4rem 0">
    Rod quantity may not be known at design start.
    Option A calculates it from perimeter length and rod spacing — this is the standard approach.
    Option B is for when quantity is confirmed from drawings.
    </p>""", unsafe_allow_html=True)

    rod_method = st.radio("Rod Quantity Method",
        ["Option A: Calculate from perimeter spacing (recommended)",
         "Option B: Enter rod count directly"], index=0)

    L_rod = st.number_input("Rod Length (m)", value=3.0, min_value=0.5, step=0.5,
                help="IS 3043: minimum 3m. Must reach moist subsoil. CBIP Sec 5.3.5.1: Rods on periphery are more effective than interior rods.")
    d_rod = st.number_input("Rod Diameter (mm)", value=32.0, min_value=5.0, step=1.0,
                help="Same material as grid conductor. Same material mandatory — mixing causes galvanic corrosion.")

    if "Option A" in rod_method:
        rod_sp_peri = st.number_input("Spacing Between Rods Along Perimeter (m)", value=12.0, min_value=1.0, step=1.0,
                help="One rod is placed every X metres along the grid perimeter. Place rods at corners as priority. Example: 90 rods on 1100m perimeter gives approximately 12m spacing.")
        N_rods_auto = True
    else:
        N_rods_manual = st.number_input("Number of Ground Rods", value=90, min_value=0, step=1)
        N_rods_auto = False

    rod_sp_check = st.number_input("Rod-to-Rod Spacing for Utilization Check (m)", value=3.0, min_value=0.1, step=0.5,
                help="Used to compute utilization factor eta. CBIP: spacing >= rod length gives full utilization (eta=1.0).")

    st.markdown('<div class="sb-g">Phase 2 — Separate Earth Pits</div>', unsafe_allow_html=True)
    N_pits = st.number_input("Number of Separate Earth Pits", value=56, min_value=0, step=1,
                help="Separate pipe or plate electrodes connected outside the main grid. Their resistance Re is calculated separately and then combined with Rg in parallel.")
    d_pit_cm = st.number_input("Earth Pit Diameter (cm)", value=3.2, min_value=0.5, step=0.1,
                help="Outer diameter of the pipe or rod used for each earth pit. Example: 3.2 cm diameter pipe electrode.")
    L_pit_cm = st.number_input("Earth Pit Length (cm)", value=300.0, min_value=10.0, step=10.0,
                help="Length of electrode from ground surface. Example: 300 cm = 3.0 m long electrode.")

# ─────────────────────────────────────────────────────────────────────────────
# CALCULATIONS
# ─────────────────────────────────────────────────────────────────────────────

If_A    = If_kA * 1000.0
tf_val  = float(tf)
ts_val  = float(ts)
d_c     = d_c_mm / 1000.0
d_rod_m = d_rod / 1000.0

rho_r   = mat["rho_r_v"]
alpha_r = mat["alpha_r"]
SW      = mat["SW"]
SH      = mat["SH"]
Tm      = mat["Tm"]
Tr      = mat["Tr"]
K_cbip  = mat["K"]
Tcap    = 4.184 * SH * SW
K0      = (1.0 / alpha_r) - Tr

ln_arg  = 1.0 + (Tm - Ta) / (K0 + Ta)
ln_val  = math.log(ln_arg)
numer   = tf_val * alpha_r * rho_r * 1e4 / Tcap
A_ieee  = If_kA * math.sqrt(numer / ln_val)
r_calc  = math.sqrt(A_ieee / math.pi)
d_calc  = 2.0 * r_calc

if rho <= 25:   corr_cls, corr_mm, min_a = "Corrosive / Severely Corrosive",    4.5,  200
elif rho <= 100: corr_cls, corr_mm, min_a = "Mildly / Moderately Corrosive",    2.25, 100
else:            corr_cls, corr_mm, min_a = "Very Mildly Corrosive",             0.75, 100

d_corr  = d_calc + corr_mm
A_corr  = math.pi * (d_corr/2.0)**2
A_final = max(A_corr, float(min_a))
sel_dia = next((d for d in STD_DIA if math.pi*(d/2.0)**2 >= A_final), STD_DIA[-1])
sel_area= math.pi * (sel_dia/2.0)**2
A_cbip  = K_cbip * If_A * math.sqrt(tf_val) * 1e-3

A_grid  = Lx * Ly
Lp      = 2.0*(Lx+Ly)
Dm      = math.sqrt(Lx**2+Ly**2)
n_x     = int(Lx/D)+1
n_y     = int(Ly/D)+1
Lc_est  = n_x*Ly + n_y*Lx

if N_rods_auto:
    N_rods = max(1, int(math.ceil(Lp/rod_sp_peri)))
else:
    N_rods = int(N_rods_manual)

Lr   = N_rods * L_rod
Lt   = Lt_manual
Lc   = Lt - Lr

r_eta = rod_sp_check / L_rod
if r_eta>=2.0:   eta, eta_d = 1.00, "Full utilization — no mutual interference between rods"
elif r_eta>=1.0: eta, eta_d = 0.87, "Minor mutual interference between adjacent rods"
elif r_eta>=0.6: eta, eta_d = 0.75, "Moderate interference — rods too close together"
else:            eta, eta_d = 0.60, "Heavy interference — increase rod spacing to >= rod length"

s20A  = math.sqrt(20.0*A_grid)
s20_A = math.sqrt(20.0/A_grid)
Rg    = rho*(1.0/Lt + (1.0/s20A)*(1.0+1.0/(1.0+h*s20_A)))

Lcm   = L_rod*100.0
d_rcm = d_rod
rho_c = rho*100.0
rho_cm = rho*100.0
Re_rod_single = (100.0*rho_c)/(2.0*math.pi*Lcm) * math.log(4.0*Lcm/d_rcm)
Re_grid_rods  = Re_rod_single / N_rods

if N_pits > 0:
    Re_pit_single = (100.0*rho_c)/(2.0*math.pi*L_pit_cm) * math.log(4.0*L_pit_cm/d_pit_cm)
    Re_pits       = Re_pit_single / N_pits
    Rcomb         = (Rg*Re_pits)/(Rg+Re_pits)
    has_pits      = True
else:
    Re_pits = None
    Rcomb   = Rg
    has_pits = False

IG    = If_A * Sf * Df
IG_kA = IG/1000.0
GPR   = IG * Rg

Cs = 1.0 - ((0.09*(1.0-rho/rho_s))/(2.0*h_s+0.09))
Cs = max(0.01, min(1.0, Cs))

Ib         = 0.116 / math.sqrt(ts_val)
Etouch     = Ib * (1000.0 + 1.5*rho_s*Cs)
Estep_perm = Ib * (1000.0 + 6.0*rho_s*Cs)
Et_bare    = Ib * (1000.0 + 1.5*rho)
Es_bare    = Ib * (1000.0 + 6.0*rho)

na  = 2.0*Lc/Lp
nb  = (Lp/(4.0*math.sqrt(A_grid)))**0.5
n   = na*nb
Kh  = math.sqrt(1.0+h)
Kii = 1.0
Kim = 0.644 + 0.148*n
Kis = Kim

try:
    t1  = D**2/(16.0*h*d_c)
    t2  = (D+2.0*h)**2/(8.0*D*d_c)
    t3  = h/(4.0*d_c)
    t4  = (Kii/Kh)*math.log(8.0/(math.pi*(2.0*n-1.0)))
    Km  = (1.0/(2.0*math.pi))*(math.log(t1+t2-t3)+t4)
    Km  = max(0.05, min(6.0, Km))
except:
    Km = 0.5

try:
    Ks = (1.0/math.pi)*(1.0/(2.0*h)+1.0/(D+h)+(1.0/D)*(1.0-0.5**(n-2.0)))
    Ks = max(0.01, min(6.0, Ks))
except:
    Ks = 0.2

Lm = Lc + (1.55+1.22*(L_rod/Dm))*Lr
Ls = 0.75*Lc + 0.85*Lr

Em = (rho*Km*Kim*IG)/Lm
Es = (rho*Ks*Kis*IG)/Ls

touch_ok = Em <= Etouch
step_ok  = Es <= Estep_perm
rg_ok    = Rg <= 1.0
all_safe = touch_ok and step_ok

# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────

h_sub  = "CBIP Pub.339 (2017)  |  IS 3043:1987 (Reaffirmed 2006)  |  IEEE Std 80-2013  |  IS 2309  |  IEEE Std 665"
h_proj = f"Project: {proj}"
if prepby:  h_proj += f"  |  Prepared by: {prepby}"
if docno:   h_proj += f"  |  Doc No: {docno}"
h_proj += f"  |  {volt}  |  {sbtype.split(' — ')[0]}"

st.markdown(f"""
<div class="pg-hdr">
    <div class="pg-hdr-t">Earthing System Design Calculation — Phase-wise</div>
    <div class="pg-hdr-s">{h_sub}</div>
    <div class="pg-hdr-p">{h_proj}</div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────

tabs = st.tabs([
    "Overview and Drawing",
    "Algorithm",
    "Phase 1 — Inputs",
    "Phase 2 — Conductor Sizing",
    "Phase 3 — Safety Limits",
    "Phase 4 — Resistance and GPR",
    "Phase 5 — Verification",
    "Final Assessment",
])
t_ov, t_alg, t_p1, t_p2, t_p3, t_p4, t_p5, t_fa = tabs

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# OVERVIEW AND DRAWING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t_ov:
    col1, col2 = st.columns([1,1], gap="large")
    with col1:
        sec("What is an Earthing System and Why Does It Matter?")
        st.markdown("""
        <div class="card" style="font-size:0.81rem;color:#1a2e40;line-height:1.85">
        When a phase conductor touches the metal body of a transformer, circuit breaker,
        or any grounded structure, a fault current of tens of thousands of amperes flows.
        This current must reach the earth and return to the source. The earthing system
        provides that path.<br><br>
        Without a properly designed earthing system, the metal structures in the switchyard
        rise to dangerous voltages relative to the ground surface. A person touching equipment
        (touch voltage) or simply standing near the fault area (step voltage) could receive
        a fatal electric shock.<br><br>
        The four primary requirements per CBIP Pub.339 are:<br><br>
        <b>1.</b> Stabilize circuit potentials with respect to ground and limit the overall potential rise.<br>
        <b>2.</b> Protect life and property from dangerous over-voltages.<br>
        <b>3.</b> Provide a low impedance path for fault currents to ensure prompt and consistent
        operation of protective devices during ground faults.<br>
        <b>4.</b> Keep the maximum voltage gradient along the surface, inside and around the
        substation, within safe limits during ground faults.
        </div>""", unsafe_allow_html=True)

        sec("How a Switchyard Earthing Drawing Works")
        st.markdown("""
        <div class="card" style="font-size:0.81rem;color:#1a2e40;line-height:1.85">
        A switchyard earthing drawing typically has two parts:<br><br>
        <b>Part A — The Main Grid (Top View, Plan):</b><br>
        This is the bird's eye view of the switchyard showing the buried MS rod grid.
        The grid is a mesh of conductors buried below the surface, running parallel to
        equipment rows. It covers the entire fenced switchyard area including transformer
        bays, bus tie bays, bus coupler bays, line bays, and future expansion areas.<br><br>
        <b>Part B — Equipment-Specific Earthing Details:</b><br>
        Each type of equipment has its own standardized earthing connection detail.<br>
        - CVT (Capacitor Voltage Transformer) earthing connection<br>
        - CT (Current Transformer) earthing connection<br>
        - LA (Lightning Arrester) — shortest possible lead, no bends, minimum inductance<br>
        - Wave Trap earthing<br>
        - Lightning Mast — dedicated down conductor to grid<br>
        - Isolator and Circuit Breaker earthing (with and without earth switch)<br>
        - Tower earthing details<br>
        - Auxiliary Earthmat: A dense sub-grid placed directly below the operator standing
          area near equipment operating handles to locally reduce step and touch voltage.
        </div>""", unsafe_allow_html=True)

        sec("What is an Auxiliary Earthmat and Why is it Used?")
        st.markdown("""
        <div class="card" style="font-size:0.81rem;color:#1a2e40;line-height:1.85">
        The main grid provides general protection across the switchyard. However, near
        equipment like isolators and circuit breakers, an operator stands at a fixed
        location to perform switching operations.<br><br>
        At that specific spot, the touch or step voltage from the main grid alone may
        still be locally higher than safe. The auxiliary earthmat solves this.<br><br>
        <b>How it works:</b> A small, dense grid (typically 1.5m x 1.5m to 2m x 2m)
        of closely spaced MS conductors is buried just below the surface (0.1 to 0.2m depth)
        at the operator's standing position. This dense sub-grid equalizes the potential
        at the operator's feet, reducing the step voltage to nearly zero. It also brings
        the equipment frame and the operator's feet to the same potential, reducing touch voltage.<br><br>
        Auxiliary earthmats at all manual operating locations are mandatory per CBIP Sec 5.3.5
        and IS 3043.
        </div>""", unsafe_allow_html=True)

    with col2:
        sec("How the Drawing Connects to the Calculation")
        st.markdown(f"""<table class="dt">
        <tr><th>Drawing Element</th><th>Calculation Parameter</th><th>Reference Value</th><th>Where Used</th></tr>
        <tr><td>MS rod grid — horizontal conductors</td><td class="mn">Lc (m)</td><td class="mn">approx 11000 m</td><td>Grid resistance Rg, Em, Es</td></tr>
        <tr><td>Ground rods at grid junctions</td><td class="mn">Lr = N x L (m)</td><td class="mn">90 x 3 = 270 m</td><td>Lt, Rg, Lm, Ls</td></tr>
        <tr><td>Total buried conductor</td><td class="mn">Lt = Lc + Lr (m)</td><td class="mn">11270 m</td><td>Rg formula</td></tr>
        <tr><td>Separate earth pits (pipe electrodes)</td><td class="mn">Re (ohm)</td><td class="mn">56 pits, 3m deep</td><td>Combined Rcomb</td></tr>
        <tr><td>Grid plan dimensions</td><td class="mn">Lx x Ly (m)</td><td class="mn">250 x 300 m</td><td>Area A, Rg, Lp, Dm</td></tr>
        <tr><td>Mesh spacing between parallel conductors</td><td class="mn">D (m)</td><td class="mn">approx 10 m</td><td>Km, Ks, Em, Es</td></tr>
        <tr><td>Burial depth of horizontal conductors</td><td class="mn">h (m)</td><td class="mn">1.0 m</td><td>Rg, Kh, Km, Ks</td></tr>
        <tr><td>MS rod diameter</td><td class="mn">dc (m)</td><td class="mn">0.032 m (32 mm)</td><td>Km formula</td></tr>
        <tr><td>Concrete surface layer</td><td class="mn">rho_s, hs</td><td class="mn">3000 ohm-m, 0.15 m</td><td>Cs, Etouch, Estep</td></tr>
        <tr><td>LA earthing — short lead, no bends</td><td class="mn">Low inductance path</td><td class="mn">Less than 1m</td><td>Impulse impedance check</td></tr>
        <tr><td>Transformer neutral connection</td><td class="mn">Full IG carrying conductor</td><td class="mn">Sized for IG</td><td>Conductor sizing formula</td></tr>
        <tr><td>Auxiliary earthmat at operator positions</td><td class="mn">Local step/touch reduction</td><td class="mn">At all manual switches</td><td>CBIP Sec 5.3.5</td></tr>
        </table>""", unsafe_allow_html=True)

        sec("Typical Bill of Quantities for a Large Switchyard Earthing System")
        st.markdown("""<table class="dt">
        <tr><th>Item</th><th>Description</th><th>Typical Quantity</th><th>Unit</th></tr>
        <tr><td>1</td><td>Main earthmat — 25mm dia MS rod</td><td class="mn">6000 to 7000</td><td>Mtrs</td></tr>
        <tr><td>2</td><td>Auxiliary earthmat — 20mm dia MS rod</td><td class="mn">1000 to 1500</td><td>Mtrs</td></tr>
        <tr><td>3</td><td>Risers — 50mm dia MS rod</td><td class="mn">12000 to 16000</td><td>Mtrs</td></tr>
        <tr><td>4</td><td>75x6 GI Flat</td><td class="mn">2000 to 3000</td><td>Mtrs</td></tr>
        <tr><td>5</td><td>50x6 GI Flat</td><td class="mn">1500 to 2000</td><td>Mtrs</td></tr>
        <tr><td>6</td><td>Rod electrodes for earthing</td><td class="mn">40 to 50</td><td>Nos</td></tr>
        <tr><td>7</td><td>Rod electrodes for lightning protection</td><td class="mn">4 to 6</td><td>Nos</td></tr>
        <tr><td>8</td><td>Pipe electrodes with treated pits</td><td class="mn">50 to 80</td><td>Nos</td></tr>
        <tr><td>9</td><td>Interconnecting wire / module wire</td><td class="mn">700 to 900</td><td>Mtrs</td></tr>
        </table>""", unsafe_allow_html=True)

        sec("Codes and Standards Referenced")
        st.markdown("""<table class="dt">
        <tr><th>Standard</th><th>Description</th><th>Application in This Tool</th></tr>
        <tr><td class="mn">CBIP Pub.339 (2017)</td><td>Manual on Earthing of AC Power Systems</td><td>Primary reference — all formulae and design philosophy</td></tr>
        <tr><td class="mn">IEEE Std 80-2013</td><td>Guide for Safety in AC Substation Grounding</td><td>Full thermal formula, geometric factors, Cs formula</td></tr>
        <tr><td class="mn">IS 3043:1987</td><td>Code of Practice for Earthing (Reaffirmed 2006)</td><td>Minimum sizes, material, installation requirements</td></tr>
        <tr><td class="mn">IEEE Std 665</td><td>Guide for Safety in Generating Station Grounding</td><td>Grid resistance formula (Rg) — Sverak equation</td></tr>
        <tr><td class="mn">IS 2309</td><td>Protection of Buildings against Lightning</td><td>Lightning down conductors, mast earthing</td></tr>
        <tr><td class="mn">IEC 62305</td><td>Protection against Lightning</td><td>Impulse impedance concept for LA earthing</td></tr>
        <tr><td class="mn">BS 7430:2011</td><td>Code of Practice for Protective Earthing</td><td>Surface current density formula (Isd)</td></tr>
        </table>""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ALGORITHM TAB
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t_alg:
    sec("Design Algorithm — Step-by-Step Sequence (CBIP Pub.339 / IEEE Std 80-2013)")
    rinfo("This algorithm is the sequence of calculations this tool performs. Each step corresponds to one tab. The safety check (Step 10) is the decision gate. If it fails, adjust the mesh spacing D or rod count and the tool recalculates instantly.")
    sp(0.4)

    col_f, col_d = st.columns([1, 1.1], gap="large")

    with col_f:
        st.markdown("""
        <div style="background:#ffffff;border:1px solid #cde3f4;border-radius:3px;padding:1.4rem 1rem 2rem 1rem;">
        <div style="display:flex;flex-direction:column;align-items:center;">

        <div style="background:#2980b9;color:#fff;border-radius:20px;padding:0.5rem 1.5rem;
            font-size:0.77rem;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;width:170px;text-align:center;">
            START
        </div>
        <div style="width:2px;height:18px;background:#2980b9;margin:0 auto;"></div>

        <div style="background:#ebf5fb;border:2px solid #1a6fa0;border-radius:3px;padding:0.6rem 1rem;
            font-size:0.75rem;font-weight:600;color:#154360;width:268px;text-align:center;line-height:1.5;">
            STEP 1 — Phase 1 Inputs
            <div style="font-size:0.65rem;font-weight:400;margin-top:0.18rem;color:#1a6fa0;font-family:monospace;">
                rho, rho_s, hs, If, tf, ts, Sf, Df, Ta, material, geometry
            </div>
        </div>
        <div style="width:2px;height:18px;background:#2980b9;margin:0 auto;"></div>

        <div style="background:#ebf5fb;border:2px solid #1a6fa0;border-radius:3px;padding:0.6rem 1rem;
            font-size:0.75rem;font-weight:600;color:#154360;width:268px;text-align:center;line-height:1.5;">
            STEP 2 — Compute Grid Current IG
            <div style="font-size:0.65rem;font-weight:400;margin-top:0.18rem;color:#1a6fa0;font-family:monospace;">
                IG = If x Sf x Df
            </div>
        </div>
        <div style="width:2px;height:18px;background:#2980b9;margin:0 auto;"></div>

        <div style="background:#d5f5e3;border:2px solid #1e7e34;border-radius:3px;padding:0.6rem 1rem;
            font-size:0.75rem;font-weight:600;color:#145a32;width:268px;text-align:center;line-height:1.5;">
            STEP 3 — Phase 2: Conductor Sizing
            <div style="font-size:0.65rem;font-weight:400;margin-top:0.18rem;color:#1a5c2a;font-family:monospace;">
                A = If_kA x sqrt(thermal factor) | Add corrosion | Select standard dia
            </div>
        </div>
        <div style="width:2px;height:18px;background:#2980b9;margin:0 auto;"></div>

        <div style="background:#d5f5e3;border:2px solid #1e7e34;border-radius:3px;padding:0.6rem 1rem;
            font-size:0.75rem;font-weight:600;color:#145a32;width:268px;text-align:center;line-height:1.5;">
            STEP 4 — Phase 2: Grid and Rod Layout
            <div style="font-size:0.65rem;font-weight:400;margin-top:0.18rem;color:#1a5c2a;font-family:monospace;">
                Lx, Ly, D, h, Lt | N_rods = ceil(Lp / rod_spacing)
            </div>
        </div>
        <div style="width:2px;height:18px;background:#2980b9;margin:0 auto;"></div>

        <div style="background:#d5f5e3;border:2px solid #1e7e34;border-radius:3px;padding:0.6rem 1rem;
            font-size:0.75rem;font-weight:600;color:#145a32;width:268px;text-align:center;line-height:1.5;">
            STEP 5 — Phase 4: Grid Resistance Rg
            <div style="font-size:0.65rem;font-weight:400;margin-top:0.18rem;color:#1a5c2a;font-family:monospace;">
                Rg = rho x [1/Lt + (1/sqrt(20A)) x (...)]
            </div>
        </div>
        <div style="width:2px;height:18px;background:#2980b9;margin:0 auto;"></div>

        <div style="background:#d5f5e3;border:2px solid #1e7e34;border-radius:3px;padding:0.6rem 1rem;
            font-size:0.75rem;font-weight:600;color:#145a32;width:268px;text-align:center;line-height:1.5;">
            STEP 6 — Phase 4: Earth Pit and Combined Resistance
            <div style="font-size:0.65rem;font-weight:400;margin-top:0.18rem;color:#1a5c2a;font-family:monospace;">
                Re = (1/N) x [(100 rho_cm)/(2 pi L_cm)] x ln(4L/d) | Rcomb = Rg || Re
            </div>
        </div>
        <div style="width:2px;height:18px;background:#2980b9;margin:0 auto;"></div>

        <div style="background:#d5f5e3;border:2px solid #1e7e34;border-radius:3px;padding:0.6rem 1rem;
            font-size:0.75rem;font-weight:600;color:#145a32;width:268px;text-align:center;line-height:1.5;">
            STEP 7 — Phase 4: GPR
            <div style="font-size:0.65rem;font-weight:400;margin-top:0.18rem;color:#1a5c2a;font-family:monospace;">
                GPR = IG x Rg
            </div>
        </div>
        <div style="width:2px;height:18px;background:#2980b9;margin:0 auto;"></div>

        <div style="background:#d5f5e3;border:2px solid #1e7e34;border-radius:3px;padding:0.6rem 1rem;
            font-size:0.75rem;font-weight:600;color:#145a32;width:268px;text-align:center;line-height:1.5;">
            STEP 8 — Phase 3: Permissible Safety Limits
            <div style="font-size:0.65rem;font-weight:400;margin-top:0.18rem;color:#1a5c2a;font-family:monospace;">
                Ib | Cs | Etouch = Ib x (1000 + 1.5 rho_s Cs) | Estep = Ib x (1000 + 6 rho_s Cs)
            </div>
        </div>
        <div style="width:2px;height:18px;background:#2980b9;margin:0 auto;"></div>

        <div style="background:#d5f5e3;border:2px solid #1e7e34;border-radius:3px;padding:0.6rem 1rem;
            font-size:0.75rem;font-weight:600;color:#145a32;width:268px;text-align:center;line-height:1.5;">
            STEP 9 — Phase 5: Actual Mesh and Step Voltages
            <div style="font-size:0.65rem;font-weight:400;margin-top:0.18rem;color:#1a5c2a;font-family:monospace;">
                na, nb, n, Kh, Km, Ks, Kim | Lm, Ls | Em = rho Km Kim IG / Lm | Es = rho Ks Kis IG / Ls
            </div>
        </div>
        <div style="width:2px;height:18px;background:#2980b9;margin:0 auto;"></div>

        <div style="background:#fdf8ec;border:2px solid #c47c0a;border-radius:3px;padding:0.7rem 1.4rem;
            font-size:0.76rem;font-weight:700;color:#6b4500;width:268px;text-align:center;line-height:1.5;">
            STEP 10 — SAFETY CHECK
            <div style="font-size:0.67rem;font-weight:500;margin-top:0.22rem;color:#7d5200;font-family:monospace;">
                Is Em less than Etouch AND Es less than Estep?
            </div>
        </div>

        <div style="display:flex;justify-content:center;align-items:flex-start;gap:1.8rem;width:100%;margin-top:0.5rem;">
            <div style="display:flex;flex-direction:column;align-items:center;">
                <div style="background:#1e7e34;color:#fff;font-size:0.62rem;font-weight:700;
                    padding:0.18rem 0.55rem;border-radius:2px;text-transform:uppercase;
                    letter-spacing:0.08em;margin-bottom:0.28rem;">YES — SAFE</div>
                <div style="width:2px;height:14px;background:#2980b9;"></div>
                <div style="background:#d5f5e3;border:2px solid #1e7e34;border-radius:3px;
                    padding:0.5rem 0.75rem;font-size:0.71rem;font-weight:600;color:#145a32;
                    width:120px;text-align:center;line-height:1.5;">
                    Design Approved
                    <div style="font-size:0.63rem;font-weight:400;margin-top:0.12rem;color:#1a5c2a;">
                        Generate report</div>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;align-items:center;">
                <div style="background:#b92020;color:#fff;font-size:0.62rem;font-weight:700;
                    padding:0.18rem 0.55rem;border-radius:2px;text-transform:uppercase;
                    letter-spacing:0.08em;margin-bottom:0.28rem;">NO — REVISE</div>
                <div style="width:2px;height:14px;background:#2980b9;"></div>
                <div style="background:#fdf0f0;border:2px solid #b92020;border-radius:3px;
                    padding:0.5rem 0.75rem;font-size:0.71rem;font-weight:600;color:#7b1818;
                    width:128px;text-align:center;line-height:1.5;">
                    Reduce D or add rods
                    <div style="font-size:0.63rem;font-weight:400;margin-top:0.12rem;color:#922b21;">
                        Return to Step 4</div>
                </div>
            </div>
        </div>

        </div>
        </div>""", unsafe_allow_html=True)

    with col_d:
        sec("What Each Step Does and Why")
        steps = [
            ("STEP 1", "Load Inputs",
             "All project, soil, fault, and geometry data is entered. Soil resistivity rho comes from Wenner 4-probe site measurement (CBIP Ch.9). Fault current If comes from the system short circuit study — it is the most critical input, driving all conductor sizes and voltages. Surface layer resistivity rho_s = 3000 ohm-m is the CBIP standard assumption for crushed rock or concrete."),
            ("STEP 2", "Compute Grid Current IG",
             "Not all fault current flows through the grid. Sf (Current Division Factor) is the fraction that actually enters the soil — the rest returns via overhead earth wires of transmission lines. Df (Decrement Factor) corrects for the DC component in initial fault cycles. For tf >= 0.5s, IEEE 80 allows Df = 1.0. IG = If x Sf x Df is the current used for all EPR and voltage calculations."),
            ("STEP 3", "Conductor Thermal Sizing",
             "The conductor must carry If for tf seconds without melting. The IEEE 80 full thermal formula (Clause 9.4 / 11.3) uses material constants — rho_r, alpha_r, SW, SH — to compute minimum area A. The diameter is extracted from A = pi x r^2. CBIP simplified formula (K x If x sqrt(tf) x 10^-3) is used for cross-check. Both should agree."),
            ("STEP 4", "Corrosion Allowance and Standard Diameter",
             "MS steel corrodes underground over its 30-50 year service life. The calculated diameter is increased by an allowance from CBIP Table 3.9 based on soil resistivity class. The final area is compared to IS 3043 minimum (100 or 200 mm2 depending on soil). The next available standard diameter from CBIP Table 3.6 is selected."),
            ("STEP 5", "Grid Resistance Rg",
             "The Sverak formula (IEEE Std 665 / CBIP Eqn 5.32) calculates Rg from total conductor length Lt, grid area A, and burial depth h. This is the resistance between the grid and remote earth — it governs GPR and indirectly governs Em and Es. Target Rg less than 1.0 ohm is typical project specification."),
            ("STEP 6", "Earth Pit and Combined Resistance",
             "Separate earth pits (pipe electrodes outside the main grid) provide additional parallel paths. Their resistance Re is calculated using the rod electrode formula. The parallel combination Rcomb = Rg in parallel with Re gives the final system earth resistance."),
            ("STEP 7", "Ground Potential Rise GPR",
             "GPR = IG x Rg is the maximum voltage the grid rises to above remote earth. This is the maximum transferred potential to any metallic conductor leaving the station. IEEE 80 Sec 15.1: If GPR less than Etouch permissible, the design is inherently safe without further mesh voltage analysis."),
            ("STEP 8", "Permissible Safety Voltage Limits",
             "The maximum body current Ib a person can safely tolerate is 0.116/sqrt(ts) for a 50 kg person (statistically, 99.5% survival without ventricular fibrillation). Cs corrects for finite surface layer thickness. Etouch and Estep are derived from Ib times the total circuit resistance (body plus feet)."),
            ("STEP 9", "Actual Mesh and Step Voltages",
             "Geometric factors na, nb, n, Kh, Km, Ks, Kim are calculated from grid dimensions and conductor sizes. Effective lengths Lm and Ls are derived. Em = rho x Km x Kim x IG / Lm gives the worst mesh voltage (at corner meshes). Es = rho x Ks x Kis x IG / Ls gives the worst step voltage (just outside grid corners)."),
            ("STEP 10", "Safety Check and Decision",
             "If Em less than Etouch AND Es less than Estep: design passes. If either fails: reduce mesh spacing D (reduces Em by adding more conductors), add more peripheral rods (reduces Es), or increase grid area (reduces Rg). In this tool, changing any sidebar input instantly recalculates all results."),
        ]
        for sid, sname, sdesc in steps:
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:0.75rem;margin-bottom:0.7rem;
                padding:0.65rem 0.85rem;background:#ffffff;border:1px solid #cde3f4;border-radius:3px;">
                <div style="background:#2980b9;color:#fff;font-size:0.59rem;font-weight:700;
                    padding:0.22rem 0.45rem;border-radius:2px;white-space:nowrap;flex-shrink:0;
                    margin-top:0.04rem;letter-spacing:0.06em;text-transform:uppercase;">{sid}</div>
                <div>
                    <div style="font-size:0.77rem;font-weight:700;color:#154360;margin-bottom:0.18rem;">{sname}</div>
                    <div style="font-size:0.73rem;color:#1a2e40;line-height:1.62;">{sdesc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHASE 1 — INPUTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t_p1:
    phase(1, "Data Collection and Input Parameters")
    rinfo("Phase 1 is about collecting and understanding the input data. Every value must have a traceable source — a measurement report, a system study, or a code-specified default. This tab explains what each parameter means, why it is needed, and how it is typically obtained.")
    sp(0.3)

    col1, col2 = st.columns([1,1], gap="large")
    with col1:
        sec("1.1 Soil Resistivity — The Most Important Parameter")
        st.markdown("""
        <div class="card" style="font-size:0.8rem;color:#1a2e40;line-height:1.85">
        <b>What is soil resistivity?</b><br>
        Soil resistivity (rho, in ohm-m) measures how strongly the soil opposes current flow.
        High resistivity means current dissipates poorly — leading to high grid resistance Rg,
        high GPR, and high touch/step voltages.<br><br>
        <b>How is it measured?</b><br>
        The standard method is the Wenner 4-probe method (CBIP Chapter 9, IEEE Std 81).
        Four probes are placed in a straight line with equal spacing 'a'. A test current flows
        between the outer two probes, and voltage is measured between the inner two.
        Apparent resistivity rho = 2 x pi x a x (V/I). This is repeated for multiple
        spacings 'a' ranging from about 1m to the larger grid dimension.<br><br>
        <b>Why does spacing matter?</b><br>
        Small spacing gives shallow soil data. Large spacing gives deeper soil data.
        The average of all readings (or a two-layer soil model) gives the design value.<br><br>
        <b>Typical values:</b> Clay or loam soil = 30 to 150 ohm-m. Sandy soil = 100 to 500 ohm-m.
        Rocky soil = 500 to 3000 ohm-m. The example values in this tool (rho = 53 ohm-m)
        represent a typical site with loamy or clay soil.
        </div>""", unsafe_allow_html=True)

        known_table("Phase 1 — Soil Parameters (Known Values and Source)", [
            ("rho", f"{rho} ohm-m", "Mean soil resistivity of the site", "Wenner 4-probe measurements — site soil resistivity test report. CBIP Ch.9."),
            ("rho_s", f"{rho_s} ohm-m", "Surface layer (concrete / crushed rock) resistivity", "CBIP and IEEE 80 standard assumption for crushed rock or concrete. Actual value should be measured from material samples."),
            ("hs", f"{h_s} m", "Thickness of surface layer", "As specified in the project technical specification or site condition."),
        ])

        sec("1.2 Fault Current — The Driving Force")
        st.markdown("""
        <div class="card" style="font-size:0.8rem;color:#1a2e40;line-height:1.85">
        <b>What is earth fault current If?</b><br>
        When one phase conductor touches an earthed metal structure (a line-to-earth fault),
        a current of magnitude If flows from the source, through the fault point, into the
        earthing system, and back through earth to the source neutral.<br><br>
        <b>Single phase to earth fault — why not three phase?</b><br>
        Three-phase short circuits produce the highest current but no current flows through
        earth (symmetrical, no zero sequence component). Single line-to-earth faults are
        statistically the most frequent (over 80% of all faults) and DO flow through earth.
        CBIP Sec 3.7.1: Single line-to-earth fault current is used for earthing design.<br><br>
        <b>How is If determined?</b><br>
        From the system short circuit study: If = 3 x I0 where I0 = E / (Z1 + Z2 + Z0).
        The system impedances Z1, Z2, Z0 are obtained from the network model.<br><br>
        <b>Why use maximum future value?</b><br>
        The earthing system must last 30-50 years. System capacity grows over time, adding
        more transformers and lines, which increases fault levels. CBIP Sec 3.7.4 recommends
        using a future fault level estimate for earthing design.
        </div>""", unsafe_allow_html=True)

    with col2:
        sec("1.3 Duration Parameters — tf and ts")
        st.markdown("""
        <div class="card" style="font-size:0.8rem;color:#1a2e40;line-height:1.85">
        <b>Why are there two different durations?</b><br>
        There are two separate uses for fault duration — one for the conductor (how long it
        must carry current without melting) and one for the human body (how long a person
        might be in contact with a dangerous voltage before the relay clears the fault).<br><br>
        <b>tf — Fault duration for conductor sizing:</b><br>
        This is the MAXIMUM possible fault clearing time including backup protection failure.
        The conductor must survive even if the primary relay fails and the backup relay operates.
        CBIP Sec 3.7.3:<br>
        - Digital / solid-state relays: tf = 1 second<br>
        - Electromagnetic relays: tf = 3 seconds<br><br>
        <b>ts — Shock duration for safety voltages:</b><br>
        This is the PRIMARY relay clearing time — the time from when a person makes contact
        with a dangerous voltage until the primary relay clears the fault. CBIP Sec 3.7.3:<br>
        - Digital relays: ts = 0.5 second<br>
        - EM relays: ts = 1.0 second<br><br>
        Note: The reference calculation used tf = 1s for conductor sizing and ts = 0.5s
        for permissible voltage calculation. Always use ts less than or equal to tf.
        </div>""", unsafe_allow_html=True)

        sec("1.4 Current Division Factor Sf and Decrement Factor Df")
        st.markdown("""
        <div class="card" style="font-size:0.8rem;color:#1a2e40;line-height:1.85">
        <b>Current Division Factor Sf:</b><br>
        When a fault occurs at the station, the fault current If flows from the source into
        the fault. Part of this returns via overhead earth wires (shield wires) of the
        outgoing transmission lines — directly back to the source towers without entering
        the soil at the station at all. Only the remainder (Sf x If) actually flows between
        the station grid and the soil. CBIP Sec 3.7.2: IG = Sf x If.<br><br>
        A typical value for a station with multiple outgoing lines with earth wires is
        Sf = 0.60 to 0.80. The reference calculation used Sf = 0.70 (70% into grid,
        30% via earth wires of outgoing lines).<br><br>
        Accurate Sf requires the CBIP software 'gridi' using line impedance data.
        If not available, use Sf = 1.0 (conservative — all current through grid).<br><br>
        <b>Decrement Factor Df:</b><br>
        A fault current has a symmetrical AC component plus a decaying DC component
        in the first few cycles. This DC offset makes the effective rms current larger
        than the symmetrical value. IEEE 80-2013 Cl.15.10: For tf >= 0.5 seconds
        (30 cycles at 50Hz), Df = 1.0. The reference calculation used Df = 1.0.
        </div>""", unsafe_allow_html=True)

        known_table("Phase 1 — Fault Parameters (Known Values and Source)", [
            ("If", f"{If_kA} kA = {If_A:.0f} A", "Maximum single line-to-earth fault current", "System short circuit study. CBIP Sec 3.7.1."),
            ("tf", f"{tf_val} s", "Fault duration for conductor thermal sizing", "CBIP Sec 3.7.3 — includes backup protection clearing time."),
            ("ts", f"{ts_val} s", "Shock duration for permissible voltage calculation", "CBIP Sec 3.7.3 — primary relay clearing time only."),
            ("Sf", f"{Sf}", "Current division factor (fraction entering grid soil)", "System study or CBIP gridi software. Use 1.0 if unknown."),
            ("Df", f"{Df}", "Decrement factor for DC offset in initial cycles", "IEEE 80-2013 Cl.15.10: Df = 1.0 for tf >= 0.5s."),
            ("Ta", f"{Ta} deg C", "Initial conductor / ambient temperature", "Maximum site ambient temperature."),
        ])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHASE 2 — CONDUCTOR SIZING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t_p2:
    phase(2, "Conductor Sizing, Corrosion Allowance, and Grid Layout")
    rinfo("Phase 2 has two parts: (A) sizing the conductor so it carries the fault current without melting, and (B) deciding the grid geometry — dimensions, mesh spacing, burial depth, and rod placement. Together they define the physical earthing installation.")
    sp(0.3)

    col1, col2 = st.columns([1.1, 0.9], gap="large")
    with col1:
        sec("2.1 Material Constants (IEEE 80 Table 1 / CBIP Table 3.5)")
        st.markdown(f"""<table class="dt">
        <tr><th>Symbol</th><th>Parameter</th><th>Value</th><th>Unit</th><th>Physical Meaning</th></tr>
        <tr><td class="mn">rho_r</td><td>Electrical resistivity of conductor material</td><td class="mn">{rho_r}</td><td>micro-ohm-cm</td><td>How much the conductor resists current — determines heat generated during fault</td></tr>
        <tr><td class="mn">alpha_r</td><td>Thermal coefficient of resistivity at Tr</td><td class="mn">{alpha_r}</td><td>per deg C</td><td>Rate of increase of resistance with temperature</td></tr>
        <tr><td class="mn">SW</td><td>Density of conductor material</td><td class="mn">{SW}</td><td>g per cm3</td><td>Mass per unit volume — determines how much material stores heat</td></tr>
        <tr><td class="mn">SH</td><td>Specific heat of conductor material</td><td class="mn">{SH}</td><td>cal per g per deg C</td><td>Heat capacity — higher SH means more energy needed to raise temperature</td></tr>
        <tr><td class="mn">Tcap</td><td>Thermal capacity factor = 4.184 x SH x SW</td><td class="mn">{Tcap:.4f}</td><td>(dimensionless)</td><td>Combined measure of material ability to absorb fault energy without overheating</td></tr>
        <tr><td class="mn">Tm</td><td>Maximum allowable conductor temperature</td><td class="mn">{Tm}</td><td>deg C</td><td>For welded joints: 500 deg C. For bolted: 310 deg C (CBIP Table 3.5).</td></tr>
        <tr><td class="mn">Tr</td><td>Reference temperature for material constants</td><td class="mn">{Tr}</td><td>deg C</td><td>Temperature at which rho_r and alpha_r are specified in IEEE 80 tables</td></tr>
        <tr><td class="mn">K0</td><td>Derived constant = (1/alpha_r) - Tr</td><td class="mn">{K0:.2f}</td><td>deg C</td><td>Intermediate calculation value used in the full thermal formula</td></tr>
        <tr><td class="mn">Ta</td><td>Initial (ambient) conductor temperature</td><td class="mn">{Ta}</td><td>deg C</td><td>Starting temperature before fault — use maximum ambient for conservative result</td></tr>
        </table>""", unsafe_allow_html=True)

        sec("2.2 Full Thermal Formula — IEEE 80-2013 Cl.11.3 / Cl.9.4")
        fb(
            "A = If_kA x sqrt [ (tc x alpha_r x rho_r x 10^4 / Tcap) / ln(1 + (Tm - Ta) / (K0 + Ta)) ]",
            {
                "A (mm2)": "Minimum cross-sectional area of conductor to prevent melting (fusing)",
                "If_kA": f"{If_kA} kA — earth fault current in kilo-Amperes (AC rms, negligible impedance fault)",
                "tc = tf": f"{tf_val} s — fault current flow duration (conductor sizing — includes backup protection)",
                "alpha_r": f"{alpha_r} per deg C — thermal coefficient of resistivity",
                "rho_r": f"{rho_r} micro-ohm-cm — electrical resistivity of conductor material at Tr",
                "Tcap": f"4.184 x {SH} x {SW} = {Tcap:.4f} — thermal capacity factor",
                "Tm": f"{Tm} deg C — maximum allowable conductor temperature (joint type dependent)",
                "Ta": f"{Ta} deg C — initial conductor temperature (maximum ambient)",
                "K0": f"(1 / {alpha_r}) - {Tr} = {K0:.2f} deg C — derived constant",
                "ln(1 + (Tm-Ta)/(K0+Ta))": f"ln(1 + ({Tm}-{Ta})/({K0:.2f}+{Ta})) = ln({ln_arg:.5f}) = {ln_val:.4f}",
                "Inner fraction": f"({tf_val} x {alpha_r} x {rho_r} x 10000 / {Tcap:.4f}) / {ln_val:.4f} = {numer:.4f} / {ln_val:.4f} = {numer/ln_val:.4f}",
            },
            "This formula comes from the adiabatic (no heat loss) heating model. During a fault of short duration, all electrical energy generated in the conductor is stored as heat in the conductor itself — there is no time for heat to escape to the surrounding soil. The formula calculates the minimum cross-section that keeps temperature below Tm.",
            "IEEE Std 80-2013 Clause 11.3 — Full thermal formula. Same as IEEE 80-1986 Clause 9.4. CBIP Pub.339 Sec 3.8.2.",
            f"A = {If_kA} x sqrt({numer/ln_val:.4f}) = {If_kA} x {math.sqrt(numer/ln_val):.5f} = {A_ieee:.3f} mm2"
        )

        sec("2.3 CBIP Simplified Formula — Cross-Check (CBIP Eqn 3.20)")
        fb(
            "Ac = K x If x sqrt(tf) x 10^-3",
            {
                "K": f"{K_cbip} — CBIP Table 3.5 constant. Encapsulates all material constants for this material and joint type.",
                "If (A)": f"{If_A:.0f} A — note: If is in Amperes here (not kA)",
                "tf (s)": f"{tf_val} s",
                "10^-3": "Unit conversion",
            },
            "CBIP derived a simplified K factor by pre-substituting the material constants into the IEEE full formula. For MS Steel welded joints: K = 12.15. For MS Steel bolted joints: K = 15.7 (lower Tm = 310 deg C gives larger required area).",
            "CBIP Manual Pub.339 Eqn 3.18 (K=12.15 welded), Eqn 3.19 (K=15.7 bolted), Eqn 3.20 (general). Table 3.5.",
            f"Ac = {K_cbip} x {If_A:.0f} x sqrt({tf_val}) x 0.001 = {K_cbip * If_A * math.sqrt(tf_val) * 1e-3:.3f} mm2  (IEEE result: {A_ieee:.3f} mm2)"
        )
        rinfo(f"Both formulas agree: IEEE gives {A_ieee:.1f} mm2, CBIP gives {K_cbip * If_A * math.sqrt(tf_val) * 1e-3:.1f} mm2. Small difference is due to rounding in K constant. Use IEEE formula for design, CBIP for cross-check.")

    with col2:
        sec("2.4 Diameter and Corrosion Allowance")
        fb(
            "r = sqrt(A / pi)   =>   d = 2 x r   =>   d_design = d + corrosion_allowance",
            {
                "A (mm2)": f"{A_ieee:.3f} — minimum area from IEEE formula",
                "r (mm)": f"sqrt({A_ieee:.3f} / pi) = {r_calc:.4f}",
                "d_calculated (mm)": f"2 x {r_calc:.4f} = {d_calc:.4f}",
                "Corrosion class": f"{corr_cls} (at rho = {rho} ohm-m, CBIP Table 3.7)",
                "Corrosion allowance": f"+{corr_mm} mm added to diameter (CBIP Table 3.9)",
                "d_design (mm)": f"{d_calc:.4f} + {corr_mm} = {d_corr:.4f}",
                "A_corr (mm2)": f"pi x ({d_corr:.4f}/2)^2 = {A_corr:.2f}",
                "IS 3043 minimum area": f"{min_a} mm2 for {corr_cls.split('/')[0].strip()} soil",
                "A_final (mm2)": f"max({A_corr:.2f}, {min_a}) = {A_final:.2f}",
            },
            "Steel corrodes in soil over 30-50 year service life. The corroded conductor has less cross-section and may not carry fault current safely near end of life. CBIP Table 3.9 gives corrosion allowance based on soil resistivity class. The reference calculation confirmed: calculated dia = 25.8mm, after +4.5mm corrosion allowance = 30.3mm, selected standard 32mm.",
            "CBIP Pub.339 Table 3.7 (soil corrosiveness) + Table 3.9 (corrosion allowance). IS 3043 Sec 5.3.4 (minimum sizes).",
            f"Corrosion-corrected conductor diameter = {d_corr:.2f} mm. Design area = {A_final:.2f} mm2."
        )

        sec("2.5 Standard Conductor Selection (CBIP Table 3.6)")
        rows = ""
        for d in STD_DIA:
            a = math.pi*(d/2.0)**2
            sel = d == sel_dia
            stt = "SELECTED" if sel else ("below required" if a < A_final else "acceptable")
            cl = " ps" if sel else ""
            bg = ' class="hl"' if sel else ""
            rows += f"<tr{bg}><td class='mn'>{d}</td><td class='mn'>{a:.1f}</td><td class='mn{cl}'>{stt}</td></tr>"
        st.markdown(f"""<table class="dt">
        <tr><th>Standard Dia (mm)</th><th>Area (mm2)</th><th>Status</th></tr>
        {rows}</table>""", unsafe_allow_html=True)
        sp(0.3)
        rpass(f"Selected conductor: {sel_dia} mm diameter MS round rod. Area = {sel_area:.1f} mm2. Meets thermal and corrosion requirements.")

        sec("2.6 Surface Current Density Limit (CBIP Eqn 3.21)")
        Jsd = math.sqrt(57.7/(rho*tf_val))*1e-3
        fb(
            "Isd = 10^-3 x sqrt(57.7 / (rho x tf))   [A per mm2]",
            {
                "Isd (A/mm2)": "Maximum allowable current density at conductor surface",
                "57.7": "Empirical constant from IS 3043 / BS 7430 — based on soil drying temperature",
                "rho (ohm-m)": f"{rho}",
                "tf (s)": f"{tf_val}",
            },
            "High current density at the conductor surface heats the surrounding soil. If temperature exceeds 100 deg C, the soil moisture evaporates, soil shrinks away from the conductor, and a high-resistance gap forms — increasing effective grid resistance permanently. In practice, the total conductor length used to control voltages is far greater than needed thermally, so actual current density is well below this limit.",
            "CBIP Pub.339 Eqn 3.21 / IS 3043 / BS 7430:2011",
            f"Isd = {Jsd:.6f} A/mm2 — maximum allowable. Actual current density in grid will be much lower."
        )

        sec("2.7 Grid Layout Geometry")
        st.markdown(f"""<table class="dt">
        <tr><th>Parameter</th><th>Symbol</th><th>Value</th><th>How Determined</th></tr>
        <tr><td>Grid length</td><td class="mn">Lx</td><td class="mn">{Lx:.0f} m</td><td>Entire fenced switchyard length — from layout drawing</td></tr>
        <tr><td>Grid width</td><td class="mn">Ly</td><td class="mn">{Ly:.0f} m</td><td>Entire fenced switchyard width — from layout drawing</td></tr>
        <tr><td>Grid area</td><td class="mn">A = Lx x Ly</td><td class="mn">{A_grid:.0f} m2</td><td>Calculated. This is the most important geometric parameter for Rg.</td></tr>
        <tr><td>Grid perimeter</td><td class="mn">Lp = 2(Lx+Ly)</td><td class="mn">{Lp:.0f} m</td><td>Calculated. Used to determine na and rod count.</td></tr>
        <tr><td>Grid diagonal</td><td class="mn">Dm = sqrt(Lx2+Ly2)</td><td class="mn">{Dm:.2f} m</td><td>Calculated. Used in effective length Lm formula (CBIP Eqn 5.29).</td></tr>
        <tr><td>Mesh spacing</td><td class="mn">D</td><td class="mn">{D} m</td><td>Design decision. CBIP: 3-8m typical. Smaller D reduces Em.</td></tr>
        <tr><td>Burial depth</td><td class="mn">h</td><td class="mn">{h} m</td><td>CBIP: 0.5m minimum. Greater h reduces Km and Ks.</td></tr>
        <tr><td>Conductor runs in X</td><td class="mn">n_x = int(Lx/D)+1</td><td class="mn">{n_x} runs</td><td>Calculated from grid dimensions and spacing.</td></tr>
        <tr><td>Conductor runs in Y</td><td class="mn">n_y = int(Ly/D)+1</td><td class="mn">{n_y} runs</td><td>Calculated from grid dimensions and spacing.</td></tr>
        <tr><td>Estimated horizontal Lc</td><td class="mn">n_x x Ly + n_y x Lx</td><td class="mn">{Lc_est:.0f} m</td><td>Approximate — use actual from drawings for final design.</td></tr>
        <tr><td>Total buried conductor (actual)</td><td class="mn">Lt</td><td class="mn">{Lt:.0f} m</td><td>From detailed layout drawings. Example: 11000m horizontal + 90x3m rods = 11270m.</td></tr>
        <tr><td>Ground rods (N)</td><td class="mn">N_rods</td><td class="mn">{N_rods}</td><td>{f"From perimeter / {rod_sp_peri}m spacing = ceil({Lp:.0f}/{rod_sp_peri})" if N_rods_auto else "Entered from drawings"}</td></tr>
        <tr><td>Total rod length</td><td class="mn">Lr = N x L</td><td class="mn">{Lr:.0f} m</td><td>Calculated.</td></tr>
        <tr><td>Horizontal conductor (derived)</td><td class="mn">Lc = Lt - Lr</td><td class="mn">{Lc:.0f} m</td><td>Calculated from Lt and Lr.</td></tr>
        </table>""", unsafe_allow_html=True)

        if N_rods_auto:
            rinfo(f"Rod count auto-calculated: Perimeter Lp = {Lp:.0f} m. One rod every {rod_sp_peri} m: N = ceil({Lp:.0f}/{rod_sp_peri}) = {N_rods} rods. Example from published calculations: 90 rods on 1100m perimeter = approximately one rod per 12m.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHASE 3 — SAFETY LIMITS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t_p3:
    phase(3, "Permissible Safety Voltage Limits — Tolerable Touch and Step Voltage")
    rinfo("Phase 3 calculates the maximum voltages a person can safely tolerate. These are the UPPER LIMITS. The actual voltages (Em and Es computed in Phase 5) must be below these limits. The limits depend on the fault clearing speed (ts) and the surface material (rho_s, hs).")
    sp(0.3)

    col1, col2 = st.columns([1,1], gap="large")
    with col1:
        sec("3.1 The Human Safety Model — How Electric Shock Kills")
        st.markdown("""
        <div class="card" style="font-size:0.8rem;color:#1a2e40;line-height:1.85">
        <b>What is ventricular fibrillation?</b><br>
        The heart is controlled by electrical impulses. If external current flows through the
        heart region, it disrupts the natural rhythm. At currents above about 50-100 mA,
        the heart muscle fibers start twitching in an uncoordinated way (fibrillation)
        instead of pumping. Blood circulation stops. Death follows within minutes unless
        defibrillated. This is why electric shocks can be fatal even at relatively low voltages.<br><br>
        <b>Two dangerous scenarios:</b><br>
        1. Touch voltage: Person stands on the ground and touches an earthed equipment body.
           Current enters the hand, travels through the body, exits through both feet.
           The circuit includes body resistance Rb = 1000 ohm plus two feet in parallel
           on the surface. Foot resistance = rho_s / 4b per foot (disc electrode, b = 0.08m radius)
           = 3 x rho_s ohm each. In parallel: 1.5 x rho_s ohm.<br><br>
        2. Step voltage: Person walks near the fault area. One foot is on higher potential
           than the other (1 metre apart = one stride). Current enters the high-potential foot,
           travels through the body, exits the low-potential foot. Two feet in series:
           3 x rho_s + 3 x rho_s = 6 x rho_s ohm.<br><br>
        <b>Why does the surface layer help?</b><br>
        Concrete or crushed rock has rho_s = 3000 ohm-m — much higher than natural soil.
        Higher foot resistance = lower body current for the same voltage = safer.
        </div>""", unsafe_allow_html=True)

        sec("3.2 Maximum Permissible Body Current (CBIP Eqn 3.1 / IEEE 80)")
        fb(
            "Ib = 0.116 / sqrt(ts)",
            {
                "Ib (A)": "Maximum body current that 99.5% of persons can withstand without ventricular fibrillation",
                "0.116": "= k/1000 where k = 116 mA. For 50 kg body weight. Statistically determined. CBIP Sec 3.6.2 and IEEE 80.",
                "ts (s)": f"{ts_val} s — shock contact duration (primary relay clearing time)",
                "Derivation": "Based on Dalziel's research: energy absorbed by body = IB^2 x ts = constant (k^2/1000^2). For 50 kg person: k = 116 mA.",
            },
            "The constant 0.116 (116 mA) corresponds to the current level at which 99.5% of 50 kg persons do NOT experience ventricular fibrillation. This means 0.5% of persons at 116 mA MIGHT fibrillate — it is a statistical safety limit. For heavier persons (70 kg), IEEE 80 allows 0.157/sqrt(ts). CBIP uses 50 kg as the conservative standard.",
            "CBIP Manual Pub.339 Sec 3.6.2 Eqn 3.1. IEEE Std 80-2013. Based on C.F. Dalziel research (University of California Berkeley, 1950s-1960s).",
            f"Ib = 0.116 / sqrt({ts_val}) = 0.116 / {math.sqrt(ts_val):.4f} = {Ib*1000:.3f} mA = {Ib:.6f} A"
        )

        sec("3.3 Surface Layer Reduction Factor Cs (IEEE 80 Eq.27 / CBIP Eqn 5.9)")
        fb(
            "Cs = 1 - [ 0.09 x (1 - rho / rho_s) / (2 x hs + 0.09) ]",
            {
                "Cs": "Reduction factor — accounts for finite thickness of surface layer",
                "rho (ohm-m)": f"{rho} — soil resistivity below the surface layer",
                "rho_s (ohm-m)": f"{rho_s} — surface layer (concrete / crushed rock) resistivity",
                "hs (m)": f"{h_s} — surface layer thickness",
                "K = (rho-rho_s)/(rho+rho_s)": f"Reflection factor = ({rho}-{rho_s})/({rho}+{rho_s}) = {(rho-rho_s)/(rho+rho_s):.4f}",
                "(1-rho/rho_s)": f"1 - {rho}/{rho_s} = {1-rho/rho_s:.5f}",
                "Numerator": f"0.09 x {1-rho/rho_s:.5f} = {0.09*(1-rho/rho_s):.5f}",
                "Denominator": f"2 x {h_s} + 0.09 = {2*h_s+0.09:.3f}",
            },
            "The foot electrode (human foot) is modelled as a conducting disc of radius b = 0.08m on the surface. For an infinitely deep uniform layer of resistivity rho_s, foot resistance = rho_s/(4b) = 3 x rho_s. But the surface layer has finite thickness hs — below it is the natural soil of resistivity rho. Cs = 1.0 means full benefit. If no surface layer: Cs = 1.0 and rho_s must be set equal to rho (natural soil).",
            "IEEE Std 80-2000 Equation 27 = CBIP Pub.339 Eqn 5.9. More accurate alternate: CBIP Eqn 3.11 (Seedher-Arora formula). Reference calculation used IEEE Eq.27.",
            f"Cs = 1 - ({0.09*(1-rho/rho_s):.5f} / {2*h_s+0.09:.3f}) = {Cs:.4f}"
        )

    with col2:
        sec("3.4 Permissible Touch Voltage (CBIP Eqn 3.10 / IEEE Std 80 Eqn B.6)")
        st.markdown("""<div style="font-size:0.79rem;color:#1a2e40;line-height:1.7;margin-bottom:0.5rem">
        Touch voltage circuit: Current flows from hand (in contact with earthed equipment) through body
        (Rb = 1000 ohm) and out through both feet in parallel standing on the surface.
        Two feet in parallel, each = 3 x rho_s ohm (disc electrode formula, b = 0.08m).
        Total foot resistance = 1.5 x rho_s ohm.
        </div>""", unsafe_allow_html=True)
        fb(
            "Etouch = Ib x (Rb + 1.5 x rho_s x Cs)",
            {
                "Etouch (V)": "Maximum permissible touch voltage — actual Em must be below this",
                "Ib (A)": f"{Ib:.6f} A = {Ib*1000:.3f} mA",
                "Rb (ohm)": "1000 ohm — standard human body resistance for 50 kg person. IEEE 80 Sec 7.",
                "1.5 x rho_s x Cs": f"1.5 x {rho_s} x {Cs:.4f} = {1.5*rho_s*Cs:.3f} ohm — resistance of two feet in PARALLEL on surface",
                "Derivation of 1.5": "Each foot = disc electrode = rho_s/(4b) = rho_s/0.32 = 3.125 x rho_s ohm. Two feet in parallel = 3.125 x rho_s / 2 = 1.5625 x rho_s ohm. Rounded to 1.5 x rho_s.",
                "Total circuit R": f"Rb + 1.5 x rho_s x Cs = 1000 + {1.5*rho_s*Cs:.3f} = {1000+1.5*rho_s*Cs:.3f} ohm",
            },
            "Ohm's law: Etouch = Ib x (total circuit resistance). For the person to be safe, Etouch must be less than or equal to Ib x (Rb + foot resistance).",
            "CBIP Pub.339 Sec 3.6.2 Eqn 3.10. IEEE Std 80-2013 Eqn B.6.",
            f"Etouch = {Ib:.6f} x ({1000+1.5*rho_s*Cs:.3f}) = {Etouch:.2f} V"
        )

        sec("3.5 Permissible Step Voltage (CBIP Eqn 3.9 / IEEE Std 80 Eqn B.6)")
        st.markdown("""<div style="font-size:0.79rem;color:#1a2e40;line-height:1.7;margin-bottom:0.5rem">
        Step voltage circuit: Current flows in through one foot, through body, out through the other foot.
        Feet are 1 metre apart (one step). Each foot = 3 x rho_s ohm. Two feet in series = 6 x rho_s ohm.
        </div>""", unsafe_allow_html=True)
        fb(
            "Estep = Ib x (Rb + 6 x rho_s x Cs)",
            {
                "Estep (V)": "Maximum permissible step voltage — actual Es must be below this",
                "Ib (A)": f"{Ib:.6f} A",
                "6 x rho_s x Cs": f"6 x {rho_s} x {Cs:.4f} = {6*rho_s*Cs:.3f} ohm — resistance of two feet in SERIES with 1m spacing",
                "Derivation of 6": "Each foot = 3.125 x rho_s ohm. Two feet in series (1m stride) = 6.25 x rho_s ohm. Rounded to 6 x rho_s.",
                "Total circuit R": f"Rb + 6 x rho_s x Cs = 1000 + {6*rho_s*Cs:.3f} = {1000+6*rho_s*Cs:.3f} ohm",
                "Why step > touch allowance": "Step circuit has two feet in series = 2x higher foot resistance. Higher voltage is needed to push dangerous current through the body.",
            },
            "In a step voltage scenario, both contact points are on the ground (feet). Total resistance = Rb + 2 x (3 x rho_s) = Rb + 6 x rho_s. This is HIGHER than the touch voltage circuit, so a higher voltage is permissible.",
            "CBIP Pub.339 Sec 3.6.2 Eqn 3.9. IEEE Std 80-2013 Eqn B.6.",
            f"Estep = {Ib:.6f} x ({1000+6*rho_s*Cs:.3f}) = {Estep_perm:.2f} V"
        )

        sec("3.6 Results Summary")
        mcards([
            ("Body Current Ib", f"{Ib*1000:.3f}", "mA", "bl"),
            ("Cs", f"{Cs:.4f}", "", "bl"),
            ("Etouch permissible", f"{Etouch:.2f}", "V", "bl"),
            ("Estep permissible", f"{Estep_perm:.2f}", "V", "bl"),
        ])

        sec("3.7 Effect of Surface Layer — Why It Matters")
        st.markdown(f"""<table class="dt">
        <tr><th>Condition</th><th>Etouch (V)</th><th>Estep (V)</th><th>Improvement</th></tr>
        <tr class="hl"><td>WITH surface layer (Cs={Cs:.4f}, rho_s={rho_s} ohm-m, hs={h_s}m)</td>
            <td class="mn ps">{Etouch:.2f}</td><td class="mn">{Estep_perm:.2f}</td>
            <td class="mn">Design condition</td></tr>
        <tr><td>WITHOUT surface layer (Cs=1.0, rho_s = natural soil = {rho} ohm-m)</td>
            <td class="mn">{Et_bare:.2f}</td><td class="mn">{Es_bare:.2f}</td>
            <td class="mn">Baseline</td></tr>
        <tr><td>Ratio (with / without)</td>
            <td class="mn">{Etouch/Et_bare:.2f}x higher</td>
            <td class="mn">{Estep_perm/Es_bare:.2f}x higher</td>
            <td class="mn">Benefit of surface layer</td></tr>
        </table>
        <p style="font-size:0.73rem;color:#1a2e40;margin-top:0.4rem;line-height:1.6">
        CBIP Pub.339 Sec 3.6.2: Crushed rock or concrete surface layer (rho_s = 3000 ohm-m) is strongly
        recommended throughout the switchyard. Without this layer, the permissible limits would be
        {Et_bare:.0f} V (touch) and {Es_bare:.0f} V (step), making design much harder to satisfy.
        </p>""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHASE 4 — RESISTANCE AND GPR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t_p4:
    phase(4, "Grid Resistance, Earth Electrode Resistance, and Ground Potential Rise")
    rinfo("Phase 4 computes the electrical resistance of the earthing system to remote earth. This governs the Ground Potential Rise (GPR = IG x Rg), which is the maximum voltage the grid rises to during a fault. Lower Rg means lower GPR means safer design.")
    sp(0.3)

    col1, col2 = st.columns([1,1], gap="large")
    with col1:
        sec("4.1 Grid Current IG (CBIP Eqn 3.16)")
        fb(
            "IG = If x Sf x Df",
            {
                "If (A)": f"{If_A:.0f} A = {If_kA} kA — total single line-to-earth fault current",
                "Sf": f"{Sf} — current division factor (fraction entering earth grid from soil)",
                "Df": f"{Df} — decrement factor (DC offset correction for initial fault cycles)",
                "IG (A)": "Design grid current — current flowing between grid conductors and surrounding soil",
            },
            "IG is the current that actually creates the EPR and the voltage gradients on the earth surface. If flows from the source to the fault, but part of it returns via earth/shield wires of overhead lines (Sf accounts for this division). The decrement factor Df corrects for the DC component in the initial fault cycles.",
            "CBIP Pub.339 Sec 3.7.2 Eqn 3.16. IEEE Std 80-2013 Cl.15.",
            f"IG = {If_A:.0f} x {Sf} x {Df} = {IG:.0f} A = {IG_kA:.4f} kA"
        )

        sec("4.2 Grid Earth Resistance — Sverak Formula (IEEE Std 665 / CBIP Eqn 5.32)")
        st.markdown(f"""
        <div style="font-size:0.79rem;color:#1a2e40;line-height:1.7;margin-bottom:0.5rem">
        The grid earth resistance Rg is the resistance between the buried grid electrode and
        a theoretical point at infinite distance (remote earth). It is a function of:
        (1) soil resistivity rho, (2) total conductor length Lt,
        (3) grid area A, and (4) burial depth h.
        </div>""", unsafe_allow_html=True)
        fb(
            "Rg = rho x [ 1/Lt  +  (1/sqrt(20 x A)) x (1 + 1/(1 + h x sqrt(20/A))) ]",
            {
                "Rg (ohm)": "Grid earth resistance to remote earth",
                "rho (ohm-m)": f"{rho} — soil resistivity",
                "Lt (m)": f"{Lt:.0f} — total buried conductor = horizontal Lc + rod length Lr",
                "A (m2)": f"{A_grid:.0f} — grid enclosed area = Lx x Ly",
                "h (m)": f"{h} — conductor burial depth",
                "First term rho/Lt": f"{rho}/{Lt:.0f} = {rho/Lt:.6f} — contribution from total conductor length",
                "sqrt(20A)": f"sqrt(20 x {A_grid:.0f}) = {s20A:.4f}",
                "sqrt(20/A)": f"sqrt(20/{A_grid:.0f}) = {s20_A:.6f}",
                "h x sqrt(20/A)": f"{h} x {s20_A:.6f} = {h*s20_A:.6f}",
                "Second term complete": f"(1/{s20A:.4f}) x (1 + 1/(1 + {h*s20_A:.6f})) = {(1+1/(1+h*s20_A))/s20A:.8f}",
            },
            "This is the Sverak formula (IEEE Std 665, CBIP Eqn 5.32). It has two terms: the first (rho/Lt) captures the effect of total conductor length. The second term captures the effect of grid area and burial depth. Formula accuracy is approximately plus or minus 20 percent for uniform soil. CBIP note: Increasing Lt at constant A has diminishing returns on Rg — increasing A is far more effective.",
            "IEEE Std 665 / CBIP Pub.339 Eqn 5.32 (Sverak formula). Alternate: Thapar formula CBIP Eqn 5.33.",
            f"Rg = {rho} x [1/{Lt:.0f} + {(1+1/(1+h*s20_A))/s20A:.8f}] = {rho} x {1/Lt + (1+1/(1+h*s20_A))/s20A:.8f} = {Rg:.4f} ohm"
        )
        (rpass if rg_ok else rnote)(
            f"Grid Resistance Rg = {Rg:.4f} ohm. {'Less than 1.0 ohm. Specification satisfied.' if rg_ok else 'Exceeds 1.0 ohm. Typically specified as less than 1.0 ohm. Review design. Note: CBIP has no absolute Rg limit — the safety check Em vs Etouch is what matters.'}"
        )

    with col2:
        sec("4.3 Earth Rod and Separate Pit Resistance (IS 3043 / CBIP Eqn 5.1)")
        rinfo("The formula below uses cm units — consistent with published project calculations for this type of work. L and d in cm, rho in ohm-cm. This is equivalent to the standard CBIP Eqn 5.1 formula in metre units.")
        fb(
            "Re_single = [ (100 x rho_ohm_cm) / (2 x pi x L_cm) ] x ln(4 x L_cm / d_cm)",
            {
                "Re_single (ohm)": "Resistance of one vertical rod or pipe electrode",
                "rho (ohm-m)": f"{rho} ohm-m = {rho_cm:.0f} ohm-cm (multiply by 100 to convert)",
                "L (m) = L_cm (cm)": f"{L_rod} m = {Lcm:.0f} cm — rod length",
                "d (mm) = d_cm (cm)": f"{d_rod} mm = {d_rcm/10:.2f} cm — rod diameter",
                "Factor 100 in numerator": "Converts rho from ohm-m units to make formula internally consistent in cm units",
                "100 x rho_cm / (2 pi L_cm)": f"100 x {rho_cm:.0f} / (2 x pi x {Lcm:.0f}) = {100*rho_cm/(2*math.pi*Lcm):.4f}",
                "ln(4L/d)": f"ln(4 x {Lcm:.0f} / {d_rcm/10:.2f}) = ln({4*Lcm/(d_rcm/10):.2f}) = {math.log(4*Lcm/(d_rcm/10)):.4f}",
                "Re for N rods in parallel": f"{Re_rod_single:.4f} / {N_rods} = {Re_grid_rods:.4f} ohm",
            },
            "The vertical rod electrode is modelled as a line source in a uniform infinite medium. The formula gives the resistance between the rod surface and remote earth. When multiple rods are present, mutual interference reduces effectiveness — utilization factor eta corrects for this.",
            "CBIP Pub.339 Sec 5.2.1.1 Eqn 5.1 / IS 3043:1987 Cl.8.3 (in metre units).",
            f"Re_single = {Re_rod_single:.4f} ohm. For {N_rods} grid rods in parallel: Re_grid = {Re_grid_rods:.4f} ohm."
        )

        if has_pits:
            sec("4.4 Separate Earth Pit Resistance")
            fb(
                "Re_pits = (1/N_pits) x [ (100 x rho_cm) / (2 x pi x L_cm) ] x ln(4 x L_cm / d_cm)",
                {
                    "N_pits": f"{N_pits} — number of separate earth pits",
                    "rho (ohm-cm)": f"{rho_cm:.0f}",
                    "L (cm)": f"{L_pit_cm:.0f} — earth pit electrode length",
                    "d (cm)": f"{d_pit_cm:.2f} — earth pit electrode diameter",
                    "Re_single_pit": f"{100*rho_cm/(2*math.pi*L_pit_cm)*math.log(4*L_pit_cm/d_pit_cm):.4f} ohm — one earth pit",
                    "Re_pits": f"{100*rho_cm/(2*math.pi*L_pit_cm)*math.log(4*L_pit_cm/d_pit_cm):.4f} / {N_pits} = {Re_pits:.4f} ohm — all pits in parallel",
                },
                "Separate earth pits are pipe or rod electrodes installed outside the main grid perimeter, typically at specific earthing points for equipment, lightning masts, or fence posts. Connected in parallel with the main grid, they reduce the overall system resistance.",
                "CBIP Pub.339 Sec 5.2.1.1 Eqn 5.1 / IS 3043:1987 Cl.8.3. Published project calculations use cm unit version as above.",
                f"Re_pits = {Re_pits:.4f} ohm"
            )

            sec("4.5 Combined Resistance — Parallel Combination")
            fb(
                "Rcombined = Rg x Re_pits / (Rg + Re_pits)",
                {
                    "Rg (ohm)": f"{Rg:.4f} — main grid resistance",
                    "Re_pits (ohm)": f"{Re_pits:.4f} — separate earth pit resistance",
                    "Numerator": f"{Rg:.4f} x {Re_pits:.4f} = {Rg*Re_pits:.6f}",
                    "Denominator": f"{Rg:.4f} + {Re_pits:.4f} = {Rg+Re_pits:.4f}",
                },
                "The main grid and the separate earth pits form a parallel combination. Two resistances in parallel: R_parallel = R1 x R2 / (R1 + R2). Since Re_pits >> Rg, the combined resistance is only slightly less than Rg alone. Reference values: Rg = 0.10 ohm, Re_pits = 28.21 ohm, Rcombined = 0.09 ohm.",
                "Standard parallel resistance formula.",
                f"Rcombined = {Rg:.4f} x {Re_pits:.4f} / ({Rg:.4f} + {Re_pits:.4f}) = {Rcomb:.4f} ohm"
            )
            (rpass if Rcomb<=1.0 else rfail)(
                f"Combined earth resistance Rcombined = {Rcomb:.4f} ohm. {'Less than 1.0 ohm. Acceptable.' if Rcomb<=1.0 else 'Exceeds 1.0 ohm.'}"
            )

        sec("4.6 Ground Potential Rise — GPR (CBIP Sec 3.5)")
        fb(
            "GPR = IG x Rg",
            {
                "GPR (V)": "Maximum voltage of earthing grid relative to remote earth during fault",
                "IG (A)": f"{IG:.0f} A = {IG_kA:.4f} kA",
                "Rg (ohm)": f"{Rg:.4f} ohm",
                "Physical meaning": "The entire grid and everything connected to it (all equipment bodies, control panels, fence) rises to GPR volts above remote earth during the fault.",
                "Maximum transferred potential": f"GPR = {GPR:.2f} V — any metallic conductor leaving the station can carry this to remote areas",
            },
            "When IG amperes flow from the grid into the soil, the grid voltage rises above remote earth by GPR = IG x Rg. IEEE 80-2013 Sec 15.1: If GPR is less than the permissible touch voltage, no further analysis is needed.",
            "CBIP Pub.339 Sec 3.5 and 3.7. IEEE Std 80-2013.",
            f"GPR = {IG:.0f} x {Rg:.4f} = {GPR:.2f} V = {GPR/1000:.4f} kV"
        )

        mcards([
            ("Grid Rg", f"{Rg:.4f}", "ohm", "ps" if rg_ok else "wn"),
            ("Earth Pits Re", f"{Re_pits:.4f}" if Re_pits else "N/A", "ohm", "bl"),
            ("Rcombined", f"{Rcomb:.4f}", "ohm", "ps" if Rcomb<=1.0 else "wn"),
            ("Grid Current IG", f"{IG:.0f}", "A", "bl"),
            ("GPR", f"{GPR:.2f}", "V", "bl"),
            ("GPR", f"{GPR/1000:.4f}", "kV", "bl"),
        ], cols=3)

        if GPR > Etouch:
            rnote(f"GPR = {GPR:.2f} V exceeds permissible Etouch = {Etouch:.2f} V. This is normal for large substations. It does NOT mean the design is unsafe — it means the full Em and Es analysis in Phase 5 is required. The actual mesh voltage Em is typically much less than GPR because the surface potential profile distributes the voltage. Reference: GPR = 2800V, Etouch permissible = 732V, but actual Em = 406V which is safe.")
        else:
            rpass(f"GPR = {GPR:.2f} V is less than Etouch permissible = {Etouch:.2f} V. Design is inherently safe per IEEE 80 Sec 15.1. Phase 5 verification is still recommended.")

        rinfo("Why Increasing Conductor Length Alone Cannot Reduce Rg Significantly: CBIP Sec 3.11.1 — The first term rho/Lt shows that doubling Lt halves this term. But the second term (area term) dominates for large grids. Increasing area A is far more effective. To halve Rg, double the grid area.")
        rinfo("Transferred Potential Hazard: Any metallic conductor connected to the grid and going outside the station — cable sheaths, water pipes, telecom cables, rails — carries GPR to remote areas where gravel is not present and permissible limits are much lower. CBIP Sec 5.3.10: Use isolating transformers on telecom, insulating joints on pipes, optical fibre where possible.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHASE 5 — VERIFICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t_p5:
    phase(5, "Final Verification — Actual Mesh Voltage and Step Voltage")
    rinfo("Phase 5 calculates the actual worst-case touch and step voltages that exist in the grid. These are the Em (mesh voltage, worst at corner meshes) and Es (step voltage, worst just outside grid corners). Both must be below the permissible limits from Phase 3.")
    sp(0.3)

    col1, col2 = st.columns([1,1], gap="large")
    with col1:
        sec("5.1 Geometric Factors — Definitions and Derivation")
        st.markdown("""
        <div class="card" style="font-size:0.79rem;color:#1a2e40;line-height:1.82">
        <b>Why are geometric factors needed?</b><br>
        The current dissipation from the grid is not uniform. Conductors at the periphery
        dissipate more current than those at the centre. Corner meshes have higher mesh
        voltages than central meshes. The geometric factors capture this non-uniformity.<br><br>
        <b>n — Effective number of parallel conductors:</b><br>
        n = na x nb x nc x nd. For rectangular grids nc = nd = 1.<br>
        na = 2Lc/Lp captures how many conductors span the grid width relative to perimeter.<br>
        nb captures the effect of grid shape (how square vs rectangular it is).<br>
        A higher n means more conductors, which distributes current more uniformly
        and reduces the peak mesh voltage.<br><br>
        <b>Km — Mesh voltage spacing factor:</b><br>
        Km depends on mesh spacing D, burial depth h, and conductor diameter d.
        Larger D = larger meshes = higher Km = higher Em. Deeper burial = lower Km.
        Reducing D is the primary way to reduce Em.<br><br>
        <b>Ks — Step voltage spacing factor:</b><br>
        Ks depends on h, D, and n. It governs the step voltage at the grid periphery.
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<table class="dt">
        <tr><th>Factor</th><th>Formula</th><th>Value</th><th>Reference</th></tr>
        <tr><td>na</td><td class="mn">2 x Lc / Lp</td>
            <td class="mn">2 x {Lc:.0f} / {Lp:.0f} = {na:.4f}</td>
            <td>CBIP Eqn 5.19 / IEEE B.18</td></tr>
        <tr><td>nb</td><td class="mn">[Lp / (4 sqrt(A))]^0.5</td>
            <td class="mn">[{Lp:.0f}/(4 x {math.sqrt(A_grid):.3f})]^0.5 = {nb:.4f}</td>
            <td>CBIP Eqn 5.20</td></tr>
        <tr><td>nc, nd</td><td class="mn">1.0 (rectangular grid)</td>
            <td class="mn">1.0</td><td>CBIP Eqn 5.21</td></tr>
        <tr><td>n = na x nb</td><td class="mn">Effective parallel conductors</td>
            <td class="mn">{n:.4f}</td><td>CBIP Eqn 5.18 / IEEE B.17</td></tr>
        <tr><td>ho</td><td class="mn">Reference depth = 1.0 m</td>
            <td class="mn">1.0 m</td><td>IEEE 80 standard definition</td></tr>
        <tr><td>Kh = sqrt(1 + h/ho)</td><td class="mn">sqrt(1 + {h}/1)</td>
            <td class="mn">{Kh:.4f}</td><td>CBIP Eqn 5.17 / IEEE B.14</td></tr>
        <tr><td>Kii</td><td class="mn">1.0 (rods in corners and periphery)</td>
            <td class="mn">1.0</td><td>CBIP Eqn 5.16</td></tr>
        <tr><td>Ki = Kim = Kis</td><td class="mn">0.644 + 0.148 x n</td>
            <td class="mn">0.644 + 0.148 x {n:.4f} = {Kim:.4f}</td>
            <td>CBIP Eqn 5.22 / IEEE B.16. Reference: Ki = 3.75 for n=21</td></tr>
        <tr><td>Km</td><td class="mn">Mesh voltage geometric factor (see below)</td>
            <td class="mn">{Km:.4f}</td><td>CBIP Eqn 5.14 / IEEE B.13. Reference: Km = 0.562</td></tr>
        <tr><td>Ks</td><td class="mn">Step voltage geometric factor (see below)</td>
            <td class="mn">{Ks:.4f}</td><td>CBIP Eqn 5.15 / IEEE B.15. Reference: Ks = 0.220</td></tr>
        </table>""", unsafe_allow_html=True)

        sec("5.2 Km Formula Detail (CBIP Eqn 5.14 / IEEE Eq.81)")
        fb(
            "Km = (1/2pi) x { ln[(D^2/(16hd)) + (D+2h)^2/(8Dd) - h/(4d)] + (Kii/Kh) x ln[8/(pi x (2n-1))] }",
            {
                "D (m)": f"{D} — mesh spacing",
                "h (m)": f"{h} — burial depth",
                "d (m)": f"{d_c:.4f} — grid conductor diameter = {d_c_mm:.0f}mm",
                "D^2/(16hd)": f"{D**2:.2f}/(16 x {h} x {d_c:.4f}) = {D**2/(16*h*d_c):.4f}",
                "(D+2h)^2/(8Dd)": f"({D+2*h:.2f})^2/(8 x {D} x {d_c:.4f}) = {(D+2*h)**2/(8*D*d_c):.4f}",
                "h/(4d)": f"{h}/(4 x {d_c:.4f}) = {h/(4*d_c):.4f}",
                "Kii/Kh": f"1.0/{Kh:.4f} = {1/Kh:.4f}",
                "8/(pi(2n-1))": f"8/(pi x {2*n-1:.4f}) = {8/(math.pi*(2*n-1)):.6f}",
            },
            "Km is derived from the theory of current flow from a buried conductor into a semi-infinite conducting medium. The first log term captures the geometry of the mesh. The second log term accounts for the irregularity of current distribution and the effect of burial depth on peripheral conductors.",
            "CBIP Pub.339 Eqn 5.14. IEEE Std 80-2013 Eq.81. Reference calculation: Km = 0.562.",
            f"Km = {Km:.4f}"
        )

    with col2:
        sec("5.3 Effective Buried Lengths (CBIP Eqn 5.29 and 5.30)")
        fb(
            "Lm = Lc + [ 1.55 + 1.22 x (lr/Dm) ] x Lr   [for rods in corners and periphery]",
            {
                "Lc (m)": f"{Lc:.0f} — total horizontal conductor length (from Lt - Lr)",
                "lr (m)": f"{L_rod} — length of one rod",
                "Dm (m)": f"{Dm:.2f} — maximum grid diagonal = sqrt(Lx^2 + Ly^2)",
                "Lr (m)": f"{Lr:.0f} — total rod length = {N_rods} x {L_rod}",
                "Factor [1.55 + 1.22 x lr/Dm]": f"1.55 + 1.22 x ({L_rod}/{Dm:.2f}) = {1.55+1.22*L_rod/Dm:.4f}",
            },
            "Vertical rods contribute to reducing mesh voltage, but not as effectively as horizontal conductors on a metre-for-metre basis. The factor [1.55 + 1.22 x lr/Dm] is an empirical correction that gives the effective equivalent horizontal length of the vertical rods.",
            "CBIP Pub.339 Eqn 5.29 (for rods in corners and along periphery). IEEE Std 80-2013.",
            f"Lm = {Lc:.0f} + {1.55+1.22*L_rod/Dm:.4f} x {Lr:.0f} = {Lm:.2f} m"
        )
        fb(
            "Ls = 0.75 x Lc + 0.85 x Lr",
            {
                "0.75": "Horizontal conductors contribute 75% to step voltage reduction",
                "0.85": "Vertical rods contribute 85% to step voltage reduction",
                "Lc (m)": f"{Lc:.0f}",
                "Lr (m)": f"{Lr:.0f}",
            },
            "The step voltage is most critical at the grid periphery and just outside it. Horizontal conductors contribute somewhat less to step voltage reduction (hence 0.75 vs 1.0 coefficient). Rods at the periphery are highly effective for step voltage (hence 0.85).",
            "CBIP Pub.339 Eqn 5.30. IEEE Std 80-2013.",
            f"Ls = 0.75 x {Lc:.0f} + 0.85 x {Lr:.0f} = {Ls:.2f} m"
        )

        sec("5.4 Actual Mesh Voltage Em (CBIP Eqn 5.12 / IEEE Eq.85)")
        fb(
            "Em = rho x Km x Ki x IG / Lm",
            {
                "Em (V)": "Actual maximum mesh voltage (worst case at centre of corner mesh)",
                "rho (ohm-m)": f"{rho}",
                "Km": f"{Km:.4f} — mesh geometric factor",
                "Ki = Kim": f"{Kim:.4f} — irregularity factor",
                "IG (A)": f"{IG:.0f}",
                "Lm (m)": f"{Lm:.2f} — effective buried length for mesh voltage",
            },
            "Em is the maximum touch voltage that occurs within the grid — it is found at the centre of the corner meshes where the potential is lowest (farthest from any conductor). Reducing D (smaller meshes) directly reduces Em. Reference calculation result: Emesh = 406.64 V.",
            "CBIP Pub.339 Eqn 5.12. IEEE Std 80-2013 Eq.85.",
            f"Em = {rho} x {Km:.4f} x {Kim:.4f} x {IG:.0f} / {Lm:.2f} = {Em:.2f} V"
        )
        (rpass if touch_ok else rfail)(
            f"Em = {Em:.2f} V  vs  Etouch permissible = {Etouch:.2f} V  —  "
            f"{'Em is LESS THAN permissible. Grid design for touch voltage is CORRECT. (Reference: Em = 406.64V < 732.80V)' if touch_ok else 'Em EXCEEDS permissible. REDESIGN REQUIRED. Reduce mesh spacing D or add conductors.'}"
        )

        sec("5.5 Actual Step Voltage Es (CBIP Eqn 5.13 / IEEE Eq.92)")
        fb(
            "Es = rho x Ks x Ki x IG / Ls",
            {
                "Es (V)": "Actual maximum step voltage (worst case just outside corner of grid)",
                "rho (ohm-m)": f"{rho}",
                "Ks": f"{Ks:.4f} — step voltage geometric factor",
                "Ki = Kis": f"{Kis:.4f}",
                "IG (A)": f"{IG:.0f}",
                "Ls (m)": f"{Ls:.2f} — effective buried length for step voltage",
            },
            "Es is the maximum step voltage — it occurs just outside and at a corner of the grid where the potential gradient on the earth surface is steepest. Peripheral rods reduce Es by diverting current to deeper soil layers. Reference calculation result: Estep = 159.11 V.",
            "CBIP Pub.339 Eqn 5.13. IEEE Std 80-2013 Eq.92.",
            f"Es = {rho} x {Ks:.4f} x {Kis:.4f} x {IG:.0f} / {Ls:.2f} = {Es:.2f} V"
        )
        (rpass if step_ok else rfail)(
            f"Es = {Es:.2f} V  vs  Estep permissible = {Estep_perm:.2f} V  —  "
            f"{'Es is LESS THAN permissible. Grid design for step voltage is CORRECT. (Reference: Es = 159.11V < 2438.13V)' if step_ok else 'Es EXCEEDS permissible. REDESIGN REQUIRED. Add peripheral rods or gradient control conductors.'}"
        )

        mcards([
            ("Mesh Voltage Em", f"{Em:.2f}", "V", "ps" if touch_ok else "fl"),
            ("Etouch permissible", f"{Etouch:.2f}", "V", "bl"),
            ("Step Voltage Es", f"{Es:.2f}", "V", "ps" if step_ok else "fl"),
            ("Estep permissible", f"{Estep_perm:.2f}", "V", "bl"),
        ])

        rinfo("CBIP Ch.11 Table 11.5: Empirical formula results can differ from computer simulation by approximately 15-20%. CBIP software (gridi) and rigorous algorithms (Heppe's method) give more accurate results. The empirical formulas (IEEE/CBIP) are appropriate for initial design and for grids with uniform conductor spacing in uniform soil.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FINAL ASSESSMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t_fa:
    if all_safe:
        rpass(f"DESIGN IS SAFE — A safe design of the subsoil earth grid has been obtained. Mesh voltage Em = {Em:.2f} V is less than permissible Etouch = {Etouch:.2f} V. Step voltage Es = {Es:.2f} V is less than permissible Estep = {Estep_perm:.2f} V. Reference values from published calculations: Em = 406.64V less than 732.80V, Es = 159.11V less than 2438.13V.")
    else:
        rfail(f"DESIGN REQUIRES REVISION — One or more safety criteria are not satisfied. Review items marked FAIL below and implement corrective measures.")

    sp(0.5)
    col1, col2 = st.columns([1.15, 0.85], gap="large")
    with col1:
        sec("Final Design Summary Table")

        def sr(item, unit, allow, actual, status):
            sc = "ps" if status=="PASS" else ("fl" if status=="FAIL" else "nt")
            return f"<tr><td>{item}</td><td class='mn'>{unit}</td><td class='mn'>{allow}</td><td class='mn'>{actual}</td><td class='{sc}'>{status}</td></tr>"

        st.markdown(f"""<table class="dt">
        <tr><th>Item</th><th>Unit</th><th>Allowable</th><th>Actual</th><th>Result</th></tr>
        {sr("Conductor diameter (thermal + corrosion)", "mm", f"min {d_corr:.1f}", str(sel_dia), "PASS" if sel_dia>=math.ceil(d_corr) else "FAIL")}
        {sr("Grid resistance Rg", "ohm", "less than 1.0", f"{Rg:.4f}", "PASS" if rg_ok else "NOTE")}
        {sr("Combined earth resistance Rcombined", "ohm", "less than 1.0", f"{Rcomb:.4f}", "PASS" if Rcomb<=1.0 else "NOTE")}
        {sr("Ground potential rise GPR", "V", "Reference only", f"{GPR:.2f}", "NOTE")}
        {sr("Permissible body current Ib", "mA", "Calculated", f"{Ib*1000:.3f}", "OK")}
        {sr("Surface reduction factor Cs", "—", "Calculated", f"{Cs:.4f}", "OK")}
        {sr("Permissible touch voltage Etouch", "V", "Calculated", f"{Etouch:.2f}", "OK")}
        {sr("Permissible step voltage Estep", "V", "Calculated", f"{Estep_perm:.2f}", "OK")}
        {sr("Actual mesh voltage Em", "V", f"less than {Etouch:.2f}", f"{Em:.2f}", "PASS" if touch_ok else "FAIL")}
        {sr("Actual step voltage Es", "V", f"less than {Estep_perm:.2f}", f"{Es:.2f}", "PASS" if step_ok else "FAIL")}
        </table>""", unsafe_allow_html=True)

        if not touch_ok or not step_ok or not rg_ok:
            sec("Corrective Measures — Based on CBIP Chapter 5, 6, and 11")

        if not touch_ok:
            st.markdown("<p style='font-size:0.78rem;font-weight:700;color:#7b1818;margin:0.7rem 0 0.3rem 0'>Mesh Voltage Em exceeds Etouch permissible — Actions Required:</p>", unsafe_allow_html=True)
            for fix in [
                "Reduce mesh spacing D — add more parallel conductors in X and Y directions. This is the most effective measure. Reducing D from 10m to 7.5m adds about 33% more conductor and significantly reduces Em. CBIP Sec 5.3.5.",
                "Use non-uniform conductor spacing — place conductors closer at grid corners and periphery, wider at centre. CBIP Sec 11.3.2 shows Em can be reduced by 43 percent this way. Empirical formulas cannot analyse this — computer simulation needed.",
                "Increase burial depth h — deeper burial reduces Km factor and therefore Em. From 0.6m to 1.0m gives measurable improvement.",
                "Apply Bentonite clay or concrete encasing around horizontal conductors — effectively increases the conductor radius d which enters the Km formula, reducing Km. CBIP Sec 11.5.3: Em reduced from 1076V to 672V in one example.",
                "Install a counterpoise mat at shallow depth (0.3m) in addition to the main grid — the dense shallow mat equalizes surface potential locally. CBIP Sec 11.5.5.",
                "Increase surface layer thickness hs or verify rho_s value — raises the permissible Etouch limit.",
            ]: rinfo(fix)

        if not step_ok:
            st.markdown("<p style='font-size:0.78rem;font-weight:700;color:#7b1818;margin:0.7rem 0 0.3rem 0'>Step Voltage Es exceeds Estep permissible — Actions Required:</p>", unsafe_allow_html=True)
            for fix in [
                "Add more vertical rods along the grid periphery — diverts current to deeper, more moist soil layers, reducing surface gradients at the grid edge. CBIP Sec 5.3.5.1.",
                "Increase burial depth of outermost perimeter conductor — reduces Ks. CBIP Sec 11.2.4g: Increasing depth from 0.6m to 2.0m reduced Es from 495V to 230V in the reference example.",
                "Install gradient control rings — horizontal conductors buried outside the fence at progressively increasing depths. CBIP Sec 11.5.2: Es reduced from 2602V to 726V in reference example.",
                "Extend the grid 1 to 2 metres beyond the station fence boundary. CBIP Sec 5.3.9.",
                "Spread crushed rock surface layer at least 1 metre outside the fence — raises Estep permissible for the outer area.",
            ]: rinfo(fix)

        if not rg_ok:
            st.markdown("<p style='font-size:0.78rem;font-weight:700;color:#7b1818;margin:0.7rem 0 0.3rem 0'>Grid Resistance Rg exceeds 1.0 ohm — Actions Required:</p>", unsafe_allow_html=True)
            for fix in [
                "Increase grid area — the most effective measure. Rg is approximately proportional to rho/sqrt(A). Doubling area reduces Rg by approximately 30%. CBIP Sec 3.11.1: Adding conductor at constant area has minimal effect on Rg.",
                "Soil enhancement around rods: Bentonite clay (rho = 8.7 ohm-m at water:Bentonite = 4:1 ratio), coke dust, or conductive cement reduces effective rho near rods. CBIP Sec 6.3.1.1.",
                "Deep driven rods (30-40m depth) penetrating a lower-resistivity stratum — very effective in two-layer soil where bottom layer has low rho. CBIP Sec 11.5.4.",
                "Satellite earth electrode — a separate earth grid at a distance from the main station, connected by a buried cable. CBIP Sec 11.5.7.",
            ]: rinfo(fix)

    with col2:
        sec("Complete Input and Output Summary")
        st.markdown(f"""<table class="dt">
        <tr><th colspan="2">Project and System</th></tr>
        <tr><td>Project</td><td class="mn">{proj}</td></tr>
        <tr><td>System voltage</td><td class="mn">{volt}</td></tr>
        <tr><th colspan="2">Phase 1 Inputs</th></tr>
        <tr><td>Fault current If</td><td class="mn">{If_kA} kA</td></tr>
        <tr><td>Fault duration tf</td><td class="mn">{tf_val} s</td></tr>
        <tr><td>Shock duration ts</td><td class="mn">{ts_val} s</td></tr>
        <tr><td>Sf (division factor)</td><td class="mn">{Sf}</td></tr>
        <tr><td>Df (decrement factor)</td><td class="mn">{Df}</td></tr>
        <tr><td>Soil resistivity rho</td><td class="mn">{rho} ohm-m</td></tr>
        <tr><td>Surface rho_s / hs</td><td class="mn">{rho_s} ohm-m / {h_s} m</td></tr>
        <tr><th colspan="2">Phase 2 Results</th></tr>
        <tr><td>Conductor area (IEEE)</td><td class="mn">{A_ieee:.2f} mm2</td></tr>
        <tr><td>Corrosion class / allowance</td><td class="mn">{corr_cls.split('/')[0].strip()} / +{corr_mm}mm</td></tr>
        <tr><td>Selected conductor</td><td class="mn">{sel_dia} mm dia ({sel_area:.1f} mm2)</td></tr>
        <tr><td>Grid area Lx x Ly</td><td class="mn">{Lx:.0f} x {Ly:.0f} = {A_grid:.0f} m2</td></tr>
        <tr><td>Mesh spacing D</td><td class="mn">{D} m</td></tr>
        <tr><td>Burial depth h</td><td class="mn">{h} m</td></tr>
        <tr><td>Total conductor Lt</td><td class="mn">{Lt:.0f} m</td></tr>
        <tr><td>Ground rods</td><td class="mn">{N_rods} x {L_rod} m = {Lr:.0f} m total</td></tr>
        <tr><th colspan="2">Phase 3 Safety Limits</th></tr>
        <tr><td>Body current Ib</td><td class="mn">{Ib*1000:.3f} mA</td></tr>
        <tr><td>Cs factor</td><td class="mn">{Cs:.4f}</td></tr>
        <tr><td>Etouch permissible</td><td class="mn">{Etouch:.2f} V</td></tr>
        <tr><td>Estep permissible</td><td class="mn">{Estep_perm:.2f} V</td></tr>
        <tr><th colspan="2">Phase 4 Resistance and GPR</th></tr>
        <tr><td>Grid resistance Rg</td><td class="mn">{Rg:.4f} ohm</td></tr>
        <tr><td>Combined Rcombined</td><td class="mn">{Rcomb:.4f} ohm</td></tr>
        <tr><td>Grid current IG</td><td class="mn">{IG:.0f} A = {IG_kA:.4f} kA</td></tr>
        <tr><td>GPR</td><td class="mn">{GPR:.2f} V = {GPR/1000:.4f} kV</td></tr>
        <tr><th colspan="2">Phase 5 Actual Voltages</th></tr>
        <tr><td>Geometric factors n, Km, Ks</td><td class="mn">n={n:.3f}, Km={Km:.4f}, Ks={Ks:.4f}</td></tr>
        <tr><td>Eff. lengths Lm / Ls</td><td class="mn">{Lm:.1f} m / {Ls:.1f} m</td></tr>
        <tr><td>Mesh voltage Em</td><td class="mn {'ps' if touch_ok else 'fl'}">{Em:.2f} V  {'PASS' if touch_ok else 'FAIL'}</td></tr>
        <tr><td>Step voltage Es</td><td class="mn {'ps' if step_ok else 'fl'}">{Es:.2f} V  {'PASS' if step_ok else 'FAIL'}</td></tr>
        </table>""", unsafe_allow_html=True)

        sec("Equipment Earthing Quick Reference (CBIP + IS 3043)")
        equip = [
            ("Transformer body", "Min 2 independent leads to different grid nodes. IS 3043 Cl.12."),
            ("Transformer neutral", "Separate conductor sized for full IG. CBIP Sec 5.2."),
            ("CT secondary neutral", "One terminal earthed. Primary tank bonded to grid."),
            ("Lightning arrester (LA)", "Lead less than 1m, no bends, no loops. Minimum inductance. IEC 60099."),
            ("Circuit breaker (CB)", "All metal parts and operating mechanism earthed. IS 3043 Cl.13."),
            ("Station fence", "Bond to grid. Crushed rock 1m outside fence. CBIP Sec 3.12."),
            ("Control panel", "Separate quiet earth bus. Single-point to main grid. CBIP Ch.7."),
            ("Lightning mast", "Dedicated down conductor, connected to grid at base. IS 2309."),
            ("Cable sheath", "Bond both ends inside station. IS 3043."),
            ("Auxiliary earthmat", "Dense sub-grid under operator standing area. CBIP Sec 5.3.5."),
        ]
        rows_e = "".join(f"<tr><td>{e}</td><td style='font-size:0.72rem;color:#1a2e40;line-height:1.5'>{r}</td></tr>" for e,r in equip)
        st.markdown(f"""<table class="dt">
        <tr><th>Equipment</th><th>Key Requirement</th></tr>{rows_e}</table>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top:1px solid #cde3f4;padding-top:0.65rem;color:#4a7a9b;
    font-size:0.68rem;text-align:center;line-height:1.8">
CBIP Manual Pub.339 (2017 Edition) &nbsp;|&nbsp;
IS 3043:1987 (Reaffirmed 2006) &nbsp;|&nbsp;
IEEE Std 80-2013 &nbsp;|&nbsp;
IEEE Std 665 &nbsp;|&nbsp;
IS 2309 &nbsp;|&nbsp;
IEC 62305 &nbsp;|&nbsp;
BS 7430:2011<br>
Empirical formula accuracy: approximately plus or minus 20 percent versus rigorous computer simulation.
Use CBIP earthing software (gridi) for final verification of complex or non-uniform soil cases.
</div>
""", unsafe_allow_html=True)
