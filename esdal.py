import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="ESDAL Theory & Simulator Engine", layout="wide")

# Header Utama
st.title("🏛️ ESDAL Simulator Engine")
st.caption("Penerjemahan Buku Akademik & Fenomena Masyarakat menjadi Alat Simulasi Interaktif")

# Sidebar - Navigasi Alur
st.sidebar.header("📌 Menu Navigasi")
pilihan_modul = st.sidebar.selectbox("Pilih Topik (Buku Acuan):", [
    "Bab 4: Eksternalitas & Pajak Pigou",
    "Bab 5: Alokasi Intertemporal Sumber Daya"
])

# ==========================================
# MODUL BAB 4 (Sesuai Alur Sketsa)
# ==========================================
if pilihan_modul == "Bab 4: Eksternalitas & Pajak Pigou":
    st.subheader("📚 1. Landasan Teori (Buku Tietenberg & Lewis - Bab 4)")
    st.markdown("""
    * **Teori:** Internalization of Externalities via Pigouvian Tax.
    * **Asumsi:** $MSC = MPC + MEC$. Tanpa intervensi, pasar hanya memperhitungkan $MPC$ sehingga terjadi *overproduction*.
    """)
    st.divider()

    col_input, col_output = st.columns([1, 2])

    with col_input:
        st.subheader("🌐 2. Fenomena & Variabel Input")
        st.write("*Atur parameter kasus pencemaran lingkungan:*")
        
        # Variabel Fenomena
        p_market = st.slider("Harga Pasar / Benefit ($P$)", 20, 100, 60)
        mpc_val = st.slider("Biaya Privat Perusahaan ($MPC$)", 5, 40, 15)
        mec_val = st.slider("Dampak Polusi ke Masyarakat ($MEC$)", 0, 50, 20)
        
        st.write("---")
        st.subheader("⚙️ 3. Solusi / Kebijakan")
        pajak = st.slider("Pajak Pigou ($t$ per unit)", 0, 50, 0)

    with col_output:
        st.subheader("📊 4. Output / Simulation Engine")
        
        # Logic Engine
        q = np.linspace(0, 100, 100)
        demand = p_market - 0.4 * q
        mpc = mpc_val + 0.2 * q
        msc = mpc + mec_val
        mpc_tax = mpc + pajak

        # Calculation Points
        q_market = max(0, (p_market - mpc_val) / 0.6)
        q_social = max(0, (p_market - mpc_val - mec_val) / 0.6)

        # Plotting
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.plot(q, demand, label="Marginal Social Benefit (Demand)", color="blue", lw=2)
        ax.plot(q, mpc, label="Private Cost (MPC)", color="red", linestyle="--")
        ax.plot(q, msc, label="Social Cost (MSC = MPC + MEC)", color="green", lw=2)
        
        if pajak > 0:
            ax.plot(q, mpc_tax, label=f"MPC + Pajak (${pajak})", color="orange", linestyle="-.")

        ax.set_xlabel("Jumlah Produksi / Limbah (Q)")
        ax.set_ylabel("Nilai Ekonomis ($)")
        ax.set_ylim(0, 110)
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

        # Insight Evaluasi
        st.info(f"""
        **📌 Hasil Evaluasi Logic Engine:**
        * **Keseimbangan Pasar Bebas ($Q_{{pasar}}$):** {q_market:.1f} unit
        * **Keseimbangan Efisien Sosial ($Q_{{efisien}}$):** {q_social:.1f} unit
        * **Status:** {'Terjadi Over-production! Sila naikkan pajak.' if pajak < mec_val else 'Eksternalitas Berhasil Diinternalisasi!' if pajak == mec_val else 'Pajak Terlalu Tinggi (Beban Industri)!'}
        """)
