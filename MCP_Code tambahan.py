import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MRP · MCP Optimizer",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #F0F4F8;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0F172A !important;
    border-right: 1px solid #1E293B;
}
[data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
}
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F1F5F9 !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
    background: #1E293B !important;
    color: #F1F5F9 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 15px !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] input:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,0.15) !important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-minimal"] {
    background: #1E293B !important;
    color: #38BDF8 !important;
    border: 1px solid #334155 !important;
}

/* ── Main area padding ── */
.block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1400px;
}

/* ── Hero header ── */
.hero-banner {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A5F 60%, #0EA5E9 100%);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(14,165,233,0.12);
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    border-radius: 50%;
    background: rgba(56,189,248,0.08);
}
.hero-title {
    font-size: 28px;
    font-weight: 600;
    color: #F1F5F9;
    margin: 0 0 6px;
    letter-spacing: -0.3px;
}
.hero-sub {
    font-size: 14px;
    color: #94A3B8;
    margin: 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(14,165,233,0.2);
    color: #38BDF8;
    border: 1px solid rgba(56,189,248,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
}

/* ── Metric cards ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 18px 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.metric-label {
    font-size: 11px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 22px;
    font-weight: 600;
    color: #0F172A;
    font-family: 'DM Mono', monospace;
    line-height: 1.2;
}
.metric-sub {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 3px;
}
.metric-card.blue  { border-top: 3px solid #0EA5E9; }
.metric-card.green { border-top: 3px solid #10B981; }
.metric-card.amber { border-top: 3px solid #F59E0B; }
.metric-card.red   { border-top: 3px solid #EF4444; }

/* ── Section headers ── */
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
    color: #0F172A;
}
.section-subtitle {
    font-size: 12px;
    color: #94A3B8;
    margin-top: 1px;
}

/* ── Upload area ── */
[data-testid="stFileUploader"] {
    background: white;
    border-radius: 12px;
    padding: 4px;
    border: 2px dashed #CBD5E1;
}
[data-testid="stFileUploader"]:hover {
    border-color: #0EA5E9;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden;
    border: 1px solid #E2E8F0 !important;
}
.dvn-scroller {
    border-radius: 10px !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {
    background: #0F172A !important;
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
    background: #1E293B !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(15,23,42,0.25) !important;
}

/* ── Info/warning boxes ── */
.info-box {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-left: 4px solid #3B82F6;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #1E40AF;
}
.warn-box {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-left: 4px solid #F59E0B;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #92400E;
}
.success-box {
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
    border-left: 4px solid #10B981;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #065F46;
}

/* ── Cost table ── */
.cost-table-wrap {
    background: white;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* ── Sidebar section label ── */
.sidebar-section {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #475569 !important;
    padding: 16px 0 6px;
    border-top: 1px solid #1E293B;
    margin-top: 8px;
}

/* ── Step badge in optimal table ── */
.step-pill {
    background: #EFF6FF;
    color: #1D4ED8;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 12px;
    font-weight: 600;
}

/* ── Divider ── */
hr { border-color: #E2E8F0 !important; margin: 24px 0 !important; }

/* ── Hide default streamlit elements ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 16px'>
        <div style='font-size:22px; font-weight:700; color:#F1F5F9; letter-spacing:-0.5px'>MCP Optimizer</div>
        <div style='font-size:12px; color:#64748B; margin-top:3px'>Material Requirements Planning</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Biaya</div>', unsafe_allow_html=True)
    setup_cost    = st.number_input("Setup Cost per Order (S)", value=750, min_value=0, help="Biaya tetap setiap kali melakukan pemesanan")
    holding_cost  = st.number_input("Holding Cost per Unit (H)", value=500, min_value=0, help="Biaya simpan per unit per periode")

    st.markdown('<div class="sidebar-section">Inventori</div>', unsafe_allow_html=True)
    initial_inventory = st.number_input("Initial Inventory", value=1000, min_value=0, help="Stok awal di periode pertama")
    safety_stock      = st.number_input("Safety Stock", value=500, min_value=0, help="Stok pengaman minimum yang harus selalu tersedia")

    st.markdown('<div class="sidebar-section">Waktu</div>', unsafe_allow_html=True)
    lead_time = st.number_input("Lead Time (periods)", value=1, min_value=0, help="Jarak antara pemesanan dan penerimaan barang")

    st.markdown("""
    <div style='margin-top:32px; padding:14px; background:#1E293B; border-radius:10px; border:1px solid #334155'>
        <div style='font-size:11px; font-weight:600; color:#38BDF8; letter-spacing:0.5px; margin-bottom:8px'>CARA PAKAI</div>
        <div style='font-size:11px; color:#94A3B8; line-height:1.6'>
            1. Atur parameter di atas<br>
            2. Upload file CSV<br>
            3. Analisis hasil otomatis<br>
            4. Download laporan
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:12px; padding:10px 14px; background:#1E293B; border-radius:10px; border:1px solid #334155'>
        <div style='font-size:10px; font-weight:600; color:#475569; letter-spacing:0.5px; margin-bottom:6px'>FORMAT CSV</div>
        <div style='font-family: "DM Mono", monospace; font-size:10px; color:#64748B; line-height:1.8'>
            Period, GR, Scheduled_Receipts<br>
            Jan, 1818, 0<br>
            Feb, 2469, 0<br>
            Mar, 2784, 500
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">MCP · Minimum Cost Per Period</div>
    <div class="hero-title">📦 MRP Optimization Dashboard</div>
    <div class="hero-sub">Hitung lot sizing optimal menggunakan metode Minimum Cost Per Period secara otomatis</div>
</div>
""", unsafe_allow_html=True)


# ─── Upload ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#EFF6FF">📂</div>
    <div>
        <div class="section-title">Upload Data</div>
        <div class="section-subtitle">File CSV dengan kolom: Period, GR, Scheduled_Receipts</div>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_csv = st.file_uploader("", type=["csv"], key="mcp_upload", label_visibility="collapsed")

if not uploaded_csv:
    st.markdown("""
    <div class="info-box">
        💡 <strong>Belum ada data.</strong> Upload file CSV untuk memulai analisis MCP. 
        Pastikan file memiliki kolom <code>Period</code>, <code>GR</code>, dan <code>Scheduled_Receipts</code>.
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─── Read & Process ───────────────────────────────────────────────────────────
df_input = pd.read_csv(uploaded_csv)
required_cols = {'GR', 'Scheduled_Receipts'}
if not required_cols.issubset(df_input.columns):
    st.markdown('<div class="warn-box">⚠️ <strong>Format CSV tidak sesuai.</strong> Pastikan ada kolom <code>GR</code> dan <code>Scheduled_Receipts</code>.</div>', unsafe_allow_html=True)
    st.stop()

periods        = len(df_input)
periods_label  = [f"P{i+1}" for i in range(periods)]
gross_req      = df_input['GR'].tolist()
scheduled_rec  = df_input['Scheduled_Receipts'].tolist()

# ── MCP Algorithm ─────────────────────────────────────────────────────────────
all_iterations      = []
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
        for k in range(i, j+1):
            nr = max(0, gross_req[k] + safety_stock - (temp_inventory + scheduled_rec[k]))
            nr_list.append(nr)
            temp_inventory += nr + scheduled_rec[k] - gross_req[k]

        net_demand = sum(nr_list)

        temp_inventory_flow = current_inventory
        cumulative_holding = 0
        for idx, k in enumerate(range(i, j+1)):
            planned_rec_p = net_demand if idx == 0 else 0
            ending_inventory = temp_inventory_flow + planned_rec_p + scheduled_rec[k] - gross_req[k]
            if ending_inventory > 0 and k < j:
                cumulative_holding += ending_inventory
            temp_inventory_flow = max(0, ending_inventory)

        total_cost      = setup_cost + (holding_cost * cumulative_holding)
        cost_per_period = total_cost / (j - i + 1)

        current_combo_info = {
            "Kombinasi Periode": f"{periods_label[i]}–{periods_label[j]}" if i != j else periods_label[i],
            "Net Requirement":   net_demand,
            "Lot Size":          net_demand,
            "Total Cost (Rp)":   total_cost,
            "Cost/Period (Rp)":  round(cost_per_period, 2),
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
        "Step": f"Step {len(optimal_combinations)+1}",
        "Periode": f"{periods_label[start]}–{periods_label[end]}" if start != end else periods_label[start],
        "Lot Size": lot_size,
        "Total Cost (Rp)": total_cost,
        "Cost/Period (Rp)": round(cost_per_period, 2),
    })

    final_planned_receipts[start] = lot_size
    current_inventory += lot_size + scheduled_rec[start] - gross_req[start]
    for k in range(start + 1, end + 1):
        current_inventory += scheduled_rec[k] - gross_req[k]
    current_inventory = max(0, current_inventory)
    i = end + 1

# ── Build Final MRP Table ──────────────────────────────────────────────────────
mrp_gross_req      = []
mrp_scheduled_rec  = []
mrp_projected_bal  = []
mrp_net_req        = []
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

# ── Build Cost Breakdown Table ────────────────────────────────────────────────
cost_breakdown = []
for k in range(periods):
    lot   = mrp_planned_receipts[k]
    pab   = mrp_projected_bal[k]
    sc    = setup_cost if lot > 0 else 0
    hc    = holding_cost * max(0, pab - safety_stock)
    total = sc + hc
    cost_breakdown.append({
        "Periode":          periods_label[k],
        "GR":               mrp_gross_req[k],
        "Lot Size (PORec)": lot,
        "PAB Akhir":        pab,
        "Setup Cost (Rp)":  sc,
        "Holding Cost (Rp)": hc,
        "Total Cost (Rp)":  total,
    })

df_cost = pd.DataFrame(cost_breakdown)

# Totals
total_setup   = df_cost["Setup Cost (Rp)"].sum()
total_holding = df_cost["Holding Cost (Rp)"].sum()
grand_total   = df_cost["Total Cost (Rp)"].sum()
total_orders  = sum(1 for x in mrp_planned_receipts if x > 0)
total_units   = sum(mrp_planned_receipts)


# ─── METRIC CARDS ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#F0FDF4">📊</div>
    <div>
        <div class="section-title">Ringkasan Hasil</div>
        <div class="section-subtitle">Hasil optimasi MCP untuk seluruh periode perencanaan</div>
    </div>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

def fmt_rp(val):
    if val >= 1_000_000:
        return f"Rp {val/1_000_000:.1f}jt"
    elif val >= 1_000:
        return f"Rp {val/1_000:.0f}rb"
    return f"Rp {val:,.0f}"

with m1:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Grand Total Cost</div>
        <div class="metric-value">{fmt_rp(grand_total)}</div>
        <div class="metric-sub">Total biaya keseluruhan</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Total Setup Cost</div>
        <div class="metric-value">{fmt_rp(total_setup)}</div>
        <div class="metric-sub">{total_orders} kali order dilakukan</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-card amber">
        <div class="metric-label">Total Holding Cost</div>
        <div class="metric-value">{fmt_rp(total_holding)}</div>
        <div class="metric-sub">Dari {total_units:,} unit total dipesan</div>
    </div>""", unsafe_allow_html=True)
with m4:
    ratio = (total_holding / grand_total * 100) if grand_total > 0 else 0
    st.markdown(f"""
    <div class="metric-card red">
        <div class="metric-label">Proporsi Holding</div>
        <div class="metric-value">{ratio:.1f}%</div>
        <div class="metric-sub">dari total biaya</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── ITERASI & OPTIMAL ────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#FFF7ED">🔍</div>
    <div>
        <div class="section-title">Proses Iterasi MCP</div>
        <div class="section-subtitle">Semua kombinasi yang diuji dan hasil terbaik tiap langkah</div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2], gap="large")
with col1:
    st.markdown("**Semua Iterasi yang Diuji**")
    df_iter = pd.DataFrame(all_iterations)
    st.dataframe(
        df_iter.style
            .format({"Total Cost (Rp)": "{:,.0f}", "Cost/Period (Rp)": "{:,.1f}", "Net Requirement": "{:,}", "Lot Size": "{:,}"})
            .set_properties(**{"font-size": "12px"}),
        use_container_width=True, height=340
    )
with col2:
    st.markdown("**Kombinasi Optimal per Langkah**")
    df_opt = pd.DataFrame(optimal_combinations)
    st.dataframe(
        df_opt.style
            .format({"Total Cost (Rp)": "{:,.0f}", "Cost/Period (Rp)": "{:,.1f}", "Lot Size": "{:,}"})
            .set_properties(**{"font-size": "12px"})
            .map(lambda _: "background-color:#F0FDF4; color:#065F46; font-weight:600",
                      subset=["Cost/Period (Rp)"]),
        use_container_width=True, height=340
    )

st.markdown("<hr>", unsafe_allow_html=True)


# ─── FINAL MRP SHEET ──────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#F0F9FF">📋</div>
    <div>
        <div class="section-title">Final MRP Sheet</div>
        <div class="section-subtitle">Tabel perencanaan material lengkap hasil optimasi MCP</div>
    </div>
</div>
""", unsafe_allow_html=True)

mrp_matrix = {"Data / Periode": [
    "Gross Requirements (GR)",
    "Scheduled Receipts (SR)",
    "Projected Available Balance (PAB)",
    "Net Requirements (NR)",
    "Planned Order Receipts (PORec)",
    "Planned Order Releases (PORel)"
]}
for k in range(periods):
    lbl = df_input['Period'].iloc[k] if 'Period' in df_input.columns else f"P{k+1}"
    mrp_matrix[lbl] = [
        mrp_gross_req[k], mrp_scheduled_rec[k], mrp_projected_bal[k],
        mrp_net_req[k],   mrp_planned_receipts[k], mrp_planned_releases[k]
    ]

df_mrp = pd.DataFrame(mrp_matrix).set_index("Data / Periode")

def style_mrp(df):
    styles = pd.DataFrame("", index=df.index, columns=df.columns)
    row_colors = {
        "Gross Requirements (GR)":          "background:#F8FAFC; font-weight:600",
        "Scheduled Receipts (SR)":           "background:#F8FAFC",
        "Projected Available Balance (PAB)": "background:#EFF6FF; color:#1D4ED8",
        "Net Requirements (NR)":             "background:#FFFBEB; color:#92400E; font-weight:600",
        "Planned Order Receipts (PORec)":    "background:#F0FDF4; color:#065F46; font-weight:600",
        "Planned Order Releases (PORel)":    "background:#FFF7ED; color:#9A3412; font-weight:600",
    }
    for row, style in row_colors.items():
        if row in df.index:
            styles.loc[row] = style
    return styles

st.dataframe(
    df_mrp.style
        .apply(style_mrp, axis=None)
        .format("{:,.0f}"),
    use_container_width=True, height=260
)

st.markdown("<hr>", unsafe_allow_html=True)


# ─── COST BREAKDOWN TABLE (BARU) ──────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#FEF3C7">💰</div>
    <div>
        <div class="section-title">Rincian Biaya per Periode</div>
        <div class="section-subtitle">Setup cost + Holding cost + Total cost tiap periode</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tambah baris total
df_cost_display = df_cost.copy()
total_row = {
    "Periode": "TOTAL",
    "GR": sum(mrp_gross_req),
    "Lot Size (PORec)": total_units,
    "PAB Akhir": "-",
    "Setup Cost (Rp)": total_setup,
    "Holding Cost (Rp)": total_holding,
    "Total Cost (Rp)": grand_total,
}
df_cost_display = pd.concat([df_cost_display, pd.DataFrame([total_row])], ignore_index=True)

def style_cost(df):
    styles = pd.DataFrame("", index=df.index, columns=df.columns)
    last = len(df) - 1
    styles.iloc[last] = "background:#0F172A; color:#F1F5F9; font-weight:700"
    for i in range(len(df)-1):
        if df.iloc[i]["Setup Cost (Rp)"] > 0:
            styles.iloc[i, df.columns.get_loc("Setup Cost (Rp)")] = "background:#EFF6FF; color:#1D4ED8; font-weight:600"
        if df.iloc[i]["Holding Cost (Rp)"] > 0:
            styles.iloc[i, df.columns.get_loc("Holding Cost (Rp)")] = "background:#FFFBEB; color:#92400E"
        styles.iloc[i, df.columns.get_loc("Total Cost (Rp)")] = "font-weight:600"
    return styles

fmt_cost = {
    "GR": "{:,.0f}", "Lot Size (PORec)": "{:,.0f}",
    "Setup Cost (Rp)": "{:,.0f}", "Holding Cost (Rp)": "{:,.0f}", "Total Cost (Rp)": "{:,.0f}"
}

st.dataframe(
    df_cost_display.style.apply(style_cost, axis=None).format(fmt_cost, na_rep="-"),
    use_container_width=True, height=460
)

st.markdown(f"""
<div class="success-box">
    ✅ <strong>Ringkasan Biaya:</strong>
    Total Setup Cost = <strong>Rp {total_setup:,.0f}</strong> ({total_orders} order) &nbsp;|&nbsp;
    Total Holding Cost = <strong>Rp {total_holding:,.0f}</strong> &nbsp;|&nbsp;
    <strong>Grand Total = Rp {grand_total:,.0f}</strong>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ─── CHARTS ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#F5F3FF">📈</div>
    <div>
        <div class="section-title">Visualisasi</div>
        <div class="section-subtitle">Grafik analisis demand, lot sizing, dan biaya</div>
    </div>
</div>
""", unsafe_allow_html=True)

chart_labels = [df_input['Period'].iloc[k] if 'Period' in df_input.columns else f"P{k+1}" for k in range(periods)]

c1, c2 = st.columns(2, gap="large")

with c1:
    fig1 = go.Figure()
    fig1.add_bar(x=chart_labels, y=mrp_gross_req, name="GR", marker_color="#0EA5E9", opacity=0.85)
    fig1.add_bar(x=chart_labels, y=mrp_planned_receipts, name="Lot Size (PORec)", marker_color="#10B981", opacity=0.85)
    fig1.update_layout(
        title=dict(text="GR vs Lot Size per Periode", font=dict(size=14, family="DM Sans")),
        barmode="group", height=320,
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(gridcolor="#F1F5F9"), yaxis=dict(gridcolor="#F1F5F9"),
        font=dict(family="DM Sans", size=11)
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = go.Figure()
    sc_vals = df_cost["Setup Cost (Rp)"].tolist()
    hc_vals = df_cost["Holding Cost (Rp)"].tolist()
    fig2.add_bar(x=chart_labels, y=sc_vals, name="Setup Cost", marker_color="#3B82F6", opacity=0.85)
    fig2.add_bar(x=chart_labels, y=hc_vals, name="Holding Cost", marker_color="#F59E0B", opacity=0.85)
    fig2.update_layout(
        title=dict(text="Setup vs Holding Cost per Periode", font=dict(size=14, family="DM Sans")),
        barmode="stack", height=320,
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(gridcolor="#F1F5F9"), yaxis=dict(gridcolor="#F1F5F9"),
        font=dict(family="DM Sans", size=11)
    )
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2, gap="large")

with c3:
    fig3 = go.Figure()
    fig3.add_scatter(
        x=chart_labels, y=mrp_projected_bal,
        mode="lines+markers",
        line=dict(color="#8B5CF6", width=2.5),
        marker=dict(size=7, color="#8B5CF6"),
        fill="tozeroy", fillcolor="rgba(139,92,246,0.08)",
        name="PAB"
    )
    fig3.add_hline(y=safety_stock, line_dash="dash", line_color="#EF4444", line_width=1.5,
                   annotation_text=f"Safety Stock ({safety_stock:,})", annotation_position="top left")
    fig3.update_layout(
        title=dict(text="Projected Available Balance (PAB)", font=dict(size=14, family="DM Sans")),
        height=280, plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(gridcolor="#F1F5F9"), yaxis=dict(gridcolor="#F1F5F9"),
        font=dict(family="DM Sans", size=11)
    )
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    if total_setup + total_holding > 0:
        fig4 = go.Figure(go.Pie(
            labels=["Setup Cost", "Holding Cost"],
            values=[total_setup, total_holding],
            hole=0.55,
            marker=dict(colors=["#3B82F6", "#F59E0B"]),
            textinfo="label+percent",
            textfont=dict(family="DM Sans", size=12),
        ))
        fig4.update_layout(
            title=dict(text="Komposisi Biaya Total", font=dict(size=14, family="DM Sans")),
            height=280, paper_bgcolor="white",
            margin=dict(l=10, r=10, t=50, b=10),
            font=dict(family="DM Sans"),
            annotations=[dict(
                text=f"Rp{grand_total/1000:.0f}rb" if grand_total < 1_000_000 else f"Rp{grand_total/1_000_000:.1f}jt",
                x=0.5, y=0.5, font_size=13, showarrow=False, font=dict(family="DM Sans", color="#0F172A")
            )]
        )
        st.plotly_chart(fig4, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ─── DOWNLOAD ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon" style="background:#F0FDF4">📥</div>
    <div>
        <div class="section-title">Download Laporan</div>
        <div class="section-subtitle">Export semua hasil analisis dalam satu file CSV</div>
    </div>
</div>
""", unsafe_allow_html=True)

csv_buffer = BytesIO()
with pd.ExcelWriter(csv_buffer, engine='xlsxwriter') if False else BytesIO() as buf:
    pass

# Build combined CSV
df_mrp_reset = df_mrp.reset_index()
df_cost_dl   = df_cost_display.copy()

csv_out = BytesIO()
with pd.ExcelWriter(csv_out, engine='openpyxl') as writer:
    df_mrp_reset.to_excel(writer, sheet_name="Final MRP Sheet", index=False)
    df_cost_dl.to_excel(writer, sheet_name="Rincian Biaya", index=False)
    pd.DataFrame(optimal_combinations).to_excel(writer, sheet_name="Optimal Combinations", index=False)
    pd.DataFrame(all_iterations).to_excel(writer, sheet_name="All Iterations", index=False)

col_dl1, col_dl2, col_dl3 = st.columns([2,2,4])
with col_dl1:
    st.download_button(
        label="📥 Download Excel Lengkap",
        data=csv_out.getvalue(),
        file_name="mcp_report_lengkap.xlsx",
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
<div style='margin-top:32px; text-align:center; font-size:11px; color:#CBD5E1'>
    MRP · MCP Optimizer — Material Requirements Planning Dashboard
</div>
""", unsafe_allow_html=True)
