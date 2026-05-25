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

# ─── Custom CSS (Pink Pastel, Cute, Soft UI) ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background (Very Light Pink/White) ── */
.stApp {
    background: #FFFDFE;
}

/* ── Sidebar (Soft Pink Pastel) ── */
[data-testid="stSidebar"] {
    background: #FFEDF1 !important; /* Pastel Pink */
    border-right: 1px solid #FFCCD5; /* Soft Border */
}

/* Sidebar Text & Titles */
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #8C5260 !important; /* Darker Soft Pink/Brown for readable text */
}

/* Sidebar Input Fields (White background in Pink Sidebar) */
[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
    background: #FFFFFF !important;
    color: #8C5260 !important;
    border: 1px solid #FFCCD5 !important;
    border-radius: 12px !important; /* Cute corner */
    font-family: 'DM Mono', monospace !important;
    font-size: 15px !important;
    box-shadow: inset 0 1px 2px rgba(255,182,193,0.2) !important;
}

/* Input Focus (Main Accent Color - Brighter Soft Pink) */
[data-testid="stSidebar"] [data-testid="stNumberInput"] input:focus {
    border-color: #FF8FAB !important;
    box-shadow: 0 0 0 2px rgba(255,143,171,0.15) !important;
}

/* Increment/Decrement Buttons */
[data-testid="stSidebar"] button[data-testid="stBaseButton-minimal"] {
    background: #FFFFFF !important;
    color: #FF8FAB !important;
    border: 1px solid #FFCCD5 !important;
    border-radius: 8px !important;
}

/* ── Main area padding ── */
.block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1400px;
}

/* ── Hero header (Cute Gradient) ── */
.hero-banner {
    background: linear-gradient(135deg, #FF99AC 0%, #FFB6C1 40%, #FFF5F7 100%);
    border-radius: 20px; /* Cuter corners */
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(255,182,193,0.3); /* Soft shadow */
}

/* Decorative Circles */
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,0.3);
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    border-radius: 50%;
    background: rgba(255,255,255,0.2);
}

.hero-title {
    font-size: 30px; /* Slightly bigger */
    font-weight: 600;
    color: #FFFFFF;
    margin: 0 0 6px;
    letter-spacing: -0.3px;
    text-shadow: 1px 1px 2px rgba(140,82,96,0.3); /* Text shadow for cute glow */
}
.hero-sub {
    font-size: 14px;
    color: #FFFFFF;
    margin: 0;
    font-weight: 400;
    opacity: 0.9;
}
.hero-badge {
    display: inline-block;
    background: #FFFFFF;
    color: #FF8FAB;
    border: 1px solid rgba(255,143,171,0.2);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 5px rgba(255,182,193,0.2);
}

/* ── Metric cards (Soft White Panels) ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}
.metric-card {
    background: white;
    border-radius: 16px; /* Cuter corners */
    padding: 20px;
    border: 1px solid #FFEDF1;
    box-shadow: 0 2px 10px rgba(255,182,193,0.1); /* Soft shadow */
    transition: transform 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(255,182,193,0.15);
}

.metric-label {
    font-size: 11px;
    font-weight: 600;
    color: #C0808F; /* Lighter soft pink/brown */
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 24px; /* Bigger value */
    font-weight: 700;
    color: #FF8FAB; /* Cute accent color for value */
    font-family: 'DM Mono', monospace;
    line-height: 1.2;
}
.metric-sub {
    font-size: 11px;
    color: #C0808F;
    margin-top: 4px;
}

/* Metric card specific borders (Pink variations) */
.metric-card.blue  { border-top: 4px solid #FF8FAB; } /* Cute Accent Pink */
.metric-card.green { border-top: 4px solid #FFC8DD; } /* Lighter Pink */
.metric-card.amber { border-top: 4px solid #FFAFCC; } /* Medium Pink */
.metric-card.red   { border-top: 4px solid #BDE0FE; } /* Soft Pastel Blue for contrast */

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 32px 0 16px;
}
.section-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 2px 5px rgba(255,182,193,0.1);
}
.section-title {
    font-size: 18px;
    font-weight: 600;
    color: #8C5260;
}
.section-subtitle {
    font-size: 12px;
    color: #C0808F;
    margin-top: 2px;
}

/* Icons background colors (Pinkish tints) */
.section-header .section-icon.upload { background:#FFF0F3; color: #FF8FAB; }
.section-header .section-icon.analysis { background:#FFF0F3; color: #FFC8DD; }
.section-header .section-icon.mrp { background:#FFF0F3; color: #FFAFCC; }
.section-header .section-icon.cost { background:#FFF0F3; color: #BDE0FE; }
.section-header .section-icon.charts { background:#FFF0F3; color: #FF99AC; }
.section-header .section-icon.download { background:#FFF0F3; color: #FF8FAB; }

/* ── Upload area (Cutest Upload) ── */
[data-testid="stFileUploader"] {
    background: white;
    border-radius: 16px;
    padding: 8px;
    border: 3px dashed #FFCCD5;
}
[data-testid="stFileUploader"]:hover {
    border-color: #FF8FAB;
    background: #FFF9FA;
}

/* ── Dataframe (Softened table) ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid #FFEDF1 !important;
    box-shadow: 0 1px 5px rgba(255,182,193,0.05);
}
.dvn-scroller {
    border-radius: 12px !important;
}

/* ── Download button (Cute accent colors) ── */
[data-testid="stDownloadButton"] button {
    background: #FF8FAB !important; /* Main accent cute pink */
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.2px !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(255,143,171,0.3) !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: #FF99AC !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255,143,171,0.4) !important;
}

/* Alternative download button */
[data-testid="stDownloadButton"]:nth-of-type(2) button {
    background: #FFFFFF !important;
    color: #FF8FAB !important;
    border: 2px solid #FF8FAB !important;
    box-shadow: 0 2px 8px rgba(255,143,171,0.15) !important;
}
[data-testid="stDownloadButton"]:nth-of-type(2) button:hover {
    background: #FFF9FA !important;
    box-shadow: 0 4px 12px rgba(255,143,171,0.2) !important;
}

/* ── Info/warning boxes (Softened Colors) ── */
.info-box, .warn-box, .success-box {
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 24px;
    font-size: 13px;
    border-left-width: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.03);
}

.info-box {
    background: #FFF9FA; /* Very light pink tint */
    border: 1px solid #FFEDF1;
    border-left-color: #FFCCD5;
    color: #8C5260;
}
.warn-box {
    background: #FFFBF0; /* Light cream/yellow tint */
    border: 1px solid #FFF1D1;
    border-left-color: #FED171;
    color: #92400E;
}
.success-box {
    background: #F0FDFA; /* Light teal tint for success */
    border: 1px solid #CCFBF1;
    border-left-color: #5EEAD4;
    color: #0F5132;
}

/* ── Cost table panel ── */
.cost-table-wrap {
    background: white;
    border-radius: 16px;
    border: 1px solid #FFEDF1;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(255,182,193,0.08);
}

/* ── Sidebar section label ── */
.sidebar-section {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #C0808F !important;
    padding: 20px 0 8px;
    border-top: 1px solid #FFCCD5;
    margin-top: 12px;
}

/* ── Step badge in optimal table (Pink badges) ── */
.step-pill {
    background: #FFF0F3;
    color: #FF8FAB;
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
}

/* ── Cute style overrides for the footer and center text ── */
.cute-footer {
    margin-top: 32px;
    text-align: center;
    font-size: 12px;
    color: #8C5260;
    opacity: 0.7;
    border-top: 1px solid #FFEDF1;
    padding-top: 20px;
}

/* ── Divider (Softened) ── */
hr { border-color: #FFEDF1 !important; margin: 32px 0 !important; }

/* ── Hide default streamlit elements ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 16px; text-align: center;'>
        <div style='font-size:26px; font-weight:700; color:#FF8FAB; letter-spacing:-0.5px; text-shadow: 1px 1px 1px rgba(140,82,96,0.1);'>MCP Optimizer</div>
        <div style='font-size:12px; color:#C0808F; margin-top:4px; font-weight: 400;'>Material Requirements Planning</div>
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

    # Pinkish themed info boxes in sidebar
    st.markdown("""
    <div style='margin-top:32px; padding:16px; background:#FFF9FA; border-radius:12px; border:1px solid #FFEDF1; box-shadow: inset 0 1px 3px rgba(255,182,193,0.1);'>
        <div style='font-size:11px; font-weight:600; color:#FF8FAB; letter-spacing:0.5px; margin-bottom:8px'>CARA PAKAI</div>
        <div style='font-size:11px; color:#8C5260; line-height:1.6'>
            1. Atur parameter di atas<br>
            2. Upload file CSV<br>
            3. Analisis hasil otomatis<br>
            4. Download laporan
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:12px; padding:12px 16px; background:#FFF9FA; border-radius:12px; border:1px solid #FFEDF1; box-shadow: inset 0 1px 3px rgba(255,182,193,0.1);'>
        <div style='font-size:10px; font-weight:600; color:#C0808F; letter-spacing:0.5px; margin-bottom:6px'>FORMAT CSV</div>
        <div style='font-family: "DM Mono", monospace; font-size:10px; color:#A0707F; line-height:1.8'>
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
    <div class="section-icon upload">📂</div>
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
        "GR":                mrp_gross_req[k],
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


# ─── METRIC CARDS (Pink Variations) ─────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon upload">📊</div>
    <div>
        <div class="section-title">Ringkasan Hasil</div>
        <div class="section-subtitle">Hasil optimasi MCP untuk seluruh periode perencanaan</div>
    </div>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

# Simple currency formatter (No division by 1000 for small numbers, for clarity)
def fmt_rp_simple(val):
    if val >= 1_000_000:
        return f"Rp {val/1_000_000:.1f}jt"
    elif val >= 1_000:
        return f"Rp {val/1_000:.1f}rb" # Show decimals for small rb
    return f"Rp {val:,.0f}"

with m1:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Grand Total Cost</div>
        <div class="metric-value">{fmt_rp_simple(grand_total)}</div>
        <div class="metric-sub">Total biaya keseluruhan</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Total Setup Cost</div>
        <div class="metric-value">{fmt_rp_simple(total_setup)}</div>
        <div class="metric-sub">{total_orders} kali order dilakukan</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-card amber">
        <div class="metric-label">Total Holding Cost</div>
        <div class="metric-value">{fmt_rp_simple(total_holding)}</div>
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
    <div class="section-icon upload">🔍</div>
    <div>
        <div class="section-title">Proses Iterasi MCP</div>
        <div class="section-subtitle">Semua kombinasi yang diuji dan hasil terbaik tiap langkah</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Pinkish accents in the tables (Subtle color mapping)
df_iter_styled = pd.DataFrame(all_iterations).style.format({
    "Total Cost (Rp)": "{:,.0f}",
    "Cost/Period (Rp)": "{:,.1f}",
    "Net Requirement": "{:,}",
    "Lot Size": "{:,}"
}).set_properties(**{"font-size": "12px"})

col1, col2 = st.columns([3, 2], gap="large")
with col1:
    st.markdown("**Semua Iterasi yang Diuji**")
    st.dataframe(df_iter_styled, use_container_width=True, height=340)

with col2:
    st.markdown("**Kombinasi Optimal per Langkah**")
    df_opt_styled = pd.DataFrame(optimal_combinations).style.format({
        "Total Cost (Rp)": "{:,.0f}",
        "Cost/Period (Rp)": "{:,.1f}",
        "Lot Size": "{:,}"
    }).set_properties(**{"font-size": "12px"}).map(
        # Pink highlight for the best cost
        lambda _: "background-color:#FFF0F3; color:#FF8FAB; font-weight:600",
        subset=["Cost/Period (Rp)"]
    )
    st.dataframe(df_opt_styled, use_container_width=True, height=340)

hr_styled = "<hr>"
st.markdown(hr_styled, unsafe_allow_html=True)


# ─── FINAL MRP SHEET ──────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon upload">📋</div>
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

# Pinkish and Soft contrasting colors for MRP table
def style_mrp_cute(df):
    styles = pd.DataFrame("", index=df.index, columns=df.columns)
    row_colors = {
        "Gross Requirements (GR)":          "background:#FFF9FA; font-weight:600", # Lighter pink
        "Scheduled Receipts (SR)":          "background:#FFF9FA",
        "Projected Available Balance (PAB)": "background:#FFF0F3; color:#FF8FAB", # Cute Pink accent
        "Net Requirements (NR)":             "background:#FFFBEB; color:#92400E; font-weight:600", # Orange contrasting
        "Planned Order Receipts (PORec)":    "background:#F0FDF4; color:#0F5132; font-weight:600", # Green contrasting
        "Planned Order Releases (PORel)":    "background:#FFF7ED; color:#9A3412; font-weight:600", # Reddish Contrasting
    }
    for row, style in row_colors.items():
        if row in df.index:
            styles.loc[row] = style
    return styles

st.dataframe(
    df_mrp.style
        .apply(style_mrp_cute, axis=None)
        .format("{:,.0f}"),
    use_container_width=True, height=260
)

st.markdown(hr_styled, unsafe_allow_html=True)


# ─── COST BREAKDOWN TABLE (Pink Variations) ──────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon upload">💰</div>
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

# Pink themed table style
def style_cost_cute(df):
    styles = pd.DataFrame("", index=df.index, columns=df.columns)
    last = len(df) - 1
    # Total row (Pink accent background)
    styles.iloc[last] = "background:#FF8FAB; color:#FFFFFF; font-weight:700" 
    
    for i in range(len(df)-1):
        if df.iloc[i]["Setup Cost (Rp)"] > 0:
            # Highlight Setup Cost column
            styles.iloc[i, df.columns.get_loc("Setup Cost (Rp)")] = "background:#FFF0F3; color:#FF8FAB; font-weight:600"
        if df.iloc[i]["Holding Cost (Rp)"] > 0:
            # Highlight Holding Cost column (contrasting orange)
            styles.iloc[i, df.columns.get_loc("Holding Cost (Rp)")] = "background:#FFFBEB; color:#92400E"
        # Total Cost column (bold)
        styles.iloc[i, df.columns.get_loc("Total Cost (Rp)")] = "font-weight:600"
    return styles

fmt_cost_display = {
    "GR": "{:,.0f}", "Lot Size (PORec)": "{:,.0f}",
    "Setup Cost (Rp)": "{:,.0f}", "Holding Cost (Rp)": "{:,.0f}", "Total Cost (Rp)": "{:,.0f}"
}

st.dataframe(
    df_cost_display.style.apply(style_cost_cute, axis=None).format(fmt_cost_display, na_rep="-"),
    use_container_width=True, height=460
)

# Cute summary box with pink text
st.markdown(f"""
<div style='background: #FFF9FA; border: 1px solid #FFEDF1; border-left: 5px solid #FF8FAB; border-radius: 12px; padding: 14px 18px; margin-top: 16px; font-size: 13px; color: #8C5260; box-shadow: 0 2px 5px rgba(255,182,193,0.05);'>
    ✅ <strong>Ringkasan Biaya:</strong>
    Total Setup Cost = <strong style='color:#FF8FAB'>Rp {total_setup:,.0f}</strong> ({total_orders} order) &nbsp;|&nbsp;
    Total Holding Cost = <strong style='color:#C0808F'>Rp {total_holding:,.0f}</strong> &nbsp;|&nbsp;
    <strong>Grand Total = <strong style='color:#FF8FAB'>Rp {grand_total:,.0f}</strong></strong>
</div>
""", unsafe_allow_html=True)

st.markdown(hr_styled, unsafe_allow_html=True)


# ─── CHARTS (Pinkish Themed Charts) ────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon upload">📈</div>
    <div>
        <div class="section-title">Visualisasi</div>
        <div class="section-subtitle">Grafik analisis demand, lot sizing, dan biaya</div>
    </div>
</div>
""", unsafe_allow_html=True)

chart_labels = [df_input['Period'].iloc[k] if 'Period' in df_input.columns else f"P{k+1}" for k in range(periods)]

# Cute Plotly Layout Base (White bg, DM Sans font, Soft colors)
plotly_layout_base = dict(
    plot_bgcolor="white", paper_bgcolor="white",
    xaxis=dict(gridcolor="#FFEDF1"), yaxis=dict(gridcolor="#FFEDF1"),
    font=dict(family="DM Sans", size=11, color="#8C5260"),
    margin=dict(l=10, r=10, t=50, b=10),
)

c1, c2 = st.columns(2, gap="large")

with c1:
    fig1 = go.Figure()
    # Contrasting colors (Pink Variations / Cute Contouring)
    fig1.add_bar(x=chart_labels, y=mrp_gross_req, name="GR", marker_color="#FF99AC", marker=dict(line=dict(color="#FF8FAB", width=1)), opacity=0.9)
    fig1.add_bar(x=chart_labels, y=mrp_planned_receipts, name="Lot Size (PORec)", marker_color="#BDE0FE", marker=dict(line=dict(color="#8CC7FE", width=1)), opacity=0.9)
    fig1.update_layout(
        title=dict(text="GR vs Lot Size per Periode", font=dict(size=14, family="DM Sans", color="#8C5260")),
        barmode="group", height=320,
        legend=dict(orientation="h", y=-0.2),
        **plotly_layout_base
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = go.Figure()
    sc_vals = df_cost["Setup Cost (Rp)"].tolist()
    hc_vals = df_cost["Holding Cost (Rp)"].tolist()
    # Stacked colors (Cute Contrast)
    fig2.add_bar(x=chart_labels, y=sc_vals, name="Setup Cost", marker_color="#FF8FAB", opacity=0.9)
    fig2.add_bar(x=chart_labels, y=hc_vals, name="Holding Cost", marker_color="#C0808F", opacity=0.9)
    fig2.update_layout(
        title=dict(text="Setup vs Holding Cost per Periode", font=dict(size=14, family="DM Sans", color="#8C5260")),
        barmode="stack", height=320,
        legend=dict(orientation="h", y=-0.2),
        **plotly_layout_base
    )
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2, gap="large")

with c3:
    fig3 = go.Figure()
    # Purple accented line chart for balance flow
    fig3.add_scatter(
        x=chart_labels, y=mrp_projected_bal,
        mode="lines+markers",
        line=dict(color="#FF8FAB", width=3), # Accent pink
        marker=dict(size=8, color="#FF8FAB", line=dict(color="white", width=2)), # Marker Contour white
        fill="tozeroy", fillcolor="rgba(255,143,171,0.08)", # Lighter pink fill
        name="PAB"
    )
    # Contrasting Safety stock line (soft red)
    fig3.add_hline(y=safety_stock, line_dash="dash", line_color="#FF99AC", line_width=1.5,
                   annotation_text=f"Safety Stock ({safety_stock:,})", annotation_position="top left", annotation_font=dict(color="#FF99AC"))
    fig3.update_layout(
        title=dict(text="Projected Available Balance (PAB)", font=dict(size=14, family="DM Sans", color="#8C5260")),
        height=320,
        **plotly_layout_base
    )
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    if total_setup + total_holding > 0:
        # Contrasting Pie colors
        fig4 = go.Figure(go.Pie(
            labels=["Setup Cost", "Holding Cost"],
            values=[total_setup, total_holding],
            hole=0.6,
            marker=dict(colors=["#FF8FAB", "#C0808F"]), # Main pink and darker soft brown contrast
            textinfo="label+percent",
            textfont=dict(family="DM Sans", size=12, color="white"), # White font for dark backgrounds
            direction="clockwise", # Cute movement
        ))
        # Value formatter inside Pie
        def fmt_grand_simple_chart(val):
             if val >= 1_000_000:
                 return f"Rp{val/1_000_000:.1f}jt"
             return f"Rp{val/1000:.1f}rb"

        fig4.update_layout(
            title=dict(text="Komposisi Biaya Total", font=dict(size=14, family="DM Sans", color="#8C5260")),
            height=320, paper_bgcolor="white",
            margin=dict(l=10, r=10, t=50, b=10),
            font=dict(family="DM Sans", color="#8C5260"),
            # Center annotation (Grand Total Value in Center)
            annotations=[dict(
                text=fmt_grand_simple_chart(grand_total),
                x=0.5, y=0.5, font_size=15, showarrow=False, font=dict(family="DM Sans", color="#FF8FAB", weight="bold")
            )]
        )
        st.plotly_chart(fig4, use_container_width=True)

st.markdown(hr_styled, unsafe_allow_html=True)


# ─── DOWNLOAD ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon upload">📥</div>
    <div>
        <div class="section-title">Download Laporan</div>
        <div class="section-subtitle">Export semua hasil analisis dalam satu file CSV</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Cute Excel/CSV builder with sheets
csv_buffer = BytesIO()

# Reset index for sheets compatibility
df_mrp_dl   = df_mrp.reset_index()
df_cost_dl_full = df_cost_display.copy()

csv_simple_all_reset = pd.concat([df_mrp_dl, pd.DataFrame(optimal_combinations), pd.DataFrame(all_iterations)], axis=1)

output_excel_buffer = BytesIO()
with pd.ExcelWriter(output_excel_buffer, engine='xlsxwriter') as writer:
    df_mrp_dl.to_excel(writer, sheet_name="Final MRP Sheet", index=False)
    df_cost_dl_full.to_excel(writer, sheet_name="Rincian Biaya", index=False)
    pd.DataFrame(optimal_combinations).to_excel(writer, sheet_name="Optimal Combinations", index=False)
    pd.DataFrame(all_iterations).to_excel(writer, sheet_name="All Iterations", index=False)

col_dl1, col_dl2, col_dl3 = st.columns([2,2,4])
with col_dl1:
    st.download_button(
        label="📥 Download Excel Lengkap",
        data=output_excel_buffer.getvalue(),
        file_name="mcp_report_lengkap.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
with col_dl2:
    csv_simple_data = BytesIO()
    df_mrp_dl.to_csv(csv_simple_data, index=False)
    st.download_button(
        label="📄 Download MRP Sheet (CSV)",
        data=csv_simple_data.getvalue(),
        file_name="final_mrp_sheet.csv",
        mime="text/csv"
    )

# Softened footer text
st.markdown("""
<div class="cute-footer">
    MRP · MCP Optimizer — Material Requirements Planning Dashboard
</div>
""", unsafe_allow_html=True)
