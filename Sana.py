import os
import easyocr
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# 1. Folder Ragaan itti kuufamu uumuu
SAVE_DIR = "Kuusaa_Ragaa"
os.makedirs(SAVE_DIR, exist_ok=True)

# App Configuration
st.set_page_config(
    page_title="TRIAD",
    page_icon="📚",
    layout="wide"
)

# Header & Creator Info
st.title("🏫 TRIAD APP")
st.markdown("### Appii Barattoota Daree Keessatti Dandeetti Sadiin Qoodu")
st.sidebar.info("Designed & Developed by **KN (Kitesa Negasa)**")

# ==========================================
# IDDOO ITTI SUURAA, SEENSA FI KAAYYOO GALCHITU
# ==========================================
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Suura Kalaqaa")

# Suuraa 'qixxeessaa.jpg' jedhu foldera keessaa barbaadee fiduuf
profile_pic_path = "qixxeessaa.jpg"
if os.path.exists(profile_pic_path):
    st.sidebar.image(profile_pic_path, caption="Qixxeessaa Nagaasaa (KN)", use_container_width=True)
else:
    st.sidebar.warning("Suuraan 'qixxeessaa.jpg' jedhu hin argamne. Maaloo foldera koodii kana wajjin jiru keessa kaa'i.")

# Seensa Dhuunfaa Kee
st.sidebar.markdown("### 📝 Seensa  (Introduction)")
st.sidebar.write(
    "Baga Nagaan Gara  TRIAD appilikeeshiniikootti nagaan Dhuftan! Ani barsiisaa Qixxeessaa Nagaasaa Jedhama.Mogaasni maqaa appikoo TRIAD jedhu Afaan Ingiliffaan (Tracking Rates in Academic Development)itti hiikama, "
    "Kunis,Baratoota Dandeetti Sadiin Suuta baratoo,Giddugaleeyyii fi ciccimoo jennee Qabxii isaani gosa barnootan battalleen ykn qormaata giddugaleessaan ykn semisteeran adda baasnee deggeruuf kan tajaajiludha.Appiinkun Kutaalee Gurguddoo kudhan(10) kan of keessaa qabuu fi manneen barnotaa sadarkaa 1ffaa(1-6),sadarkaa giddugaleessaa(7-8) fi sadarkaa 2ffaa(9-12) keessatti tajaajila kennuu kan danda'udha."
)

# Kaayyoo Appii Kanaa
st.sidebar.markdown("### 🎯 Kaayyoo Appichaa (App Objective)")
st.sidebar.write(
    "Kaayyoon Guddaan kalaqa appi kana daree barnootaa keessatti barattoota dandeett isaanitiin adda baasuun deggersa barbaachisaa kennuun qabxii barattoota foyyeessuuf kan kalaqamedha, "
   
)
# ==========================================

# Sidebar - Qajeelfama Itti Fayyadamaa
st.sidebar.markdown("---")
st.sidebar.subheader("📖 Qajeelfama Itti Fayyadamaa Appichaa")
st.sidebar.markdown(
    """
1. **Madda Ragaa:** Faayilii haaraa  kuusaa qabxii ykn roosteera excell qopha'e galchuun fe'uu ykn ragaa kanaan dura kuufame (Saved) jiru galchuu.
2. **Kuusuu (Save):** Faayiliin fe'ame akka kuufamuuf buttoon 'Save' xuquu.
3. **Qindaa'ina:** Column maqaa barataa, koorniyaa, fi gosa barnootaa keessatti argamu filachuu.
4. **Bu'aa Ilaali:** Gosa barnootaan dandeettii barattootaa (Ciccimoo, Giddu-galeeyyii, Suuta baratoo) koorniyaan xiinxalame ilaaluu!
"""
)

# Cache OCR reader to avoid reloading
@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en'])

# Sidebar - Madda Ragaa Filachuu (Upload vs Saved)
st.sidebar.markdown("---")
st.sidebar.subheader("🗄️ Madda Ragaa Filadhu")
madda_ragaa = st.sidebar.radio(
    "Filannoo kee:",
    ["📤 Ragaa Haaraa Fe'uu (Upload)", "📁 Ragaa Kuufame Filachuu (Saved)"]
)

df = None
file_extension = ""
image_to_process = None

# ==========================================
# FILANNOO 1: RAGAA HAARAA FE'UU
# ==========================================
if madda_ragaa == "📤 Ragaa Haaraa Fe'uu (Upload)":
    st.subheader("📂 Step 1: Faayila (Excel/CSV) ykn Suuraa (Image) Fe'i")
    uploaded_file = st.file_uploader(
        "Faayilii qabxii barattootaa ykn suuraa filadhu", 
        type=["csv", "xlsx", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # Save Button (Kuusuuf)
        if st.button("💾 Faayilii Kana Kuusi (Save File)"):
            file_path = os.path.join(SAVE_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Faayiliin '{uploaded_file.name}' milkaa'inaan kuufameera! Gara 'Ragaa Kuufame' tti deemtee argachuu dandeessa.")

        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
            st.success("Faayiliin kee milkaa'inaan fe'ameera!")
        elif file_extension == 'xlsx':
            xls = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Sheet Excel filadhu:", xls.sheet_names)
            skip = st.number_input(
                "Sarara irraa kaafamu (Header Row Index):",
                min_value=0, max_value=10, value=0
            )
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=skip)
            st.success("Faayiliin Excel milkaa'inaan fe'ameera!")
        elif file_extension in ['png', 'jpg', 'jpeg']:
            image_to_process = Image.open(uploaded_file)
            st.image(image_to_process, caption="Suuraa Fe’ame", use_container_width=True)

# ==========================================
# FILANNOO 2: RAGAA KUUFAME BANA
# ==========================================
else:
    st.subheader("📁 Faayiloota Kuufaman (Saved Files)")
    saved_files = os.listdir(SAVE_DIR)
    
    if not saved_files:
        st.info("Kuusaa keessa ragaan tokkoyyuu hin jiru. Maaloo jalqaba ragaa haaraa fe'uun 'Save' godhi.")
    else:
        selected_file = st.selectbox("Faayilii barbaaddu filadhu:", saved_files)
        file_path = os.path.join(SAVE_DIR, selected_file)
        file_extension = selected_file.split('.')[-1].lower()

        # Delete Button (Haquuf)
        if st.button("🗑️ Faayilii Kana Haqi (Delete)"):
            os.remove(file_path)
            st.success(f"Faayiliin '{selected_file}' haqameera!")
            st.rerun()

        # Daataa Dubbisuu
        if os.path.exists(file_path):
            if file_extension == 'csv':
                df = pd.read_csv(file_path)
            elif file_extension == 'xlsx':
                xls = pd.ExcelFile(file_path)
                sheet_name = st.selectbox("Sheet Excel filadhu:", xls.sheet_names)
                skip = st.number_input(
                    "Sarara irraa kaafamu (Header Row Index):",
                    min_value=0, max_value=10, value=0
                )
                df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skip)
            elif file_extension in ['png', 'jpg', 'jpeg']:
                image_to_process = Image.open(file_path)
                st.image(image_to_process, caption="Suuraa Kuufame", use_container_width=True)

# ==========================================
# SUURAA (IMAGE) IRRAA DUBBISUU (OCR)
# ==========================================
if image_to_process is not None:
    st.info("Suuraa irraa barreeffama dubbisuu (OCR) eegalaara... Maaloo xiqqoo turi!")
    with st.spinner("Suuraa irraa daataa baasaa jira..."):
        image_np = np.array(image_to_process)
        reader = load_ocr_reader()
        results = reader.readtext(image_np)
        extracted_texts = [res[1] for res in results]

        if extracted_texts:
            st.success("Daataan suuraa irraa milkaa'inaan dubbifameera!")
            st.write("**Barreeffama Suuraa keessaa argame:**", extracted_texts)
        else:
            st.error("Suuraa kana irraa barreeffama argachuu hin danda’amne.")

# ==========================================
# GAMAAGGAMA FI QOODINSA QABXII (EXCEL/CSV)
# ==========================================
if df is not None:
    # Step 2 & 3: Qindaa'ina kolomanii
    st.subheader("⚙️ Step 2 & 3: Qindaa'ina Kolomanii fi Daataa Waliigalaa")
    all_columns = df.columns.tolist()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        name_col = st.selectbox("Kolomanii Maqaa Barataa qabatee jiru:", all_columns, index=0)
    with col_b:
        gender_col = st.selectbox(
            "Kolonii Saala (Gender) - [Fkn: Dhi/Dha ykn M/F]:",
            all_columns,
            index=1 if len(all_columns) > 1 else 0,
        )
    with col_c:
        subject_cols = st.multiselect(
            "Kolomanii  Gosa Barnootaa qabatee jiru:",
            [col for col in all_columns if col not in [name_col, gender_col]],
        )

    # 📊 Mul'stuu Ragaa fe'ame( Preview) fi Baay'ina Barattoota Waliigalaa (Summary Metrics)
    st.markdown("---")
    st.subheader("👀 Daataa Jalqabaa fi Baay'ina Barattoota Waliigalaa")
    
    # Herrega Baay'ina Dhiiraa fi Dhalaaa waliigalaa (Galmaa'an hunda)
    dhiira_total = len(df[df[gender_col].astype(str).str.contains("Dhi|M", case=False)])
    dhalaa_total = len(df[df[gender_col].astype(str).str.contains("Dha|F", case=False)])
    total_students = dhiira_total + dhalaa_total

    # Metric Cards agarsiisuuf (Waliigala)
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("👥 Waliigala Galmaa'an", f"{total_students}")
    m_col2.metric("👦 Dhiira", f"{dhiira_total}")
    m_col3.metric("👧 Dhalaa", f"{dhalaa_total}")

    st.dataframe(df.head(), use_container_width=True)

    # Quiz Qabxii Gara 100tti jijjiiruu (Scaling option)
    st.markdown("---")
    use_scaling = st.checkbox("xiinxala battallen (Fkn: 10 ykn 20) gara 100tti jijjiiruu (Scale to 100%)")
    max_score_input = 100
    if use_scaling:
        max_score_input = st.number_input(
            "Qabxii Waliigalaa (Maximum Possible Score, fkn: 10, 20, 50):",
            min_value=1,
            value=10,
        )

    if subject_cols and name_col and gender_col:
        st.markdown("---")
        st.subheader("🔍 Step 4: Barbaacha Ragaa barataa Dhuunfaa(search)")

        # Search Bar
        search_query = st.text_input("🔍 Maqaa Barataa Barbaadi (Barbaachaaf asitti barreessi):")

        filtered_main_df = df.copy()
        if search_query:
            filtered_main_df = filtered_main_df[
                filtered_main_df[name_col].astype(str).str.contains(search_query, case=False, na=False)
            ]
            st.info(f"Bu'aa barbaacha barataa: '{search_query}'")
            st.dataframe(filtered_main_df, use_container_width=True, hide_index=True)
            st.markdown("---")

        # Gosa barnootaan qooduu fi koorniyaan ibsuu
        for subj in subject_cols:
            st.markdown(f"### 📖 Gosa Barnootaa: **{subj}**")

            scores = pd.to_numeric(df[subj], errors="coerce")

            if use_scaling and max_score_input > 0:
                scores = (scores / max_score_input) * 100

            temp_df = df.copy()
            temp_df["Calculated_Score"] = scores

            ciccimoo = temp_df[temp_df["Calculated_Score"] >= 80]
            giddu = temp_df[
                (temp_df["Calculated_Score"] >= 50) & (temp_df["Calculated_Score"] < 80)
            ]
            suuta = temp_df[
                (temp_df["Calculated_Score"] < 50) & (temp_df["Calculated_Score"].notna())
            ]
            
            # Barattoota qoraman (Ciccimoo + Giddu-galeeyyii + Suuta barattoota)
            qoraman_df = pd.concat([ciccimoo, giddu galeeyyii, suuta barattoota])
            
            # Barattoota qabxii hin qabne (None / Absent / Missing)
            none_df = temp_df[temp_df["Calculated_Score"].isna()]

            # Baay'ina waligalaa barattoota qoraman (Dhiira + Dhalaa)
            dhiira_qoraman = len(qoraman_df[qoraman_df[gender_col].astype(str).str.contains("Dhi|M", case=False)])
            dhalaa_qoraman = len(qoraman_df[qoraman_df[gender_col].astype(str).str.contains("Dha|F", case=False)])
            waliigala_qoraman = dhiira_qoraman + dhalaa_qoraman

            # Baay'ina barattoota None ta'an
            dhiira_none = len(none_df[none_df[gender_col].astype(str).str.contains("Dhi|M", case=False)])
            dhalaa_none = len(none_df[none_df[gender_col].astype(str).str.contains("Dha|F", case=False)])
            waliigala_none = dhiira_none + dhalaa_none

            # Agarsiisuu Baay'ina Qoraman fi Galmaa'an Gosa Barnoota Kanaan
            st.info(f"📊 **Xiinxala Gosa Barnootaa Kanaa ({subj}):**\n"
                    f"- **Waliigala Barattoota Qoraman:** {waliigala_qoraman} (👦 Dhiira: {dhiira_qoraman} | 👧 Dhalaa: {dhalaa_qoraman})\n"
                    f"- **Barattoota Qabxii Hin Qabne (None/Absent):** {waliigala_none} (👦 Dhiira: {dhiira_none} | 👧 Dhalaa: {dhalaa_none})\n"
                    f"- **Waliigala Galmaa'an (Qoraman + None):** {waliigala_qoraman + waliigala_none}")

            display_cols = list(dict.fromkeys([name_col, gender_col, subj]))

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(label="🌟 Ciccimoo (≥ 80%)", value=f"{len(ciccimoo)} Barattoota")
                if not ciccimoo.empty:
                    dhiira_c = len(ciccimoo[ciccimoo[gender_col].astype(str).str.contains("Dhi|M", case=False)])
                    dhalaa_c = len(ciccimoo[ciccimoo[gender_col].astype(str).str.contains("Dha|F", case=False)])
                    st.caption(f"👥 Dhiira: {dhiira_c} | Dhalaa: {dhalaa_c}")
                    st.dataframe(ciccimoo[display_cols], use_container_width=True, hide_index=True)

            with col2:
                st.metric(label="📊 Giddu-galeeyyii (50-79.9%)", value=f"{len(giddu)} Barattoota")
                if not giddu.empty:
                    dhiira_g = len(giddu[giddu[gender_col].astype(str).str.contains("Dhi|M", case=False)])
                    dhalaa_g = len(giddu[giddu[gender_col].astype(str).str.contains("Dha|F", case=False)])
                    st.caption(f"👥 Dhiira: {dhiira_g} | Dhalaa: {dhalaa_g}")
                    st.dataframe(giddu[display_cols], use_container_width=True, hide_index=True)

            with col3:
                st.metric(label="⚠️ Suuta Baratoo (< 50%)", value=f"{len(suuta)} Baratoo")
                if not suuta.empty:
                    dhiira_s = len(suuta[suuta[gender_col].astype(str).str.contains("Dhi|M", case=False)])
                    dhalaa_s = len(suuta[suuta[gender_col].astype(str).str.contains("Dha|F", case=False)])
                    st.caption(f"👥 Dhiira: {dhiira_s} | Dhalaa: {dhalaa_s}")
                    st.dataframe(suuta[display_cols], use_container_width=True, hide_index=True)

            st.markdown("---")

else:
    st.info("Maaloo jalqabaaf faayilii kee (Excel, CSV) ykn Suuraa (PNG/JPG) fe'i, ykn ragaa kanaan dura kuufame filadhu.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Created with ❤️ by Kitesa Negasa | Educational Analytics App</p>",
    unsafe_allow_html=True,
)
