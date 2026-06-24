import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import io
import pytz

st.set_page_config(
    page_title="Production Scheduling · SPT Optimizer",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "df_input" not in st.session_state:
    st.session_state.df_input = None

wib = pytz.timezone("Asia/Jakarta")
current_hour = datetime.now(wib).hour
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ─── DASHBOARD BACKGROUND (DARK PURPLE LIKE MCP OPTIMIZER) ─── */
.stApp {
    background: #2D1A29; /* Warna ungu gelap pekat */
    color: #F3EAF0;
}

/* Mengubah warna teks judul standar Streamlit agar kontras di latar gelap */
h1, h2, h3, h4, h5, h6, p, span, label {
    color: #F3EAF0 !important;
}

/* ─── SIDEBAR (DARKER PINK WITH ANIMATED BUBBLES) ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #A84460 0%, #611C31 100%) !important; /* Pink lebih gelap / Maroon Mauve */
    border-right: 1px solid #A84460 !important;
    padding-top: 0 !important;
    position: relative;
    overflow: hidden !important;
}

/* Inject Gelembung Animasi via CSS */
[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0; left: 0;
    background: 
        radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 4px, transparent 4px),
        radial-gradient(circle at 75% 40%, rgba(255, 255, 255, 0.08) 8px, transparent 8px),
        radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.12) 6px, transparent 6px),
        radial-gradient(circle at 80% 85%, rgba(255, 255, 255, 0.06) 12px, transparent 12px),
        radial-gradient(circle at 15% 30%, rgba(255, 255, 255, 0.07) 10px, transparent 10px);
    background-size: 100% 100%;
    animation: floatBubbles 12s linear infinite;
    pointer-events: none;
}

@keyframes floatBubbles {
    0% { background-position: 0px 0px; }
    100% { background-position: 0px -200px; }
}

[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio fieldset { border: none !important; padding: 0 !important; margin: 0 !important; }

/* Item Menu Navigasi di Sidebar */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 11px 14px !important;
    margin-bottom: 5px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background: rgba(255, 255, 255, 0.15) !important;
}

/* Menu Aktif saat Diklik */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] {
    background: rgba(255, 255, 255, 0.25) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label p,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label span {
    color: #FFE5EC !important; /* Teks menu warna pink terang cerah */
    font-size: 13.5px !important;
    font-weight: 400 !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] p,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] span {
    font-weight: 700 !important;
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label input[type="radio"] { display: none !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child { display: none !important; }

/* ─── HERO BANNER (MATCHED TO DARK COMPLEXION) ─── */
.hero-banner {
    background: linear-gradient(135deg, #4A2840 0%, #3D1E33 100%);
    border-radius: 18px;
    padding: 34px 38px;
    margin-bottom: 22px;
    border: 1px solid #5C3250;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 160px; height: 160px;
    background: rgba(255, 143, 171, 0.08);
    border-radius: 50%;
}
.hero-title {
    font-size: 26px;
    font-weight: 700;
    color: #FFB3C6 !important;
    margin: 0 0 7px;
    line-height: 1.3;
    position: relative;
}
.hero-sub {
    font-size: 13.5px;
    color: #CDB3C5 !important;
    margin: 0;
    font-weight: 400;
    position: relative;
}

/* ─── DASHBOARD CARDS ─── */
.dashboard-box {
    background: #362031;
    border: 1px solid #4D3147;
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.dashboard-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #A84460, #FF8FAB);
    border-radius: 16px 16px 0 0;
}
.box-title {
    font-size: 15px;
    font-weight: 600;
    color: #FFB3C6 !important;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.box-text {
    font-size: 13.5px;
    color: #E2D1DE !important;
    line-height: 1.78;
}

/* ─── METRIC CARDS ─── */
.metric-card {
    background: #362031;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid #4D3147;
    text-align: center;
}
.metric-card.pastel-blue  { border-top: 4px solid #BFFCC6; }
.metric-card.pastel-pink  { border-top: 4px solid #FF8FAB; }
.metric-card.pastel-green { border-top: 4px solid #FFC6FF; }
.metric-label { font-size: 11px; font-weight: 600; color: #CDB3C5 !important; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.metric-value { font-size: 22px; font-weight: 600; color: #FFF8FA !important; font-family: 'DM Mono', monospace; }

/* ─── SECTION & UTILS ─── */
.section-header { display: flex; align-items: center; gap: 10px; margin: 24px 0 14px; }
.section-title  { font-size: 18px; font-weight: 700; color: #FFB3C6 !important; }
.info-box { background: #3D2237; border-left: 4px solid #A84460; border-radius: 0 10px 10px 0; padding: 13px 16px; margin-bottom: 20px; font-size: 13px; color: #E2D1DE !important; }
hr { border-color: #4D3147 !important; }
</style>
""", unsafe_allow_html=True)

# SVG icon strings (outline style)
ICONS = {
    "home": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z"/><path d="M9 21V12h6v9"/></svg>""",
    "edit": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>""",
    "table": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/></svg>""",
    "chart": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 16V10M12 16V8M17 16v-4"/></svg>""",
    "download": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v13M7 11l5 5 5-5"/><path d="M5 20h14"/></svg>""",
    "clock": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>""",
    "tool": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>""",
    "star": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>""",
}

def icon(name, color="#FFB3C6", size=16):
    svg = ICONS.get(name, "")
    return f'<span style="display:inline-flex;align-items:center;width:{size}px;height:{size}px;color:{color};flex-shrink:0">{svg}</span>'

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding: 22px 16px 16px 16px; position: relative; z-index: 2;'>
        <div style='display:flex; align-items:center; gap:10px; margin-bottom:4px;'>
            <span style='display:inline-flex;align-items:center;width:28px;height:28px;color:#FFFFFF;background:rgba(255,255,255,0.2);border-radius:8px;padding:5px;box-sizing:border-box;'>{ICONS["clock"]}</span>
            <span style='font-size: 18px; font-weight: 700; color: #FFFFFF;'>Base Ind. Eng.</span>
        </div>
        <div style='font-size: 11px; color: #FFCCD7; margin-top: 2px; margin-left: 38px; letter-spacing: 0.3px;'>
            Shortest Processing Time Optimizer
        </div>
    </div>
    <div style='height:1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent); margin: 0 12px 14px; position: relative; z-index: 2;'></div>
    """, unsafe_allow_html=True)

    menu_pilihan = st.radio(
        "Navigasi Halaman:",
        [
            "🏠  Dashboard",
            "📝  Input Data Job",
            "📋  Hasil Penjadwalan SPT",
            "📊  Hasil Gantt Chart",
            "📥  Download Hasil"
        ],
        index=0
    )

# ─── ENGINE KALKULASI ─────────────────────────────────────────────────────────
df_spt = None
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

# ─── HALAMAN 1: DASHBOARD ─────────────────────────────────────────────────────
if menu_pilihan == "🏠  Dashboard":
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">{icon("star", "#FFB3C6", 22)} &nbsp;{sapaan}, {user_name}!</div>
        <div class="hero-sub" style="margin-top:8px;">Selamat datang di sistem optimasi urutan pengerjaan tunggal (Single Machine Scheduling).</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="dashboard-box">
        <div class="box-title">{icon("clock", "#FF8FAB", 17)} &nbsp;Apa itu Aturan Shortest Processing Time (SPT)?</div>
        <div class="box-text">
            <b>Shortest Processing Time (SPT)</b> adalah salah satu metode penjadwalan prioritas di mana pekerjaan yang memiliki
            <b>waktu proses paling pendek</b> akan dikerjakan terlebih dahulu. Secara analitis, aturan ini sangat efektif untuk
            meminimalkan waktu tunggu, mengurangi penumpukan antrean (Work-In-Process), serta menekan nilai
            <i>Mean Lateness</i> hingga titik paling rendah.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="dashboard-box">
        <div class="box-title">{icon("tool", "#FF8FAB", 17)} &nbsp;Langkah Penggunaan Aplikasi Web</div>
        <div class="box-text">
            1. Buka menu samping, lalu pilih <b>"Input Data Job"</b>. Di sana Anda bisa memasukkan data secara Manual via Tabel atau Upload CSV.<br><br>
            2. Sistem secara otomatis akan memproses urutan penjadwalan di latar belakang tanpa perlu menekan tombol hitung.<br><br>
            3. Klik menu <b>"Hasil Penjadwalan SPT"</b> untuk melihat hasil analisis tabel perhitungan performa keterlambatan.<br><br>
            4. Klik menu <b>"Hasil Gantt Chart"</b> untuk melihat urutan lini masa pengerjaan mesin secara horizontal.<br><br>
            5. Gunakan menu <b>"Download Hasil"</b> untuk mengunduh seluruh ringkasan tabel data penjadwalan ke berkas CSV.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── HALAMAN 2: INPUT DATA JOB ────────────────────────────────────────────────
elif menu_pilihan == "📝  Input Data Job":
    st.markdown(f"""<div class="section-header">{icon("edit","#FF8FAB",20)}<div class="section-title">Input Data Job (Pekerjaan)</div></div>""", unsafe_allow_html=True)

    input_method = st.radio(
        "Pilih Metode Memasukkan Data:",
        ("Manual Input (Ketik di Tabel)", "Otomatis (Upload File CSV)"),
        horizontal=True
    )

    if input_method == "Manual Input (Ketik di Tabel)":
        st.markdown("""
        <div class="info-box">
            💡 <b>Petunjuk:</b> Isikan daftar pekerjaan langsung pada komponen tabel di bawah ini.
            Data yang Anda ketik akan otomatis direkam ke dalam sistem secara real-time untuk halaman visualisasi hasil.
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
            st.toast("Data tabel manual diperbarui!", icon="✏️")
    else:
        st.markdown("""
        <div class="info-box">
            📂 <b>Format Kolom CSV:</b> Pastikan file CSV Anda memiliki nama kolom header yang sesuai:
            <code style="background-color: #4A2840; padding: 2px 6px; border-radius: 4px; color: #FFB3C6; font-weight: bold;">Job | Waktu Proses | Due date</code>
        </div>
        """, unsafe_allow_html=True)
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
                else:
                    st.error("❌ Gagal memetakan kolom. Pastikan file CSV memiliki kolom: 'Job', 'Waktu Proses', dan 'Due date'.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat membaca file: {e}")

# ─── HALAMAN 3: HASIL PENJADWALAN SPT ─────────────────────────────────────────
elif menu_pilihan == "📋  Hasil Penjadwalan SPT":
    st.markdown(f"""<div class="section-header">{icon("table","#FF8FAB",20)}<div class="section-title">Tabel Urutan Penyelesaian SPT</div></div>""", unsafe_allow_html=True)
    if df_spt is not None:
        df_display = df_spt.copy()
        df_display.columns = ["Job", "Waktu proses", "Due date (d)", "Start_Time", "Saat selesai (c)", "Lateness (c-d)"]
        df_display = df_display[["Job", "Waktu proses", "Due date (d)", "Saat selesai (c)", "Lateness (c-d)"]]
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        st.markdown("<hr>", unsafe_allow_html=True)
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
elif menu_pilihan == "📊  Hasil Gantt Chart":
    st.markdown(f"""<div class="section-header">{icon("chart","#FF8FAB",20)}<div class="section-title">Gantt Chart Urutan Pengerjaan Mesin</div></div>""", unsafe_allow_html=True)
    if df_spt is not None:
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
            barmode='stack', height=200, plot_bgcolor="#362031", paper_bgcolor="#2D1A29", showlegend=False,
            margin=dict(l=10, r=10, t=20, b=20),
            xaxis=dict(tickmode='array', tickvals=tick_vals, gridcolor="#4D3147", side="bottom", tickfont=dict(color='#F3EAF0')),
            yaxis=dict(visible=False)
        )
        st.plotly_chart(fig_gantt, use_container_width=True)
    else:
        st.warning("⚠️ Gantt chart belum dapat dibuat. Silakan isi data di menu 'Input Data Job'.")

# ─── HALAMAN 5: DOWNLOAD ──────────────────────────────────────────────────────
elif menu_pilihan == "📥  Download Hasil":
    st.markdown(f"""<div class="section-header">{icon("download","#FF8FAB",20)}<div class="section-title">Unduh Hasil Eksperimen</div></div>""", unsafe_allow_html=True)
    if df_spt is not None:
        st.markdown(f"""
        <div class="dashboard-box">
            <div class="box-title">{icon("download","#FF8FAB",17)} &nbsp;Ekspor Berkas CSV Hasil Perhitungan Terjadwal</div>
            <div class="box-text">
                Rangkaian matriks data urutan pengerjaan optimal Shortest Processing Time (SPT) mencakup kalkulasi
                saat mulai (<i>start time</i>), saat pengerjaan selesai (<i>completion time</i>), dan selisih keterlambatan batas waktu (<i>lateness</i>)
                dapat diunduh secara penuh di bawah ini.
            </div>
        </div>
        """, unsafe_allow_html=True)
        csv_buffer = io.StringIO()
        df_spt.to_csv(csv_buffer, index=False)
        st.download_button(
            label="  Download Hasil Analisis Penjadwalan (.CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"Hasil_Optimasi_SPT_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning("⚠️ Tidak ada data kalkulasi yang tersedia. Selesaikan pengisian di menu 'Input Data Job' terlebih dahulu.")
