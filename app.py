import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# KONFIGURASI HALAMAN
# Mengatur tampilan dasar website seperti judul tab, ikon, dan layout
# =============================================================================
st.set_page_config(
    page_title="Dashboard DBD Indonesia",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Warna tema yang digunakan di seluruh halaman
PRIMARY, PRIMARY_DARK, PRIMARY_LIGHT = "#0B5FA5", "#073B69", "#E8F1FB"
ACCENT, BG, TEXT_MUTED = "#2E86DE", "#F5F8FB", "#5A6B7B"

# CSS kustom tampilan website
st.markdown(f"""
<style>
    .stApp {{ background-color: {BG}; }}
    html, body, [class*="css"] {{ font-family: 'Segoe UI', 'Inter', sans-serif; }}

    section[data-testid="stSidebar"] {{ background-color: {PRIMARY_DARK}; }}
    section[data-testid="stSidebar"] * {{ color: #EAF2FA !important; }}
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stRadio label {{ font-weight: 600; }}
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background-color: #0F5893; border-color: {PRIMARY};
    }}

    h1 {{ color: {PRIMARY_DARK}; font-weight: 800; letter-spacing: -0.5px; }}
    h2, h3 {{ color: {PRIMARY_DARK}; font-weight: 700; }}

    .hero {{
        background: linear-gradient(135deg, {PRIMARY_DARK} 0%, {PRIMARY} 100%);
        padding: 1.6rem 2rem; border-radius: 12px; color: white;
        margin-bottom: 1.4rem; box-shadow: 0 4px 14px rgba(11,95,165,0.2);
    }}
    .hero h1 {{ color: white !important; margin-bottom: 0.3rem; font-size: 1.7rem; }}
    .hero p {{ color: #DCEBFA; font-size: 1rem; margin: 0; max-width: 780px; line-height: 1.6; }}

    .section-card {{
        background-color: white; border-radius: 12px; padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem; box-shadow: 0 2px 10px rgba(11,95,165,0.07);
        border: 1px solid #E3ECF5;
    }}
    .section-title {{
        display: flex; align-items: center; gap: 0.5rem; color: {PRIMARY_DARK};
        font-size: 1.35rem; font-weight: 700; margin-bottom: 0.9rem;
        border-bottom: 2px solid {PRIMARY_LIGHT}; padding-bottom: 0.5rem;
    }}

    .subcard {{
        background-color: {PRIMARY_LIGHT}; border-radius: 10px; padding: 1rem 1.2rem;
        height: 100%; border: 1px solid #D6E6F7; margin-bottom: 0.5rem;
    }}
    .subcard h4 {{ color: {PRIMARY_DARK}; margin: 0 0 0.5rem 0; font-size: 0.98rem; font-weight: 700; }}
    .subcard p, .subcard li {{ color: {TEXT_MUTED}; font-size: 0.92rem; line-height: 1.6; }}

    .section-card p, .section-card li {{
        font-size: 0.95rem; color: #2C3E50; line-height: 1.75;
    }}

    div[data-testid="stImage"] img {{ border-radius: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }}
    .stCheckbox label, .stRadio label {{ color: {PRIMARY_DARK}; font-weight: 500; }}
    hr {{ margin: 0.5rem 0 1.5rem 0; border-color: #DCE6F0; }}
</style>
""", unsafe_allow_html=True)


# LOAD DATASET
df = pd.read_csv("DBD.csv")
ALL_YEARS = sorted(df["Tahun"].unique())

# =============================================================================
# FUNGSI TAMPILAN (UI HELPERS)
# =============================================================================
def hero(title, subtitle):
    # Menampilkan banner biru di bagian atas setiap halaman
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

# Daftar ikon untuk setiap judul subbab di halaman Home
SECTION_ICONS = {
    "Apa itu DBD?": "📖",
    "Penyebab & Penularan": "🦟",
    "Gejala DBD": "🌡️",
    "Jenis-jenis DBD": "🏥",
    "Pencegahan DBD": "🛡️",
    "Penanganan DBD": "💊",
}

def section_start(title):
    # Membuka card putih dengan judul subbab di dalamnya
    icon = SECTION_ICONS.get(title, "")
    label = f"{icon} {title}" if icon else title
    st.markdown(f'<div class="section-card"><div class="section-title">{label}</div>', unsafe_allow_html=True)

def section_end():
    # Menutup card putih yang dibuka oleh section_start()
    st.markdown('</div>', unsafe_allow_html=True)

def subcard(title, body_html):
    # Membuat kotak biru muda di dalam card, digunakan untuk informasi berdampingan
    st.markdown(f'<div class="subcard"><h4>{title}</h4>{body_html}</div>', unsafe_allow_html=True)

def render_section(sec):
    # Merender satu subbab lengkap: judul, gambar (jika ada), teks, dan kolom (jika ada)
    section_start(sec["title"])
    if sec.get("image"):
        st.image(sec["image"], use_container_width=True)
    if sec.get("text"):
        st.write(sec["text"])
    if sec.get("columns"):
        cols = st.columns(len(sec["columns"]))
        for col, items in zip(cols, sec["columns"]):
            with col:
                for sub_title, sub_html in items:
                    subcard(sub_title, sub_html)
    section_end()

# =============================================================================
# FUNGSI GRAFIK
# =============================================================================
def make_pie(x, y, title):
    # Membuat diagram lingkaran (pie chart)
    # x = label (tahun atau nama provinsi), y = jumlah kasus
    fig, ax = plt.subplots(figsize=(6.6, 4.8), dpi=140)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    if not y or sum(y) == 0:
        ax.text(0.5, 0.5, "Tidak ada data kasus\nuntuk provinsi ini",
                ha="center", va="center", fontsize=9, color="gray", transform=ax.transAxes)
        ax.axis("off")
    else:
        n = len(y)
        colors = plt.cm.Blues([0.35 + 0.5 * i / max(n - 1, 1) for i in range(n)])
        total = sum(y)
        _, texts, autotexts = ax.pie(
            y, labels=[str(v) for v in x],
            autopct=lambda p: f"{p:.1f}%\n({int(round(p * total / 100)):,})",
            startangle=140, pctdistance=0.72, colors=colors,
            wedgeprops=dict(edgecolor="white", linewidth=1.2),
            labeldistance=1.12
        )
        for t in texts: t.set_fontsize(7.5)
        for a in autotexts: a.set_fontsize(6.5); a.set_color("white"); a.set_fontweight("bold")
    ax.set_title(title, fontsize=9.5, fontweight="bold", color=PRIMARY_DARK, pad=14)
    return fig

def make_chart(kind, x, y, title, xlabel="", ylabel="Jumlah Kasus",
               missing_years=None, all_years=None, rotate_xticks=False):
    # Membuat diagram garis atau diagram batang
    # missing_years digunakan untuk memberi shading merah pada tahun tanpa data
    fig, ax = plt.subplots(figsize=(6.6, 3.4), dpi=140)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    if kind == "Diagram Garis":
        # ax.plot membuat garis dengan titik bulat di setiap data
        ax.plot(x, y, marker="o", markersize=4, color=ACCENT, linewidth=1.6, zorder=3, label=ylabel)
        for xi, yi in zip(x, y):
            ax.annotate(f"{int(yi):,}", (xi, yi), textcoords="offset points",
                        xytext=(0, 6), ha="center", fontsize=6.5, color=PRIMARY_DARK)
    else:
        # ax.bar membuat batang vertikal untuk setiap data
        max_val = max(y) if y else 1
        ax.bar(x, y, color=ACCENT, width=0.6, zorder=3, label=ylabel)
        for xi, yi in zip(x, y):
            ax.text(xi, yi + max_val * 0.01, f"{int(yi):,}", ha="center", fontsize=6.5, color=PRIMARY_DARK)

    # Tambahkan shading untuk tahun yang tidak tersedia di dataset
    if missing_years and all_years:
        y_min, y_max = ax.get_ylim()
        if y_max == y_min:
            y_max += 1
            ax.set_ylim(y_min, y_max)
        y_mid = (y_min + y_max) / 2
        for i, year in enumerate(missing_years):
            ax.axvspan(year - 0.45, year + 0.45, color="#f5c6cb", alpha=0.45, zorder=1,
                       label="Data Tidak Tersedia" if i == 0 else "")
            ax.text(year, y_mid, "Data\nTidak\nTersedia", ha="center", va="center",
                    fontsize=6, color="#c0392b", style="italic", zorder=4)
        ax.set_xticks(all_years)
        ax.set_xticklabels([str(v) for v in all_years], fontsize=7.5)
    elif rotate_xticks:
        # Miringkan label sumbu X agar tidak bertumpuk (untuk Top 10 Provinsi)
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    ax.tick_params(axis="both", labelsize=7.5)
    ax.set_xlabel(xlabel, fontsize=8.5)
    ax.set_ylabel(ylabel, fontsize=8.5)
    ax.set_title(title, fontsize=9.5, fontweight="bold", color=PRIMARY_DARK)
    ax.grid(axis="y", linestyle="--", alpha=0.4, color="#D6E6F7", linewidth=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    # Tambahkan legend - filter duplikat label "Data Tidak Tersedia"
    handles, labels = ax.get_legend_handles_labels()
    seen = set()
    final_handles, final_labels = [], []
    for h, l in zip(handles, labels):
        if l not in seen:
            seen.add(l)
            final_handles.append(h)
            final_labels.append(l)
    ax.legend(final_handles, final_labels, frameon=False, fontsize=7)
    return fig

# =============================================================================
# KESIMPULAN OTOMATIS berdasarkan data provinsi yang dipilih
# =============================================================================
def generate_kesimpulan(province, data):
    valid = data[data["Jumlah Kasus"] > 0]
    if valid.empty:
        return f"Provinsi {province} tidak memiliki data kasus DBD yang tercatat."
    tahun = valid["Tahun"].astype(int).tolist()
    kasus = valid["Jumlah Kasus"].astype(int).tolist()
    i_max, i_min = valid["Jumlah Kasus"].idxmax(), valid["Jumlah Kasus"].idxmin()
    rata = sum(kasus) / len(kasus)
    tren = "meningkat" if kasus[-1] > kasus[0] else ("menurun" if kasus[-1] < kasus[0] else "stabil")
    hasil = [
        f"Dari {tahun[0]}–{tahun[-1]}, kasus DBD di {province} {tren} dari {kasus[0]:,} menjadi {kasus[-1]:,} kasus.",
        f"Tertinggi pada {int(valid.at[i_max, 'Tahun'])} ({int(valid.at[i_max, 'Jumlah Kasus']):,} kasus), "
        f"terendah pada {int(valid.at[i_min, 'Tahun'])} ({int(valid.at[i_min, 'Jumlah Kasus']):,} kasus)."
    ]
    if len(kasus) >= 2:
        selisih = kasus[-1] - kasus[-2]
        arah = "meningkat" if selisih > 0 else "menurun"
        hasil.append(f"Pada {tahun[-1]}, kasus {arah} {abs(selisih):,} dibanding {tahun[-2]}.")
    if kasus[-1] > rata * 1.2:
        hasil.append(f"Kasus {tahun[-1]} di atas rata-rata ({int(rata):,}), perlu perhatian lebih.")
    elif kasus[-1] < rata * 0.8:
        hasil.append(f"Kasus {tahun[-1]} di bawah rata-rata ({int(rata):,}), kondisi relatif terkendali.")
    return " ".join(hasil)

# =============================================================================
# KONTEN HALAMAN HOME
# Format: title (judul), image (gambar opsional), text (paragraf), columns (subcard berdampingan)
# =============================================================================
HOME_SECTIONS = [
    {
        "title": "Apa itu DBD?", "image": "nyamuk_dbd.jpg",
        "text": """Demam Berdarah Dengue (DBD) adalah penyakit yang disebabkan oleh virus dengue dan ditularkan melalui gigitan nyamuk Aedes aegypti maupun Aedes albopictus yang telah terinfeksi. Penyakit ini banyak ditemukan di wilayah beriklim tropis dan subtropis, termasuk Indonesia, sehingga masih menjadi salah satu masalah kesehatan yang perlu mendapat perhatian. Jumlah kasus DBD di Indonesia masih cukup tinggi setiap tahunnya dan umumnya mengalami peningkatan pada musim hujan, ketika perkembangbiakan nyamuk menjadi lebih cepat.

DBD dapat menyerang semua kelompok usia, mulai dari anak-anak hingga orang dewasa. Gejala awal yang sering muncul adalah demam tinggi secara tiba-tiba yang dapat disertai sakit kepala, nyeri otot dan sendi, mual, muntah, serta munculnya ruam atau bintik kemerahan pada kulit. Pada beberapa kasus, kondisi penderita dapat berkembang menjadi lebih serius apabila tidak mendapatkan penanganan yang tepat.

Pengenalan terhadap DBD menjadi hal yang penting karena penyakit ini dapat dicegah melalui upaya menjaga kebersihan lingkungan dan mengurangi tempat berkembang biaknya nyamuk. Selain itu, mengenali gejala sejak dini juga dapat membantu memperoleh penanganan yang lebih cepat sehingga risiko terjadinya komplikasi dapat diminimalkan."""
    },
    {
        "title": "Penyebab & Penularan",
        "text": """DBD disebabkan oleh virus dengue yang dibawa oleh nyamuk *Aedes aegypti* sebagai vektor utama. Nyamuk ini aktif menggigit pada pagi dan sore hari, serta berkembang biak di genangan air bersih seperti bak mandi, vas bunga, dan tempat penampungan air lainnya.

Penularan terjadi ketika nyamuk yang terinfeksi virus dengue menggigit manusia sehat. Virus kemudian masuk ke dalam aliran darah dan berkembang biak, sehingga menimbulkan gejala dalam 4–10 hari setelah gigitan. DBD **tidak menular** secara langsung dari satu orang ke orang lain.""",
        "columns": [
            [("Faktor Risiko", "<ul><li>Tinggal atau berkunjung ke daerah endemis DBD</li><li>Lingkungan dengan banyak genangan air</li><li>Musim hujan (November–Mei)</li><li>Kurangnya kesadaran menjaga kebersihan lingkungan</li></ul>")],
            [("Kondisi yang Memperparah", "<ul><li>Infeksi dengue untuk kedua kalinya</li><li>Kondisi imun tubuh yang lemah</li><li>Keterlambatan penanganan medis</li><li>Usia anak-anak dan lansia</li></ul>")],
        ],
    },
    {
        "title": "Gejala DBD",
        "text": "Gejala DBD biasanya muncul 4–10 hari setelah gigitan nyamuk yang terinfeksi dan berlangsung selama 2–7 hari. Gejala dibedakan menjadi tiga fase:",
        "columns": [
            [("Fase Demam (Hari 1–3)", "<ul><li>Demam tinggi mendadak (38–40°C)</li><li>Sakit kepala hebat</li><li>Nyeri di belakang mata</li><li>Nyeri otot dan sendi</li><li>Mual dan muntah</li><li>Ruam kemerahan pada kulit</li></ul>")],
            [("Fase Kritis (Hari 4–5)", "<ul><li>Demam turun namun kondisi memburuk</li><li>Kebocoran plasma darah</li><li>Penurunan trombosit (&lt; 100.000/mm³)</li><li>Nyeri perut hebat</li><li>Muntah terus-menerus</li><li>Perdarahan (mimisan, gusi berdarah)</li></ul>")],
            [("Fase Pemulihan (Hari 6–7)", "<ul><li>Cairan kembali ke pembuluh darah</li><li>Trombosit mulai meningkat</li><li>Nafsu makan membaik</li><li>Kondisi tubuh berangsur pulih</li><li>Ruam dapat muncul kembali</li></ul>")],
        ],
    },
    {
        "title": "Jenis-jenis DBD",
        "text": "Berdasarkan tingkat keparahannya, infeksi dengue dibagi menjadi beberapa klasifikasi:",
        "columns": [
            [
                ("Demam Dengue (DD)", "<p>Bentuk infeksi dengue yang paling ringan. Penderita mengalami demam tinggi disertai sakit kepala, nyeri otot, dan ruam, namun tidak terjadi kebocoran plasma maupun perdarahan yang serius. Kondisi ini biasanya membaik sendiri dalam 7 hari.</p>"),
                ("DBD Derajat III", "<p>Ditandai dengan kegagalan sirkulasi, yaitu nadi yang lemah dan cepat, tekanan darah menurun, serta gelisah. Penderita membutuhkan penanganan medis segera untuk mencegah kondisi memburuk.</p>"),
            ],
            [
                ("DBD Derajat I & II", "<p>Derajat I: Demam disertai gejala umum, uji tourniquet positif, dan trombosit menurun. Derajat II: Gejala lebih berat disertai perdarahan spontan seperti mimisan atau gusi berdarah, serta kebocoran plasma yang mulai terjadi.</p>"),
                ("Sindrom Syok Dengue (SSD)", "<p>Bentuk paling berat dari infeksi dengue. Terjadi syok akibat kebocoran plasma yang masif, tekanan darah sangat rendah, dan dapat mengancam jiwa apabila tidak segera mendapat pertolongan medis.</p>"),
            ],
        ],
    },
    {
        "title": "Pencegahan DBD", "image": "cegah_dbd.jpg",
        "text": "Pencegahan DBD dilakukan melalui gerakan **3M Plus** yang dianjurkan oleh Kementerian Kesehatan RI:",
        "columns": [
            [("3M Plus", "<ul><li><b>Menguras</b> tempat penampungan air secara rutin minimal seminggu sekali</li><li><b>Menutup</b> rapat tempat penampungan air agar nyamuk tidak dapat bertelur</li><li><b>Mendaur ulang</b> atau membuang barang bekas yang dapat menampung air</li><li><b>Plus:</b> Menggunakan lotion anti nyamuk, memasang kelambu, memelihara ikan pemakan jentik</li></ul>")],
            [("Upaya Tambahan", "<ul><li>Melakukan fogging di lingkungan yang berisiko tinggi</li><li>Menaburkan bubuk abate pada tempat penampungan air</li><li>Memakai pakaian lengan panjang saat berada di luar ruangan</li><li>Segera ke dokter apabila muncul gejala demam tinggi mendadak</li></ul>")],
        ],
    },
    {
        "title": "Penanganan DBD", "image": "penanganan.jpg",
        "text": "Hingga saat ini belum ada obat antivirus yang secara khusus dapat membunuh virus dengue. Penanganan DBD bersifat suportif, yaitu bertujuan untuk meredakan gejala dan mencegah komplikasi.",
        "columns": [
            [("Penanganan di Rumah", "<ul><li>Istirahat yang cukup</li><li>Perbanyak minum air putih, jus, atau oralit</li><li>Konsumsi obat penurun demam (parasetamol), <b>hindari aspirin dan ibuprofen</b></li><li>Pantau suhu tubuh dan kondisi secara berkala</li><li>Segera ke rumah sakit jika kondisi memburuk</li></ul>")],
            [("Penanganan Medis", "<ul><li>Pemberian cairan infus untuk mencegah dehidrasi</li><li>Pemantauan kadar trombosit dan hematokrit secara berkala</li><li>Transfusi trombosit jika trombosit sangat rendah (&lt; 10.000/mm³)</li><li>Penanganan intensif di ICU untuk kasus DBD berat atau SSD</li></ul>")],
        ],
    },
]

# =============================================================================
# SIDEBAR - NAVIGASI
# =============================================================================
st.sidebar.markdown("### Menu Navigasi")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "Visualisasi Data", "Top 10 Provinsi"])

# =============================================================================
# HALAMAN HOME
# Menampilkan informasi edukasi tentang DBD secara lengkap
# =============================================================================
if app_mode == "Home":
    hero("Dashboard DBD Indonesia",
         "Selamat datang di website visualisasi data dan edukasi Demam Berdarah Dengue (DBD) di Indonesia. "
         "Website ini menyajikan informasi lengkap seputar DBD serta data kasus dari seluruh provinsi di Indonesia.")

    # Render semua subbab Home secara otomatis dari list HOME_SECTIONS
    for sec in HOME_SECTIONS:
        render_section(sec)

# =============================================================================
# HALAMAN VISUALISASI DATA
# =============================================================================
elif app_mode == "Visualisasi Data":
    hero("Visualisasi DBD di Indonesia", "Eksplorasi tren kasus DBD per provinsi berdasarkan data tahunan.")

    # Pilihan provinsi dan jenis diagram di sidebar
    selected_province = st.sidebar.selectbox("Pilih Provinsi", sorted(df["Provinsi"].unique()))
    chart_type = st.sidebar.radio("Pilih Jenis Diagram", ["Diagram Garis", "Diagram Batang", "Diagram Lingkaran"])

    # Filter data berdasarkan provinsi yang dipilih
    province_data = df[df["Provinsi"] == selected_province].sort_values("Tahun")

    # Cari tahun yang tidak ada datanya untuk provinsi ini
    missing_years = [y for y in ALL_YEARS if y not in province_data["Tahun"].tolist()]

    # Tampilkan grafik
    section_start(f"Grafik Kasus DBD — {selected_province}")
    if missing_years:
        st.info(
            f"**{selected_province}** hanya memiliki data untuk tahun: "
            f"**{', '.join(map(str, province_data['Tahun'].tolist()))}**. "
            f"Tahun **{', '.join(map(str, missing_years))}** tidak tersedia."
        )

    if chart_type == "Diagram Lingkaran":
        pie_data = province_data[province_data["Jumlah Kasus"] > 0]
        total = pie_data["Jumlah Kasus"].sum()
        fig = make_pie(
            pie_data["Tahun"].astype(int).tolist(),
            pie_data["Jumlah Kasus"].tolist(),
            title=f"Proporsi Kasus DBD per Tahun – {selected_province}\n(Total: {total:,} kasus)"
        )
    else:
        fig = make_chart(
            chart_type, province_data["Tahun"].tolist(), province_data["Jumlah Kasus"].tolist(),
            title=f"Kasus DBD – {selected_province}", xlabel="Tahun",
            missing_years=missing_years, all_years=ALL_YEARS
        )
    st.pyplot(fig)
    section_end()

    # Tampilkan kesimpulan otomatis berdasarkan data provinsi
    section_start("Kesimpulan")
    st.write(generate_kesimpulan(selected_province, province_data))
    section_end()

    # Tabel data lengkap (opsional, muncul jika checkbox dicentang)
    section_start("Data Lengkap")
    if st.checkbox("Tampilkan Data Lengkap"):
        st.dataframe(
            province_data[["Tahun", "Provinsi", "Jumlah Penduduk", "Jumlah Kasus", "Jumlah Meninggal"]].reset_index(drop=True),
            use_container_width=True
        )
    section_end()

# =============================================================================
# HALAMAN TOP 10 PROVINSI
# =============================================================================
elif app_mode == "Top 10 Provinsi":
    hero("Top 10 Provinsi Kasus DBD", "Peringkat provinsi dengan jumlah kasus DBD tertinggi berdasarkan tahun yang dipilih.")

    # Pilihan tahun dan jenis diagram di sidebar
    selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(df["Tahun"].unique()))
    chart_type_top = st.sidebar.radio("Pilih Jenis Diagram", ["Diagram Garis", "Diagram Batang", "Diagram Lingkaran"])

    # Filter dan urutkan data, ambil 10 provinsi teratas
    top_10 = df[df["Tahun"] == selected_year].sort_values("Jumlah Kasus", ascending=False).head(10)

    # Tampilkan grafik Top 10
    section_start(f"10 Provinsi Tertinggi — {selected_year}")
    if chart_type_top == "Diagram Lingkaran":
        total = top_10["Jumlah Kasus"].sum()
        fig = make_pie(
            top_10["Provinsi"].tolist(),
            top_10["Jumlah Kasus"].tolist(),
            title=f"10 Provinsi dengan Kasus DBD Tertinggi Tahun {selected_year}\n(Total: {total:,} kasus)"
        )
    else:
        fig = make_chart(
            chart_type_top, top_10["Provinsi"].tolist(), top_10["Jumlah Kasus"].tolist(),
            title=f"10 Provinsi dengan Kasus DBD Tertinggi Tahun {selected_year}",
            rotate_xticks=True
        )
    st.pyplot(fig)
    section_end()

    # Tabel data lengkap Top 10 (opsional, muncul jika checkbox dicentang)
    section_start("Data Lengkap")
    if st.checkbox("Tampilkan Data Lengkap"):
        st.dataframe(
            top_10[["Provinsi", "Jumlah Kasus", "Jumlah Meninggal"]].reset_index(drop=True),
            use_container_width=True
        )
    section_end()