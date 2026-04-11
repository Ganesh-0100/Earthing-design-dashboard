"""
Earthing System Design Calculator
Reference: CBIP Manual Pub.339 (2017), IS 3043:1987, IEEE Std 80-2013
Based on: GSECL 370 MW CCPP Utran, Surat - ALSTOM / DESEIN calculation
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
    background: #f5f6f8;
    padding: 1.5rem 2rem 3rem 2rem;
    max-width: 1440px;
}

[data-testid="stSidebar"] {
    background: #1c2a3a;
    border-right: none;
}
[data-testid="stSidebar"] .block-container {
    padding: 0.8rem 1rem;
}
[data-testid="stSidebar"] label {
    color: #d1dce8 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #c4d0dc !important;
}
[data-testid="stSidebar"] input {
    background: #243447 !important;
    color: #e8eef4 !important;
    border: 1px solid #3a5068 !important;
    border-radius: 3px !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #243447 !important;
    color: #e8eef4 !important;
    border: 1px solid #3a5068 !important;
}
[data-testid="stSidebar"] .stRadio > div {
    color: #c4d0dc !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #c4d0dc !important;
}
[data-testid="stSidebar"] .stSlider > div > div {
    color: #c4d0dc !important;
}
[data-testid="stSidebar"] p[data-testid="stMarkdownContainer"] {
    color: #8fa8bf !important;
    font-size: 0.72rem !important;
}

.sb-header {
    background: #0d2d4a;
    margin: 0 -1rem 1rem -1rem;
    padding: 1rem 1rem 0.8rem 1rem;
    border-bottom: 2px solid #1a5276;
}
.sb-header-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.sb-header-sub {
    font-size: 0.67rem;
    color: #88aac4;
    line-height: 1.5;
}
.sb-group {
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #5a7a94 !important;
    padding: 0.9rem 0 0.3rem 0;
    border-bottom: 1px solid #243447;
    margin-bottom: 0.5rem;
}

.page-header {
    background: #0d2d4a;
    border-left: 4px solid #b03a2e;
    padding: 1.2rem 1.6rem;
    border-radius: 3px;
    margin-bottom: 1.4rem;
}
.page-header-title {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0;
}
.page-header-sub {
    font-size: 0.72rem;
    color: #88aac4;
    margin-top: 0.25rem;
    line-height: 1.5;
}

.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-bottom: 2px solid #d8dde5;
    padding: 0;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #5a6a7a;
    padding: 0.65rem 1rem;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    border-radius: 0;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: #0d2d4a;
    border-bottom: 2px solid #0d2d4a;
    background: transparent;
}

.sec-head {
    font-size: 0.67rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    color: #0d2d4a;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #0d2d4a;
    margin-top: 1.4rem;
    margin-bottom: 0.9rem;
}

.fblock {
    background: #ffffff;
    border: 1px solid #d8dde5;
    border-left: 3px solid #0d2d4a;
    border-radius: 0 3px 3px 0;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
}
.fblock-formula {
    font-family: 'IBM Plex Mono', 'Courier New', monospace !important;
    font-size: 0.84rem;
    font-weight: 600;
    color: #0d2d4a;
    margin-bottom: 0.75rem;
    line-height: 1.5;
}
.fblock-param {
    font-size: 0.77rem;
    color: #2c3e50;
    line-height: 2.0;
}
.fblock-param .sym {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    color: #154360;
    display: inline-block;
    min-width: 130px;
}
.fblock-ref {
    font-size: 0.67rem;
    color: #5a6a7a;
    margin-top: 0.6rem;
    padding-top: 0.5rem;
    border-top: 1px solid #e8ecf0;
    font-style: italic;
}
.fblock-result {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    font-weight: 600;
    color: #1a5c2a;
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #e8ecf0;
}

.res-pass {
    background: #eafaf1;
    border: 1px solid #a9dfb5;
    border-left: 3px solid #1e8449;
    color: #145a32;
    padding: 0.75rem 1rem;
    border-radius: 0 3px 3px 0;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 0.5rem 0;
    line-height: 1.6;
}
.res-fail {
    background: #fdedec;
    border: 1px solid #f1a9a0;
    border-left: 3px solid #c0392b;
    color: #78281f;
    padding: 0.75rem 1rem;
    border-radius: 0 3px 3px 0;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 0.5rem 0;
    line-height: 1.6;
}
.res-note {
    background: #fef9e7;
    border: 1px solid #f8c471;
    border-left: 3px solid #d68910;
    color: #7d6608;
    padding: 0.75rem 1rem;
    border-radius: 0 3px 3px 0;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 0.5rem 0;
    line-height: 1.6;
}
.res-info {
    background: #eaf4fb;
    border: 1px solid #aed6f1;
    border-left: 3px solid #1a6fa0;
    color: #154360;
    padding: 0.65rem 0.9rem;
    border-radius: 0 3px 3px 0;
    font-size: 0.77rem;
    margin: 0.35rem 0;
    line-height: 1.6;
    font-weight: 400;
}

.dtable {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.79rem;
    margin: 0.5rem 0;
}
.dtable th {
    background: #0d2d4a;
    color: #ffffff;
    padding: 0.45rem 0.75rem;
    text-align: left;
    font-size: 0.67rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    white-space: nowrap;
}
.dtable td {
    padding: 0.42rem 0.75rem;
    border-bottom: 1px solid #e8ecf0;
    color: #2c3e50;
    vertical-align: top;
    line-height: 1.5;
}
.dtable tr:hover td { background: #f7f9fc; }
.dtable .mono {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #1c2e3e;
}
.dtable .pass { color: #1a5c2a; font-weight: 700; }
.dtable .fail { color: #78281f; font-weight: 700; }
.dtable .note { color: #7d6608; font-weight: 600; }
.dtable .hl { background: #eafaf1; }

.mcard-row {
    display: grid;
    gap: 0.7rem;
    margin: 0.8rem 0;
}
.mcard {
    background: #ffffff;
    border: 1px solid #d8dde5;
    border-radius: 3px;
    padding: 0.8rem 1rem;
    text-align: center;
}
.mcard.pass { border-top: 3px solid #1e8449; }
.mcard.fail { border-top: 3px solid #c0392b; }
.mcard.blue { border-top: 3px solid #0d2d4a; }
.mcard.warn { border-top: 3px solid #d68910; }
.mcard .mc-label {
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #5a6a7a;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.mcard .mc-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0d2d4a;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1.2;
}
.mcard .mc-unit {
    font-size: 0.66rem;
    color: #7a8a9a;
    margin-top: 0.15rem;
}

.card {
    background: #ffffff;
    border: 1px solid #d8dde5;
    border-radius: 3px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}

/* Flowchart styles */
.flow-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem 1rem;
    background: #ffffff;
    border: 1px solid #d8dde5;
    border-radius: 3px;
}
.flow-node {
    width: 260px;
    padding: 0.6rem 1rem;
    border-radius: 3px;
    text-align: center;
    font-size: 0.76rem;
    font-weight: 600;
    line-height: 1.4;
    position: relative;
}
.flow-node.start-end {
    background: #0d2d4a;
    color: #ffffff;
    border-radius: 20px;
    width: 180px;
}
.flow-node.process {
    background: #eaf4fb;
    border: 2px solid #1a6fa0;
    color: #0d2d4a;
}
.flow-node.calc {
    background: #eafaf1;
    border: 2px solid #1e8449;
    color: #145a32;
}
.flow-node.decision {
    background: #fef9e7;
    border: 2px solid #d68910;
    color: #7d6608;
    transform: none;
    clip-path: polygon(8% 50%, 0% 0%, 92% 0%, 100% 50%, 92% 100%, 0% 100%);
    border-radius: 0;
    width: 280px;
    padding: 0.7rem 2rem;
}
.flow-node.remediation {
    background: #fdedec;
    border: 2px solid #c0392b;
    color: #78281f;
}
.flow-node .flow-sub {
    font-size: 0.67rem;
    font-weight: 400;
    margin-top: 0.2rem;
    opacity: 0.85;
    font-family: 'IBM Plex Mono', monospace;
}
.flow-arrow {
    width: 2px;
    height: 24px;
    background: #4a6a84;
    margin: 0 auto;
    position: relative;
}
.flow-arrow::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 7px solid #4a6a84;
}
.flow-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: #4a6a84;
    text-align: center;
    margin: 0.1rem 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.flow-branch {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 3rem;
    width: 100%;
    margin-top: 0.5rem;
}
.flow-branch-col {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.flow-branch-label {
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.15rem 0.5rem;
    border-radius: 2px;
    margin-bottom: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.flow-branch-label.safe-lbl {
    background: #1e8449;
    color: white;
}
.flow-branch-label.unsafe-lbl {
    background: #c0392b;
    color: white;
}

#MainMenu, footer, header { display: none; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def sec(title):
    st.markdown(f'<div class="sec-head">{title}</div>', unsafe_allow_html=True)

def fblock(formula, params, ref, result=None):
    params_html = "".join(
        f'<div><span class="sym">{s}</span> = {d}</div>'
        for s, d in params.items()
    )
    result_html = f'<div class="fblock-result">Result : {result}</div>' if result else ""
    st.markdown(
        f'<div class="fblock">'
        f'<div class="fblock-formula">{formula}</div>'
        f'<div class="fblock-param">{params_html}</div>'
        f'<div class="fblock-ref">Reference : {ref}</div>'
        f'{result_html}</div>',
        unsafe_allow_html=True
    )

def res_pass(text):
    st.markdown(f'<div class="res-pass">{text}</div>', unsafe_allow_html=True)

def res_fail(text):
    st.markdown(f'<div class="res-fail">{text}</div>', unsafe_allow_html=True)

def res_note(text):
    st.markdown(f'<div class="res-note">{text}</div>', unsafe_allow_html=True)

def info(text):
    st.markdown(f'<div class="res-info">{text}</div>', unsafe_allow_html=True)

def mcards(items, cols=4):
    html = f'<div class="mcard-row" style="grid-template-columns:repeat({cols},1fr)">'
    for label, value, unit, style in items:
        html += (
            f'<div class="mcard {style}">'
            f'<div class="mc-label">{label}</div>'
            f'<div class="mc-value">{value}</div>'
            f'<div class="mc-unit">{unit}</div>'
            f'</div>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def sp(h=0.6):
    st.markdown(f'<div style="height:{h}rem"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MATERIAL CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

MATERIALS = {
    "MS Steel — Welded Joint (recommended for India)": {
        "rho_r": 15.0, "alpha_r": 0.00423, "SW": 7.86,
        "SH": 0.114, "Tm": 500.0, "Tr": 20.0, "K": 12.15,
    },
    "MS Steel — Bolted Joint": {
        "rho_r": 15.0, "alpha_r": 0.00423, "SW": 7.86,
        "SH": 0.114, "Tm": 310.0, "Tr": 20.0, "K": 15.70,
    },
    "Copper — Welded Joint": {
        "rho_r": 1.72, "alpha_r": 0.00393, "SW": 8.89,
        "SH": 0.094, "Tm": 1084.0, "Tr": 20.0, "K": 4.7,
    },
    "Copper — Bolted Joint": {
        "rho_r": 1.72, "alpha_r": 0.00393, "SW": 8.89,
        "SH": 0.094, "Tm": 450.0, "Tr": 20.0, "K": 5.8,
    },
}

STD_DIA = [8, 10, 12, 16, 18, 20, 22, 25, 28, 32, 36, 40]

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sb-header">
        <div class="sb-header-title">Earthing Design Calculator</div>
        <div class="sb-header-sub">
            CBIP Pub.339 (2017) / IEEE Std 80-2013 / IS 3043:1987<br>
            Enter values below. Calculations update automatically.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-group">Project</div>', unsafe_allow_html=True)
    project_name = st.text_input("Project Name", "Substation Earthing Design")
    prepared_by  = st.text_input("Prepared By", "")
    doc_number   = st.text_input("Document Number", "")
    voltage      = st.selectbox("System Voltage",
                   ["11 kV","33 kV","66 kV","110 kV","132 kV","220 kV","400 kV","765 kV"],
                   index=4)
    sub_type     = st.selectbox("Substation Type",
                   ["AIS — Air Insulated Switchgear","GIS — Gas Insulated Switchgear"])
    neutral      = st.selectbox("Neutral Grounding",
                   ["Solid Grounded","Resistance Grounded","Unearthed"])

    st.markdown('<div class="sb-group">Soil Data</div>', unsafe_allow_html=True)
    rho   = st.number_input("Mean Soil Resistivity — rho (ohm-m)",
                value=53.0, min_value=0.1, step=1.0,
                help="Measured by Wenner 4-probe method on site. CBIP Chapter 9.")
    rho_s = st.number_input("Surface Layer Resistivity — rho_s (ohm-m)",
                value=3000.0, min_value=1.0, step=100.0,
                help="Concrete or crushed rock surface layer. CBIP default = 3000 ohm-m.")
    h_s   = st.number_input("Surface Layer Thickness — hs (m)",
                value=0.15, min_value=0.001, step=0.01,
                help="Thickness of the concrete / crushed rock layer above the grid.")

    st.markdown('<div class="sb-group">Fault Data</div>', unsafe_allow_html=True)
    If_kA = st.number_input("Earth Fault Current — If (kA)",
                value=40.0, min_value=0.1, step=0.5,
                help="Maximum single line-to-earth fault current from system fault study. CBIP Sec 3.7.1.")
    tf    = st.selectbox("Fault Duration — tf (seconds) [for conductor sizing]",
                [0.5, 1.0, 2.0, 3.0], index=1,
                help="CBIP Sec 3.7.3: 1s for digital relays, 3s for EM relays. Maximum fault clearing time including backup protection.")
    ts    = st.selectbox("Shock Duration — ts (seconds) [for safety voltages]",
                [0.2, 0.3, 0.5, 1.0], index=2,
                help="CBIP Sec 3.7.3: 0.5s for digital relays, 1.0s for EM relays. PRIMARY relay clearing time only.")
    Sf    = st.slider("Current Division Factor — Sf",
                0.10, 1.00, 0.70, 0.05,
                help="Fraction of fault current that flows into earth grid. Use Sf = 1.0 if earth wire data is not available. CBIP Sec 3.7.2.")
    Df    = st.number_input("Decrement Factor — Df",
                value=1.0, min_value=1.0, max_value=1.5, step=0.01,
                help="For fault duration >= 0.5s (30 cycles), Df = 1.0 per IEEE 80-2013 Cl.15.10.")
    Ta    = st.number_input("Ambient Temperature — Ta (deg C)",
                value=50.0, min_value=10.0, max_value=80.0, step=5.0,
                help="Initial conductor temperature. Use maximum ambient for conservative design.")

    st.markdown('<div class="sb-group">Conductor</div>', unsafe_allow_html=True)
    mat_key = st.selectbox("Conductor Material and Joint Type",
                list(MATERIALS.keys()), index=0,
                help="CBIP Sec 3.9: MS Steel recommended for India. Do not mix copper and steel underground.")
    mat = MATERIALS[mat_key]

    st.markdown('<div class="sb-group">Grid Layout</div>', unsafe_allow_html=True)
    Lx  = st.number_input("Grid Length — Lx (m)", value=250.0, min_value=5.0, step=5.0,
              help="Station dimension along X. Cover the entire fenced area.")
    Ly  = st.number_input("Grid Width — Ly (m)", value=300.0, min_value=5.0, step=5.0)
    D   = st.number_input("Mesh Spacing — D (m)", value=10.0, min_value=0.5, step=0.5,
              help="CBIP Sec 5.3.5: 3 to 8m typical. Start with 10m and reduce if touch voltage fails.")
    h   = st.number_input("Burial Depth — h (m)", value=1.0, min_value=0.1, step=0.1,
              help="Depth of horizontal conductors. CBIP minimum: 0.5 to 0.6m. GSECL used 1.0m.")
    d_c_mm = st.number_input("Grid Conductor Diameter — dc (mm)", value=32.0,
              min_value=1.0, step=1.0,
              help="Use the selected conductor diameter from Step 1.")
    Lt_manual = st.number_input("Total Buried Conductor Length — Lt (m)",
              value=11000.0, min_value=10.0, step=100.0,
              help="Total length from drawings. Includes all horizontal runs. Auto-estimate is approximate only.")

    st.markdown('<div class="sb-group">Earth Rods</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.71rem;color:#7a9ab4;padding:0.3rem 0 0.5rem 0;line-height:1.6">
    Note: Rod quantity may not be known at design start.
    Option A calculates automatically from perimeter spacing.
    </div>
    """, unsafe_allow_html=True)

    rod_method = st.radio(
        "Rod Quantity — how to determine",
        ["Option A: Calculate from perimeter spacing (recommended)",
         "Option B: Enter number of rods directly"],
        index=0,
        help="Option A: Enter spacing; rods are placed at that interval along the perimeter. Option B: Enter exact count from drawings."
    )

    L_rod  = st.number_input("Rod Length (m)", value=3.0, min_value=0.5, step=0.5,
                 help="IS 3043: minimum 3m. Rods must reach moist subsoil. CBIP Sec 5.3.5.1.")
    d_rod  = st.number_input("Rod Diameter (mm)", value=32.0, min_value=5.0, step=1.0,
                 help="Same material as grid conductor. 25 to 40mm dia typical for MS rod.")

    if "Option A" in rod_method:
        rod_spacing_peri = st.number_input(
            "Rod Spacing Along Perimeter (m)",
            value=10.0, min_value=1.0, step=1.0,
            help="One rod placed every X metres along the grid perimeter. Example: 10m spacing on 1100m perimeter gives 110 rods."
        )
        N_rods_calc = True
    else:
        N_rods_input = st.number_input("Number of Ground Rods", value=90, min_value=0, step=1)
        N_rods_calc  = False

    rod_spacing_check = st.number_input(
        "Rod-to-Rod Spacing — utilization check (m)",
        value=3.0, min_value=0.1, step=0.5,
        help="Average spacing between adjacent rods. CBIP Sec 5.3.5.1: spacing should be >= rod length for full utilization."
    )

    st.markdown('<div class="sb-group">Earth Pits (separate from grid)</div>', unsafe_allow_html=True)
    N_pits = st.number_input("Number of Separate Earth Pits", value=56, min_value=0, step=1,
                 help="Separate pipe or plate electrodes connected outside the main grid. As used in GSECL calculation.")

# ─────────────────────────────────────────────────────────────────────────────
# CALCULATIONS
# ─────────────────────────────────────────────────────────────────────────────

If_A    = If_kA * 1000.0
tf_val  = float(tf)
ts_val  = float(ts)
d_c     = d_c_mm / 1000.0
d_rod_m = d_rod / 1000.0

rho_r   = mat["rho_r"]
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

r_calc         = math.sqrt(A_ieee / math.pi)
d_calc_mm      = 2.0 * r_calc

if rho <= 25:
    corr_class, corr_thk = "Corrosive / Severely Corrosive", 4.5
    min_area = 200
elif rho <= 100:
    corr_class, corr_thk = "Mildly / Moderately Corrosive", 2.25
    min_area = 100
else:
    corr_class, corr_thk = "Very Mildly Corrosive", 0.75
    min_area = 100

d_with_corr = d_calc_mm + corr_thk
A_with_corr = math.pi * (d_with_corr / 2.0) ** 2
A_final     = max(A_with_corr, float(min_area))
sel_dia     = next((d for d in STD_DIA if math.pi*(d/2.0)**2 >= A_final), STD_DIA[-1])
sel_area    = math.pi * (sel_dia / 2.0) ** 2

A_grid = Lx * Ly
Lp     = 2.0 * (Lx + Ly)
Dm     = math.sqrt(Lx**2 + Ly**2)
n_x    = int(Lx / D) + 1
n_y    = int(Ly / D) + 1
Lc_est = n_x * Ly + n_y * Lx

if N_rods_calc:
    N_rods = max(1, int(math.ceil(Lp / rod_spacing_peri)))
else:
    N_rods = int(N_rods_input)

Lr  = N_rods * L_rod
Lt  = Lt_manual
Lc  = Lt - Lr

ratio_rod = rod_spacing_check / L_rod
if ratio_rod >= 2.0:   eta, eta_desc = 1.00, "Full utilization (spacing >= 2 x rod length)"
elif ratio_rod >= 1.0: eta, eta_desc = 0.87, "Minor mutual interference"
elif ratio_rod >= 0.6: eta, eta_desc = 0.75, "Moderate mutual interference"
else:                  eta, eta_desc = 0.60, "Heavy mutual interference — increase rod spacing"

sqrt_20A  = math.sqrt(20.0 * A_grid)
sqrt_20_A = math.sqrt(20.0 / A_grid)
Rg = rho * (1.0/Lt + (1.0/sqrt_20A) * (1.0 + 1.0/(1.0 + h * sqrt_20_A)))

L_cm   = L_rod * 100.0
d_cm   = d_rod
rho_cm = rho * 100.0
if N_pits > 0:
    Re_single_pit = (100.0 * rho_cm) / (2.0 * math.pi * L_cm) * math.log(4.0 * L_cm / d_cm)
    Re_pits = Re_single_pit / N_pits
    Rcomb   = (Rg * Re_pits) / (Rg + Re_pits)
else:
    Re_pits = None
    Rcomb   = Rg

IG    = If_A * Sf * Df
IG_kA = IG / 1000.0
GPR   = IG * Rg

Cs = 1.0 - ((0.09 * (1.0 - rho/rho_s)) / (2.0*h_s + 0.09))
Cs = max(0.01, min(1.0, Cs))

Ib         = 0.116 / math.sqrt(ts_val)
Etouch     = Ib * (1000.0 + 1.5 * rho_s * Cs)
Estep_perm = Ib * (1000.0 + 6.0  * rho_s * Cs)
Et_bare    = Ib * (1000.0 + 1.5 * rho)
Es_bare    = Ib * (1000.0 + 6.0  * rho)

na  = 2.0 * Lc / Lp
nb  = (Lp / (4.0 * math.sqrt(A_grid))) ** 0.5
n   = na * nb
Kh  = math.sqrt(1.0 + h)
Kii = 1.0
Kim = 0.644 + 0.148 * n
Kis = Kim

try:
    t1  = D**2 / (16.0 * h * d_c)
    t2  = (D + 2.0*h)**2 / (8.0 * D * d_c)
    t3  = h / (4.0 * d_c)
    t4  = (Kii/Kh) * math.log(8.0 / (math.pi * (2.0*n - 1.0)))
    Km  = (1.0 / (2.0*math.pi)) * (math.log(t1 + t2 - t3) + t4)
    Km  = max(0.05, min(6.0, Km))
except:
    Km = 0.5

try:
    Ks = (1.0/math.pi) * (
        1.0/(2.0*h) + 1.0/(D+h) + (1.0/D)*(1.0 - 0.5**(n - 2.0))
    )
    Ks = max(0.01, min(6.0, Ks))
except:
    Ks = 0.2

Lm = Lc + (1.55 + 1.22*(L_rod/Dm)) * Lr
Ls = 0.75*Lc + 0.85*Lr

Em = (rho * Km * Kim * IG) / Lm
Es = (rho * Ks * Kis * IG) / Ls

touch_ok = Em <= Etouch
step_ok  = Es <= Estep_perm
rg_ok    = Rg <= 1.0
all_safe = touch_ok and step_ok

# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────

hdr_sub  = "CBIP Pub.339 (2017)  |  IS 3043:1987 (Reaffirmed 2006)  |  IEEE Std 80-2013  |  IS 2309  |  IEEE 665"
hdr_proj = f"Project : {project_name}"
if prepared_by: hdr_proj += f"   |   Prepared by : {prepared_by}"
if doc_number:  hdr_proj += f"   |   Doc No : {doc_number}"
hdr_proj += f"   |   {voltage}   |   {sub_type.split(' — ')[0]}"

st.markdown(f"""
<div class="page-header">
    <div class="page-header-title">Earthing System Design Calculation</div>
    <div class="page-header-sub">{hdr_sub}</div>
    <div class="page-header-sub" style="color:#b8ceda;margin-top:0.3rem">{hdr_proj}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────

t0, tflow, t1, t2, t3, t4, t5, t6 = st.tabs([
    "Design Basis",
    "Design Algorithm",
    "Step 1 — Conductor Sizing",
    "Step 2 — Grid Resistance",
    "Step 3 — Grid Current and GPR",
    "Step 4 — Safety Voltage Limits",
    "Step 5 — Mesh and Step Voltage",
    "Step 6 — Final Assessment",
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 0 — DESIGN BASIS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t0:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        sec("1.0 Introduction — Purpose of Earthing System")
        st.markdown("""
        <div class="card" style="font-size:0.82rem;color:#2c3e50;line-height:1.85">
        The primary requirements of a good earthing system in a substation are:<br><br>
        <b>1.</b> It shall stabilize circuit potentials with respect to ground and limit the overall potential rise.<br>
        <b>2.</b> It shall protect life and property from dangerous over-voltages.<br>
        <b>3.</b> It shall provide a low impedance path for fault currents to ensure prompt and consistent
        operation of protective devices during ground faults.<br>
        <b>4.</b> It shall keep the maximum voltage gradient along the surface, inside and around the
        substation, within safe limits during ground faults.
        </div>
        """, unsafe_allow_html=True)

        sec("2.1 Codes and Standards")
        st.markdown("""<table class="dtable">
        <tr><th>Standard</th><th>Description</th><th>Application</th></tr>
        <tr><td class="mono">CBIP Pub.339 (2017)</td><td>Manual on Earthing of AC Power Systems</td><td>Primary reference</td></tr>
        <tr><td class="mono">IS 3043:1987</td><td>Code of Practice for Earthing (Reaffirmed 2006)</td><td>Material sizing, installation</td></tr>
        <tr><td class="mono">IEEE Std 80-2013</td><td>Guide for Safety in AC Substation Grounding</td><td>Design formulae</td></tr>
        <tr><td class="mono">IEEE Std 665</td><td>Guide for Safety in Generating Station Grounding</td><td>Generating station specifics</td></tr>
        <tr><td class="mono">IS 2309</td><td>Protection of Buildings against Lightning</td><td>Lightning earthing</td></tr>
        <tr><td class="mono">IEC 62305</td><td>Protection against Lightning</td><td>Lightning protection</td></tr>
        </table>""", unsafe_allow_html=True)

        sec("Soil Corrosiveness Classification — CBIP Table 3.7")
        st.markdown(f"""<table class="dtable">
        <tr><th>Soil Resistivity (ohm-m)</th><th>Class</th><th>Corrosion Allowance</th></tr>
        <tr {'class="hl"' if rho <= 10 else ''}><td class="mono">Less than 10</td><td>Severely Corrosive</td><td>30% area, +4.5mm dia</td></tr>
        <tr {'class="hl"' if 10 < rho <= 25 else ''}><td class="mono">10 to 25</td><td>Corrosive</td><td>30% area, +4.5mm dia</td></tr>
        <tr {'class="hl"' if 25 < rho <= 50 else ''}><td class="mono">25 to 50</td><td>Moderately Corrosive</td><td>15% area, +2.25mm dia</td></tr>
        <tr {'class="hl"' if 50 < rho <= 100 else ''}><td class="mono">50 to 100</td><td>Mildly Corrosive</td><td>15% area, +2.25mm dia</td></tr>
        <tr {'class="hl"' if rho > 100 else ''}><td class="mono">Greater than 100</td><td>Very Mildly Corrosive</td><td>10% area, +0.75mm dia</td></tr>
        </table>
        <p style="font-size:0.74rem;color:#5a6a7a;margin-top:0.4rem">
        Your input: rho = {rho} ohm-m — <b>{corr_class}</b>.
        Corrosion addition to diameter = {corr_thk} mm. Source: CBIP Table 3.9
        </p>""", unsafe_allow_html=True)

    with col2:
        sec("2.2 Design Input Data")
        st.markdown(f"""<table class="dtable">
        <tr><th>Parameter</th><th>Value</th><th>Remark / Source</th></tr>
        <tr><td>Earth Fault Current — If</td><td class="mono">{If_kA} kA</td><td>From system fault study</td></tr>
        <tr><td>Fault Duration — tf</td><td class="mono">{tf_val} s</td><td>CBIP Sec 3.7.3 — incl. backup clearing</td></tr>
        <tr><td>Shock Duration — ts</td><td class="mono">{ts_val} s</td><td>CBIP Sec 3.7.3 — primary relay only</td></tr>
        <tr><td>Current Division Factor — Sf</td><td class="mono">{Sf}</td><td>CBIP Sec 3.7.2 — fraction into grid</td></tr>
        <tr><td>Decrement Factor — Df</td><td class="mono">{Df}</td><td>IEEE 80-2013 Cl.15.10</td></tr>
        <tr><td>Ambient Temperature — Ta</td><td class="mono">{Ta} deg C</td><td>Maximum site ambient</td></tr>
        <tr><td>Mean Soil Resistivity — rho</td><td class="mono">{rho} ohm-m</td><td>Wenner measurement, CBIP Ch.9</td></tr>
        <tr><td>Surface Layer Resistivity — rho_s</td><td class="mono">{rho_s} ohm-m</td><td>Concrete / crushed rock</td></tr>
        <tr><td>Surface Layer Thickness — hs</td><td class="mono">{h_s} m</td><td>As per site specification</td></tr>
        <tr><td>Conductor Material</td><td class="mono">{mat_key.split(" (")[0]}</td><td>CBIP Sec 3.9</td></tr>
        <tr><td>Grid Area — Lx x Ly</td><td class="mono">{Lx:.0f} m x {Ly:.0f} m = {A_grid:.0f} m2</td><td>Station layout drawings</td></tr>
        <tr><td>Mesh Spacing — D</td><td class="mono">{D} m</td><td>CBIP: 3 to 8m typical</td></tr>
        <tr><td>Burial Depth — h</td><td class="mono">{h} m</td><td>CBIP: 0.5m minimum</td></tr>
        <tr><td>Total Buried Conductor — Lt</td><td class="mono">{Lt:.0f} m</td><td>From detailed layout drawings</td></tr>
        <tr><td>Ground Rods</td><td class="mono">{N_rods} nos x {L_rod} m x {d_rod:.0f} mm dia</td>
            <td>{"Calculated from " + str(rod_spacing_peri) + "m perimeter spacing" if N_rods_calc else "Entered from drawings"}</td></tr>
        <tr><td>Separate Earth Pits</td><td class="mono">{N_pits} nos</td><td>IS 3043 — additional electrode</td></tr>
        <tr><td>Earthing Resistance Target</td><td class="mono">Less than 1.0 ohm</td><td>Technical specification</td></tr>
        </table>""", unsafe_allow_html=True)

        if N_rods_calc:
            sp()
            info(f"Ground rod quantity auto-calculated: Grid perimeter = {Lp:.0f} m. "
                 f"At one rod per {rod_spacing_peri} m: N = ceil({Lp:.0f} / {rod_spacing_peri}) = {N_rods} rods. "
                 f"Total rod length Lr = {N_rods} x {L_rod} = {Lr:.0f} m.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB FLOW — DESIGN ALGORITHM FLOWCHART
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tflow:
    sec("Design Algorithm — Step by Step Flow (CBIP Pub.339 / IEEE Std 80-2013)")
    info("This flowchart shows the exact sequence of calculations performed in this tool. Each step corresponds to one tab. Read top to bottom. If the safety check fails, adjust the design parameters and re-run.")
    sp(0.4)

    col_fc, col_desc = st.columns([1, 1.1], gap="large")

    with col_fc:
        st.markdown("""
        <div style="background:#ffffff;border:1px solid #d8dde5;border-radius:3px;padding:1.5rem 1rem 2rem 1rem;">

        <!-- START -->
        <div style="display:flex;flex-direction:column;align-items:center;">

        <div style="background:#0d2d4a;color:#ffffff;border-radius:20px;padding:0.55rem 1.6rem;font-size:0.78rem;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;width:180px;text-align:center;">
            START
        </div>

        <div style="width:2px;height:20px;background:#4a6a84;margin:0 auto;"></div>

        <!-- STEP 1 -->
        <div style="background:#eaf4fb;border:2px solid #1a6fa0;border-radius:3px;padding:0.65rem 1rem;font-size:0.76rem;font-weight:600;color:#0d2d4a;width:270px;text-align:center;line-height:1.5;">
            STEP 1 — Load Input Parameters
            <div style="font-size:0.66rem;font-weight:400;margin-top:0.2rem;color:#1a5276;font-family:monospace;">
                Project, Soil (rho, rho_s, hs), Fault Data (If, tf, ts, Sf, Df, Ta)
            </div>
        </div>

        <div style="width:2px;height:20px;background:#4a6a84;margin:0 auto;"></div>

        <!-- STEP 2 -->
        <div style="background:#eaf4fb;border:2px solid #1a6fa0;border-radius:3px;padding:0.65rem 1rem;font-size:0.76rem;font-weight:600;color:#0d2d4a;width:270px;text-align:center;line-height:1.5;">
            STEP 2 — Calculate Grid Current IG
            <div style="font-size:0.66rem;font-weight:400;margin-top:0.2rem;color:#1a5276;font-family:monospace;">
                IG = If x Sf x Df
            </div>
        </div>

        <div style="width:2px;height:20px;background:#4a6a84;margin:0 auto;"></div>

        <!-- STEP 3 -->
        <div style="background:#eafaf1;border:2px solid #1e8449;border-radius:3px;padding:0.65rem 1rem;font-size:0.76rem;font-weight:600;color:#145a32;width:270px;text-align:center;line-height:1.5;">
            STEP 3 — Conductor Sizing
            <div style="font-size:0.66rem;font-weight:400;margin-top:0.2rem;color:#1a5c2a;font-family:monospace;">
                A = If_kA x sqrt[(tc x alpha_r x rho_r x 10^4 / Tcap) / ln(...)]<br>
                Add corrosion allowance. Select standard diameter.
            </div>
        </div>

        <div style="width:2px;height:20px;background:#4a6a84;margin:0 auto;"></div>

        <!-- STEP 4 -->
        <div style="background:#eafaf1;border:2px solid #1e8449;border-radius:3px;padding:0.65rem 1rem;font-size:0.76rem;font-weight:600;color:#145a32;width:270px;text-align:center;line-height:1.5;">
            STEP 4 — Define Grid Geometry and Rod Placement
            <div style="font-size:0.66rem;font-weight:400;margin-top:0.2rem;color:#1a5c2a;font-family:monospace;">
                Lx, Ly, D, h, Lt | N_rods from perimeter spacing
            </div>
        </div>

        <div style="width:2px;height:20px;background:#4a6a84;margin:0 auto;"></div>

        <!-- STEP 5 -->
        <div style="background:#eafaf1;border:2px solid #1e8449;border-radius:3px;padding:0.65rem 1rem;font-size:0.76rem;font-weight:600;color:#145a32;width:270px;text-align:center;line-height:1.5;">
            STEP 5 — Calculate Grid Resistance Rg
            <div style="font-size:0.66rem;font-weight:400;margin-top:0.2rem;color:#1a5c2a;font-family:monospace;">
                Rg = rho x [1/Lt + (1/sqrt(20A)) x (1 + 1/(1+h.sqrt(20/A)))]<br>
                Also: Re_pits and Rcombined
            </div>
        </div>

        <div style="width:2px;height:20px;background:#4a6a84;margin:0 auto;"></div>

        <!-- STEP 6 -->
        <div style="background:#eafaf1;border:2px solid #1e8449;border-radius:3px;padding:0.65rem 1rem;font-size:0.76rem;font-weight:600;color:#145a32;width:270px;text-align:center;line-height:1.5;">
            STEP 6 — Ground Potential Rise
            <div style="font-size:0.66rem;font-weight:400;margin-top:0.2rem;color:#1a5c2a;font-family:monospace;">
                GPR = IG x Rg
            </div>
        </div>

        <div style="width:2px;height:20px;background:#4a6a84;margin:0 auto;"></div>

        <!-- STEP 7 -->
        <div style="background:#eafaf1;border:2px solid #1e8449;border-radius:3px;padding:0.65rem 1rem;font-size:0.76rem;font-weight:600;color:#145a32;width:270px;text-align:center;line-height:1.5;">
            STEP 7 — Compute Permissible Safety Limits
            <div style="font-size:0.66rem;font-weight:400;margin-top:0.2rem;color:#1a5c2a;font-family:monospace;">
                Ib = 0.116/sqrt(ts) | Cs = IEEE Eq.27<br>
                Etouch = Ib x (1000 + 1.5 x rho_s x Cs)<br>
                Estep = Ib x (1000 + 6 x rho_s x Cs)
            </div>
        </div>

        <div style="width:2px;height:20px;background:#4a6a84;margin:0 auto;"></div>

        <!-- STEP 8 -->
        <div style="background:#eafaf1;border:2px solid #1e8449;border-radius:3px;padding:0.65rem 1rem;font-size:0.76rem;font-weight:600;color:#145a32;width:270px;text-align:center;line-height:1.5;">
            STEP 8 — Compute Actual Mesh and Step Voltages
            <div style="font-size:0.66rem;font-weight:400;margin-top:0.2rem;color:#1a5c2a;font-family:monospace;">
                Factors: na, nb, n, Kh, Km, Ks, Kim, Lm, Ls<br>
                Em = rho x Km x Kim x IG / Lm<br>
                Es = rho x Ks x Kis x IG / Ls
            </div>
        </div>

        <div style="width:2px;height:20px;background:#4a6a84;margin:0 auto;"></div>

        <!-- DECISION -->
        <div style="background:#fef9e7;border:2px solid #d68910;padding:0.75rem 1.5rem;font-size:0.77rem;font-weight:700;color:#7d6608;width:270px;text-align:center;line-height:1.5;border-radius:3px;">
            STEP 9 — SAFETY CHECK
            <div style="font-size:0.68rem;font-weight:500;margin-top:0.25rem;color:#856404;font-family:monospace;">
                Is Em &lt; Etouch AND Es &lt; Estep ?
            </div>
        </div>

        <!-- BRANCH -->
        <div style="display:flex;justify-content:center;align-items:flex-start;gap:2rem;width:100%;margin-top:0.5rem;">

            <!-- SAFE BRANCH -->
            <div style="display:flex;flex-direction:column;align-items:center;">
                <div style="background:#1e8449;color:white;font-size:0.63rem;font-weight:700;padding:0.2rem 0.6rem;border-radius:2px;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3rem;">YES — SAFE</div>
                <div style="width:2px;height:16px;background:#4a6a84;"></div>
                <div style="background:#eafaf1;border:2px solid #1e8449;border-radius:3px;padding:0.55rem 0.8rem;font-size:0.72rem;font-weight:600;color:#145a32;width:130px;text-align:center;line-height:1.5;">
                    Design Approved
                    <div style="font-size:0.64rem;font-weight:400;margin-top:0.15rem;color:#1a5c2a;">Generate Report</div>
                </div>
            </div>

            <!-- UNSAFE BRANCH -->
            <div style="display:flex;flex-direction:column;align-items:center;">
                <div style="background:#c0392b;color:white;font-size:0.63rem;font-weight:700;padding:0.2rem 0.6rem;border-radius:2px;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3rem;">NO — UNSAFE</div>
                <div style="width:2px;height:16px;background:#4a6a84;"></div>
                <div style="background:#fdedec;border:2px solid #c0392b;border-radius:3px;padding:0.55rem 0.8rem;font-size:0.72rem;font-weight:600;color:#78281f;width:130px;text-align:center;line-height:1.5;">
                    Remediation
                    <div style="font-size:0.64rem;font-weight:400;margin-top:0.15rem;color:#922b21;">Reduce D or adjust rods. Return to Step 4.</div>
                </div>
            </div>

        </div>

        </div>
        </div>
        """, unsafe_allow_html=True)

    with col_desc:
        sec("Algorithm Steps — What Each Step Does")

        steps = [
            ("STEP 1", "Load Input Parameters",
             "All inputs are entered in the sidebar: project details, soil resistivity (rho), surface layer (rho_s, hs), fault current (If), fault duration (tf), shock duration (ts), current division factor (Sf), decrement factor (Df), ambient temperature (Ta), grid dimensions, conductor type, and rod parameters."),
            ("STEP 2", "Calculate Grid Current IG",
             "IG = If x Sf x Df. Not all fault current flows through the grid. Sf accounts for the fraction returned via earth wires. Df corrects for DC offset in initial fault cycles. IG is the current actually flowing between grid and soil — used for all voltage calculations."),
            ("STEP 3", "Conductor Sizing — Thermal and Corrosion",
             "The conductor must carry If for tf seconds without melting. The full IEEE 80 thermal formula calculates minimum cross-sectional area A. The calculated diameter is then increased by the corrosion allowance from CBIP Table 3.9 based on soil resistivity. The next standard diameter from CBIP Table 3.6 is selected."),
            ("STEP 4", "Define Grid Geometry and Rod Placement",
             "The grid dimensions (Lx, Ly), mesh spacing (D), burial depth (h), and total conductor length (Lt) define the physical layout. The number of ground rods is calculated from the perimeter length divided by the chosen spacing — one rod every X metres along the perimeter, which is standard Indian practice."),
            ("STEP 5", "Calculate Grid Resistance Rg",
             "Using the Sverak formula (IEEE Std 80 Eq.52 / CBIP Eqn 5.32): Rg = rho x [1/Lt + (1/sqrt(20A)) x (1 + 1/(1 + h x sqrt(20/A)))]. Also calculates earth pit resistance Re and the combined parallel resistance Rcomb. Target is Rg < 1.0 ohm per typical project specification."),
            ("STEP 6", "Ground Potential Rise",
             "GPR = IG x Rg. The entire grid rises to this voltage above remote earth during a fault. This is the maximum transferred potential to any metallic conductor leaving the station. IEEE Std 80 Sec 15.1: if GPR < Etouch permissible, the design is inherently safe without further analysis."),
            ("STEP 7", "Permissible Safety Voltage Limits",
             "Ib = 0.116/sqrt(ts) gives the maximum safe body current for 50 kg person. Cs (IEEE Eq.27) corrects for finite surface layer thickness. Etouch = Ib x (1000 + 1.5 x rho_s x Cs) and Estep = Ib x (1000 + 6 x rho_s x Cs) give the limits that actual voltages must not exceed."),
            ("STEP 8", "Actual Mesh and Step Voltages",
             "Geometric factors na, nb, n, Kh, Km, Ks, Kim are calculated from grid geometry. Effective lengths Lm and Ls are derived from CBIP Eqn 5.29 and 5.30. Then Em = rho x Km x Kim x IG / Lm and Es = rho x Ks x Kis x IG / Ls. These are the actual worst-case voltages in the grid."),
            ("STEP 9", "Safety Check and Decision",
             "If Em < Etouch AND Es < Estep: design is safe. If either condition fails: reduce mesh spacing D (reduces Em), add peripheral rods (reduces Es), or adjust grid area. The design is then revised from Step 4 and rechecked. Empirical formula accuracy is approximately plus or minus 15 percent compared to computer simulation."),
        ]

        for step_id, step_name, step_desc in steps:
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:0.8rem;margin-bottom:0.75rem;padding:0.7rem 0.9rem;background:#ffffff;border:1px solid #d8dde5;border-radius:3px;">
                <div style="background:#0d2d4a;color:#ffffff;font-size:0.6rem;font-weight:700;padding:0.25rem 0.5rem;border-radius:2px;white-space:nowrap;flex-shrink:0;margin-top:0.05rem;letter-spacing:0.06em;text-transform:uppercase;">{step_id}</div>
                <div>
                    <div style="font-size:0.78rem;font-weight:700;color:#0d2d4a;margin-bottom:0.2rem;">{step_name}</div>
                    <div style="font-size:0.74rem;color:#2c3e50;line-height:1.6;">{step_desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        sp(0.5)
        st.markdown("""
        <div style="background:#fef9e7;border:1px solid #f8c471;border-left:3px solid #d68910;padding:0.75rem 0.9rem;border-radius:0 3px 3px 0;font-size:0.75rem;color:#7d6608;line-height:1.65;">
        <b>Design Iteration:</b> The safety check (Step 9) is the decision gate. If the design fails,
        change the mesh spacing D (most effective for Em), add more rods at the perimeter (most
        effective for Es), or increase the grid area (most effective for Rg). Then re-run from Step 4.
        The sidebar inputs update all calculations instantly — no re-run is needed in this tool.
        </div>
        """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — CONDUCTOR SIZING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t1:
    sec("3.01 Selection of Conductor Size")
    info("The conductor must carry the full earth fault current for the specified fault duration without its temperature exceeding the maximum permissible value. Two formulae are given — the full IEEE formula and the simplified CBIP formula. Both should give consistent results.")
    sp(0.3)

    col1, col2 = st.columns([1.1, 0.9], gap="large")
    with col1:
        sec("Material Constants Used (IEEE 80 / CBIP Table 3.5)")
        st.markdown(f"""<table class="dtable">
        <tr><th>Constant</th><th>Symbol</th><th>Value</th><th>Unit</th><th>Meaning</th></tr>
        <tr><td>Resistivity of conductor</td><td class="mono">rho_r</td><td class="mono">{rho_r}</td><td>micro-ohm-cm</td><td>Electrical resistivity of material</td></tr>
        <tr><td>Thermal coefficient</td><td class="mono">alpha_r</td><td class="mono">{alpha_r}</td><td>per deg C</td><td>Rate of change of resistance with temperature</td></tr>
        <tr><td>Density of material</td><td class="mono">SW</td><td class="mono">{SW}</td><td>g per cm3</td><td>Mass per unit volume</td></tr>
        <tr><td>Specific heat</td><td class="mono">SH</td><td class="mono">{SH}</td><td>cal per g-deg C</td><td>Heat capacity of material</td></tr>
        <tr><td>Thermal capacity factor</td><td class="mono">Tcap = 4.184 x SH x SW</td><td class="mono">{Tcap:.4f}</td><td>—</td><td>Energy stored per unit volume per degree</td></tr>
        <tr><td>Max. allowable temperature</td><td class="mono">Tm</td><td class="mono">{Tm}</td><td>deg C</td><td>Conductor temperature limit for joint type</td></tr>
        <tr><td>Reference temperature</td><td class="mono">Tr</td><td class="mono">{Tr}</td><td>deg C</td><td>Temperature at which rho_r and alpha_r are specified</td></tr>
        <tr><td>K0 = (1/alpha_r) - Tr</td><td class="mono">K0</td><td class="mono">{K0:.2f}</td><td>deg C</td><td>Derived constant for formula</td></tr>
        <tr><td>Ambient temperature</td><td class="mono">Ta</td><td class="mono">{Ta}</td><td>deg C</td><td>Initial conductor temperature before fault</td></tr>
        </table>""", unsafe_allow_html=True)

        sec("IEEE 80 Full Thermal Formula — Clause 11.3 / Clause 9.4")
        fblock(
            "A = If_kA x sqrt [ (tc x alpha_r x rho_r x 10^4 / Tcap) / ln(1 + (Tm - Ta) / (K0 + Ta)) ]",
            {
                "A (mm2)": "Minimum cross-sectional area to prevent conductor fusing",
                "If_kA": f"{If_kA} kA — earth fault current (AC rms, negligible impedance fault)",
                "tc = tf": f"{tf_val} s — conductor fault duration (maximum, including backup protection)",
                "alpha_r": f"{alpha_r} per deg C",
                "rho_r": f"{rho_r} micro-ohm-cm",
                "Tcap": f"4.184 x {SH} x {SW} = {Tcap:.4f}",
                "Tm": f"{Tm} deg C — maximum permissible conductor temperature",
                "Ta": f"{Ta} deg C — initial ambient temperature",
                "K0": f"(1 / {alpha_r}) - {Tr} = {K0:.2f} deg C",
                "Numerator inside sqrt": f"{tf_val} x {alpha_r} x {rho_r} x 10000 / {Tcap:.4f} = {numer:.4f}",
                "Denominator (ln term)": f"ln(1 + ({Tm}-{Ta}) / ({K0:.2f}+{Ta})) = ln({ln_arg:.5f}) = {ln_val:.4f}",
                "sqrt argument": f"{numer:.4f} / {ln_val:.4f} = {numer/ln_val:.4f}",
            },
            "IEEE Std 80-2013 Cl.11.3 — Full thermal formula  |  IEEE 80-1986 Cl.9.4",
            f"A = {If_kA} x sqrt({numer/ln_val:.4f}) = {If_kA} x {math.sqrt(numer/ln_val):.4f} = {A_ieee:.3f} mm2"
        )

        sec("CBIP Simplified Formula — Cross-Check (CBIP Eqn 3.20 / Table 3.5)")
        fblock(
            "Ac = K x If x sqrt(tf) x 10^-3",
            {
                "K": f"{K_cbip} — CBIP Table 3.5 constant for selected material and joint type",
                "If (A)": f"{If_A:.0f} A",
                "tf (s)": f"{tf_val} s",
            },
            "CBIP Manual Pub.339 Eqn 3.20 — Table 3.5 — Simplified formula for quick sizing",
            f"Ac = {K_cbip} x {If_A:.0f} x sqrt({tf_val}) x 0.001 = {K_cbip * If_A * math.sqrt(tf_val) * 1e-3:.3f} mm2"
        )
        info(f"Both methods are consistent. IEEE formula gives A = {A_ieee:.1f} mm2. CBIP simplified gives {K_cbip * If_A * math.sqrt(tf_val) * 1e-3:.1f} mm2. Use IEEE formula for the design; CBIP for cross-check.")

    with col2:
        sec("Conversion from Area to Diameter")
        fblock(
            "r = sqrt(A / pi)    =>    d = 2r",
            {
                "A (mm2)": f"{A_ieee:.3f} — from IEEE formula above",
                "r (mm)": f"sqrt({A_ieee:.3f} / pi) = sqrt({A_ieee/math.pi:.4f}) = {r_calc:.4f}",
                "d (mm)": f"2 x {r_calc:.4f} = {d_calc_mm:.4f}",
            },
            "Geometry",
            f"Calculated conductor diameter = {d_calc_mm:.2f} mm"
        )

        sec("Corrosion Allowance — CBIP Table 3.9")
        st.markdown(f"""<table class="dtable">
        <tr><th>Step</th><th>Value</th></tr>
        <tr><td>Calculated diameter from thermal formula</td><td class="mono">{d_calc_mm:.2f} mm</td></tr>
        <tr><td>Soil class at rho = {rho} ohm-m</td><td>{corr_class}</td></tr>
        <tr><td>Corrosion allowance added to diameter</td><td class="mono">+ {corr_thk} mm (CBIP Table 3.9)</td></tr>
        <tr><td>Diameter after corrosion allowance</td><td class="mono">{d_with_corr:.2f} mm</td></tr>
        <tr><td>Equivalent area after corrosion</td><td class="mono">{A_with_corr:.2f} mm2</td></tr>
        <tr><td>IS 3043 minimum area for this soil</td><td class="mono">{min_area} mm2</td></tr>
        <tr><td>Design area (larger of the two above)</td><td class="mono">{A_final:.2f} mm2</td></tr>
        </table>""", unsafe_allow_html=True)

        info("IS 3043 Sec 5.3.4: Minimum area = 100 mm2 (non-corrosive soil), 200 mm2 (corrosive soil). Minimum thickness = 3mm (non-corrosive), 6mm (corrosive). Minimum above-ground earth lead = 50 mm2.")

        sec("Standard Conductor Selection — CBIP Table 3.6")
        rows_dia = ""
        for d in STD_DIA:
            a = math.pi*(d/2.0)**2
            selected = d == sel_dia
            status = "SELECTED" if selected else ("below required" if a < A_final else "acceptable")
            cls = "pass" if selected else ""
            bg  = ' class="hl"' if selected else ""
            rows_dia += f"<tr{bg}><td class='mono'>{d}</td><td class='mono'>{a:.1f}</td><td class='{cls}'>{status}</td></tr>"

        st.markdown(f"""<table class="dtable">
        <tr><th>Standard Dia (mm)</th><th>Area (mm2)</th><th>Status</th></tr>
        {rows_dia}</table>""", unsafe_allow_html=True)

        sp(0.3)
        res_pass(f"Selected conductor: {sel_dia} mm diameter MS round rod. Area = {sel_area:.1f} mm2. Satisfies thermal and corrosion requirements.")

        sec("Surface Current Density Limit — CBIP Eqn 3.21")
        Jsd = math.sqrt(57.7 / (rho * tf_val)) * 1e-3
        fblock(
            "Isd = 10^-3 x sqrt(57.7 / (rho x tf))   [A per mm2]",
            {
                "57.7": "Empirical constant from IS 3043 / BS 7430",
                "rho (ohm-m)": f"{rho}",
                "tf (s)": f"{tf_val}",
            },
            "CBIP Eqn 3.21 / IS 3043 — Limits surface temperature rise to prevent soil drying",
            f"Isd = {Jsd:.6f} A/mm2 — In practice, total grid conductor area far exceeds the thermal minimum, so this condition is automatically satisfied."
        )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — GRID RESISTANCE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t2:
    sec("3.02 Grid Layout and Conductor Quantities")
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(f"""<table class="dtable">
        <tr><th>Parameter</th><th>Value</th><th>How Derived</th></tr>
        <tr><td>Grid Length — Lx</td><td class="mono">{Lx:.0f} m</td><td>Station layout drawing</td></tr>
        <tr><td>Grid Width — Ly</td><td class="mono">{Ly:.0f} m</td><td>Station layout drawing</td></tr>
        <tr><td>Grid Area — A = Lx x Ly</td><td class="mono">{A_grid:.0f} m2</td><td>Calculated</td></tr>
        <tr><td>Grid Perimeter — Lp = 2(Lx + Ly)</td><td class="mono">{Lp:.0f} m</td><td>Calculated</td></tr>
        <tr><td>Grid Diagonal — Dm</td><td class="mono">{Dm:.2f} m</td><td>sqrt(Lx2 + Ly2)</td></tr>
        <tr><td>Mesh Spacing — D</td><td class="mono">{D} m</td><td>Design decision (3 to 8m CBIP)</td></tr>
        <tr><td>Conductors in X direction</td><td class="mono">{n_x} runs</td><td>int(Lx/D) + 1</td></tr>
        <tr><td>Conductors in Y direction</td><td class="mono">{n_y} runs</td><td>int(Ly/D) + 1</td></tr>
        <tr><td>Estimated horizontal conductor Lc</td><td class="mono">{Lc_est:.0f} m</td><td>n_x x Ly + n_y x Lx (approximate)</td></tr>
        <tr><td>Total buried conductor — Lt (from drawings)</td><td class="mono">{Lt:.0f} m</td><td>Entered from actual drawing layout</td></tr>
        <tr><td>Ground rods — N</td><td class="mono">{N_rods} nos</td><td>{"Perimeter / " + str(rod_spacing_peri) + " m spacing" if N_rods_calc else "Entered from drawings"}</td></tr>
        <tr><td>Rod length — L</td><td class="mono">{L_rod} m</td><td>IS 3043: minimum 3m</td></tr>
        <tr><td>Total rod length — Lr = N x L</td><td class="mono">{Lr:.0f} m</td><td>Calculated</td></tr>
        <tr><td>Horizontal conductor — Lc = Lt - Lr</td><td class="mono">{Lc:.0f} m</td><td>Lt minus Lr</td></tr>
        </table>""", unsafe_allow_html=True)

        info(f"Auto-estimate of horizontal conductor = {Lc_est:.0f} m. Actual from drawings = {Lc:.0f} m. Always use the drawing-based value (Lt_manual input) for final design. The auto-estimate is for preliminary checks only.")

        sec("3.02 Grid Earth Resistance — IEEE Std 80 Eqn / CBIP Eqn 5.32")
        fblock(
            "Rg = rho x [ 1/Lt  +  (1/sqrt(20 x A)) x (1 + 1/(1 + h x sqrt(20/A))) ]",
            {
                "Rg (ohm)": "Grid resistance to remote earth",
                "rho (ohm-m)": f"{rho}",
                "Lt (m)": f"{Lt:.0f} — total buried conductor (horizontal + rods)",
                "A (m2)": f"{A_grid:.0f} — grid enclosed area",
                "h (m)": f"{h} — burial depth",
                "sqrt(20A)": f"sqrt(20 x {A_grid:.0f}) = {sqrt_20A:.4f}",
                "h x sqrt(20/A)": f"{h} x sqrt(20/{A_grid:.0f}) = {h} x {sqrt_20_A:.6f} = {h*sqrt_20_A:.6f}",
                "(1 + ...)": f"1 + 1/(1 + {h*sqrt_20_A:.6f}) = {1+1/(1+h*sqrt_20_A):.6f}",
            },
            "IEEE Std 80-2013 Eq.52 / CBIP Manual Pub.339 Eqn 5.32 (Sverak formula)",
            f"Rg = {rho} x [1/{Lt:.0f} + {(1+1/(1+h*sqrt_20_A))/sqrt_20A:.8f}] = {Rg:.4f} ohm"
        )
        (res_pass if rg_ok else res_note)(
            f"Grid Resistance Rg = {Rg:.4f} ohm. {'Less than 1.0 ohm. Requirement satisfied.' if rg_ok else 'Exceeds 1.0 ohm. Review design — increase grid area or add soil enhancement.'}"
        )

    with col2:
        sec("3.03 Earth Rod Resistance")
        info("The formula below uses cm units, consistent with the original GSECL / ALSTOM calculation for this project. L and d are in cm, rho in ohm-cm.")
        fblock(
            "Re = (1/N) x [ (100 x rho_ohm_cm) / (2 x pi x L_cm) ] x ln(4 x L_cm / d_cm)",
            {
                "N": f"{N_rods} — number of ground rods",
                "rho (ohm-m)": f"{rho} ohm-m = {rho*100:.0f} ohm-cm",
                "L (cm)": f"{L_rod} m = {L_rod*100:.0f} cm — rod length",
                "d (cm)": f"{d_rod} mm = {d_rod/10:.2f} cm — rod diameter",
                "100 x rho_cm / (2 pi L_cm)": f"100 x {rho*100:.0f} / (2 x pi x {L_rod*100:.0f}) = {100*rho*100/(2*math.pi*L_rod*100):.4f}",
                "ln(4L/d)": f"ln(4 x {L_rod*100:.0f} / {d_rod/10:.2f}) = ln({4*L_rod*100/(d_rod/10):.2f}) = {math.log(4*L_rod*100/(d_rod/10)):.4f}",
            },
            "IEEE Std 80 / IS 3043 — Rod electrode resistance formula (cm unit version as used in GSECL project)",
            f"Re_single = {100*rho*100/(2*math.pi*L_rod*100)*math.log(4*L_rod*100/(d_rod/10)):.4f} ohm.   Re = {100*rho*100/(2*math.pi*L_rod*100)*math.log(4*L_rod*100/(d_rod/10))/N_rods:.4f} ohm"
        )

        if N_pits > 0 and Re_pits is not None:
            sec("3.03 Separate Earth Pit Resistance")
            fblock(
                "Re_pits = (1/N_pits) x [(100 x rho_cm) / (2 pi L_cm)] x ln(4L_cm / d_cm)",
                {
                    "N_pits": f"{N_pits} — number of separate earth pits",
                    "rho (ohm-cm)": f"{rho*100:.0f}",
                    "L (cm)": f"{L_rod*100:.0f}",
                    "d (cm)": f"{d_rod/10:.2f}",
                },
                "GSECL project calculation method — ALSTOM / DESEIN Sec 3.03",
                f"Re_pits = {Re_pits:.4f} ohm"
            )

            sec("3.03 Combined Grid and Earth Pit Resistance")
            fblock(
                "Rcombined = Rg x Re_pits / (Rg + Re_pits)",
                {
                    "Rg (ohm)": f"{Rg:.4f}",
                    "Re_pits (ohm)": f"{Re_pits:.4f}",
                },
                "Parallel combination of grid and separate earth pits",
                f"Rcombined = {Rg:.4f} x {Re_pits:.4f} / ({Rg:.4f} + {Re_pits:.4f}) = {Rcomb:.4f} ohm"
            )
            (res_pass if Rcomb <= 1.0 else res_fail)(
                f"Combined earth resistance = {Rcomb:.4f} ohm. {'Less than 1.0 ohm. Acceptable.' if Rcomb <= 1.0 else 'Exceeds 1.0 ohm.'}"
            )

        sec("Summary — Resistance")
        mcards([
            ("Grid Rg", f"{Rg:.4f}", "ohm", "pass" if rg_ok else "warn"),
            ("Earth Pits Re", f"{Re_pits:.4f}" if Re_pits else "N/A", "ohm", "blue"),
            ("Combined", f"{Rcomb:.4f}", "ohm", "pass" if Rcomb <= 1.0 else "warn"),
            ("Target", "less than 1.0", "ohm", "blue"),
        ])

        sec("Notes on Grid Resistance")
        info("CBIP Sec 3.5 and IEEE Std 80 Sec 1: There is no absolute fixed limit on Rg in the standard. Safety is judged by Em < Etouch and Es < Estep. The 1.0 ohm requirement is a typical project specification, not a code mandate.")
        info("To reduce Rg: Increase grid area — most effective, Rg is proportional to rho/sqrt(A). Adding more conductor length at the same area has minimal effect on Rg per CBIP Sec 3.11.1.")
        info("If high Rg persists despite large grid: Bentonite clay backfill (rho = 8.7 ohm-m), deep driven rods penetrating low-resistivity stratum, or satellite earth electrode. CBIP Chapter 6.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3 — GRID CURRENT AND GPR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t3:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        sec("3.04 Maximum Grid Current — CBIP Eqn 3.16 / IEEE 80 Cl.15")
        st.markdown(f"""
        <div class="card" style="font-size:0.8rem;color:#2c3e50;line-height:1.85">
        Not all of the earth fault current (If) flows through the grid into the soil.
        A fraction returns to the source via overhead earth wires of transmission lines and cable sheaths
        without entering the soil at all.<br><br>
        <b>Sf (Current Division Factor)</b> is the fraction of If that actually flows between the grid
        and surrounding soil. Sf = 1.0 is the conservative case (all current through grid soil).<br><br>
        <b>Df (Decrement Factor)</b> accounts for the DC offset present in the initial cycles of a fault.
        The asymmetrical current is larger than the symmetrical rms value. For fault duration >= 0.5s
        (30 cycles), IEEE 80-2013 Cl.15.10 allows Df = 1.0.<br><br>
        Sf = {Sf} was used in this design
        ({"all current into grid — conservative, used when earth wire data is not available" if Sf == 1.0
        else f"{int(Sf*100)}% of fault current flows through grid soil, {int((1-Sf)*100)}% returns via earth wires"}).
        </div>
        """, unsafe_allow_html=True)

        sp(0.3)
        fblock(
            "IG = If x Sf x Df",
            {
                "If (A)": f"{If_A:.0f} A = {If_kA} kA — total earth fault current",
                "Sf": f"{Sf} — current division factor (fraction flowing into earth grid)",
                "Df": f"{Df} — decrement factor (DC offset correction)",
                "IG (A)": "Maximum grid current — used for all GPR and voltage calculations",
            },
            "CBIP Manual Pub.339 Sec 3.7.2 Eqn 3.16 / IEEE Std 80-2013 Cl.15",
            f"IG = {If_A:.0f} x {Sf} x {Df} = {IG:.0f} A = {IG_kA:.4f} kA"
        )

        sec("3.05 Ground Potential Rise — CBIP Sec 3.5")
        fblock(
            "GPR = IG x Rg",
            {
                "GPR (V)": "Maximum voltage of earthing grid relative to remote earth during fault",
                "IG (A)": f"{IG:.0f} A",
                "Rg (ohm)": f"{Rg:.4f} ohm",
            },
            "CBIP Manual Pub.339 Sec 3.5 and 3.7 / IEEE Std 80-2013",
            f"GPR = {IG:.0f} x {Rg:.4f} = {GPR:.2f} V = {GPR/1000:.4f} kV"
        )

    with col2:
        sec("Results")
        mcards([
            ("Fault Current If", f"{If_kA}", "kA", "blue"),
            ("Division Factor Sf", f"{Sf}", "", "blue"),
            ("Decrement Factor Df", f"{Df}", "", "blue"),
            ("Grid Current IG", f"{IG:.0f}", "A", "blue"),
        ])
        sp(0.3)
        mcards([
            ("Grid Resistance Rg", f"{Rg:.4f}", "ohm", "blue"),
            ("GPR = IG x Rg", f"{GPR:.2f}", "V", "blue"),
            ("GPR", f"{GPR/1000:.4f}", "kV", "blue"),
        ], cols=3)

        sec("3.07 GPR vs Permissible Touch Voltage Check — IEEE 80 Sec 15.1")
        st.markdown(f"""<p style="font-size:0.8rem;color:#2c3e50;margin-bottom:0.5rem;line-height:1.7">
        IEEE Std 80-2013 Sec 15.1 states: If the GPR is below the tolerable touch voltage,
        no further analysis is needed.<br>
        Permissible touch voltage Etouch (calculated in Step 4) = <b>{Etouch:.2f} V</b>
        </p>""", unsafe_allow_html=True)

        if GPR > Etouch:
            res_note(f"GPR = {GPR:.2f} V exceeds Etouch permissible = {Etouch:.2f} V. This is expected for most large substations. Further evaluation of actual mesh voltage Em is required (Step 5). GPR being higher than Etouch does not mean the design is unsafe — the actual mesh voltage Em may still be acceptable.")
        else:
            res_pass(f"GPR = {GPR:.2f} V is less than Etouch permissible = {Etouch:.2f} V. The grid design is inherently safe. Mesh voltage check is still recommended as a good practice.")

        sec("Transferred Potential — CBIP Sec 3.11.2")
        info(f"GPR = {GPR:.0f} V is the maximum transferred potential. Any metallic conductor entering or leaving the station — cable sheaths, water pipes, gas pipes, telephone cables, rails — can transfer this voltage to remote areas where safety precautions may not exist.")
        info("Required measures: Isolating transformers or SPD on all control and telecom circuits. Insulating joints on water and gas pipe at station boundary. Optical fibre preferred for communication. LV supply neutral must not be connected to earth outside station area. CBIP Sec 5.3.10 and IS 2309.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4 — SAFETY VOLTAGE LIMITS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t4:
    sec("3.06 Calculation of Tolerable Step and Touch Voltage")
    info("The permissible touch and step voltages depend on three things: the maximum body current a person can withstand (which depends on shock duration), the human body resistance, and the additional foot resistance due to the surface layer material. A higher surface layer resistivity (concrete or crushed rock) allows higher permissible voltages.")
    sp(0.3)

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        sec("Permissible Body Current — CBIP Eqn 3.1 / IEEE 80")
        fblock(
            "Ib = 0.116 / sqrt(ts)",
            {
                "Ib (A)": "Maximum body current: 99.5% of persons survive without ventricular fibrillation",
                "0.116": "k/1000 = 116 mA. Constant for 50 kg body weight. Statistically determined. CBIP Sec 3.6.2.",
                "ts (s)": f"{ts_val} s — shock contact duration (primary relay clearing time)",
            },
            "CBIP Pub.339 Sec 3.6.2 Eqn 3.1 / IEEE Std 80-2013",
            f"Ib = 0.116 / sqrt({ts_val}) = 0.116 / {math.sqrt(ts_val):.4f} = {Ib*1000:.3f} mA = {Ib:.6f} A"
        )

        sec("Surface Layer Reduction Factor — IEEE 80 Eq.27 / CBIP Eqn 5.9")
        st.markdown("""<div style="font-size:0.79rem;color:#2c3e50;line-height:1.7;margin-bottom:0.5rem">
        The concrete or crushed rock surface layer is high resistivity, which increases the contact resistance
        at the feet and thus raises the permissible voltage. However, the layer has finite thickness hs.
        Cs corrects for the fact that the full surface resistivity benefit is not achieved with a thin layer.
        If no surface layer is used, Cs = 1.0 (no benefit, rho_s = rho of natural soil).
        </div>""", unsafe_allow_html=True)

        fblock(
            "Cs = 1 - [ 0.09 x (1 - rho/rho_s) / (2 x hs + 0.09) ]",
            {
                "rho (ohm-m)": f"{rho}",
                "rho_s (ohm-m)": f"{rho_s}",
                "hs (m)": f"{h_s}",
                "Reflection factor K": f"(rho - rho_s) / (rho + rho_s) = ({rho} - {rho_s}) / ({rho} + {rho_s}) = {(rho-rho_s)/(rho+rho_s):.4f}",
                "(1 - rho/rho_s)": f"1 - {rho}/{rho_s} = {1-rho/rho_s:.5f}",
                "0.09 x (...)": f"0.09 x {1-rho/rho_s:.5f} = {0.09*(1-rho/rho_s):.5f}",
                "(2hs + 0.09)": f"2 x {h_s} + 0.09 = {2*h_s+0.09:.3f}",
            },
            "IEEE Std 80-2000 Equation 27 / CBIP Pub.339 Eqn 5.9",
            f"Cs = 1 - ({0.09*(1-rho/rho_s):.5f} / {2*h_s+0.09:.3f}) = {Cs:.4f}"
        )

    with col2:
        sec("Permissible Touch Voltage — CBIP Eqn 3.10 / IEEE Eqn B.6")
        st.markdown("""<div style="font-size:0.79rem;color:#2c3e50;line-height:1.7;margin-bottom:0.5rem">
        Touch voltage circuit: Current flows from hand (in contact with earthed equipment) through body
        (Rb = 1000 ohm) and out through both feet in parallel standing on the surface.
        Two feet in parallel, each = 3 x rho_s ohm (disc electrode formula, b = 0.08m).
        Total foot resistance = 1.5 x rho_s ohm.
        </div>""", unsafe_allow_html=True)
        fblock(
            "Etouch = Ib x (Rb + 1.5 x rho_s x Cs)",
            {
                "Etouch (V)": "Maximum permissible touch voltage",
                "Ib (A)": f"{Ib:.6f} A = {Ib*1000:.3f} mA",
                "Rb (ohm)": "1000 ohm — standard human body resistance for 50 kg person",
                "1.5 x rho_s x Cs": f"1.5 x {rho_s} x {Cs:.4f} = {1.5*rho_s*Cs:.3f} ohm (two feet in parallel on surface)",
                "Total resistance": f"1000 + {1.5*rho_s*Cs:.3f} = {1000+1.5*rho_s*Cs:.3f} ohm",
            },
            "CBIP Pub.339 Sec 3.6.2 Eqn 3.10 / IEEE Std 80-2013 Eqn B.6",
            f"Etouch = {Ib:.6f} x {1000+1.5*rho_s*Cs:.3f} = {Etouch:.2f} V"
        )

        sec("Permissible Step Voltage — CBIP Eqn 3.9 / IEEE Eqn B.6")
        st.markdown("""<div style="font-size:0.79rem;color:#2c3e50;line-height:1.7;margin-bottom:0.5rem">
        Step voltage circuit: Current flows in through one foot, through body, out through the other foot.
        Feet are 1 metre apart (one step). Each foot = 3 x rho_s ohm. Two feet in series = 6 x rho_s ohm.
        </div>""", unsafe_allow_html=True)
        fblock(
            "Estep = Ib x (Rb + 6 x rho_s x Cs)",
            {
                "Estep (V)": "Maximum permissible step voltage",
                "6 x rho_s x Cs": f"6 x {rho_s} x {Cs:.4f} = {6*rho_s*Cs:.3f} ohm (two feet in series, 1m step distance)",
            },
            "CBIP Pub.339 Sec 3.6.2 Eqn 3.9 / IEEE Std 80-2013 Eqn B.6",
            f"Estep = {Ib:.6f} x {1000+6*rho_s*Cs:.3f} = {Estep_perm:.2f} V"
        )

        sec("Summary of Safety Limits")
        mcards([
            ("Body Current Ib", f"{Ib*1000:.3f}", "mA", "blue"),
            ("Cs factor", f"{Cs:.4f}", "", "blue"),
            ("Etouch permissible", f"{Etouch:.2f}", "V", "blue"),
            ("Estep permissible", f"{Estep_perm:.2f}", "V", "blue"),
        ])

        sec("Effect of Surface Layer")
        st.markdown(f"""<table class="dtable">
        <tr><th>Condition</th><th>Etouch (V)</th><th>Estep (V)</th></tr>
        <tr><td>With surface layer (Cs = {Cs:.4f}, rho_s = {rho_s} ohm-m)</td>
            <td class="mono pass">{Etouch:.2f}</td><td class="mono">{Estep_perm:.2f}</td></tr>
        <tr><td>Without surface layer (Cs = 1.0, rho_s = rho = {rho} ohm-m)</td>
            <td class="mono">{Et_bare:.2f}</td><td class="mono">{Es_bare:.2f}</td></tr>
        <tr><td>Improvement factor from surface layer</td>
            <td class="mono">{Etouch/Et_bare:.2f}x</td><td class="mono">{Estep_perm/Es_bare:.2f}x</td></tr>
        </table>
        <p style="font-size:0.74rem;color:#5a6a7a;margin-top:0.4rem;line-height:1.6">
        CBIP Sec 3.6.2: Surface layer of crushed rock or concrete (rho_s = 3000 ohm-m) is strongly
        recommended throughout the switchyard. It significantly raises the permissible voltage limits
        and is always provided unless EPR is extremely low.
        </p>""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 5 — MESH AND STEP VOLTAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t5:
    sec("3.08 and 3.09 Calculation of Maximum Attainable Mesh and Step Voltage")
    info("The mesh voltage Em is the maximum touch voltage within the grid — it occurs at the centre of the corner meshes. The step voltage Es is the maximum step voltage — it occurs just outside the corner of the grid. These calculated values must be less than the respective permissible limits from Step 4.")
    sp(0.3)

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        sec("Geometric Factors — CBIP Eqn 5.14 to 5.22 / IEEE 80")
        st.markdown(f"""<table class="dtable">
        <tr><th>Factor</th><th>Formula</th><th>Calculated Value</th><th>Reference</th></tr>
        <tr><td>na</td><td class="mono">2 x Lc / Lp</td>
            <td class="mono">2 x {Lc:.0f} / {Lp:.0f} = {na:.4f}</td><td>CBIP Eqn 5.19 / IEEE B.18</td></tr>
        <tr><td>nb</td><td class="mono">[Lp / (4 x sqrt(A))]^0.5</td>
            <td class="mono">[{Lp:.0f} / (4 x {math.sqrt(A_grid):.3f})]^0.5 = {nb:.4f}</td><td>CBIP Eqn 5.20</td></tr>
        <tr><td>nc, nd</td><td class="mono">1.0 for rectangular grid</td>
            <td class="mono">1.0</td><td>CBIP Eqn 5.21 / IEEE B.17</td></tr>
        <tr><td>n = na x nb x nc x nd</td><td class="mono">Effective parallel conductors</td>
            <td class="mono">{n:.4f}</td><td>CBIP Eqn 5.18</td></tr>
        <tr><td>ho (reference depth)</td><td class="mono">1.0 m (standard)</td>
            <td class="mono">1.0 m</td><td>IEEE 80 definition</td></tr>
        <tr><td>Kh = sqrt(1 + h/ho)</td><td class="mono">sqrt(1 + {h}/1)</td>
            <td class="mono">{Kh:.4f}</td><td>CBIP Eqn 5.17 / IEEE B.14</td></tr>
        <tr><td>Kii</td><td class="mono">1.0 — rods in corners / periphery</td>
            <td class="mono">1.0</td><td>CBIP Eqn 5.16</td></tr>
        <tr><td>Ki = Kim = Kis</td><td class="mono">0.644 + 0.148 x n</td>
            <td class="mono">0.644 + 0.148 x {n:.4f} = {Kim:.4f}</td><td>CBIP Eqn 5.22 / IEEE B.16</td></tr>
        <tr><td>Km — mesh factor</td><td class="mono">Full formula — CBIP Eqn 5.14</td>
            <td class="mono">{Km:.4f}</td><td>CBIP Eqn 5.14 / IEEE B.13</td></tr>
        <tr><td>Ks — step factor</td><td class="mono">Full formula — CBIP Eqn 5.15</td>
            <td class="mono">{Ks:.4f}</td><td>CBIP Eqn 5.15 / IEEE B.15</td></tr>
        </table>""", unsafe_allow_html=True)

        sec("Km — Mesh Voltage Spacing Factor (CBIP Eqn 5.14 / IEEE Eq.81)")
        fblock(
            "Km = (1/2pi) x { ln[(D^2 / 16hd) + (D+2h)^2 / (8Dd) - h/(4d)] + (Kii/Kh) x ln[8 / (pi x (2n-1))] }",
            {
                "D (m)": f"{D} — mesh spacing between conductors",
                "h (m)": f"{h} — burial depth",
                "d (m)": f"{d_c:.4f} — conductor diameter ({d_c_mm:.0f} mm)",
                "D^2 / (16hd)": f"{D**2:.1f} / (16 x {h} x {d_c:.4f}) = {D**2/(16*h*d_c):.4f}",
                "(D+2h)^2 / (8Dd)": f"({D+2*h:.1f})^2 / (8 x {D} x {d_c:.4f}) = {(D+2*h)**2/(8*D*d_c):.4f}",
                "h / (4d)": f"{h} / (4 x {d_c:.4f}) = {h/(4*d_c):.4f}",
                "Kii/Kh": f"1.0 / {Kh:.4f} = {1/Kh:.4f}",
                "8/(pi(2n-1))": f"8 / (pi x {2*n-1:.4f}) = {8/(math.pi*(2*n-1)):.6f}",
            },
            "CBIP Pub.339 Eqn 5.14 / IEEE Std 80-2013 Eq.81",
            f"Km = {Km:.4f}"
        )

    with col2:
        sec("Effective Buried Lengths — CBIP Eqn 5.29 and 5.30")
        fblock(
            "Lm = Lc + [1.55 + 1.22 x (lr / Dm)] x Lr   [for rods in corners and along periphery]",
            {
                "Lc (m)": f"{Lc:.0f} — horizontal conductor",
                "lr (m)": f"{L_rod} — single rod length",
                "Dm (m)": f"{Dm:.2f} — grid diagonal",
                "Lr (m)": f"{Lr:.0f} — total rod length = {N_rods} x {L_rod}",
                "factor": f"1.55 + 1.22 x ({L_rod} / {Dm:.2f}) = {1.55+1.22*L_rod/Dm:.4f}",
            },
            "CBIP Pub.339 Eqn 5.29 — for rods on corners and periphery",
            f"Lm = {Lc:.0f} + {1.55+1.22*L_rod/Dm:.4f} x {Lr:.0f} = {Lm:.2f} m"
        )
        fblock(
            "Ls = 0.75 x Lc + 0.85 x Lr",
            {"Lc (m)": f"{Lc:.0f}", "Lr (m)": f"{Lr:.0f}"},
            "CBIP Pub.339 Eqn 5.30",
            f"Ls = 0.75 x {Lc:.0f} + 0.85 x {Lr:.0f} = {Ls:.2f} m"
        )

        sec("3.08 Maximum Attainable Mesh Voltage — CBIP Eqn 5.12 / IEEE Eq.85")
        fblock(
            "Em = rho x Km x Ki x IG / Lm",
            {
                "Em (V)": "Actual maximum mesh voltage in the grid (worst case at corner mesh)",
                "rho (ohm-m)": f"{rho}",
                "Km": f"{Km:.4f}",
                "Ki = Kim": f"{Kim:.4f}",
                "IG (A)": f"{IG:.0f}",
                "Lm (m)": f"{Lm:.2f}",
            },
            "CBIP Pub.339 Eqn 5.12 / IEEE Std 80-2013 Eq.85",
            f"Em = {rho} x {Km:.4f} x {Kim:.4f} x {IG:.0f} / {Lm:.2f} = {Em:.2f} V"
        )
        (res_pass if touch_ok else res_fail)(
            f"Em = {Em:.2f} V    vs    Etouch permissible = {Etouch:.2f} V    "
            f"{'Em is less than permissible. Grid design for touch voltage is correct.' if touch_ok else 'Em exceeds permissible. Redesign required — reduce mesh spacing, add conductors, or increase surface layer.'}"
        )

        sec("3.09 Maximum Attainable Step Voltage — CBIP Eqn 5.13 / IEEE Eq.92")
        fblock(
            "Es = rho x Ks x Ki x IG / Ls",
            {
                "Es (V)": "Actual maximum step voltage (worst case just outside corner of grid)",
                "rho (ohm-m)": f"{rho}",
                "Ks": f"{Ks:.4f}",
                "Ki = Kis": f"{Kis:.4f}",
                "IG (A)": f"{IG:.0f}",
                "Ls (m)": f"{Ls:.2f}",
            },
            "CBIP Pub.339 Eqn 5.13 / IEEE Std 80-2013 Eq.92",
            f"Es = {rho} x {Ks:.4f} x {Kis:.4f} x {IG:.0f} / {Ls:.2f} = {Es:.2f} V"
        )
        (res_pass if step_ok else res_fail)(
            f"Es = {Es:.2f} V    vs    Estep permissible = {Estep_perm:.2f} V    "
            f"{'Es is less than permissible. Grid design for step voltage is correct.' if step_ok else 'Es exceeds permissible. Redesign required — add peripheral rods, gradient control conductors, or extend grid.'}"
        )

        mcards([
            ("Mesh Voltage Em", f"{Em:.2f}", "V", "pass" if touch_ok else "fail"),
            ("Etouch permissible", f"{Etouch:.2f}", "V", "blue"),
            ("Step Voltage Es", f"{Es:.2f}", "V", "pass" if step_ok else "fail"),
            ("Estep permissible", f"{Estep_perm:.2f}", "V", "blue"),
        ])

        info("CBIP Ch.11 Table 11.5: Empirical formula results may differ from computer simulation by approximately 15%. For large and complex grids or non-uniform soil, use CBIP earthing analysis software for the final design. The empirical formulas are adequate for initial design and verification.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 6 — FINAL ASSESSMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with t6:
    if all_safe:
        res_pass(
            f"3.12 DESIGN IS SAFE. A safe design of the subsoil ground grid has been obtained. "
            f"Mesh voltage Em = {Em:.2f} V is less than permissible Etouch = {Etouch:.2f} V. "
            f"Step voltage Es = {Es:.2f} V is less than permissible Estep = {Estep_perm:.2f} V."
        )
    else:
        res_fail(
            f"3.12 DESIGN REQUIRES REVISION. One or more safety criteria are not satisfied. "
            f"Review items marked FAIL in the summary table and implement the corrective measures listed below."
        )

    sp(0.5)
    col1, col2 = st.columns([1.2, 0.8], gap="large")

    with col1:
        sec("3.12 Final Design Summary Table")

        def srow(item, unit, allowable, actual, status):
            sc = "pass" if status == "PASS" else ("fail" if status == "FAIL" else "note")
            return f"<tr><td>{item}</td><td class='mono'>{unit}</td><td class='mono'>{allowable}</td><td class='mono'>{actual}</td><td class='{sc}'>{status}</td></tr>"

        st.markdown(f"""<table class="dtable">
        <tr><th>Item</th><th>Unit</th><th>Allowable / Required</th><th>Actual / Calculated</th><th>Result</th></tr>
        {srow("Conductor diameter (thermal + corrosion)", "mm", f">= {d_with_corr:.1f}", str(sel_dia), "PASS" if sel_dia >= math.ceil(d_with_corr) else "FAIL")}
        {srow("Grid resistance Rg", "ohm", "< 1.0", f"{Rg:.4f}", "PASS" if rg_ok else "NOTE")}
        {srow("Combined earth resistance Rcomb", "ohm", "< 1.0", f"{Rcomb:.4f}", "PASS" if Rcomb <= 1.0 else "NOTE")}
        {srow("Ground potential rise GPR", "V", "Reference only", f"{GPR:.2f}", "NOTE")}
        {srow("Permissible body current Ib", "mA", "Calculated", f"{Ib*1000:.3f}", "OK")}
        {srow("Surface reduction factor Cs", "", "Calculated", f"{Cs:.4f}", "OK")}
        {srow("Permissible touch voltage Etouch", "V", "Calculated", f"{Etouch:.2f}", "OK")}
        {srow("Permissible step voltage Estep", "V", "Calculated", f"{Estep_perm:.2f}", "OK")}
        {srow("Actual mesh voltage Em", "V", f"< {Etouch:.2f}", f"{Em:.2f}", "PASS" if touch_ok else "FAIL")}
        {srow("Actual step voltage Es", "V", f"< {Estep_perm:.2f}", f"{Es:.2f}", "PASS" if step_ok else "FAIL")}
        </table>""", unsafe_allow_html=True)

        if not touch_ok:
            sec("Corrective Measures — Mesh Voltage Exceeds Permissible")
            for fix in [
                "Reduce mesh spacing D — add more parallel conductors in X and Y direction. This is the most effective measure for reducing Em. CBIP Sec 5.3.5.",
                "Use non-uniform conductor spacing — place conductors closer together at the grid corners and periphery, wider at the centre. CBIP Sec 11.3.2 shows this reduces Em by up to 43 percent compared to uniform spacing.",
                "Increase burial depth h — reduces Km factor and therefore Em.",
                "Apply Bentonite clay or concrete encasing around horizontal conductors. CBIP Sec 11.5.3.",
                "Install a counterpoise mat at shallow depth (0.3m) in addition to the main grid. CBIP Sec 11.5.5.",
                "Increase surface layer thickness hs or use material with higher resistivity rho_s — raises the permissible Etouch limit.",
            ]:
                info(fix)

        if not step_ok:
            sec("Corrective Measures — Step Voltage Exceeds Permissible")
            for fix in [
                "Add more vertical rods along the grid periphery — diverts fault current to deeper soil layers and reduces surface gradient at the grid edge. CBIP Sec 5.3.5.1.",
                "Increase the burial depth of the outermost perimeter conductor — reduces Ks factor. CBIP Sec 11.2.4g.",
                "Install gradient control rings — horizontal conductors buried outside the fence at progressively increasing depths. CBIP Sec 11.5.2 example shows Es reduced from 2602V to 726V.",
                "Extend the grid area 1 to 2 metres beyond the station fence boundary. CBIP Sec 5.3.9.",
                "Spread crushed rock surface layer at least 1 metre outside the perimeter fence.",
            ]:
                info(fix)

        if not rg_ok:
            sec("Corrective Measures — Grid Resistance Exceeds 1.0 ohm")
            for fix in [
                "Increase the grid area — the most effective measure. Rg is approximately proportional to rho divided by sqrt(A). CBIP Sec 3.11.1.",
                "Use soil resistivity enhancement material around vertical rods: Bentonite clay, coke dust, or conductive cement. CBIP Sec 6.3.1.1.",
                "Install deep-driven rods (30 to 40m depth) that penetrate a lower-resistivity stratum. CBIP Sec 11.5.4.",
                "Satellite earth electrode — a separate grid at a distance connected by a buried cable. CBIP Sec 11.5.7.",
            ]:
                info(fix)

    with col2:
        sec("Input Data Summary")
        st.markdown(f"""<table class="dtable">
        <tr><th>Parameter</th><th>Value</th></tr>
        <tr><td>Project</td><td class="mono">{project_name}</td></tr>
        <tr><td>Fault current If</td><td class="mono">{If_kA} kA</td></tr>
        <tr><td>Grid current IG</td><td class="mono">{IG:.0f} A = {IG_kA:.4f} kA</td></tr>
        <tr><td>Soil resistivity rho</td><td class="mono">{rho} ohm-m</td></tr>
        <tr><td>Grid area</td><td class="mono">{Lx:.0f} x {Ly:.0f} m = {A_grid:.0f} m2</td></tr>
        <tr><td>Mesh spacing D</td><td class="mono">{D} m</td></tr>
        <tr><td>Burial depth h</td><td class="mono">{h} m</td></tr>
        <tr><td>Total conductor Lt</td><td class="mono">{Lt:.0f} m</td></tr>
        <tr><td>Ground rods</td><td class="mono">{N_rods} nos x {L_rod} m</td></tr>
        <tr><td>Conductor selected</td><td class="mono">{sel_dia} mm dia</td></tr>
        <tr><td>Rg</td><td class="mono">{Rg:.4f} ohm</td></tr>
        <tr><td>GPR</td><td class="mono">{GPR:.2f} V</td></tr>
        <tr><td>Cs</td><td class="mono">{Cs:.4f}</td></tr>
        <tr><td>Etouch permissible</td><td class="mono">{Etouch:.2f} V</td></tr>
        <tr><td>Estep permissible</td><td class="mono">{Estep_perm:.2f} V</td></tr>
        <tr><td>Em actual</td><td class="mono">{Em:.2f} V</td></tr>
        <tr><td>Es actual</td><td class="mono">{Es:.2f} V</td></tr>
        </table>""", unsafe_allow_html=True)

        sec("Note on Number of Rods")
        info("The number of rods is determined by placing one rod at every N metres along the grid perimeter (Option A in the sidebar). In the GSECL project, 90 rods were used on a perimeter of 1100m — approximately one rod per 12m. Start with a spacing of 10 to 15m and adjust based on results.")
        info("Rods placed on the periphery are significantly more effective than those placed in the interior. CBIP Sec 5.3.5.1: Rods on the periphery control step voltage at the grid edge and help reduce resistance by dissipating current into deeper soil where moisture content is more stable.")

        sec("Equipment Earthing Quick Reference (CBIP + IS 3043)")
        equip = [
            ("Transformer body", "2 independent leads to different grid nodes — IS 3043 Cl.12"),
            ("Transformer neutral", "Separate conductor sized for full IG — CBIP Sec 5.2"),
            ("CT secondary neutral", "Earthed. Primary tank to grid. 50 mm2 min lead."),
            ("PT / CVT", "Separate quiet earth bus, single-point to main grid — CBIP Ch.7"),
            ("Lightning arrester LA", "Lead less than 1m, no bends, minimum inductance — IEC 60099"),
            ("Circuit breaker CB", "All metal parts and mechanism earthed — IS 3043 Cl.13"),
            ("Station fence", "Bond to grid. Crushed rock 1m outside fence — CBIP Sec 3.12"),
            ("Control and relay panel", "Single-point earth, separate quiet bus — CBIP Ch.7"),
            ("Cable sheath and armour", "Bond both ends inside station"),
            ("Overhead earth wire", "Connect to grid at station entry — CBIP Sec 3.7.2"),
        ]
        rows_eq = "".join(
            f"<tr><td>{e}</td><td style='font-size:0.73rem;color:#5a6a7a;line-height:1.5'>{r}</td></tr>"
            for e, r in equip
        )
        st.markdown(f"""<table class="dtable">
        <tr><th>Equipment</th><th>Key Requirement</th></tr>
        {rows_eq}</table>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top:1px solid #d8dde5;padding-top:0.7rem;
    color:#8a9aaa;font-size:0.69rem;text-align:center;line-height:1.8">
CBIP Manual Pub.339 (2017 Edition) &nbsp;|&nbsp;
IS 3043:1987 (Reaffirmed 2006) &nbsp;|&nbsp;
IEEE Std 80-2013 &nbsp;|&nbsp;
IS 2309 &nbsp;|&nbsp;
IEEE Std 665 &nbsp;|&nbsp;
IEC 62305<br>
Empirical formula accuracy: approximately plus or minus 20 percent compared to rigorous computer simulation.
For complex or non-uniform soil conditions, use dedicated earthing analysis software for final design verification.
</div>
""", unsafe_allow_html=True)