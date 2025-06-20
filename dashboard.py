import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style="dark")

hospital_df = pd.read_csv('hospital_df.csv', delimiter=';')

with st.sidebar:
    categories = hospital_df["propinsi"].unique()  # Ambil semua kategori unik
    selected_categories = st.selectbox(
        label="Pilih Provinsi",
        options=categories
    )
    categories_kabupaten = hospital_df[hospital_df["propinsi"] == selected_categories]["kab"].unique()

    # Selectbox untuk memilih kabupaten
    selected_kabupaten = st.selectbox(
        label="Pilih Kabupaten",
        options=categories_kabupaten
    )

    main_df = hospital_df[hospital_df["propinsi"] == selected_categories]

    main_df_kab = hospital_df[hospital_df["kab"] == selected_kabupaten]

st.header('Data Rumah Sakit di Indonesia 🏥')

with st.container():
    st.subheader(f"Data Jumlah Rumah sakit di Propinsi {selected_categories}")
    tab1, tab2, tab3, tab4 = st.tabs(["Jenis", "Kelas", "Status Blu","Kepemilikan"])

    with tab1:
        st.write(f"Jumlah Rumah Sakit di {selected_categories} Berdasarkan Jenis")
        byjenis = main_df.groupby(by = 'jenis').size()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=byjenis.values, y=byjenis.index, palette='viridis')

        plt.title('Jumlah Rumah Sakit di Berdasarkan jenis')
        plt.ylabel('jenis')
        plt.xlabel('Jumlah Rumah Sakit')
        st.pyplot(plt)
        with st.expander("Lihat Data"):
            st.dataframe(byjenis)


    with tab2:
        st.write(f"Jumlah Rumah Sakit di {selected_categories} Berdasarkan Kelas")
        byclass = main_df.groupby(by = 'kelas').size()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=byclass.values, y=byclass.index, palette='viridis')

        plt.title('Jumlah Rumah Sakit di Berdasarkan Kelas')
        plt.ylabel('Kelas')
        plt.xlabel('Jumlah Rumah Sakit')
        st.pyplot(plt)
        with st.expander("Lihat Data"):
            st.dataframe(byclass)

    with tab3:
        st.write(f"Jumlah Rumah Sakit di {selected_categories} Berdasarkan Status Blu")
        bystatus = main_df.groupby(by = 'status_blu').size()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=bystatus.values, y=bystatus.index, palette='viridis')

        plt.title('Jumlah Rumah Sakit di Berdasarkan Status BLUD')
        plt.ylabel('Status BLUD')
        plt.xlabel('Jumlah Rumah Sakit')
        st.pyplot(plt)
        st.caption("Insight : ")
        st.caption("BLU (Badan Layanan Umum) adalah unit organisasi pemerintah yang dibentuk untuk memberikan layanan kepada masyarakat dan dikelola dengan prinsip otonomi keuangan.")
        st.caption("BLUD (Badan Layanan Umum Daerah) adalah badan yang mirip dengan BLU, namun dibentuk di tingkat daerah (provinsi atau kabupaten/kota).")
        with st.expander("Lihat Data"):
            st.dataframe(bystatus)

    with tab4:
        st.write(f"Jumlah Rumah Sakit di {selected_categories} Berdasarkan Kepemilikan")
        bypemilik = main_df.groupby(by = 'kepemilikan').size()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=bypemilik.values, y=bypemilik.index, palette='viridis')

        plt.title('Jumlah Rumah Sakit di Berdasarkan Kepemilikan')
        plt.ylabel('Kepemilikan')
        plt.xlabel('Jumlah Rumah Sakit')
        st.pyplot(plt)
        with st.expander("Lihat Data"):
            st.dataframe(bypemilik)

with st.container():
    st.subheader(f"Kabupaten di {selected_categories} dengan jumlah Rumah Sakit Terbanyak dan Tersedikit")
    total_hospital_per_kab = main_df.groupby("kab")["nama"].count().sort_values(ascending=False).reset_index()

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 10))
    colors = ["#F95454", "#9694FF", "#9694FF", "#9694FF", "#9694FF", "#9694FF", "#9694FF"]

    sns.barplot(
        x = "nama",
        y = "kab",
        data = total_hospital_per_kab.head(7),
        palette = colors,
        ax = ax[0]
    )

    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("7 Kabupaten dengan Jumlah Rumah Sakit Terbanyak", loc="center", fontsize=24)
    ax[0].tick_params(axis='y', labelsize=20)
    ax[0].tick_params(axis='x', labelsize=20)

    sns.barplot(
        x = "nama",
        y = "kab",
        data = total_hospital_per_kab.sort_values(by="nama", ascending=True).head(7),
        palette = colors,
        ax = ax[1]
    )

    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("7 Kabupaten dengan Jumlah Rumah Sakit Terendah", loc="center", fontsize=24)
    ax[1].tick_params(axis='y', labelsize=20)
    ax[1].tick_params(axis='x', labelsize=20)

    plt.tight_layout()
    st.pyplot(fig)
    with st.expander("Lihat Data"):
        st.dataframe(total_hospital_per_kab)

with st.container():
    st.subheader(f"Kabupaten di {selected_categories} dengan Total layanan terbanyak dan tersedikit")
    total_layanan_per_kab = main_df.groupby("kab")["total_layanan"].sum().sort_values(ascending=False).reset_index()

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))

    colors = ["#F95454", "#9694FF", "#9694FF", "#9694FF", "#9694FF", "#9694FF", "#9694FF"]

    sns.barplot(x="total_layanan", y="kab", data=total_layanan_per_kab.head(7), palette=colors, ax=ax[0])

    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("7 Kabupaten dengan Total Layanan Terbanyak", loc="center", fontsize=24)
    ax[0].tick_params(axis ='y', labelsize=20)
    ax[0].tick_params(axis ='x', labelsize=20)

    sns.barplot(x="total_layanan", y="kab", data=total_layanan_per_kab.sort_values(by="total_layanan", ascending=True).head(7),
                palette=colors, ax=ax[1])

    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("7 Kabupaten dengan Total Layanan Terendah", loc="center", fontsize=24)
    ax[1].tick_params(axis ='y', labelsize=20)
    ax[1].tick_params(axis ='x', labelsize=20)

    plt.tight_layout()
    st.pyplot(fig)
    with st.expander("Lihat Data"):
        st.dataframe(total_layanan_per_kab)

with st.container():
    st.subheader(f"Kabupaten di {selected_categories} dengan Total Tempat Tidur terbanyak dan tersedikit")
    total_tempat_tidur_per_kab = main_df.groupby("kab")["total_tempat_tidur"].sum().sort_values(ascending=False).reset_index()

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))

    colors = ["#F95454", "#9694FF", "#9694FF", "#9694FF", "#9694FF", "#9694FF", "#9694FF"]

    sns.barplot(x="total_tempat_tidur", y="kab", data=total_tempat_tidur_per_kab.head(7), palette=colors, ax=ax[0])

    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("7 Kabupaten dengan Total tempat_tidur Terbanyak", loc="center", fontsize=24)
    ax[0].tick_params(axis ='y', labelsize=20)
    ax[0].tick_params(axis ='x', labelsize=20)

    sns.barplot(x="total_tempat_tidur", y="kab", data=total_tempat_tidur_per_kab.sort_values(by="total_tempat_tidur", ascending=True).head(7),
                palette=colors, ax=ax[1])

    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("7 Kabupaten dengan Total tempat_tidur Terendah", loc="center", fontsize=24)
    ax[1].tick_params(axis ='y', labelsize=20)
    ax[1].tick_params(axis ='x', labelsize=20)

    plt.tight_layout()
    st.pyplot(fig)
    with st.expander("Lihat Data"):
        st.dataframe(total_tempat_tidur_per_kab)

with st.container():
    st.subheader("Apakah status BLU memengaruhi jumlah tenaga kerja, Total Layanan, total tempat tidur?")
    tab1, tab2, tab3 = st.tabs(["Tenaga Kerja", "Tempat Tidur", "Total Layanan"])

    with tab1:
        st.write(f"Apakah status BLU memengaruhi Total Tenaga Kerja di {selected_categories}")
        total_tenaga_kerja_for_status_blu = main_df.groupby("status_blu")["total_tenaga_kerja"].sum().sort_values(ascending=False).reset_index()

        fig, ax = plt.subplots(figsize=(20, 10))

        colors = ["#EBEAFF", "#EBEAFF", "#3D3BF3"]

        sns.barplot(x="status_blu", y="total_tenaga_kerja", data=total_tenaga_kerja_for_status_blu, palette=colors)
            
        ax.set_title("Jumlah Tenaga Kerja Berdasarkan Status BLU", loc="center", fontsize=24)
        ax.set_ylabel("Status BLU", loc="center", fontsize=20)
        ax.set_xlabel("Total Tenaga Kerja", loc="center", fontsize=20)
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=15)
        st.pyplot(fig)
        with st.expander("Lihat Data"):
            st.dataframe(total_tenaga_kerja_for_status_blu)
        
    with tab2:
        st.write(f"Apakah status BLU memengaruhi Total Tempat Tidur di {selected_categories}")
        total_tempat_tidur_for_status_blu = main_df.groupby("status_blu")["total_tempat_tidur"].sum().sort_values(ascending=False).reset_index()

        fig, ax = plt.subplots(figsize=(20, 10))

        colors = ["#EBEAFF", "#EBEAFF", "#3D3BF3"]

        sns.barplot(x="status_blu", y="total_tempat_tidur", data=total_tempat_tidur_for_status_blu, palette=colors)

        ax.set_title("Jumlah Tempat Tidur Berdasarkan Status BLU", loc="center", fontsize=24)
        ax.set_xlabel("Status BLU", loc="center", fontsize=20)
        ax.set_ylabel("Total Tempat Tidur", loc="center", fontsize=20)
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=15)
        st.pyplot(fig)
        with st.expander("Lihat Data"):
            st.dataframe(total_tempat_tidur_for_status_blu)

    with tab3:
        st.write(f"Apakah status BLU memengaruhi Total Layanan di {selected_categories}")
        total_layanan_for_status_blu = main_df.groupby("status_blu")["total_layanan"].sum().sort_values(ascending=False).reset_index()

        fig, ax = plt.subplots(figsize=(20, 10))

        colors = ["#EBEAFF", "#EBEAFF", "#3D3BF3"]

        sns.barplot(x="status_blu", y="total_layanan", data=total_layanan_for_status_blu, palette=colors)

        ax.set_title("Jumlah Total Layanan Berdasarkan Status BLU", loc="center", fontsize=24)
        ax.set_xlabel("Status BLU", loc="center", fontsize=20)
        ax.set_ylabel("Total Total Layanan", loc="center", fontsize=20)
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=15)
        st.pyplot(fig)
        with st.expander("Lihat Data"):
            st.dataframe(total_layanan_for_status_blu)

with st.container():
    st.subheader("Apakah status kelas memengaruhi jumlah tenaga kerja, Total Layanan, total tempat tidur?")
    tab1, tab2, tab3 = st.tabs(["Tenaga Kerja", "Tempat Tidur", "Total Layanan"])

    with tab1:
        st.write(f"Apakah status kelas memengaruhi Total Tenaga Kerja di {selected_categories}")
        total_tenaga_kerja_for_kelas = main_df.groupby("kelas")["total_tenaga_kerja"].sum().sort_values(ascending=False).reset_index()

        fig, ax = plt.subplots(figsize=(20, 10))

        colors = ["#3D3BF3", "#EBEAFF", "#EBEAFF", "#EBEAFF","#EBEAFF","#EBEAFF","#EBEAFF"]

        sns.barplot(x="kelas", y="total_tenaga_kerja", data=total_tenaga_kerja_for_kelas, palette=colors)
            
        ax.set_title("Jumlah Tenaga Kerja Berdasarkan Status kelas", loc="center", fontsize=24)
        ax.set_ylabel("Status kelas", loc="center", fontsize=20)
        ax.set_xlabel("Total Tenaga Kerja", loc="center", fontsize=20)
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=15)
        st.pyplot(fig)
        with st.expander("Lihat Data"):
            st.dataframe(total_tenaga_kerja_for_kelas)
        
    with tab2:
        st.write(f"Apakah status kelas memengaruhi Total Tempat Tidur di {selected_categories}")
        total_tempat_tidur_for_kelas = main_df.groupby("kelas")["total_tempat_tidur"].sum().sort_values(ascending=False).reset_index()

        fig, ax = plt.subplots(figsize=(20, 10))

        colors = ["#3D3BF3", "#EBEAFF", "#EBEAFF", "#EBEAFF","#EBEAFF","#EBEAFF","#EBEAFF"]

        sns.barplot(x="kelas", y="total_tempat_tidur", data=total_tempat_tidur_for_kelas, palette=colors)

        ax.set_title("Jumlah Tempat Tidur Berdasarkan Status kelas", loc="center", fontsize=24)
        ax.set_xlabel("Status kelas", loc="center", fontsize=20)
        ax.set_ylabel("Total Tempat Tidur", loc="center", fontsize=20)
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=15)
        st.pyplot(fig)
        with st.expander("Lihat Data"):
            st.dataframe(total_tempat_tidur_for_kelas)

    with tab3:
        st.write(f"Apakah status kelas memengaruhi Total Layanan di {selected_categories}")
        total_layanan_for_kelas = main_df.groupby("kelas")["total_layanan"].sum().sort_values(ascending=False).reset_index()

        fig, ax = plt.subplots(figsize=(20, 10))

        colors = ["#3D3BF3", "#EBEAFF", "#EBEAFF", "#EBEAFF","#EBEAFF","#EBEAFF","#EBEAFF"]

        sns.barplot(x="kelas", y="total_layanan", data=total_layanan_for_kelas, palette=colors)

        ax.set_title("Jumlah Total Layanan Berdasarkan Status kelas", loc="center", fontsize=24)
        ax.set_xlabel("Status kelas", loc="center", fontsize=20)
        ax.set_ylabel("Total Total Layanan", loc="center", fontsize=20)
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=15)
        st.pyplot(fig)
        with st.expander("Lihat Data"):
            st.dataframe(total_layanan_for_kelas)

with st.container():
    st.subheader(f"Data Jumlah Rumah sakit di Propinsi {selected_categories} Kabupaten {selected_kabupaten}")

    main_df_kab_total = main_df_kab.groupby(['nama']).agg({
    'total_tempat_tidur': 'sum',
    'total_layanan': 'sum',
    'total_tenaga_kerja': 'sum'
    }).reset_index()
    main_df_kab_total['Total'] = main_df_kab_total[["total_tempat_tidur", "total_layanan", "total_tenaga_kerja"]].sum(axis=1)
    main_df_kab_total.sort_values(by='Total', ascending=True, inplace=True)
    main_df_kab_total = main_df_kab_total.reset_index(drop=True)
    
    # Membuat horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot horizontal bar chart
    ax.barh(main_df_kab_total["nama"], main_df_kab_total["total_tempat_tidur"], label="Tempat Tidur", color="skyblue")
    ax.barh(main_df_kab_total["nama"], main_df_kab_total["total_layanan"], label="Layanan", color="lightgreen", left=main_df_kab_total["total_tempat_tidur"])
    ax.barh(main_df_kab_total["nama"], main_df_kab_total["total_tenaga_kerja"], label="Tenaga Kerja", color="salmon", 
            left=main_df_kab_total["total_tempat_tidur"] + main_df_kab_total["total_layanan"])

    # Menambahkan label dan judul
    ax.set_title("Agregasi Rumah Sakit Berdasarkan nama (Horizontal)", fontsize=16)
    ax.set_xlabel("Total", fontsize=12)
    ax.set_ylabel("Nama Rumah Sakit", fontsize=12)
    ax.legend()

    plt.tight_layout()
    st.pyplot(fig)
    with st.expander("Lihat Data"):
        st.dataframe(main_df_kab_total)

with st.container():
    st.subheader(f"Data Jumlah Rumah sakit di Propinsi {selected_categories} kabupaten {selected_kabupaten}")
    tab1, tab2, tab3, tab4 = st.tabs(["Jenis", "Kelas", "Status Blu","Kepemilikan"])

    with tab1:
        st.write(f"Jumlah Rumah Sakit di {selected_kabupaten} Berdasarkan Jenis")
        byjenis_kab = main_df_kab.groupby(by = 'jenis').size()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=byjenis_kab.values, y=byjenis_kab.index, palette='viridis')

        plt.title('Jumlah Rumah Sakit di Berdasarkan jenis')
        plt.ylabel('jenis')
        plt.xlabel('Jumlah Rumah Sakit')
        st.pyplot(plt)
        with st.expander("Lihat Data"):
            st.dataframe(byjenis_kab)


    with tab2:
        st.write(f"Jumlah Rumah Sakit di {selected_kabupaten} Berdasarkan Kelas")
        byclass_kab = main_df_kab.groupby(by = 'kelas').size()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=byclass_kab.values, y=byclass_kab.index, palette='viridis')

        plt.title('Jumlah Rumah Sakit di Berdasarkan Kelas')
        plt.ylabel('Kelas')
        plt.xlabel('Jumlah Rumah Sakit')
        st.pyplot(plt)
        with st.expander("Lihat Data"):
            st.dataframe(byclass_kab)

    with tab3:
        st.write(f"Jumlah Rumah Sakit di {selected_kabupaten} Berdasarkan Status Blu")
        bystatus_kab = main_df_kab.groupby(by = 'status_blu').size()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=bystatus_kab.values, y=bystatus_kab.index, palette='viridis')

        plt.title('Jumlah Rumah Sakit di Berdasarkan Status BLUD')
        plt.ylabel('Status BLUD')
        plt.xlabel('Jumlah Rumah Sakit')
        st.pyplot(plt)
        st.caption("Insight : ")
        st.caption("BLU (Badan Layanan Umum) adalah unit organisasi pemerintah yang dibentuk untuk memberikan layanan kepada masyarakat dan dikelola dengan prinsip otonomi keuangan.")
        st.caption("BLUD (Badan Layanan Umum Daerah) adalah badan yang mirip dengan BLU, namun dibentuk di tingkat daerah (provinsi atau kabupaten/kota).")
        with st.expander("Lihat Data"):
            st.dataframe(bystatus_kab)

    with tab4:
        st.write(f"Jumlah Rumah Sakit di {selected_kabupaten} Berdasarkan Kepemilikan")
        bypemilik_kab = main_df_kab.groupby(by = 'kepemilikan').size()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=bypemilik_kab.values, y=bypemilik_kab.index, palette='viridis')

        plt.title('Jumlah Rumah Sakit di Berdasarkan Kepemilikan')
        plt.ylabel('Kepemilikan')
        plt.xlabel('Jumlah Rumah Sakit')
        st.pyplot(plt)
        with st.expander("Lihat Data"):
            st.dataframe(bypemilik_kab)

st.caption('Copyright (c) Kelompok 10')
st.caption('Muhammad Habib Nur Aiman')
st.caption('M. Habiburrohman Al-Fathir')
st.caption('Rabbani Yuki Arfiansyach')


