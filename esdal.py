import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="ESDAL Simulator - Tietenberg & Lewis", layout="wide")

st.title("🌱 ESDAL Interactive Simulator")
st.caption("Simulator Ekonomi Sumber Daya Alam & Lingkungan (Acuan: Tietenberg & Lewis, 2018)")

# Sidebar Menu
menu = st.sidebar.radio("Pilih Modul Pembelajaran:", [
    "Bab 4: Eksternalitas & Open Access",
    "Bab 5: Alokasi Intertemporal (Two-Period Model)"
])

# ==========================================
# MODUL 1: BAB 4
# ==========================================
if menu == "Bab 4: Eksternalitas & Open Access":
    st.header("🎣 Bab 4: Property Rights & Externalities")
    st.write("""
    **Konsep:** Membandingkan tingkat eksploitasi sumber daya milik bersama (*Open Access*) 
    dengan intervensi kebijakan berupa **Pajak Pigou (Pigouvian Tax)**.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ Parameter Simulator")
        harga = st.slider("Harga Produk ($P$)", 10, 100, 50)
        cost_private = st.slider("Biaya Privat Marginal ($MC_{private}$)", 5, 50, 20)
        cost_external = st.slider("Biaya Polusi/Kerusakan ($MEC$)", 0, 40, 15)
        pajak = st.slider("Tarif Pajak Lingkungan ($t$)", 0, 40, 0)
        
    with col2:
        st.subheader("📊 Grafis Keseimbangan Pasar")
        q = np.linspace(0, 100, 100)
        mb = harga - 0.3 * q
        mc_p = cost_private + 0.2 * q
        mc_s = mc_p + cost_external
        mc_tax = mc_p + pajak
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(q, mb, label="Marginal Benefit (Demand)", color="blue", linewidth=2)
        ax.plot(q, mc_p, label="Private MC (Tanpa Pajak)", color="red", linestyle="--")
        ax.plot(q, mc_s, label="Social MC (Private + MEC)", color="green", linewidth=2)
        if pajak > 0:
            ax.plot(q, mc_tax, label=f"Private MC + Pajak (${pajak})", color="orange", linestyle="-.")
            
        ax.set_xlabel("Tingkat Produksi / Eksploitasi (Q)")
        ax.set_ylabel("Nilai ($)")
        ax.set_ylim(0, 120)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
    st.info(f"""
    💡 **Analisis:** - Tanpa pajak, industri memproduksi berdasarkan *Private MC*.  
    - Ketika ada eksternalitas ($MEC = {cost_external}$), alokasi pasar menyebabkan *over-production* yang merugikan sosial.
    - Pasang **Pajak = {cost_external}** untuk menginternalisasi eksternalitas dan mencapai efisiensi sosial!
    """)

# ==========================================
# MODUL 2: BAB 5
# ==========================================
elif menu == "Bab 5: Alokasi Intertemporal (Two-Period Model)":
    st.header("⏳ Bab 5: Dynamic Efficiency (Two-Period Model)")
    st.write("""
    **Konsep:** Bagaimana alokasi cadangan sumber daya tak terbarukan (seperti batu bara/minyak) 
    dibagi antara **Generasi 1 (Hari Ini)** dan **Generasi 2 (Masa Depan)** berdasarkan suku bunga (*Discount Rate*).
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ Parameter Simulator")
        total_q = st.slider("Total Cadangan Sumber Daya ($Q_{total}$)", 10, 100, 30)
        r = st.slider("Discount Rate / Suku Bunga ($r$ in %)", 0, 30, 10) / 100.0
        
        # Logika Alokasi Sederhana
        # P1 - MC = (P2 - MC)/(1+r) -> Q1 + Q2 = Total
        # Misal Demand P = 8 - 0.2*Q, MC = 2
        # Net MB1 = 6 - 0.2*Q1; Net MB2 = (6 - 0.2*Q2)/(1+r)
        # 6 - 0.2*Q1 = (6 - 0.2*(Total - Q1))/(1+r)
        q1 = (6 * r + 0.2 * total_q) / (0.2 * (2 + r))
        q1 = max(0, min(q1, total_q))
        q2 = total_q - q1
        
        st.metric("Alokasi Generasi 1 (Q1)", f"{q1:.2f} unit")
        st.metric("Alokasi Generasi 2 (Q2)", f"{q2:.2f} unit")
        
    with col2:
        st.subheader("📊 Pembagian Cadangan Antar-Generasi")
        fig, ax = plt.subplots(figsize=(6, 4))
        generations = ['Generasi 1 (Sekarang)', 'Generasi 2 (Masa Depan)']
        allocations = [q1, q2]
        
        bars = ax.bar(generations, allocations, color=['#2b5c8f', '#d95f02'])
        ax.set_ylabel("Jumlah Konsumsi (Q)")
        ax.set_ylim(0, total_q)
        
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f"{yval:.2f}", ha='center', va='bottom')
            
        st.pyplot(fig)
        
    st.warning(f"""
    📢 **Refleksi Mahasiswa:** Saat suku bunga (*Discount Rate*) dinaikkan menjadi **{r*100:.0f}%**, Generasi 1 cenderung mengambil porsi sumber daya yang **lebih banyak** dibanding Generasi 2.  
    *Mengapa egoisme generasi sekarang makin tinggi ketika suku bunga naik? Sila baca bab 5 buku Tietenberg!*
    """)
