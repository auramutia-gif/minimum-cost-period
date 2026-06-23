import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Konfigurasi halaman utama
st.set_page_config(
    page_title="Production Scheduling · SPT Optimizer",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── LOGIKAL WAKTU REAL-TIME (Sapaan Dinamis) ───────────────────────────────
current_hour = datetime.now().hour
if 4 <= current_hour < 11:
    sapaan = "Selamat Pagi"
elif 11 <= current_hour < 15:
    sapaan = "Selamat Siang"
elif 15 <= current_hour < 18:
    sapaan = "Selamat Sore"
else:
    sapaan = "Selamat Malam"

# Nama user dinamis (bisa disesuaikan lewat profile summary/state)
user_name = "Aura Mutia Azzahra" 

# ─── Custom CSS (Soft Pastel Pink & Purple Theme) ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #FFF8F9; } /* Latar belakang pink pastel super soft */

/* Desain Sidebar Pastel Pink Modis */
[data-testid="stSidebar"] { 
    background: linear-gradient(180deg, #FAD0C4 0%, #FFD1DC 100%) !important; 
    border-right: 1px solid #F8C3CD; 
}
[data-testid="stSidebar"] * { color: #5D434A !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #4A3137 !important; }

/* Hero Banner Soft Pink */
.hero-banner {
    background: linear-gradient(135deg, #FFB7B2 0%, #FFC6FF 100%);
    border-radius: 16px; padding: 30px 35px; margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(255, 183, 178, 0.2);
}
.hero-title { font-size: 26px; font-weight: 600; color: #4A3137; margin: 0 0 6px; }
.hero-sub { font-size: 13px; color: #6D4C54; margin: 0; }

/* Penjelasan Aturan SPT Box */
.spt-explainer {
    background: #FFFFFF; border: 1px solid #FFD1DC; border-radius: 12px;
    padding: 16px 20px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(255,183,178,0.1);
}
.spt-explainer-title { font-size: 14px; font-weight: 600; color: #4A3137; margin-bottom: 4px; display: flex; align-items: center; gap: 6px; }
.spt-explainer-text { font-size: 13px; color: #6D4C54; line-height: 1.5; }

/* Desain 3 Metric Cards */
.metric-card {
    background: white; border-radius: 12px; padding: 18px 20px;
    border: 1px solid #FFD1DC; box-shadow: 0 4px 12px rgba(255,183,178,0.15);
    text-align: center;
}
.metric-card.pastel-blue { border-top: 4px solid #BFFCC6; }  
.metric-card.pastel-pink { border-top: 4px solid #FFB7B2; } 
.metric-card.pastel-green { border-top: 4px solid #FFC6FF; }

.metric-label { font-size: 12px; font-weight: 600; color: #8A6D75; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.metric-value { font-size: 22px; font-weight: 600; color: #4A3137; font-family: 'DM Mono', monospace; }

.section-header { display: flex; align-items: center; gap: 10px; margin: 24px 0 14px; }
.section-title { font-size: 16px; font-weight: 600; color: #4A3137; }
.info-box { background: #FFF0F2; border-left: 4px solid #FFB7B2; border-radius: 0 8px 8px 0; padding: 12px 16px; margin-bottom: 20px; font-size: 13px; color: #6D4C54; }
hr { border-color: #FFD1DC !important; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR NAVIGATION & MENU BUTTONS ───────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding: 20px 0 10px'>
        <div style='font-size: 14px; color: #6D4C54; font-weight: 500;'>✨ {sapaan},</div>
        <div style='font-size: 20px; font-weight: 700; color: #4A3137;'>{user_name}</div>
        <div style='font-size: 11px; color: #8A6D75; margin-top: 2px;'>Selamat datang di SPT Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    # Elemen Menu Navigasi Samping Mockup (Sesuai Permintaan)
    st.markdown("### 📌 Navigasi")
    st.button("🏠 Dashboard", use_container_width=True, type="secondary")
    st.button("📥 Input Data Job", use_container_width=True)
    st.button("📂 Upload CSV", use_container_width=True)
    st.button("📊 Hasil Penjadwalan SPT", use_container_width=True)
    st.button("📈 Hasil Gantt Chart", use_container_width=True)
    st.button("⏱️ Riwayat", use_container_width=True)
    
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Fitur Pop-Up Edukasi Aturan SPT Menarik di Sidebar
    with st.expander("💡 Pelajari Aturan SPT Lebih Dalam", expanded=False):
        st.write("""
        **Shortest Processing Time (SPT)** mendahulukan urutan kerja dari durasi pengerjaan yang paling singkat ke yang paling lama. 
        
        Sifat utamanya adalah memotong antrean panjang dengan cepat, sehingga jumlah rata-rata tumpukan barang (*Work In Process*) di pabrik berkurang drastis!
        """)

# ─── HERO BANNER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">⏱️ Shortest Processing Time (SPT) Dashboard</div>
    <div class="hero-sub">Optimasi urutan penjadwalan tunggal (Single Machine Scheduling) untuk minimasi Mean Lateness</div>
</div>
""", unsafe_allow_html=True)

# ─── UPPERBAR EXPLANATION ─────────────────────────────────────────────────────
st.markdown("""
<div class="spt-explainer">
    <div class="spt-explainer-title">⏱️ Aturan Shortest Processing Time (SPT)</div>
    <div class="spt-explainer-text">
        Pekerjaan dengan <b>waktu proses terpendek</b> akan dijadwalkan terlebih dahulu. 
        Aturan ini terbukti secara matematis optimal dalam meminimalkan <i>Mean Flow Time</i>, <i>Mean Work-in-Process</i>, dan <i>Mean Lateness</i> pada sistem mesin tunggal.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── DATA INPUT SECTION ───────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-title">📂 Input Data Job (Pekerjaan)</div>
</div>
""", unsafe_allow_html=True)

input_method = st.radio(
    "Pilih Metode Input Data:",
    ("Manual Input (Ketik di Tabel)", "Otomatis (Upload File CSV)"),
    horizontal=True
)

df_input_final = None

if input_method == "Manual Input (Ketik di Tabel)":
    st.markdown("""
    <div class="info-box">
        💡 <b>Petunjuk:</b> Isikan daftar pekerjaan pada baris kosong di bawah ini. Masukkan Nama Job, Waktu Proses (Waktu), dan Due Date. 
        Gunakan tombol <b>"Enter"</b> atau klik sel di bawahnya untuk menambah baris baru.
    </div>
    """, unsafe_allow_html=True)

    init_data = pd.DataFrame(columns=["Job_Name", "Processing_Time", "Due_Date"])
    edited_df = st.data_editor(
        init_data,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Job_Name": st.column_config.TextColumn("Job", required=True),
            "Processing_Time": st.column_config.NumberColumn("Waktu (Waktu Proses)", min_value=1, step=1, format="%d"),
            "Due_Date": st.column_config.NumberColumn("Due Date", min_value=1, step=1, format="%d")
        }
    )
    if edited_df is not None and len(edited_df) > 0:
        df_input_final = edited_df.dropna(subset=["Job_Name", "Processing_Time", "Due_Date"]).copy()

else:
    st.markdown("""
    <div class="info-box">
        📂 <b>Format Kolom CSV:</b> Pastikan file CSV Anda memiliki header atau nama kolom yang tepat yaitu: 
        <code style="background-color: #FFD1DC; padding: 2px 6px; border-radius: 4px; color: #4A3137; font-weight: bold;">Job | Waktu Proses | Due date</code>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df_csv = pd.read_csv(uploaded_file)
            col_mapping = {}
            for col in df_csv.columns:
                c_clean = col.strip().lower()
                if c_clean == 'job':
                    col_mapping[col] = 'Job_Name'
                elif 'waktu' in c_clean or 'processing' in c_clean:
                    col_mapping[col] = 'Processing_Time'
                elif 'due' in c_clean:
                    col_mapping[col] = 'Due_Date'
            
            if len(col_mapping) >= 3:
                df_csv = df_csv.rename(columns=col_mapping)
                df_input_final = df_csv[['Job_Name', 'Processing_Time', 'Due_Date']].dropna().copy()
                st.success("✅ File CSV berhasil diunggah!")
                st.dataframe(df_input_final, use_container_width=True)
            else:
                st.error("❌ Gagal memetakan kolom. Pastikan file CSV memiliki kolom: 'Job', 'Waktu Proses', dan 'Due date'.")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat membaca file: {e}")

# ─── PROSEDUR PERHITUNGAN DAN OUTPUT ──────────────────────────────────────────
if st.button("▶ Hitung Penjadwalan SPT", type="primary"):
    if df_input_final is not None and len(df_input_final) > 0:
        
        df_input_final["Processing_Time"] = df_input_final["Processing_Time"].astype(int)
        df_input_final["Due_Date"] = df_input_final["Due_Date"].astype(int)
        
        # Perhitungan Inti Aturan SPT
        df_spt = df_input_final.sort_values(by="Processing_Time", ascending=True).reset_index(drop=True)
        
        start_times = []
        comp_times = []
        current_time = 0
        
        for idx, row in df_spt.iterrows():
            start_times.append(current_time)
            current_time += row["Processing_Time"]
            comp_times.append(current_time)
            
        df_spt["Start_Time"] = start_times
        df_spt["Completion_Time"] = comp_times
        df_spt["Lateness"] = df_spt["Completion_Time"] - df_spt["Due_Date"]
        
        # ─── TABEL HASIL URUTAN SPT (Langsung Menampilkan Tabel Tanpa Teks) ───
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div class="section-header"><div class="section-title">📊 Tabel Urutan Penyelesaian SPT</div></div>""", unsafe_allow_html=True)
        
        df_display = df_spt.copy()
        df_display.columns = ["Job", "Waktu proses", "Due date (d)", "Start_Time", "Saat selesai (c)", "Lateness (c-d)"]
        df_display = df_display[["Job", "Waktu proses", "Due date (d)", "Saat selesai (c)", "Lateness (c-d)"]]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ─── VISUALISASI CHART (Gantt Chart Linear Alami) ────────────────────
        st.markdown("""<div class="section-header"><div class="section-title">📊 Gantt Chart Urutan Pengerjaan</div></div>""", unsafe_allow_html=True)
        
        pastel_colors = ['#FFB7B2', '#FFDAC1', '#E2F0CB', '#BFFCC6', '#AEC6CF', '#C3B1CE', '#FFC6FF', '#E8D6F5']
        fig_gantt = go.Figure()
        
        for idx, row in df_spt.iterrows():
            color_idx = idx % len(pastel_colors)
            fig_gantt.add_trace(go.Bar(
                x=[int(row["Processing_Time"])], 
                y=["Mesin"],
                base=[int(row["Start_Time"])],   
                orientation='h',
                name=str(row["Job_Name"]),
                text=str(row["Job_Name"]),       
                textposition='inside',           
                marker=dict(
                    color=pastel_colors[color_idx],
                    line=dict(color='#4A3137', width=1)
                ),
                hovertemplate=f"<b>Job:</b> {row['Job_Name']}<br><b>Waktu:</b> {row['Processing_Time']}<br><b>Mulai:</b> {row['Start_Time']}<br><b>Selesai:</b> {row['Completion_Time']}<extra></extra>"
            ))
        
        tick_vals = [0] + list(map(int, df_spt["Completion_Time"].values))
        
        fig_gantt.update_layout(
            barmode='stack', height=200, plot_bgcolor="white", showlegend=False,
            margin=dict(l=10, r=10, t=20, b=20),
            xaxis=dict(tickmode='array', tickvals=tick_vals, gridcolor="#FFD1DC", side="bottom"),
            yaxis=dict(visible=False)
        )
        st.plotly_chart(fig_gantt, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ─── METRIC CARDS (Hasil Akhir Berupa 3 Kolom) ────────────────────────
        st.markdown("""<div class="section-header"><div class="section-title">📋 Hasil Penjadwalan SPT</div></div>""", unsafe_allow_html=True)
        
        mean_lateness = df_spt["Lateness"].mean()
        max_lateness = df_spt["Lateness"].max()
        
        sequence_list = [str(x) for x in df_spt["Job_Name"]]
        sequence_str = " - ".join(sequence_list)
        
        kolom_rata_rata, kolom_max_lateness, kolom_urutan_hasil = st.columns(3)
        
        with kolom_rata_rata:
            st.markdown(f"""
            <div class="metric-card pastel-blue">
                <div class="metric-label">Rata-rata Lateness</div>
                <div class="metric-value">{mean_lateness:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kolom_max_lateness:
            st.markdown(f"""
            <div class="metric-card pastel-pink">
                <div class="metric-label">Maximum Lateness</div>
                <div class="metric-value">{max_lateness}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kolom_urutan_hasil:
            st.markdown(f"""
            <div class="metric-card pastel-green">
                <div class="metric-label">Urutan Hasil Penjadwalan</div>
                <div class="metric-value" style="font-size: 18px; padding-top: 4px;">{sequence_str}</div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.warning("Silakan isi data pekerjaan di tabel atau unggah file CSV terlebih dahulu sebelum menghitung.")
