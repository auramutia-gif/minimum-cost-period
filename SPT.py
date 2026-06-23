import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import io

# Konfigurasi halaman utama
st.set_page_config(
    page_title="Production Scheduling · SPT Optimizer",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── INISIALISASI SESSION STATE (Menyimpan Data Antar Halaman) ──────────────
if "df_input" not in st.session_state:
    st.session_state.df_input = None

# Logika Waktu Real-Time Sapaan
current_hour = datetime.now().hour
if 4 <= current_hour < 11:
    sapaan = "Selamat Pagi"
elif 11 <= current_hour < 15:
    sapaan = "Selamat Siang"
elif 15 <= current_hour < 18:
    sapaan = "Selamat Sore"
else:
    sapaan = "Selamat Malam"

user_name = "Aura Mutia Azzahra"

# ─── Custom CSS (Gradasi Soft Pink & Rata Kiri Profesional) ──────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #FFF8F9; } 

/* Gradasi Soft Pink Sidebar */
[data-testid="stSidebar"] { 
    background: linear-gradient(180deg, #FFEBEF 0%, #FFD1DC 100%) !important; 
    border-right: 1px solid #F8C3CD; 
}
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio fieldset { border: none; padding: 0; margin: 0; }

/* Cards & Layout Style */
.hero-banner {
    background: linear-gradient(135deg, #FFCCD5 0%, #FFB7B2 100%);
    border-radius: 16px; padding: 30px 35px; margin-bottom: 24px;
    box-shadow: 0 4px 15px rgba(255, 183, 178, 0.15);
}
.hero-title { font-size: 28px; font-weight: 600; color: #4A3137; margin: 0 0 6px; }
.hero-sub { font-size: 14px; color: #6D4C54; margin: 0; }

.dashboard-box {
    background: #FFFFFF; border: 1px solid #FFD1DC; border-radius: 14px;
    padding: 20px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(255,183,178,0.1);
}
.box-title { font-size: 16px; font-weight: 600; color: #4A3137; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.box-text { font-size: 13.5px; color: #6D4C54; line-height: 1.6; }

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

.section-header { display: flex; align-items: center; gap: 10px; margin: 20px 0 14px; }
.section-title { font-size: 18px; font-weight: 600; color: #4A3137; }
.info-box { background: #FFF0F2; border-left: 4px solid #FFB7B2; border-radius: 0 8px 8px 0; padding: 12px 16px; margin-bottom: 20px; font-size: 13px; color: #6D4C54; }
hr { border-color: #FFD1DC !important; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR NAVIGATION (Struktur Menu Baru Sesuai Permintaan) ───────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 15px 0 5px'>
        <div style='font-size: 20px; font-weight: 700; color: #4A3137;'>⏱️ SPT Dashboard</div>
        <div style='font-size: 11px; color: #8A6D75; margin-top: 2px;'>Shortest Processing Time Optimizer</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    menu_pilihan = st.radio(
        "Navigasi Halaman:",
        [
            "🏠 Dashboard", 
            "📝 Input Data Job", 
            "📋 Hasil Penjadwalan SPT", 
            "📊 Hasil Gantt Chart", 
            "📥 Download Hasil"
        ],
        index=0
    )

# ─── ENGINE KALKULASI OTOMATIS (Background Processing) ────────────────────────
df_spt = None
if st.session_state.df_input is not None and len(st.session_state.df_input) > 0:
    df_calc = st.session_state.df_input.copy()
    df_calc["Processing_Time"] = df_calc["Processing_Time"].astype(int)
    df_calc["Due_Date"] = df_calc["Due_Date"].astype(int)
    
    # Aturan Penjadwalan SPT
    df_spt = df_calc.sort_values(by="Processing_Time", ascending=True).reset_index(drop=True)
    
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


# ─── HALAMAN 1: DASHBOARD ─────────────────────────────────────────────────────
if menu_pilihan == "🏠 Dashboard":
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">✨ {sapaan}, {user_name}!</div>
        <div class="hero-sub">Selamat datang di sistem optimasi urutan pengerjaan tunggal (Single Machine Scheduling).</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-box">
        <div class="box-title">⏱️ Apa itu Aturan Shortest Processing Time (SPT)?</div>
        <div class="box-text">
            <b>Shortest Processing Time (SPT)</b> adalah salah satu metode penjadwalan prioritas di mana pekerjaan yang memiliki 
            <b>waktu proses paling pendek atau singkat</b> akan dikerjakan terlebih dahulu. Secara analitis, aturan ini sangat 
            efektif dan optimal untuk meminimalkan waktu tunggu, mengurangi penumpukan antrean (Work-In-Process), serta 
            menekan nilai <i>Mean Lateness</i> (rata-rata keterlambatan) hingga titik paling rendah.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-box">
        <div class="box-title">🛠️ Langkah Penggunaan Aplikasi Web</div>
        <div class="box-text" style="padding-left: 4px;">
            1. Buka menu samping, lalu pilih <b>"Input Data Job"</b>. Di sana Anda bisa memasukkan data secara Manual via Tabel atau Upload CSV.<br>
            2. Sistem secara otomatis akan memproses urutan penjadwalan di latar belakang tanpa perlu menekan tombol hitung.<br>
            3. Klik menu <b>"Hasil Penjadwalan SPT"</b> untuk melihat hasil analisis tabel perhitungan performa keterlambatan.<br>
            4. Klik menu <b>"Hasil Gantt Chart"</b> untuk melihat representasi visual urutan pengerjaan mesin secara horizontal.<br>
            5. Gunakan menu <b>"Download Hasil"</b> untuk mengunduh seluruh ringkasan data penjadwalan ke dalam berkas CSV.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── HALAMAN 2: INPUT DATA JOB (Gabungan Manual & CSV) ────────────────────────
elif menu_pilihan == "📝 Input Data Job":
    st.markdown("""<div class="section-header"><div class="section-title">📂 Input Data Job (Pekerjaan)</div></div>""", unsafe_allow_html=True)
    
    input_method = st.radio(
        "Pilih Metode Memasukkan Data:",
        ("Manual Input (Ketik di Tabel)", "Otomatis (Upload File CSV)"),
        horizontal=True
    )
    
    if input_method == "Manual Input (Ketik di Tabel)":
        st.markdown("""
        <div class="info-box">
            💡 <b>Petunjuk:</b> Isikan daftar pekerjaan langsung pada baris komponen tabel di bawah ini. 
            Data yang Anda ketik akan otomatis tersimpan ke dalam sistem secara real-time.
        </div>
        """, unsafe_allow_html=True)
        
        # Mengambil data awal jika sebelumnya sudah pernah di-input agar tidak hilang
        init_data = st.session_state.df_input if st.session_state.df_input is not None else pd.DataFrame(columns=["Job_Name", "Processing_Time", "Due_Date"])
        
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
            st.session_state.df_input = edited_df.dropna(subset=["Job_Name", "Processing_Time", "Due_Date"]).copy()
            st.success("✨ Data tabel manual berhasil direkam otomatis!")

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
                    st.session_state.df_input = df_csv[['Job_Name', 'Processing_Time', 'Due_Date']].dropna().copy()
                    st.success("✅ File CSV berhasil diunggah dan direkam!")
                    st.dataframe(st.session_state.df_input, use_container_width=True)
                else:
                    st.error("❌ Gagal memetakan kolom. Pastikan file CSV memiliki kolom: 'Job', 'Waktu Proses', dan 'Due date'.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat membaca file: {e}")


# ─── HALAMAN 3: HASIL PENJADWALAN SPT ─────────────────────────────────────────
elif menu_pilihan == "📋 Hasil Penjadwalan SPT":
    st.markdown("""<div class="section-header"><div class="section-title">📋 Hasil Penjadwalan Urutan SPT</div></div>""", unsafe_allow_html=True)
    
    if df_spt is not None:
        df_display = df_spt.copy()
        df_display.columns = ["Job", "Waktu proses", "Due date (d)", "Start_Time", "Saat selesai (c)", "Lateness (c-d)"]
        df_display = df_display[["Job", "Waktu proses", "Due date (d)", "Saat selesai (c)", "Lateness (c-d)"]]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Bagian 3 Kolom Metrik Ringkasan Hasil Penjadwalan
        mean_lateness = df_spt["Lateness"].mean()
        max_lateness = df_spt["Lateness"].max()
        sequence_str = " - ".join([str(x) for x in df_spt["Job_Name"]])
        
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
        st.warning("⚠️ Belum ada data pengerjaan yang terekam. Silakan isi atau unggah data terlebih dahulu di menu 'Input Data Job'.")


# ─── HALAMAN 4: HASIL GANTT CHART ─────────────────────────────────────────────
elif menu_pilihan == "📊 Hasil Gantt Chart":
    st.markdown("""<div class="section-header"><div class="section-title">📊 Gantt Chart Urutan Pengerjaan Mesin</div></div>""", unsafe_allow_html=True)
    
    if df_spt is not None:
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
    else:
        st.warning("⚠️ Gantt chart belum dapat dibuat. Silakan isi atau unggah data terlebih dahulu di menu 'Input Data Job'.")


# ─── HALAMAN 5: DOWNLOAD HASIL (Fitur Baru Pengganti Riwayat) ────────────────
elif menu_pilihan == "📥 Download Hasil":
    st.markdown("""<div class="section-header"><div class="section-title">📥 Unduh Hasil Optimasi Eksperimen</div></div>""", unsafe_allow_html=True)
    
    if df_spt is not None:
        st.markdown("""
        <div class="dashboard-box">
            <div class="box-title">💾 Ekspor Berkas CSV Hasil Akhir</div>
            <div class="box-text">
                Seluruh rangkaian kalkulasi data urutan penjadwalan tunggal, meliputi durasi mulai (<i>start time</i>), 
                saat pengerjaan selesai (<i>completion time</i>), hingga nilai penalti keterlambatan waktu (<i>lateness</i>) telah 
                dikompilasi ke dalam format tabel yang siap digunakan untuk laporan produksi.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Membuat Buffer String Menjadi File CSV Virtual
        csv_buffer = io.StringIO()
        df_spt.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download Hasil Optimasi (.CSV)",
            data=csv_data,
            file_name=f"Hasil_Optimasi_SPT_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning("⚠️ Tidak ada data hasil perhitungan optimasi yang bisa diunduh. Silakan lengkapi berkas di menu 'Input Data Job' terlebih dahulu.")
