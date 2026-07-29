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
            
            qoraman_df = pd.concat([ciccimoo, giddu, suuta])
            none_df = temp_df[temp_df["Calculated_Score"].isna()]

            dhiira_qoraman = len(qoraman_df[qoraman_df[gender_col].astype(str).str.contains("Dhi|M", case=False)])
            dhalaa_qoraman = len(qoraman_df[qoraman_df[gender_col].astype(str).str.contains("Dha|F", case=False)])
            waliigala_qoraman = dhiira_qoraman + dhalaa_qoraman

            dhiira_none = len(none_df[none_df[gender_col].astype(str).str.contains("Dhi|M", case=False)])
            dhalaa_none = len(none_df[none_df[gender_col].astype(str).str.contains("Dha|F", case=False)])
            waliigala_none = dhiira_none + dhalaa_none

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
                st.metric(label="⚠️ Suuta Barattoota (< 50%)", value=f"{len(suuta)} Barattoota")
                if not suuta.empty:
                    dhiira_s = len(suuta[suuta[gender_col].astype(str).str.contains("Dhi|M", case=False)])
                    dhalaa_s = len(suuta[suuta[gender_col].astype(str).str.contains("Dha|F", case=False)])
                    st.caption(f"👥 Dhiira: {dhiira_s} | Dhalaa: {dhalaa_s}")
                    st.dataframe(suuta[display_cols], use_container_width=True, hide_index=True)

            st.markdown(f"### 🖨️ Barattoota Gosa Barnootaa **{subj}** Maxansiisuuf (Print)")
            
            print_category = st.selectbox(
                f"Gita dandeettii isaanii filadhu ({subj}):",
                ["Ciccimoo (≥ 80%)", "Giddu-galeeyyii (50-79.9%)", "Suuta Barattoota (< 50%)", "Waliigala Qoraman Hunda"],
                key=f"print_select_{subj}"
            )

            if print_category == "Ciccimoo (≥ 80%)":
                export_df = ciccimoo[display_cols]
                title_text = f"Barattoota Ciccimoo Gosa Barnootaa {subj}"
            elif print_category == "Giddu-galeeyyii (50-79.9%)":
                export_df = giddu[display_cols]
                title_text = f"Barattoota Giddu-galeeyyii Gosa Barnootaa {subj}"
            elif print_category == "Suuta Barattoota (< 50%)":
                export_df = suuta[display_cols]
                title_text = f"Suuta Barattoota Gosa Barnootaa {subj}"
            else:
                export_df = qoraman_df[display_cols]
                title_text = f"Barattoota Qoraman Hunda Gosa Barnootaa {subj}"

            if not export_df.empty:
                csv_data = export_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"📥 Faayilii {print_category} Buusuu (Download CSV)",
                    data=csv_data,
                    file_name=f"{subj}_{print_category.split()[0]}_barattoota.csv",
                    mime="text/csv",
                    key=f"download_{subj}"
                )

                html_table = export_df.to_html(classes='table table-striped', index=False)
                print_html = f"""
                <html>
                <head>
                    <title>{title_text}</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        h2 {{ text-align: center; color: #333; }}
                        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                        th {{ background-color: #f2f2f2; }}
                    </style>
                </head>
                <body>
                    <h2>🏫 TRIAD APP - {title_text}</h2>
                    {html_table}
                    <script>
                        window.onload = function() {{ window.print(); }}
                    </script>
                </body>
                </html>
                """
                
                st.components.v1.html(
                    f"""
                    <script>
                    function printContent() {{
                        var myWindow = window.open('', '', 'height=600,width=800');
                        myWindow.document.write(`{print_html}`);
                        myWindow.document.close();
                        myWindow.focus();
                    }}
                    </script>
                    <button onclick="printContent()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">
                        🖨️ Kallattiin Print Godhuu (Direct Print)
                    </button>
                    """,
                    height=50
                )
            else:
                st.warning(f"Ragaan ramaddii kanaaf argame hin jiru.")

            st.markdown("---")

    # ==========================================
    # KAARDII BARATAA QOPHEESSUU (STUDENT ID CARD)
    # ==========================================
    st.markdown("---")
    st.subheader("🪪 Kaardii Barataa Qopheessuu (Student ID Card Generator)")
    
    student_list = df[name_col].unique().tolist() if name_col in df.columns else []
    if student_list:
        selected_student = st.selectbox("Barataa Kaardii isaaf qopheessuuf barbaaddu filadhu:", student_list)
        
        if selected_student:
            student_data = df[df[name_col] == selected_student].iloc[0]
            s_name = student_data[name_col]
            s_gender = student_data[gender_col] if gender_col in df.columns else "N/A"
            
            # Kaardii HTML Template
            card_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    .card {{
                        width: 350px;
                        border: 2px solid #2e7d32;
                        border-radius: 12px;
                        padding: 20px;
                        font-family: Arial, sans-serif;
                        background: #ffffff;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                        text-align: center;
                        margin: auto;
                    }}
                    .school-title {{
                        font-size: 18px;
                        font-weight: bold;
                        color: #1b5e20;
                    }}
                    .card-header {{
                        font-size: 13px;
                        color: #555;
                        margin-bottom: 10px;
                    }}
                    .student-info {{
                        text-align: left;
                        font-size: 15px;
                        margin: 10px 0;
                        padding: 5px;
                        background: #f1f8e9;
                        border-radius: 4px;
                    }}
                    .footer {{
                        margin-top: 15px;
                        font-size: 11px;
                        color: #777;
                        border-top: 1px solid #ddd;
                        padding-top: 8px;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="school-title">🏫 TRIAD APP SCHOOL</div>
                    <div class="card-header">Kaardii Eenyummaa Barataa (Student ID Card)</div>
                    <hr>
                    <div class="student-info"><b>Maqaa:</b> {s_name}</div>
                    <div class="student-info"><b>Saala:</b> {s_gender}</div>
                    <div class="student-info"><b>Daree:</b> Barataa/tuu Qormaataa</div>
                    <div class="footer">Designed & Developed by Kitesa Negasa</div>
                </div>
            </body>
            </html>
            """
            
            # Agarsiisuu Kaardichaa
            st.components.v1.html(card_html, height=260)
            
            # Download Button for Student Card
            st.download_button(
                label=f"📥 Kaardii {s_name} Buusuu (Download Card HTML)",
                data=card_html.encode('utf-8'),
                file_name=f"Kaardii_{s_name}.html",
                mime="text/html"
            )
else:
    st.info("Maaloo jalqabaaf faayilii kee (Excel, CSV) ykn Suuraa (PNG/JPG) fe'i, ykn ragaa kanaan dura kuufame filadhu.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Created with ❤️ by Kitesa Negasa | Educational Analytics App</p>",
    unsafe_allow_html=True,
)
