import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import io

st.set_page_config(
    page_title="Production Scheduling · SPT Optimizer",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── INISIALISASI SESSION STATE ───
if "df_input" not in st.session_state:
    st.session_state.df_input = None

# ─── REAL-TIME CLOCK TRIGGER ───
current_time_now = datetime.now()
current_hour = current_time_now.hour

if 4 <= current_hour < 11:
    sapaan = "Selamat Pagi"
elif 11 <= current_hour < 15:
    sapaan = "Selamat Siang"
elif 15 <= current_hour < 18:
    sapaan = "Selamat Sore"
else:
    sapaan = "Selamat Malam"

user_name = "Aura Mutia Azzahra"
try:
    if hasattr(st, "context") and hasattr(st.context, "user") and st.context.user.name:
        user_name = st.context.user.name
    elif hasattr(st, "experimental_user") and st.experimental_user.get("name"):
        user_name = st.experimental_user["name"]
except Exception:
    pass

# Link URL Mentah Unsplash Pilihanmu untuk Full Background Sidebar
unsplash_sidebar_bg = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=500&q=80"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
}}
.stApp {{
    background: #FFF8FA;
}}

/* ─── LATAR BELAKANG FULL SIDEBAR ─── */
[data-testid="stSidebar"] {{
    background-image: url("{unsplash_sidebar_bg}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    border-right: 1px solid #FFB3C6 !important;
}}

/* Efek Glassmorphism Kontainer Menu Utama agar Tulisan Terbaca Jelas */
.sidebar-brand-box {{
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
    border: 1px solid rgba(255, 179, 198, 0.5);
    box-shadow: 0 4px 15px rgba(92, 26, 48, 0.05);
    text-align: center;
}}
.sidebar-title {{
    font-size: 20px;
    font-weight: 700;
    color: #5C1A30;
    margin: 0;
}}
.sidebar-subtitle {{
    font-size: 11px;
    color: #8A3A50;
    margin-top: 4px;
    letter-spacing: 0.3px;
}}

/* Styling Navigasi Radio Button Kontainer */
[data-testid="stSidebar"] .stRadio {{
    background: rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    padding: 12px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.5);
}}

/* Sembunyikan Label Judul Radio Bawaan Streamlit */
[data-testid="stSidebar"] .stRadio > label {{ 
    display: none !important; 
}}

/* Desain Elemen Baris Opsi Menu */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {{
    background: rgba(255, 255, 255, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin-bottom: 6px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    display: flex !important;
    align-items: center !important;
}}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {{
    background: rgba(255, 255, 255, 0.7) !important;
    border-color: #FFB3C6 !important;
    transform: translateY(-1px);
}}

/* Ketika Menu Sedang Aktif/Diklik */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] {{
    background: #FFFFFF !important;
    border: 1px solid #FF8FAB !important;
    box-shadow: 0 4px 12px rgba(255, 143, 171, 0.25) !important;
}}

/* Warna Teks Menu */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label p {{
    color: #5C1A30 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    margin: 0 !important;
}}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] p {{
    font-weight: 700 !important;
    color: #5C1A30 !important;
}}

/* Sembunyikan Bulatan Radio Asli */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] input[type="radio"] {{ display: none !important; }}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {{ display: none !important; }}

/* ─── HERO BANNER ─── */
.hero-banner {{
    background: linear-gradient(135deg, #FFE5EC 0%, #FFC2D1 60%, #FFB3C6 100%);
    border-radius: 18px;
    padding: 34px 38px;
    margin-bottom: 22px;
    border: 1px solid #FFB3C6;
    position: relative;
    overflow: hidden;
}}
.hero-title {{
    font-size: 26px;
    font-weight: 700;
    color: #5C1A30;
    margin: 0 0 7px;
}}
.hero-sub {{
    font-size: 13.5px;
    color: #8A3A50;
    margin: 0;
}}

/* ─── DASHBOARD CARDS ─── */
.dashboard-box {{
    background: #FFFFFF;
    border: 1px solid #FFD6E4;
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 16px;
    position: relative;
}}
.box-title {{
    font-size: 15px;
    font-weight: 600;
    color: #5C1A30;
    margin-bottom: 10px;
}}
.box-text {{
    font-size: 13.5px;
    color: #6D404E;
    line-height: 1.78;
}}

/* ─── METRIC CARDS ─── */
.metric-card {{
    background: white;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid #FFD6E4;
    text-align: center;
}}
.metric-card.pastel-blue  {{ border-top: 4px solid #BFFCC6; }}
.metric-card.pastel-pink  {{ border-top: 4px solid #FF8FAB; }}
.metric-card.pastel-green {{ border-top: 4px solid #FFC6FF; }}
.metric-label {{ font-size: 11px; font-weight: 600; color: #9A6070; text-transform: uppercase; }}
.metric-value {{ font-size: 22px; font-weight: 600; color: #5C1A30; font-family: 'DM Mono', monospace; }}

.section-header {{ display: flex; align-items: center; gap: 10px; margin: 24px 0 14px; }}
.section-title  {{ font-size: 18px; font-weight: 700; color: #5C1A30; }}
.info-box {{ background: #FFF3F6; border-left: 4px solid #FFB3C6; border-radius: 0 10px 10px 0; padding: 13px 16px; margin-bottom: 20px; font-size: 13px; color: #6D404E; }}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    # Header box transparan estetik di atas background gambar
    st.markdown("""
    <div class="sidebar-brand-box">
        <div class="sidebar-title">⏱️ SPT Dashboard</div>
        <div class="sidebar-subtitle">Shortest Processing Time Optimizer</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigasi Menu Utama menggunakan emoji (menghindari bug kebocoran kode SVG)
    menu_pilihan = st.radio(
        "Navigasi Halaman:",
        [
            "🏠 Dashboard",
            "📝 Input Data Job",
            "📊 Hasil Penjadwalan SPT",
            "📈 Hasil Gantt Chart",
            "📥 Download Hasil"
        ],
        index=0
    )

# ─── ENGINE KALKULASI ─────────────────────────────────────────────────────────
df_spt = None
fig_gantt = None
if st.session_state.df_input is not None and len(st.session_state.df_input) > 0:
    df_calc = st.session_state.df_input.copy()
    df_calc["Processing_Time"] = df_calc["Processing_Time"].astype(int)
    df_calc["Due_Date"] = df_calc["Due_Date"].astype(int)
    df_spt = df_calc.sort_values(by="Processing_Time", ascending=True).reset_index(drop=True)
    start_times, comp_times, current_time = [], [], 0
    for idx, row in df_spt.iterrows():
        start_times.append(current_time)
        current_time += row["Processing_Time"]
        comp_times.append(current_time)
    df_spt["Start_Time"] = start_times
    df_spt["Completion_Time"] = comp_times
    df_spt["Lateness"] = df_spt["Completion_Time"] - df_spt["Due_Date"]

    pastel_colors = ['#FFB3C6', '#FFDAC1', '#C9F0CB', '#BFFCC6', '#AEC6CF', '#C3B1CE', '#FFC6FF', '#E8D6F5']
    fig_gantt = go.Figure()
    for idx, row in df_spt.iterrows():
        color_idx = idx % len(pastel_colors)
        fig_gantt.add_trace(go.Bar(
            x=[int(row["Processing_Time"])], y=["Mesin"], base=[int(row["Start_Time"])],
            orientation='h', name=str(row["Job_Name"]), text=str(row["Job_Name"]),
            textposition='inside',
            marker=dict(color=pastel_colors[color_idx], line=dict(color='#5C1A30', width=1)),
            hovertemplate=f"<b>Job:</b> {row['Job_Name']}<br><b>Waktu:</b> {row['Processing_Time']}<br><b>Mulai:</b> {row['Start_Time']}<br><b>Selesai:</b> {row['Completion_Time']}<extra></extra>"
        ))
    tick_vals = [0] + list(map(int, df_spt["Completion_Time"].values))
    fig_gantt.update_layout(
        barmode='stack', height=200, plot_bgcolor="white", showlegend=False,
        margin=dict(l=10, r=10, t=20, b=20),
        xaxis=dict(tickmode='array', tickvals=tick_vals, gridcolor="#FFE5EC", side="bottom"),
        yaxis=dict(visible=False)
    )

# ─── HALAMAN 1: DASHBOARD ─────────────────────────────────────────────────────
if menu_pilihan == "🏠 Dashboard":
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">✨ {sapaan}, {user_name}!</div>
        <div class="hero-sub" style="margin-top:8px;">Selamat datang di sistem optimasi urutan pengerjaan tunggal (Single Machine Scheduling).</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="dashboard-box">
        <div class="box-title">⏱️ &nbsp;Apa itu Aturan Shortest Processing Time (SPT)?</div>
        <div class="box-text">
            <b>Shortest Processing Time (SPT)</b> adalah salah satu metode penjadwalan prioritas di mana pekerjaan yang memiliki
            <b>waktu proses paling pendek</b> akan dikerjakan terlebih dahulu. Secara analitis, aturan ini sangat efektif untuk
            meminimalkan waktu tunggu, mengurangi penumpukan antrean (Work-In-Process), serta menekan nilai
            <i>Mean Lateness</i> hingga titik paling rendah.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── HALAMAN 2: INPUT DATA JOB ────────────────────────────────────────────────
elif menu_pilihan == "📝 Input Data Job":
    st.markdown(f"""<div class="section-header"><div class="section-title">📝 Input Data Job (Pekerjaan)</div></div>""", unsafe_allow_html=True)

    input_method = st.radio(
        "Pilih Metode Memasukkan Data:",
        ("Manual Input (Ketik di Tabel)", "Otomatis (Upload File CSV)"),
        horizontal=True
    )

    if input_method == "Manual Input (Ketik di Tabel)":
        st.markdown("""
        <div class="info-box">
            💡 <b>Petunjuk:</b> Isikan daftar pekerjaan langsung pada komponen tabel di bawah ini.
            Data yang Anda ketik akan otomatis direkam ke dalam sistem secara real-time.
        </div>
        """, unsafe_allow_html=True)

        init_data = st.session_state.df_input if st.session_state.df_input is not None else pd.DataFrame(columns=["Job_Name", "Processing_Time", "Due_Date"])
        edited_df = st.data_editor(
            init_data, num_rows="dynamic", use_container_width=True,
            column_config={
                "Job_Name": st.column_config.TextColumn("Job", required=True),
                "Processing_Time": st.column_config.NumberColumn("Waktu Proses", min_value=1, step=1, format="%d"),
                "Due_Date": st.column_config.NumberColumn("Due Date", min_value=1, step=1, format="%d")
            }
        )
        if edited_df is not None and len(edited_df) > 0:
            st.session_state.df_input = edited_df.dropna(subset=["Job_Name", "Processing_Time", "Due_Date"]).copy()

    else:
        uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                df_csv = pd.read_csv(uploaded_file)
                col_mapping = {}
                for col in df_csv.columns:
                    c_clean = col.strip().lower()
                    if c_clean == 'job': col_mapping[col] = 'Job_Name'
                    elif 'waktu' in c_clean or 'processing' in c_clean: col_mapping[col] = 'Processing_Time'
                    elif 'due' in c_clean: col_mapping[col] = 'Due_Date'
                if len(col_mapping) >= 3:
                    df_csv = df_csv.rename(columns=col_mapping)
                    st.session_state.df_input = df_csv[['Job_Name', 'Processing_Time', 'Due_Date']].dropna().copy()
                    st.success("✅ File CSV berhasil diunggah!")
                    st.dataframe(st.session_state.df_input, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {e}")

# ─── HALAMAN 3: HASIL PENJADWALAN SPT ─────────────────────────────────────────
elif menu_pilihan == "📊 Hasil Penjadwalan SPT":
    st.markdown(f"""<div class="section-header"><div class="section-title">📊 Tabel Urutan Penyelesaian SPT</div></div>""", unsafe_allow_html=True)
    if df_spt is not None:
        df_display = df_spt.copy()
        df_display.columns = ["Job", "Waktu proses", "Due date (d)", "Start_Time", "Saat selesai (c)", "Lateness (c-d)"]
        df_display = df_display[["Job", "Waktu proses", "Due date (d)", "Saat selesai (c)", "Lateness (c-d)"]]
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        mean_lateness = df_spt["Lateness"].mean()
        max_lateness = df_spt["Lateness"].max()
        sequence_str = " → ".join([str(x) for x in df_spt["Job_Name"]])
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card pastel-blue"><div class="metric-label">Rata-rata Lateness</div><div class="metric-value">{mean_lateness:.3f}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card pastel-pink"><div class="metric-label">Maximum Lateness</div><div class="metric-value">{max_lateness}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card pastel-green"><div class="metric-label">Urutan Penjadwalan</div><div class="metric-value" style="font-size:14px;padding-top:4px;">{sequence_str}</div></div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Belum ada data pekerjaan. Silakan isi data di menu 'Input Data Job'.")

# ─── HALAMAN 4: GANTT CHART ────────────────────────────────────────────────────
elif menu_pilihan == "📈 Hasil Gantt Chart":
    st.markdown(f"""<div class="section-header"><div class="section-title">📈 Gantt Chart Urutan Pengerjaan Mesin</div></div>""", unsafe_allow_html=True)
    if df_spt is not None and fig_gantt is not None:
        st.plotly_chart(fig_gantt, use_container_width=True)
    else:
        st.warning("⚠️ Gantt chart belum dapat dibuat. Silakan isi data di menu 'Input Data Job'.")

# ─── HALAMAN 5: DOWNLOAD ──────────────────────────────────────────────────────
elif menu_pilihan == "📥 Download Hasil":
    st.markdown(f"""<div class="section-header"><div class="section-title">📥 Unduh Hasil Eksperimen</div></div>""", unsafe_allow_html=True)
    if df_spt is not None:
        csv_buffer = io.StringIO()
        df_spt.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📊 Download Tabel Analisis Penjadwalan (.CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"Tabel_Hasil_SPT_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning("⚠️ Tidak ada data kalkulasi yang tersedia.")
