import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Konfigurasi
st.set_page_config(page_title="Dashboard Analisis Tip Restoran", layout="wide")
st.markdown(
    """
    <style>
    [class*="st-key-bg_kpi"] {
        background-color: #111A2B;
        border: 2px solid #FFFFFF;
        padding: 16px;
    }
    
    [class*="st-key-bg_bar"] {
        background-color: #111A2B;
        border: 2px solid #FFFFFF;
        padding: 16px;
    }
    
    [class*="st-key-bg_scatter"] {
        background-color: #111A2B;
        border: 2px solid #FFFFFF;
        padding: 16px;
    }
    
    [class*="st-key-bg_heatmap"] {
        background-color: #111A2B;
        border: 2px solid #FFFFFF;
        padding: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
sns.set_theme(style = "darkgrid")

#Load Data
path = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
df_dashboard = pd.read_csv(path)
df_dashboard["tip_pct"] = (df_dashboard["tip"] / df_dashboard["total_bill"]) * 100
df_dashboard["pendapatan"] = df_dashboard["total_bill"] + df_dashboard["tip"]

#Fitur Filter
st.sidebar.header("Filter Dashboard")

days_value = ["Thur", "Fri","Sat", "Sun"]
selected_days = st.sidebar.multiselect(
    label = "The Open Days of Restaurant",
    options= days_value,
    default= days_value
)

times_value = list(df_dashboard["time"].unique())
selected_times = st.sidebar.multiselect(
    label="The Dining Session",
    options = times_value,
    default = times_value
)

sex_value = list(df_dashboard["sex"].unique())
selected_sex = st.sidebar.multiselect(
    label="Genders of Customers",
    options = sex_value,
    default=sex_value
)

smoker_value = list(df_dashboard["smoker"].unique())
selected_smoker = st.sidebar.multiselect(
    label="Smokers of Customers",
    options = smoker_value,
    default=smoker_value
)

size_value = sorted(list(df_dashboard["size"].unique()))
selected_size = st.sidebar.multiselect(
    label="Size of Customers",
    options = size_value,
    default=size_value
)

df_filtered = df_dashboard[
    (df_dashboard["day"].isin(selected_days)) &
    (df_dashboard["time"].isin(selected_times)) &
    (df_dashboard["sex"].isin(selected_sex)) &
    (df_dashboard["smoker"].isin(selected_smoker)) &
    (df_dashboard["size"].isin(selected_size))
]

if df_filtered.empty:
    st.warning("Tidak ada data yang sesuai dengan filter. Silakan pilih minimal satu opsi pada setiap filter.")
    st.stop()

#Membuat Judul Dashboard
st.title("DASHBOARD ANALISIS TIP RESTORAN")
st.caption("Dashboard Latihan Untuk Praktikum 9 Sains Data")

#Membuat KPI
with st.container(border=True, key="bg_kpi"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pendapatan", 
                  f"${df_filtered['pendapatan'].sum():,.0f}")
    with col2:
        st.metric("Rata-Rata Persentase Tip",
                  f"{df_filtered['tip_pct'].mean():.2f}%")
    with col3:
        st.metric("Total Tip",
                  f"${df_filtered['tip'].sum():,.2f}")
    with col4:
        st.metric("Jumlah Transaksi",
                  len(df_filtered))

#Membuat Visualisasi Tengah (Bar Chart)
##Persiapan dataset visualisasi
tagihan_perhari = df_filtered.groupby("day")["total_bill"].sum().reindex(days_value).dropna().reset_index()
tip_pct_perkelompok = df_filtered.groupby(["sex", "smoker"])["tip_pct"].mean().reset_index()
size_rerata_total_bill = df_filtered.groupby("size")["total_bill"].mean().reset_index()

##Membuat visualisasi bar chart
def atur_barchart(fig, ax, label_x, label_y, fmt):
    warna_kartu = "#111A2B"
    warna_teks = "#FFFFFF"
    warna_grid = "#2A3550"
    
    fig.patch.set_facecolor(warna_kartu)
    ax.set_facecolor(warna_kartu)
    ax.set_xlabel(label_x, color=warna_teks)
    ax.set_ylabel(label_y, color=warna_teks)
    ax.tick_params(colors=warna_teks)
    ax.grid(axis="y", color=warna_grid)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color(warna_grid)
        
    for container in ax.containers:
        ax.bar_label(container, fmt=fmt, color=warna_teks, fontsize=10, padding=3)

with st.container(border = True, key = "bg_bar"):
    col1_bar, col2_bar, col3_bar = st.columns(3)
    with col1_bar:
        st.markdown("**Total Tagihan per Hari**")
        fig1, ax1 = plt.subplots()
        sns.barplot(tagihan_perhari, x = "day",
                    y = "total_bill", color = "#2F80FF",
                    ax = ax1)
        atur_barchart(fig1, ax1, "Hari", "Total Tagihan ($)", "${:,.0f}")
        st.pyplot(fig1)
        plt.close(fig1)

    with col2_bar:
        st.markdown("**Rata-Rata Persentase Tip per Gender dan Smoker**")
        fig2, ax2 = plt.subplots()
        sns.barplot(tip_pct_perkelompok, x = "sex", y = "tip_pct",
                    hue = "smoker", palette= {"No": "#005A9C", "Yes": "#60C1E5"}, ax = ax2)
        atur_barchart(fig2, ax2, "Gender", "Persentase Tip (%)", "%.2f%%")
        sns.move_legend(
            ax2, loc = "lower right",title="Smoker", 
            fontsize=10, title_fontsize=12,
            markerscale=1.5, labelspacing=0.8, borderpad=1
            )
        st.pyplot(fig2)
        plt.close(fig2)

    with col3_bar:
        st.markdown("**Size Vs Rata-Rata Total Tagihan**")
        fig3, ax3 = plt.subplots()
        sns.barplot(size_rerata_total_bill, x = "size",
                    y = "total_bill", color = "#118AB2", ax=ax3)
        atur_barchart(fig3, ax3, "Jumlah Orang", 
                      "Rata-Rata Tagihan ($)", "$%.2f")
        st.pyplot(fig3)
        plt.close(fig3)

#Membuat Visualisasi Bawah
##Membuat Visualisasi Scatter plot
col_scatter, col_heatmap = st.columns(2)
def atur_scatter(fig, ax, label_x, label_y):
    warna_kartu = "#111A2B"
    warna_teks = "#FFFFFF"
    warna_grid = "#2A3550"
    
    fig.patch.set_facecolor(warna_kartu)
    ax.set_facecolor(warna_kartu)
    ax.set_xlabel(label_x, color=warna_teks, fontweight="bold")
    ax.set_ylabel(label_y, color=warna_teks, fontweight="bold")
    ax.tick_params(colors=warna_teks)
    ax.grid(axis="y", color=warna_grid)
    ax.grid(axis="x", color=warna_grid)
    ax.set_axisbelow(True)

with col_scatter:
    with st.container(border= True, key = "bg_scatter"):
        st.markdown("**Hubungan Tagihan dan Tip**")
        
        fig4, ax4 = plt.subplots()
        sns.scatterplot(df_filtered, x = "total_bill", y = "tip", ax = ax4, color = "#2F80FF")
        atur_scatter(fig4, ax4, "Total Tagihan", "Tip")
        st.pyplot(fig4)
        plt.close(fig4)

##Membuat Heatmap
heatmap_df_total = pd.crosstab(
    df_filtered["time"], 
    df_filtered["day"]
)

with col_heatmap:
    with st.container(border= True, key = "bg_heatmap"):
        st.markdown("**Jumlah Transaksi per Hari dan Sesi Makan**")
        
        fig5, ax5 = plt.subplots()
        fig5.patch.set_facecolor("#111A2B")
        ax5.set_facecolor("#111A2B")
        sns.heatmap(heatmap_df_total, annot=True,
                    fmt = "d", cmap = "crest_r",
                    linecolor = "#111A2B", linewidths=1.5,
                    ax = ax5)
        ax5.set_xlabel("Day", color="#FFFFFF", fontweight="bold")
        ax5.set_ylabel("Time", color="#FFFFFF", fontweight="bold")
        ax5.tick_params(colors="#FFFFFF")
        st.pyplot(fig5)
        plt.close(fig5)

with st.expander("**Dataset Overview**"):
    st.dataframe(df_filtered, use_container_width=True)