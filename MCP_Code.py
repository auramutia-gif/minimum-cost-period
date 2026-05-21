import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="MRP MCP Final", layout="wide")
st.title("MRP App – Minimum Cost per Period (MCP) Only")

# Sidebar parameters
st.sidebar.header("Parameters")
setup_cost = st.sidebar.number_input("Setup Cost per Order (S)", value=500)
holding_cost = st.sidebar.number_input("Holding Cost per Unit (H)", value=5)
initial_inventory = st.sidebar.number_input("Initial Inventory", value=30)
lead_time = st.sidebar.number_input("Lead Time (periods)", value=1, min_value=0)
safety_stock = st.sidebar.number_input("Safety Stock", value=0)

# Main Dashboard Area
st.subheader("MCP (Minimum Cost Per Period) Optimization")
uploaded_csv = st.file_uploader("Upload CSV (Period, GR, Scheduled_Receipts)", type=["csv"], key="mcp_upload")

if uploaded_csv:
    # 1. Membaca Data Input
    df_input = pd.read_csv(uploaded_csv)
    periods = len(df_input)
    periods_label = [f"P{i+1}" for i in range(periods)]
    gross_req = df_input['GR'].tolist()
    scheduled_rec = df_input['Scheduled_Receipts'].tolist()

    all_iterations = []
    optimal_combinations = []
    
    # List untuk menampung hasil akhir tabel MRP
    final_planned_receipts = [0] * periods
    
    i = 0
    current_inventory = initial_inventory

    # 2. Algoritma Iterasi MCP
    while i < periods:
        best_combo = None
        combos_tried = []
        local_prev_cost_per_period = None

        for j in range(i, periods):
            # Kalkulasi Net Requirement (NR) kumulatif untuk sub-periode [i sampai j]
            temp_inventory = current_inventory
            nr_list = []
            for k in range(i, j+1):
                nr = max(0, gross_req[k] + safety_stock - (temp_inventory + scheduled_rec[k]))
                nr_list.append(nr)
                temp_inventory += nr + scheduled_rec[k] - gross_req[k]

            net_demand = sum(nr_list)

            # Kalkulasi Holding Cost berdasarkan sisa Inventory akhir periode (termasuk efek SR)
            temp_inventory_flow = current_inventory
            cumulative_holding = 0
            
            for idx, k in enumerate(range(i, j+1)):
                planned_rec_p = net_demand if idx == 0 else 0
                ending_inventory = temp_inventory_flow + planned_rec_p + scheduled_rec[k] - gross_req[k]
                
                if ending_inventory > 0 and k < j:
                    cumulative_holding += ending_inventory
                
                temp_inventory_flow = max(0, ending_inventory)

            total_cost = setup_cost + (holding_cost * cumulative_holding)
            cost_per_period = total_cost / (j-i+1)

            current_combo_info = {
                "Period Combination": f"{periods_label[i]}-{periods_label[j]}" if i!=j else periods_label[i],
                "Net Requirement": net_demand,
                "Lot Size": net_demand,
                "Total Cost": total_cost,
                "Cost per Period": cost_per_period
            }
            combos_tried.append(current_combo_info)

            # Aturan Berhenti MCP: Jika Cost per Period mulai naik, kunci kombinasi sebelumnya
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
            "Period Combination": f"{periods_label[start]}-{periods_label[end]}" if start!=end else periods_label[start],
            "Lot Size": lot_size,
            "Total Cost": total_cost,
            "Cost per Period": cost_per_period
        })

        # Alokasikan keputusan Lot Size ke periode awal pemesanan
        final_planned_receipts[start] = lot_size

        # Update Aktual Inventory Gudang untuk melangkah ke step berikutnya
        current_inventory += lot_size + scheduled_rec[start] - gross_req[start]
        for k in range(start+1, end+1):
            current_inventory += scheduled_rec[k] - gross_req[k]
        current_inventory = max(0, current_inventory)

        i = end + 1

    # 3. Penyusunan Tabel Hasil Akhir MRP Berdasarkan Keputusan MCP
    mrp_gross_req = []
    mrp_scheduled_rec = []
    mrp_projected_bal = []
    mrp_net_req = []
    mrp_planned_receipts = final_planned_receipts.copy()
    mrp_planned_releases = [0] * periods

    temp_inv = initial_inventory
    for k in range(periods):
        mrp_gross_req.append(gross_req[k])
        mrp_scheduled_rec.append(scheduled_rec[k])
        
        # Hitung Net Requirement Aktual di tabel akhir
        nr_aktual = max(0, gross_req[k] + safety_stock - (temp_inv + scheduled_rec[k]))
        mrp_net_req.append(nr_aktual)
        
        # Hitung saldo akhir persediaan (Projected Available Balance)
        temp_inv += mrp_planned_receipts[k] + scheduled_rec[k] - gross_req[k]
        mrp_projected_bal.append(temp_inv)
        
        # Hitung Planned Order Releases berdasarkan Lead Time (Penggeseran Periode Mundur)
        release_period = k - int(lead_time)
        if release_period >= 0:
            mrp_planned_releases[release_period] = mrp_planned_receipts[k]

    # Membuat Dataframe untuk Tabel MRP Utama
    mrp_matrix = {
        "Data / Period": [
            "Gross Requirements", 
            "Scheduled Receipts", 
            "Projected Available Balance", 
            "Net Requirements", 
            "Planned Order Receipts", 
            "Planned Order Releases"
        ]
    }
    
    for k in range(periods):
        mrp_matrix[f"P{k+1}"] = [
            mrp_gross_req[k],
            mrp_scheduled_rec[k],
            mrp_projected_bal[k],
            mrp_net_req[k],
            mrp_planned_receipts[k],
            mrp_planned_releases[k]
        ]
    
    df_mrp_matrix = pd.DataFrame(mrp_matrix).set_index("Data / Period")

    # 4. Tampilan Output di Aplikasi Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📋 All Iterations Tested")
        st.dataframe(pd.DataFrame(all_iterations), use_container_width=True)
    with col2:
        st.markdown("### 🏆 Optimal Combination per Step")
        st.dataframe(pd.DataFrame(optimal_combinations), use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 Final MRP Sheet (MCP Optimized)")
    st.dataframe(df_mrp_matrix, use_container_width=True)

    # 5. Fasilitas Download Data Hasil Gabungan
    csv_buffer = BytesIO()
    # Menggabungkan Matrix MRP, Iterasi, dan Hasil Optimal ke dalam satu struktur unduhan
    df_all_mcp = pd.DataFrame(all_iterations)
    df_opt_mcp = pd.DataFrame(optimal_combinations)
    combined = pd.concat([df_all_mcp, df_opt_mcp], keys=["All Iterations", "Optimal"])
    
    combined.to_csv(csv_buffer)
    st.download_button(
        label="📥 Download MCP Optimization Report (CSV)", 
        data=csv_buffer.getvalue(), 
        file_name="mcp_only_report.csv", 
        mime="text/csv"
    )
