import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Production Scheduling · SPT Optimizer",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS (Pastel Palette Theme) ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #FAF8F6; }
[data-testid="stSidebar"] { background: #4A3E4D !important; border-right: 1px solid #D6C7D9; }
[data-testid="stSidebar"] * { color: #F5EFF6 !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #FFFFFF !important; }

.hero-banner {
    background: linear-gradient(135deg, #A896B0 0%, #C3B1CE 50%, #E2D4E7 100%);
    border-radius: 16px; padding: 30px 35px; margin-bottom: 24px;
}
.hero-title { font-size: 26px; font-weight: 600; color: #FFFFFF; margin: 0 0 6px; }
.hero-sub { font-size: 13px; color: #F5EFF6; margin: 0; }

.metric-card {
    background: white; border-radius: 12px; padding: 18px 20px;
    border: 1px solid #E5DEE6; box-shadow: 0 2px 8px rgba(168,150,176,0.1);
    text-align: center;
}
.metric-card.pastel-blue { border-top: 4px solid #AEC6CF; }
.metric-card.pastel-pink { border-top: 4px solid #FFB7B2; }
.metric-card.pastel-green { border-top: 4px solid #BFFCC6; }

.metric-label { font-size: 12px; font-weight: 600; color: #8A7A93; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.metric-value { font-size: 22px; font-weight: 600; color: #4A3E4D; font-family: 'DM Mono', monospace; }

.section-header { display: flex; align-items: center; gap: 10px; margin: 24px 0 14px; }
.section-title { font-size: 16px; font-weight: 600; color: #4A3E4D; }
.info-box { background: #F3EEF5; border-left: 4px solid #C3B1CE; border-radius: 0 8px 8px 0; padding: 12px 16px; margin-bottom: 20px; font-size: 13px; color: #64536D; }
hr { border-color: #E5DEE6 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Input ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 16px'>
        <div style='font-size:22px; font-weight:700; color:#FFFFFF;'>SPT Scheduler</div>
        <div style='font-size:12px; color:#D6C7D9; margin-top:3px'>Shortest Processing Time Rule</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("⏱️ **Aturan SPT:** Pekerjaan dengan waktu proses terpendek akan dijadwalkan terlebih dahulu untuk meminimalkan *Mean Lateness*.")

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">⏱️ Shortest Processing Time (SPT) Dashboard</div>
    <div class="hero-sub">Optimasi urutan penjadwalan tunggal (Single Machine Scheduling) untuk minimasi Mean Lateness</div>
</div>
""", unsafe_allow_html=True)

# ─── Data Input Section ───────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-title">📂 Input Data Job (Pekerjaan)</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    💡 <b>Petunjuk:</b> Isikan daftar pekerjaan pada baris kosong di bawah ini. Masukkan Nama Job, Waktu Proses (Waktu), dan Due Date. 
    Gunakan tombol <b>"Enter"</b> atau klik sel di bawahnya untuk menambah baris baru.
</div>
""", unsafe_allow_html=True)

# Dataframe baseline dikosongkan sesuai permintaan
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

if st.button("▶ Hitung Penjadwalan SPT", type="primary"):
    # Validasi agar tidak error saat data kosong
    if edited_df is not None and len(edited_df) > 0 and not edited_df.dropna(subset=["Job_Name", "Processing_Time", "Due_Date"]).empty:
        df_jobs = edited_df.dropna(subset=["Job_Name", "Processing_Time", "Due_Date"]).copy()
        
        # Pastikan tipe data numerik
        df_jobs["Processing_Time"] = df_jobs["Processing_Time"].astype(int)
        df_jobs["Due_Date"] = df_jobs["Due_Date"].astype(int)
        
        # ─── SPT Calculation Logic ────────────────────────────────────────────
        # Urutkan waktu proses dari yang terkecil sampai terbesar
        df_spt = df_jobs.sort_values(by="Processing_Time", ascending=True).reset_index(drop=True)
        
        start_times = []
        comp_times = []
        current_time = 0
        
        for idx, row in df_spt.iterrows():
            start_times.append(current_time)
            current_time += row["Processing_Time"]
            comp_times.append(current_time)
            
        df_spt["Start_Time"] = start_times
        df_spt["Completion_Time"] = comp_times
        
        # Lateness = Saat Selesai (c) - Due Date (d)
        df_spt["Lateness"] = df_spt["Completion_Time"] - df_spt["Due_Date"]
        
        # ─── TABEL HASIL URUTAN SPT ───────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Penyelesaian :")
        st.markdown("1. Urutan waktu proses dari yang terkecil sampai yang terbesar")
        st.markdown("2. Hitung saat selesai (kolom c)")
        st.markdown("3. Hitung Lateness = saat selesai – due date = c - d")
        
        df_display = df_spt.copy()
        df_display.columns = ["Job", "Waktu proses", "Due date (d)", "Start_Time", "Saat selesai (c)", "Lateness (c-d)"]
        df_display = df_display[["Job", "Waktu proses", "Due date (d)", "Saat selesai (c)", "Lateness (c-d)"]]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ─── VISUALISASI CHART (Gantt Chart Linear Sesuai Gambar) ──────────────
        st.markdown("""<div class="section-header"><div class="section-title">📊 Gantt Chart Urutan Pengerjaan</div></div>""", unsafe_allow_html=True)
        
        # Palet Warna Pastel untuk Chart Berurutan
        pastel_colors = ['#FFB7B2', '#FFDAC1', '#E2F0CB', '#BFFCC6', '#AEC6CF', '#C3B1CE', '#FFC6FF', '#E8D6F5']
        
        fig_gantt = go.Figure()
        
        # Menggunakan struktur bar tunggal berlapis (stacked) mendatar seperti timeline gambar
        for idx, row in df_spt.iterrows():
            color_idx = idx % len(pastel_colors)
            fig_gantt.add_trace(go.Bar(
                x=[row["Processing_Time"]],
                y=["Mesin"],
                base=[row["Start_Time"]],
                orientation='h',
                name=str(row["Job_Name"]),
                text=f"{row['Job_Name']}",
                textposition='inside',
                insidetextanchor='center',
                marker=dict(
                    color=pastel_colors[color_idx],
                    line=dict(color='#4A3E4D', width=1)
                ),
                hovertemplate=f"<b>Job:</b> {row['Job_Name']}<br><b>Waktu:</b> {row['Processing_Time']}<br><b>Mulai:</b> {row['Start_Time']}<br><b>Selesai:</b> {row['Completion_Time']}<extra></extra>"
            ))
        
        # Pengaturan sumbu X agar mencantumkan titik-titik milestone waktu pengerjaan
        tick_vals = [0] + list(df_spt["Completion_Time"].values)
        
        fig_gantt.update_layout(
            barmode='stack',
            height=200,
            plot_bgcolor="white",
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=20),
            xaxis=dict(
                tickmode='array',
                tickvals=tick_vals,
                gridcolor="#E5DEE6",
                side="bottom"
            ),
            yaxis=dict(
                visible=False
            )
        )
        st.plotly_chart(fig_gantt, use_container_width=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ─── METRIC CARDS (Hasil Penjadwalan SPT di Bagian Akhir) ─────────────
        st.markdown("""<div class="section-header"><div class="section-title">📋 Hasil Penjadwalan SPT</div></div>""", unsafe_allow_html=True)
        
        # Hitung Nilai Performa
        mean_lateness = df_spt["Lateness"].mean()
        max_lateness = df_spt["Lateness"].max()
        
        # Format string urutan hasil: e.g., 4-8-1-3-7-2-5-6
        sequence_list = [str(x) for x in df_spt["Job_Name"]]
        sequence_str = " - ".join(sequence_list)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-card pastel-blue">
                <div class="metric-label">Rata-rata Lateness</div>
                <div class="metric-value">{mean_lateness:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card pastel-pink">
                <div class="metric-label">Maximum Lateness</div>
                <div class="metric-value">{max_lateness}</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card pastel-green">
                <div class="metric-label">Urutan Hasil</div>
                <div class="metric-value" style="font-size: 18px; padding-top: 4px;">{sequence_str}</div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.warning("Silakan masukkan data pekerjaan terlebih dahulu pada tabel secara lengkap (Nama Job, Waktu, dan Due Date).")
