import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(
    page_title="MRP · MCP Optimizer",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght=300;400;500;600&family=DM+Mono:wght=400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #FDF6F9;
}

[data-testid="stSidebar"] {
    background: #3D1A2E !important;
    border-right: 1px solid #5C2A45;
}
[data-testid="stSidebar"] * {
    color: #F5D6E8 !important;
}
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FDE8F2 !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
    background: #5C2A45 !important;
    color: #FDE8F2 !important;
    border: 1px solid #8B4F72 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 15px !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] input:focus {
    border-color: #F4A7C9 !important;
    box-shadow: 0 0 0 2px rgba(244,167,201,0.2) !important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-minimal"] {
    background: #5C2A45 !important;
    color: #F4A7C9 !important;
    border: 1px solid #8B4F72 !important;
}

.block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1400px;
}

/* Updated Hero Banner using Flexbox for Side-by-Side layout */
.hero-container {
    background: linear-gradient(135deg, #3D1A2E 0%, #7B3560 55%, #E8789F 100%);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(244,167,201,0.15);
    z-index: 1;
}
.hero-container::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
    z-index: 1;
}
.hero-content {
    position: relative;
    z-index: 2;
}
.hero-logo-wrapper {
    position: relative;
    z-index: 2;
    background: rgba(255, 255, 255, 0.9);
    padding: 8px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
}
.hero-title {
    font-size: 28px;
    font-weight: 600;
    color: #FDE8F2;
    margin: 0 0 6px;
    letter-spacing: -0.3px;
}
.hero-sub {
    font-size: 14px;
    color: #F5C2D8;
    margin: 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(244,167,201,0.2);
    color: #F9C8DE;
    border: 1px solid rgba(244,167,201,0.4);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
}

.metric-card {
    background: white;
    border-radius: 12px;
    padding: 18px 20px;
    border: 1px solid #F5D6E8;
    box-shadow: 0 1px 6px rgba(180,80,130,0.07);
}
.metric-label {
    font-size: 11px;
    font-weight: 600;
    color: #C084A0;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 22px;
    font-weight: 600;
    color: #3D1A2E;
    font-family: 'DM Mono', monospace;
    line-height: 1.2;
}
.metric-sub {
    font-size: 11px;
    color: #C084A0;
    margin-top: 3px;
}
.metric-card.blue  { border-top: 3px solid #E8789F; }
.metric-card.green { border-top: 3px solid #D4A0BC; }
.metric-card.amber { border-top: 3px solid #F0B8D0; }

.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 24px 0 14px;
}
.section-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #3D1A2E;
}
.section-subtitle {
    font-size: 12px;
    color: #B07090;
    margin-top: 1px;
}

[data-testid="stFileUploader"] {
    background: white;
    border-radius: 12px;
    padding: 4px;
    border: 2px dashed #F0B8D0;
}
[data-testid="stFileUploader"]:hover {
    border-color: #E8789F;
}

[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden;
    border: 1px solid #F5D6E8 !important;
}

[data-testid="stDownloadButton"] button {
    background: #7B3560 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    letter-spacing: 0.2px !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: #3D1A2E !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(123,53,96,0.3) !important;
}

.info-box {
    background: #FFF0F7;
    border: 1px solid #F9C8DE;
    border-left: 4px solid #E8789F;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #7B3560;
}
.warn-box {
    background: #FFF5F0;
    border: 1px solid #FDD5C0;
    border-left: 4px solid #F0956A;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #8B3A1A;
}
.success-box {
    background: #FFF0F7;
    border: 1px solid #F5C2D8;
    border-left: 4px solid #D4709A;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #7B3560;
}

.sidebar-section {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #8B4F72 !important;
    padding: 16px 0 6px;
    border-top: 1px solid #5C2A45;
    margin-top: 8px;
}

hr { border-color: #F5D6E8 !important; margin: 24px 0 !important; }

#MainMenu, footer { visibility: hidden; }

header[data-testid="stHeader"] {
    background-color: transparent !important;
    background-image: none !important;
}

header[data-testid="stHeader"] button {
    background-color: #FFF0F7 !important;
    color: #7B3560 !important;
    border: 1px solid #F9C8DE !important;
    margin-left: 10px !important;
    border-radius: 8px !important;
}
header[data-testid="stHeader"] button:hover {
    background-color: #7B3560 !important;
    color: white !important;
}

.stDataEditor {
    border-radius: 10px !important;
    border: 1px solid #F5D6E8 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 16px'>
        <div style='font-size:22px; font-weight:700; color:#FDE8F2; letter-spacing:-0.5px'>MCP Optimizer</div>
        <div style='font-size:12px; color:#8B4F72; margin-top:3px'>Material Requirements Planning</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Cost Parameters</div>', unsafe_allow_html=True)
    setup_cost    = st.number_input("Setup Cost per Order (S)", value=750, min_value=0, help="Fixed cost each time an order is placed")
    holding_cost  = st.number_input("Holding Cost per Unit (H)", value=500, min_value=0, help="Storage cost per unit per period")

    st.markdown('<div class="sidebar-section">Inventory</div>', unsafe_allow_html=True)
    initial_inventory = st.number_input("Initial Inventory", value=1000, min_value=0, help="Opening stock at the first period")
    safety_stock      = st.number_input("Safety Stock", value=500, min_value=0, help="Minimum safety stock that must always be maintained")

    st.markdown('<div class="sidebar-section">Time</div>', unsafe_allow_html=True)
    lead_time = st.number_input("Lead Time (periods)", value=1, min_value=0, help="Gap between ordering and receiving goods")

    st.markdown("""
    <div style='margin-top:24px; padding:14px; background:#5C2A45; border-radius:10px; border:1px solid #8B4F72'>
        <div style='font-size:11px; font-weight:600; color:#F4A7C9; letter-spacing:0.5px; margin-bottom:8px'>HOW TO USE</div>
        <div style='font-size:11px; color:#C084A0; line-height:1.6'>
            1. Set parameters above<br>
            2. Enter data manually <b>or</b> upload CSV<br>
            3. Results are calculated automatically<br>
            4. Download the report
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ─── Watermark section at the bottom of the sidebar ───
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='border-top: 1px solid #5C2A45; padding-top: 16px; text-align: center;'>
        <div style='font-size: 9px; color: #8B4F72; text-transform: uppercase; letter-spacing: 1px;'>Powered by</div>
        <div style='font-size: 12px; font-weight: 600; color: #F4A7C9; margin-top: 2px;'>ELITE Laboratory</div>
        <div style='font-size: 10px; color: #C084A0; font-style: italic;'>Basic Industrial Engineering</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Hero Banner with Logo ELITE ──────────────────────────────────────────────
# Menggunakan link langsung image_e51407.png yang Anda upload
st.markdown("""
<div class="hero-container">
    <div class="hero-content">
        <div class="hero-badge">MCP · Minimum Cost Per Period</div>
        <div class="hero-title">📦 MRP Optimization Dashboard</div>
        <div class="hero-sub">Automatically calculate optimal lot sizing using the Minimum Cost Per Period method</div>
    </div>
    <div class="hero-logo-wrapper">
        <img src="https://instances.static.asst.ai/fe34bb76-2f3b-486d-ab12-680c65792ba2/image_e51407.png" width="85" alt="ELITE Logo">
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Data Input Section ───────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#FFF0F7">📂</div>
    <div>
        <div class="section-title">Data Input</div>
        <div class="section-subtitle">Enter data manually below, or upload a CSV file with columns: Period, GR, Scheduled_Receipts</div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_manual, tab_upload = st.tabs(["✏️  Manual Entry", "📤  Upload CSV"])

df_input = None

# ── Tab 1: Manual Entry ───────────────────────────────────────────────────────
with tab_manual:
    st.markdown("""
    <div class="info-box">
        💡 <strong>Manual Entry.</strong> Fill out the table below. <br>
        • Click the <b>+ Add row</b> button at the bottom of the table to insert a new period.<br>
        • To <b>delete a row</b>, click/check the box on the leftmost side of the row you want to remove, then press the <b>Delete</b> key on your keyboard.
    </div>
    """, unsafe_allow_html=True)

    default_data = pd.DataFrame(columns=["Period", "GR", "Scheduled_Receipts"])

    edited_df = st.data_editor(
        default_data,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Period": st.column_config.TextColumn(
                "Period", 
                help="e.g., P1, W1, Jan, Week 1", 
                width="small",
                required=True
            ),
            "GR": st.column_config.NumberColumn(
                "Gross Requirements (GR)", 
                min_value=0, 
                step=1, 
                format="%d",
                help="Enter the GR value (Numerical)"
            ),
            "Scheduled_Receipts": st.column_config.NumberColumn(
                "Scheduled Receipts (SR)", 
                min_value=0, 
                step=1, 
                format="%d",
                help="Enter the SR value (Numerical)"
            ),
        },
        height=420,
    )

    if st.button("▶  Run MCP with Manual Data", type="primary"):
        if edited_df is not None and len(edited_df) > 0:
            cleaned_df = edited_df.dropna(subset=['Period', 'GR'])
            if len(cleaned_df) < 1:
                st.markdown('<div class="warn-box">⚠️ Please fill in at least the "Period" and "GR" columns for one row before running the optimization.</div>', unsafe_allow_html=True)
            else:
                df_input = cleaned_df.copy()
                st.session_state["df_input"] = df_input
                st.session_state["source"] = "manual"
                st.rerun()
        else:
            st.markdown('<div class="warn-box">⚠️ Please click "+ Add row" and enter your period data first.</div>', unsafe_allow_html=True)
            
# ── Tab 2: CSV Upload ─────────────────────────────────────────────────────────
with tab_upload:
    st.markdown("""
    <div class="info-box">
        💡 <strong>CSV Upload.</strong> Upload a CSV file containing columns 
        <code>Period</code>, <code>GR</code>, and <code>Scheduled_Receipts</code>. 
        The file will be processed automatically once uploaded.
    </div>
    """, unsafe_allow_html=True)

    uploaded_csv = st.file_uploader("", type=["csv"], key="mcp_upload", label_visibility="collapsed")

    if uploaded_csv:
        df_csv = pd.read_csv(uploaded_csv)
        required_cols = {'GR', 'Scheduled_Receipts'}
        if not required_cols.issubset(df_csv.columns):
            st.markdown('<div class="warn-box">⚠️ <strong>Incorrect CSV format.</strong> Please ensure the file has <code>GR</code> and <code>Scheduled_Receipts</code> columns.</div>', unsafe_allow_html=True)
        else:
            df_input = df_csv.copy()
            st.session_state["df_input"] = df_input
            st.session_state["source"] = "csv"
            st.markdown(f'<div class="success-box">✅ <strong>File uploaded successfully.</strong> {len(df_csv)} periods loaded.</div>', unsafe_allow_html=True)
            st.dataframe(df_csv, use_container_width=True, height=300)

if df_input is None and "df_input" in st.session_state:
    df_input = st.session_state["df_input"]

if df_input is None:
    st.markdown("""
    <div class="info-box">
        💡 <strong>No data yet.</strong> Enter data in the <b>Manual Entry</b> tab and click Run, 
        or upload a CSV file in the <b>Upload CSV</b> tab.
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─── Read & Process ───────────────────────────────────────────────────────────
if df_input is not None:
    df_input.columns = df_input.columns.str.strip()
    df_input = df_input.dropna(how='all')

    if 'Period' in df_input.columns:
        df_input = df_input[df_input['Period'].notna()]
        df_input = df_input[df_input['Period'].astype(str).str.strip().str.lower() != 'none']
        periods_label = df_input['Period'].astype(str).tolist()
    else:
        periods_label = [f"P{i+1}" for i in range(len(df_input))]

    if 'GR' in df_input.columns:
        df_input = df_input.dropna(subset=['GR'])
        df_input = df_input[df_input['GR'].astype(str).str.strip().str.lower() != 'none']
        gross_req = pd.to_numeric(df_input['GR'], errors='coerce').fillna(0).astype(int).tolist()
    else:
        gross_req = [0] * len(df_input)

    if 'Scheduled_Receipts' in df_input.columns:
        scheduled_rec = pd.to_numeric(df_input['Scheduled_Receipts'], errors='coerce').fillna(0).astype(int).tolist()
    elif 'SR' in df_input.columns:
        scheduled_rec = pd.to_numeric(df_input['SR'], errors='coerce').fillna(0).astype(int).tolist()
    else:
        scheduled_rec = [0] * len(df_input)

    periods = len(gross_req)
    periods_label = periods_label[:periods]

# ── MCP Algorithm ─────────────────────────────────────────────────────────────
all_iterations       = []
optimal_combinations = []
final_planned_receipts = [0] * periods

i = 0
current_inventory = initial_inventory

while i < periods:
    best_combo = None
    combos_tried = []
    local_prev_cost_per_period = None

    for j in range(i, periods):
        temp_inventory = current_inventory
        nr_list = []
        for k in range(i, j + 1):
            nr = max(0, gross_req[k] + safety_stock - (temp_inventory + scheduled_rec[k]))
            nr_list.append(nr)
            temp_inventory += nr + scheduled_rec[k] - gross_req[k]

        net_demand = sum(nr_list)

        temp_inventory_flow = current_inventory
        cumulative_holding  = 0
        for idx, k in enumerate(range(i, j + 1)):
            planned_rec_p    = net_demand if idx == 0 else 0
            ending_inventory = temp_inventory_flow + planned_rec_p + scheduled_rec[k] - gross_req[k]
            if ending_inventory > 0 and k < j:
                cumulative_holding += ending_inventory
            temp_inventory_flow = max(0, ending_inventory)

        total_cost      = setup_cost + (holding_cost * cumulative_holding)
        cost_per_period = total_cost / (j - i + 1)

        current_combo_info = {
            "Period Combination": f"{periods_label[i]}–{periods_label[j]}" if i != j else periods_label[i],
            "Net Requirement":    net_demand,
            "Lot Size":           net_demand,
            "Total Cost":         total_cost,
            "Cost/Period":        round(cost_per_period, 2),
        }
        combos_tried.append(current_combo_info)

        if local_prev_cost_per_period is not None and cost_per_period > local_prev_cost_per_period:
            break
        else:
            best_combo = (i, j, net_demand, total_cost, cost_per_period)
            local_prev_cost_per_period = cost_per_period

    if best_combo is None:
        best_combo = (i, i, nr_list[0], setup_cost, setup_cost)

    all_iterations.extend(combos_tried)
    start, end, lot_size, total_cost, cost_per_period = best_combo

    optimal_combinations.append({
        "Step":        f"Step {len(optimal_combinations) + 1}",
        "Period":      f"{periods_label[start]}–{periods_label[end]}" if start != end else periods_label[start],
        "Lot Size":    lot_size,
        "Total Cost":  total_cost,
        "Cost/Period": round(cost_per_period, 2),
    })

    final_planned_receipts[start] = lot_size
    current_inventory += lot_size + scheduled_rec[start] - gross_req[start]
    for k in range(start + 1, end + 1):
        current_inventory += scheduled_rec[k] - gross_req[k]
    current_inventory = max(0, current_inventory)
    i = end + 1


# ── Build Final MRP Table ──────────────────────────────────────────────────────
mrp_gross_req        = []
mrp_scheduled_rec    = []
mrp_projected_bal    = []
mrp_net_req          = []
mrp_planned_receipts = final_planned_receipts.copy()
mrp_planned_releases = [0] * periods

temp_inv = initial_inventory
for k in range(periods):
    mrp_gross_req.append(gross_req[k])
    mrp_scheduled_rec.append(scheduled_rec[k])
    nr_aktual = max(0, gross_req[k] + safety_stock - (temp_inv + scheduled_rec[k]))
    mrp_net_req.append(nr_aktual)
    temp_inv += mrp_planned_receipts[k] + scheduled_rec[k] - gross_req[k]
    mrp_projected_bal.append(temp_inv)
    release_period = k - int(lead_time)
    if release_period >= 0:
        mrp_planned_releases[release_period] = mrp_planned_receipts[k]


# ── Build Cost Breakdown Table ─────────────────────────────────────────────────
cost_breakdown = []
for k in range(periods):
    lot   = mrp_planned_receipts[k]
    pab   = mrp_projected_bal[k]
    sc    = setup_cost if lot > 0 else 0
    hc    = holding_cost * max(0, pab - safety_stock)
    total = sc + hc
    cost_breakdown.append({
        "Period":          periods_label[k],
        "GR":              mrp_gross_req[k],
        "Lot Size (PORec)": lot,
        "Ending Balance":  pab,
        "Setup Cost":      sc,
        "Holding Cost":    hc,
        "Total Cost":      total,
    })

df_cost = pd.DataFrame(cost_breakdown)

total_setup   = df_cost["Setup Cost"].sum()
total_holding = df_cost["Holding Cost"].sum()
grand_total   = df_cost["Total Cost"].sum()
total_orders  = sum(1 for x in mrp_planned_receipts if x > 0)
total_units   = sum(mrp_planned_receipts)


# ─── METRIC CARDS ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#FFF0F7">📊</div>
    <div>
        <div class="section-title">Results Summary</div>
        <div class="section-subtitle">MCP optimization results for the entire planning horizon</div>
    </div>
</div>
""", unsafe_allow_html=True)

def fmt_rp(val):
    if val >= 1_000_000:
        return f"Rp {val/1_000_000:.1f}M"
    elif val >= 1_000:
        return f"Rp {val/1_000:.0f}K"
    return f"Rp {val:,.0f}"

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Grand Total Cost</div>
        <div class="metric-value">{fmt_rp(grand_total)}</div>
        <div class="metric-sub">Overall total cost</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Total Setup Cost</div>
        <div class="metric-value">{fmt_rp(total_setup)}</div>
        <div class="metric-sub">{total_orders} order(s) placed</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-card amber">
        <div class="metric-label">Total Holding Cost</div>
        <div class="metric-value">{fmt_rp(total_holding)}</div>
        <div class="metric-sub">From {total_units:,} units ordered in total</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── ITERATION TABLES ─────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#FFF0F7">🔍</div>
    <div>
        <div class="section-title">MCP Iteration Process</div>
        <div class="section-subtitle">All combinations tested and the best result for each step</div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2], gap="large")
with col1:
    st.markdown("**All Iterations Tested**")
    df_iter = pd.DataFrame(all_iterations)
    st.dataframe(
        df_iter.style
            .format({"Total Cost": "{:,.0f}", "Cost/Period": "{:,.1f}", "Net Requirement": "{:,}", "Lot Size": "{:,}"})
            .set_properties(**{"font-size": "12px"}),
        use_container_width=True, height=340
    )
with col2:
    st.markdown("**Optimal Combination per Step**")
    df_opt = pd.DataFrame(optimal_combinations)
    st.dataframe(
        df_opt.style
            .format({"Total Cost": "{:,.0f}", "Cost/Period": "{:,.1f}", "Lot Size": "{:,}"})
            .set_properties(**{"font-size": "12px"})
            .map(lambda _: "background-color:#FFF0F7; color:#7B3560; font-weight:600",
                 subset=["Cost/Period"]),
        use_container_width=True, height=340
    )

st.markdown("<hr>", unsafe_allow_html=True)


# ─── FINAL MRP SHEET ──────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#FFF5F9">📋</div>
    <div>
        <div class="section-title">Final MRP Sheet</div>
        <div class="section-subtitle">Complete material planning table from MCP optimization</div>
    </div>
</div>
""", unsafe_allow_html=True)

mrp_matrix = {"Row / Period": [
    "Gross Requirements (GR)",
    "Scheduled Receipts (SR)",
    "Projected Available Balance (PAB)",
    "Net Requirements (NR)",
    "Planned Order Receipts (PORec)",
    "Planned Order Releases (PORel)"
]}
for k in range(periods):
    lbl = periods_label[k]
    mrp_matrix[lbl] = [
        mrp_gross_req[k], mrp_scheduled_rec[k], mrp_projected_bal[k],
        mrp_net_req[k], mrp_planned_receipts[k], mrp_planned_releases[k]
    ]

df_mrp = pd.DataFrame(mrp_matrix).set_index("Row / Period")

def style_mrp(df):
    styles = pd.DataFrame("", index=df.index, columns=df.columns)
    row_colors = {
        "Gross Requirements (GR)":           "background:#FDF6F9; font-weight:600",
        "Scheduled Receipts (SR)":            "background:#FDF6F9",
        "Projected Available Balance (PAB)":  "background:#FFF0F7; color:#7B3560",
        "Net Requirements (NR)":              "background:#FFE8F2; color:#9B2D5A; font-weight:600",
        "Planned Order Receipts (PORec)":     "background:#FFF5FB; color:#7B3560; font-weight:600",
        "Planned Order Releases (PORel)":     "background:#FFEEF6; color:#C96B9A; font-weight:600",
    }
    for row, style in row_colors.items():
        if row in df.index:
            styles.loc[row] = style
    return styles

st.dataframe(
    df_mrp.style.apply(style_mrp, axis=None).format("{:,.0f}"),
    use_container_width=True, height=260
)

st.markdown("<hr>", unsafe_allow_html=True)


# ─── COST BREAKDOWN TABLE ──────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#FFE8F2">💰</div>
    <div>
        <div class="section-title">Cost Breakdown by Period</div>
        <div class="section-subtitle">Setup cost + Holding cost + Total cost per period</div>
    </div>
</div>
""", unsafe_allow_html=True)

df_cost_display = df_cost.copy()
total_row = {
    "Period":          "TOTAL",
    "GR":              sum(mrp_gross_req),
    "Lot Size (PORec)": total_units,
    "Ending Balance":  "-",
    "Setup Cost":      total_setup,
    "Holding Cost":    total_holding,
    "Total Cost":      grand_total,
}
df_cost_display = pd.concat([df_cost_display, pd.DataFrame([total_row])], ignore_index=True)

def style_cost(df):
    styles = pd.DataFrame("", index=df.index, columns=df.columns)
    last = len(df) - 1
    styles.iloc[last] = "background:#3D1A2E; color:#FDE8F2; font-weight:700"
    for i in range(len(df) - 1):
        if df.iloc[i]["Setup Cost"] > 0:
            styles.iloc[i, df.columns.get_loc("Setup Cost")] = "background:#FFF0F7; color:#7B3560; font-weight:600"
        if df.iloc[i]["Holding Cost"] > 0:
            styles.iloc[i, df.columns.get_loc("Holding Cost")] = "background:#FFE8F2; color:#9B2D5A"
        styles.iloc[i, df.columns.get_loc("Total Cost")] = "font-weight:600"
    return styles

fmt_cost = {
    "GR": "{:,.0f}", "Lot Size (PORec)": "{:,.0f}",
    "Setup Cost": "{:,.0f}", "Holding Cost": "{:,.0f}", "Total Cost": "{:,.0f}"
}

st.dataframe(
    df_cost_display.style.apply(style_cost, axis=None).format(fmt_cost, na_rep="-"),
    use_container_width=True, height=460
)

st.markdown(f"""
<div class="success-box">
    ✅ <strong>Cost Summary:</strong>
    Total Setup Cost = <strong>Rp {total_setup:,.0f}</strong> ({total_orders} order(s)) &nbsp;|&nbsp;
    Total Holding Cost = <strong>Rp {total_holding:,.0f}</strong> &nbsp;|&nbsp;
    <strong>Grand Total = Rp {grand_total:,.0f}</strong>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ─── CHARTS ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#FFF0F7">📈</div>
    <div>
        <div class="section-title">Visualization</div>
        <div class="section-subtitle">Demand, lot sizing, and cost analysis charts</div>
    </div>
</div>
""", unsafe_allow_html=True)

chart_labels = periods_label

c1, c2 = st.columns(2, gap="large")

with c1:
    fig1 = go.Figure()
    fig1.add_bar(x=chart_labels, y=mrp_gross_req, name="GR", marker_color="#F472B6", opacity=0.9)
    fig1.add_bar(x=chart_labels, y=mrp_planned_receipts, name="Lot Size (PORec)", marker_color="#7E1D4E", opacity=0.9)
    fig1.update_layout(
        title=dict(text="GR vs Lot Size per Period", font=dict(size=14, family="DM Sans")),
        barmode="group", height=340,
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(gridcolor="#FDF0F5"),
        yaxis=dict(gridcolor="#FDF0F5"),
        font=dict(family="DM Sans", size=11)
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    sc_vals = df_cost["Setup Cost"].tolist()
    hc_vals = df_cost["Holding Cost"].tolist()
    fig2 = go.Figure()
    fig2.add_bar(x=chart_labels, y=sc_vals, name="Setup Cost", marker_color="#7E1D4E", opacity=0.9)
    fig2.add_bar(x=chart_labels, y=hc_vals, name="Holding Cost", marker_color="#FBCFE8", opacity=0.95)
    fig2.update_layout(
        title=dict(text="Setup vs Holding Cost per Period", font=dict(size=14, family="DM Sans")),
        barmode="stack", height=340,
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(gridcolor="#FDF0F5"),
        yaxis=dict(gridcolor="#FDF0F5"),
        font=dict(family="DM Sans", size=11)
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ─── DOWNLOAD ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#FFF0F7">📥</div>
    <div>
        <div class="section-title">Download Report</div>
        <div class="section-subtitle">Export all analysis results in a single file</div>
    </div>
</div>
""", unsafe_allow_html=True)

df_mrp_reset = df_mrp.reset_index()
df_cost_dl   = df_cost_display.copy()

csv_out = BytesIO()
with pd.ExcelWriter(csv_out, engine='openpyxl') as writer:
    df_mrp_reset.to_excel(writer, sheet_name="Final MRP Sheet", index=False)
    df_cost_dl.to_excel(writer, sheet_name="Cost Breakdown", index=False)
    pd.DataFrame(optimal_combinations).to_excel(writer, sheet_name="Optimal Combinations", index=False)
    pd.DataFrame(all_iterations).to_excel(writer, sheet_name="All Iterations", index=False)

col_dl1, col_dl2, col_dl3 = st.columns([2, 2, 4])
with col_dl1:
    st.download_button(
        label="📥 Download Full Excel Report",
        data=csv_out.getvalue(),
        file_name="mcp_report_full.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
with col_dl2:
    csv_simple = BytesIO()
    df_mrp_reset.to_csv(csv_simple, index=False)
    st.download_button(
        label="📄 Download MRP Sheet (CSV)",
        data=csv_simple.getvalue(),
        file_name="final_mrp_sheet.csv",
        mime="text/csv"
    )

st.markdown("""
<div style='margin-top:32px; text-align:center; font-size:11px; color:#C084A0'>
    MRP · MCP Optimizer — Material Requirements Planning Dashboard
</div>
""", unsafe_allow_html=True)
