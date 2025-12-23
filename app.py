import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import weibull_min
from fpdf import FPDF
import os

# --- 1. PAGE CONFIG & BRANDING ---
st.set_page_config(page_title="MoZ CapEx Strategic Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stMetricValue"] { font-size: 30px; font-weight: bold; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
        border: 1px solid #eceeef;
    }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PROFESSIONAL PDF CLASS (MATCHES REPORT FORMAT) ---
class MoZReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CONFIDENTIAL EXECUTIVE MEMORANDUM', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'To: Board of Directors, WestProp Holdings', 0, 1, 'L')
        self.cell(0, 5, 'Subject: 20-Year Capital Reserve Strategic Analysis', 0, 1, 'L')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, title, 0, 1, 'L', fill=True)
        self.ln(5)

# --- 3. SESSION STATE & SYNC CALLBACKS ---
def sync_usd_i(): st.session_state.usd_slider = st.session_state.usd_i
def sync_usd_s(): st.session_state.usd_i = st.session_state.usd_slider
def sync_zwg_i(): st.session_state.zwg_slider = st.session_state.zwg_i
def sync_zwg_s(): st.session_state.zwg_i = st.session_state.zwg_slider

for key, val in [("usd_slider", 14.2), ("usd_i", 14.2), ("zwg_slider", 10.0), ("zwg_i", 10.0)]:
    if key not in st.session_state: st.session_state[key] = val
if 'has_run' not in st.session_state: st.session_state.has_run = False

# --- 4. COMPONENT DNA ---
COMPONENTS = {
    "AI_HVAC_Systems": {"cost": 8800000, "life": 22, "local": 0.3},
    "4MW_Solar_Microgrid": {"cost": 6880000, "life": 12, "local": 0.15},
    "Roofing_High_Grade": {"cost": 9900000, "life": 25, "local": 0.5},
    "Escalators_Elevators": {"cost": 2400000, "life": 20, "local": 0.4},
    "LED_Retrofit": {"cost": 3400000, "life": 19, "local": 0.2}
}

@st.cache_data
def run_simulation(usd_rate, zwg_rate, iterations):
    np.random.seed(42) # ENSURES DASHBOARD MATCHES REPORT EXACTLY
    horizon, all_runs = 20, []
    u_r, z_r = usd_rate / 100, zwg_rate / 100
    for _ in range(iterations):
        yearly_spend = np.zeros(horizon + 1)
        for name, data in COMPONENTS.items():
            fail_year = int(round(weibull_min.rvs(3.5, scale=data['life']/0.9)))
            if 0 < fail_year <= horizon:
                l_part = (data['cost'] * data['local']) * ((1 + z_r) ** fail_year)
                i_part = (data['cost'] * (1 - data['local'])) * ((1 + u_r) ** fail_year)
                yearly_spend[fail_year] += (l_part + i_part)
        all_runs.append(yearly_spend)
    res = np.array(all_runs)
    return res.mean(axis=0), np.percentile(res, 95, axis=0)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("📈 Economic Stress Test")
    
    # USD Inflation Section
    st.markdown("### USD Import Inflation (%)", help="Current stress-test baseline is 14.2% based on specialized tech imports.")
    c1, c2 = st.columns([2, 1])
    with c1: st.slider("USD Slider", 2.0, 20.0, step=0.1, key="usd_slider", on_change=sync_usd_s, label_visibility="collapsed")
    with c2: st.number_input("USD Box", 2.0, 20.0, step=0.1, key="usd_i", on_change=sync_usd_i, label_visibility="collapsed")
    
    st.divider()
    
    # Local Labor Inflation Section (NEW TOOLTIP ADDED)
    st.markdown("### Local Labor Inflation (%)", 
                help="Applies to civil works and local materials. The WestProp stabilization target for long-term planning is 10.0%.")
    c3, c4 = st.columns([2, 1])
    with c3: st.slider("ZWG Slider", 2.0, 50.0, step=0.1, key="zwg_slider", on_change=sync_zwg_s, label_visibility="collapsed")
    with c4: st.number_input("ZWG Box", 2.0, 50.0, step=0.1, key="zwg_i", on_change=sync_zwg_i, label_visibility="collapsed")
    
    st.divider()
    
    # Simulation Precision Section (NEW TOOLTIP ADDED)
    n_sims = st.select_slider("Simulation Precision", 
                              options=[1000, 5000, 10000], 
                              value=5000,
                              help="Higher precision (10k) reduces statistical noise in the P95 Risk Case, vital for formal board reporting.")
    
    # Action Buttons
    col_run, col_ref = st.columns(2)
    with col_run: run_btn = st.button("🚀 Run", type="primary", use_container_width=True)
    with col_ref: 
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.usd_i = 14.2; st.session_state.usd_slider = 14.2
            st.session_state.zwg_i = 10.0; st.session_state.zwg_slider = 10.0
            st.rerun()

# --- 6. MAIN DASHBOARD ---
st.title("🏙️ Mall of Zimbabwe: 20-Year CapEx Tool")
st.write("Strategic Reserve Forecasting for the $100M+ WestProp Flagship Asset.")

if run_btn:
    st.session_state.has_run = True
    mean_vals, p95_vals = run_simulation(st.session_state.usd_i, st.session_state.zwg_i, n_sims)
    st.session_state.results = (mean_vals, p95_vals)

if st.session_state.has_run:
    mean_vals, p95_vals = st.session_state.results
    total_mean, total_p95 = mean_vals.sum(), p95_vals.sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Avg. 20-Year Spend", f"${total_mean/1e6:.1f}M")
    m2.metric("P95 Risk Case", f"${total_p95/1e6:.1f}M", f"{((total_p95/total_mean)-1)*100:.1f}% Risk Gap", delta_color="inverse")
    m3.metric("Annual Reserve Needed", f"${(total_mean/20)/1e6:.2f}M")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(range(21)), y=mean_vals, name="Expected Mean", marker_color='seagreen'))
    fig.add_trace(go.Scatter(x=list(range(21)), y=p95_vals, name="95th Percentile Risk", line=dict(color='crimson', dash='dash')))
    fig.update_layout(title=f"CapEx Waterfall ({st.session_state.usd_i}% USD Inflation)", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    # --- DYNAMIC INSIGHTS EXPANDER (DIRECTLY BELOW CHART) ---
    with st.expander("📝 Strategic Interpretation"):
        st.info(f"""
        - At **{st.session_state.usd_i}%** USD inflation, the replacement cost of technology triples roughly every 8 years.
        - The **Annual Reserve** of **${(total_mean/20)/1e6:.2f}M** should be indexed to hard-currency assets to prevent purchasing power erosion.
        """)

    # --- DYNAMIC PDF GENERATOR (MATCHES ATTACHED FORMAT) ---
    if st.button("📑 Generate & Download PDF Report"):
        try:
            fig.write_image("live_chart.png")
            pdf = MoZReport()
            pdf.add_page()
            
            # Page 1: Viz & Table
            pdf.chapter_title('1. Capital Expenditure (CapEx) Forecast Visualization')
            pdf.image('live_chart.png', x=10, w=190)
            pdf.ln(10)
            pdf.chapter_title('2. Financial Benchmarks')
            pdf.set_font('Arial', '', 10)
            pdf.cell(95, 10, 'Total 20yr Expected Spend (Mean)', 1); pdf.cell(95, 10, f'${total_mean/1e6:.1f} Million', 1); pdf.ln()
            pdf.cell(95, 10, 'Total 20yr Risk Case (P95)', 1); pdf.cell(95, 10, f'${total_p95/1e6:.1f} Million', 1); pdf.ln()
            pdf.cell(95, 10, 'Annual Reserve Contribution', 1); pdf.cell(95, 10, f'${(total_mean/20)/1e6:.2f} Million', 1); pdf.ln()
            
            # Page 2: Interpretation
            pdf.add_page()
            pdf.chapter_title('3. Executive Strategic Interpretation')
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 8, (
                f"The 20-Year CapEx Waterfall for the Mall of Zimbabwe provides a high-level financial roadmap "
                f"for maintaining this $100M+ asset. At {st.session_state.usd_i}% USD inflation, "
                f"the expected total spend is ${total_mean/1e6:.1f}M.\n\n"
                f"STRATEGIC INSIGHTS:\n"
                f"- The 'Safety Gap': The difference between the mean and the ${total_p95/1e6:.1f}M risk case "
                f"necessitates holding reserves in hard assets.\n"
                f"- Annual Reserve: Based on this simulation, a contribution of ${(total_mean/20)/1e6:.2f}M "
                f"per year is recommended beginning at opening in 2028."
            ))
            pdf.output("MoZ_Dynamic_Report.pdf")
            with open("MoZ_Dynamic_Report.pdf", "rb") as f:
                st.download_button("📥 Click here to Save PDF", f, file_name="MoZ_Strategic_Report.pdf")
        except Exception as e:
            st.error(f"Error generating PDF: {e}. Ensure Kaleido is installed.")

else:
    # --- LANDING PAGE (With New Image) ---
    if os.path.exists("assets/mall_render.jpg"):
        st.image("assets/mall_render.jpg", use_container_width=True)
    else:
        st.warning("⚠️ Image not found: assets/mall_render.jpg")

    st.info("👈 Set parameters and click **'Run'** to generate the analysis.")