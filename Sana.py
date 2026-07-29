import os
import easyocr
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import base64

# 1. Folder Ragaan itti kuufamu uumuu
SAVE_DIR = "Kuusaa_Ragaa"
os.makedirs(SAVE_DIR, exist_ok=True)

# App Configuration & Modern Styling
st.set_page_config(
    page_title="TRIAD Analytics Dashboard",
    page_icon="📚",
    layout="wide"
)

# Modern CSS Injection (Fonts, Colors, Borders, Shadows)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Cover Page Styling */
    .cover-container {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #4caf50 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 30px;
    }
    
    /* Modern Card Container */
    .stCard {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    h1, h2, h3 {
        color: #1b5e20;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Cover Page Navigation
if 'entered_app' not in st.session_state:
    st.session_state.entered_app = False

# ==========================================
# COVER PAGE (FUULA DURAA AMMAYYAA)
# ==========================================
if not st.session_state.entered_app:
    st.markdown("""
        <div class="cover-container">
            <h1>🏫 TRIAD ANALYTICS SYSTEM</h1>
            <h3>Appii Barattoota Daree Keessatti Dandeetti Sadiin Qoodu</h3>
            <p style="font-size: 16px; max-width: 700px; margin: auto; line-height: 1.6;">
                Baga Nagaan Gara TRIAD appilikeeshinii kootti nagaan Dhuftan! Mogaasni maqaa appikoo TRIAD jedhama.Hiikni TRIAD: 
                Afaan Ingiliffaan <b>(Tracking Rates in Academic Development)</b> jechuudha. Barattoota dandeettii 
                isaaniitiin adda baasuun deggersa barbaachisaa kennuuf kan qopha'edha.
            </p>
            <br>
            <p style="font-size: 14px; opacity: 0.9;">Designed & Developed by <b>Kitesa Negasa Feyisa</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    col_cov1, col_cov2, col_cov3 = st.columns([1, 2, 1])
    with col_cov2:
        if st.button("🚀 Gara Appii kanaa Seenuuf (Enter Dashboard)", use_container_width=True, key="enter_app_main_button"):
            st.session_state.entered_app = True
            st.rerun()
    st.stop()

# Header & Creator Info inside App
st.title("🏫 TRIAD APP DASHBOARD")
st.markdown("### Appii Barattoota Daree Keessatti Dandeetti Sadiin Qoodu")
st.sidebar.info("Designed & Developed by **KN (Kitesa Negasa)**")

if st.sidebar.button("🏠 Fuula Duraa (Cover Page) Deebi'uu", key="sidebar_back_cover_btn"):
    st.session_state.entered_app = False
    st.rerun()

# ==========================================
# IDDOO ITTI SUURAA, SEENSA FI KAAYYOO GALCHITU
# ==========================================
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Suura Kalaqaa")

profile_pic_path = "qixxeessaa.jpg"
if os.path.exists(profile_pic_path):
    st.sidebar.image(profile_pic_path, caption="Qixxeessaa Nagaasaa (KN)", use_container_width=True)
else:
    st.sidebar.warning("Suuraan 'qixxeessaa.jpg' jedhu hin argamne.")

st.sidebar.markdown("### 📝 Seensa (Introduction)")
st.sidebar.write(
    "Barnoonni bu'uura misoomaa fi guddina hawaasaati. Sadarkaa amma irra jirruutti, saffisi fi qulqullinni barnootaa akka fooyya’uuf tooftaa ammayyaa’aa fayyadamuun dirqama ta’a. Akkaataa kanaan, rakkoolee qormaataa fi madaallii barattootaa keessatti mul’atan hiikuuf, akkasumas barsiisotaaf qorannoo dandeettii saffisaa (Diagnostic Assessment) kennuuf appilikeeshinii haaraa maqaan isaa TRIAD (Tracking Rates In Academic Development) jedhamu qopheesseera. Appiin kun sadarkaa mana barumsaa Aanaa Meettaa Walqixxeetti qulqullina barnootaa mirkaneessuuf shoora olaanaa qaba., "
    "sadarkaa giddugaleessaa(7-8) fi sadarkaa 2ffaa(9-12) keessatti tajaajila kennuu kan danda'udha."
)

st.sidebar.markdown("### 🎯 Kaayyoo Appichaa")
st.sidebar.write(
    "Kaayyoon Guddaan kalaqa appi kana daree barnootaa keessatti barattoota dandeettii isaanitiin adda baasuun "
    "deggersa barbaachisaa kennuun qabxii barattoota foyyeessuuf kan kalaqamedha."
)

st.sidebar.markdown("---")
st.sidebar.subheader("📖 Qajeelfama Itti Fayyadamaa")
st.sidebar.markdown(
    """
1. **Madda Ragaa:** Faayilii haaraa ykn ragaa kuufame filachuu.
2. **Kuusuu (Save):** Faayiliin fe'ame akka kuufamuuf buttoon 'Save' xuquu.
3. **Qindaa'ina:** Column maqaa, koorniyaa, fi gosa barnootaa filachuu.
4. **Bu'aa Ilaali:** Dandeettii barattootaa fi xiinxala guutuu ilaali!
"""
)

@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en'])

st.sidebar.markdown("---")
st.sidebar.subheader("🗄️ Madda Ragaa Filadhu")
madda_ragaa = st.sidebar.radio(
    "Filannoo kee:",
    ["📤 Ragaa Haaraa Fe'uu (Upload)", "📁 Ragaa Kuufame Filachuu (Saved)"],
    key="madda_ragaa_radio"
)

df = None
file_extension = ""
image_to_process = None

if madda_ragaa == "📤 Ragaa Haaraa Fe'uu (Upload)":
    st.subheader("📂 Step 1: Faayila (Excel/CSV) ykn Suuraa (Image) Fe'i")
    uploaded_file = st.file_uploader(
        "Faayilii qabxii barattootaa ykn suuraa filadhu", 
        type=["csv", "xlsx", "png", "jpg", "jpeg"],
        key="file_uploader_main"
    )

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if st.button("💾 Faayilii Kana Kuusi (Save File)", key="save_uploaded_file_btn"):
            file_path = os.path.join(SAVE_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Faayiliin '{uploaded_file.name}' milkaa'inaan kuufameera!")

        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
            st.success("Faayiliin kee milkaa'inaan fe'ameera!")
        elif file_extension == 'xlsx':
            xls = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Sheet Excel filadhu:", xls.sheet_names, key="excel_sheet_upload")
            skip = st.number_input("Sarara irraa kaafamu (Header Row Index):", min_value=0, max_value=10, value=0, key="skip_rows_upload")
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=skip)
            st.success("Faayiliin Excel milkaa'inaan fe'ameera!")
        elif file_extension in ['png', 'jpg', 'jpeg']:
            image_to_process = Image.open(uploaded_file)
            st.image(image_to_process, caption="Suuraa Fe’ame", use_container_width=True)

else:
    st.subheader("📁 Faayiloota Kuufaman (Saved Files)")
    saved_files = os.listdir(SAVE_DIR)
    
    if not saved_files:
        st.info("Kuusaa keessa ragaan tokkoyyuu hin jiru.")
    else:
        selected_file = st.selectbox("Faayilii barbaaddu filadhu:", saved_files, key="select_saved_file_dropdown")
        file_path = os.path.join(SAVE_DIR, selected_file)
        file_extension = selected_file.split('.')[-1].lower()

        if st.button("🗑️ Faayilii Kana Haqi (Delete)", key="delete_saved_file_btn"):
            os.remove(file_path)
            st.success(f"Faayiliin '{selected_file}' haqameera!")
            st.rerun()

        if os.path.exists(file_path):
            if file_extension == 'csv':
                df = pd.read_csv(file_path)
            elif file_extension == 'xlsx':
                xls = pd.ExcelFile(file_path)
                sheet_name = st.selectbox("Sheet Excel filadhu:", xls.sheet_names, key="excel_sheet_saved")
                skip = st.number_input("Sarara irraa kaafamu (Header Row Index):", min_value=0, max_value=10, value=0, key="skip_rows_saved")
                df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skip)
            elif file_extension in ['png', 'jpg', 'jpeg']:
                image_to_process = Image.open(file_path)
                st.image(image_to_process, caption="Suuraa Kuufame", use_container_width=True)

if image_to_process is not None:
    st.info("Suuraa irraa barreeffama dubbisuu (OCR) eegalaara...")
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

if df is not None:
    st.subheader("⚙️ Step 2 & 3: Qindaa'ina Kolomanii fi Daataa Waliigalaa")
    all_columns = df.columns.tolist()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        name_col = st.selectbox("Kolomanii Maqaa Barataa:", all_columns, index=0, key="col_name_select")
    with col_b:
        gender_col = st.selectbox("Kolonii Saala (Gender):", all_columns, index=1 if len(all_columns) > 1 else 0, key="col_gender_select")
    with col_c:
        subject_cols = st.multiselect("Kolomanii Gosa Barnootaa:", [col for col in all_columns if col not in [name_col, gender_col]], key="col_subjects_multiselect")

    # Lakk. Eenyummaa, Kutaa, fi Daree (Kutaa fi Daree Excel irraa dubbisuu dhiisee iddoo Lakk ID cinaatti akka barreessitu qindaa'e)
    st.markdown("##### Qindaa'ina Lakk. Eenyummaa, Kutaa fi Daree Barataa")
    col_id_1, col_id_2, col_id_3 = st.columns(3)
    with col_id_1:
        id_num_col = st.selectbox("Kolomanii Lakk. Eenyummaa/Roll (ID):", ["Hin jiru"] + all_columns, key="col_id_select")
    with col_id_2:
        manual_grade = st.text_input("Kutaa (Grade) Galchi:", value="", placeholder="Fkn: 9", key="manual_grade_input")
    with col_id_3:
        manual_section = st.text_input("Daree (Section) Galchi:", value="", placeholder="Fkn: A", key="manual_section_input")

    st.markdown("---")
    st.subheader("👀 Daataa Jalqabaa fi Baay'ina Barattoota Waliigalaa")
    
    dhiira_total = len(df[df[gender_col].astype(str).str.contains("Dhi|M", case=False)])
    dhalaa_total = len(df[df[gender_col].astype(str).str.contains("Dha|F", case=False)])
    total_students = dhiira_total + dhalaa_total

    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("👥 Waliigala Galmaa'an", f"{total_students}")
    m_col2.metric("👦 Dhiira", f"{dhiira_total}")
    m_col3.metric("👧 Dhalaa", f"{dhalaa_total}")

    st.dataframe(df.head(), use_container_width=True)

    st.markdown("---")
    use_scaling = st.checkbox("xiinxala battallen gara 100tti jijjiiruu (Scale to 100%)", key="use_scaling_checkbox")
    max_score_input = 100
    if use_scaling:
        max_score_input = st.number_input("Qabxii Waliigalaa (Maximum Possible Score):", min_value=1, value=10, key="max_score_input_val")

    if subject_cols and name_col and gender_col:
        st.markdown("---")
        st.subheader("🔍 Step 4: Barbaacha Ragaa Barataa Dhuunfaa fi Xiinxala Gosa Barnootaa")

        search_query = st.text_input("🔍 Maqaa Barataa Barbaadi:", key="search_student_text_input")

        filtered_main_df = df.copy()
        if search_query:
            filtered_main_df = filtered_main_df[
                filtered_main_df[name_col].astype(str).str.contains(search_query, case=False, na=False)
            ]
            st.info(f"Bu'aa barbaacha barataa: '{search_query}'")
            st.dataframe(filtered_main_df, use_container_width=True, hide_index=True)
            st.markdown("---")

        for subj in subject_cols:
            st.markdown(f"### 📖 Gosa Barnootaa: **{subj}**")

            scores = pd.to_numeric(df[subj], errors="coerce")
            if use_scaling and max_score_input > 0:
                scores = (scores / max_score_input) * 100

            temp_df = df.copy()
            temp_df["Calculated_Score"] = scores

            ciccimoo = temp_df[temp_df["Calculated_Score"] >= 80]
            giddu = temp_df[(temp_df["Calculated_Score"] >= 50) & (temp_df["Calculated_Score"] < 80)]
            suuta = temp_df[(temp_df["Calculated_Score"] < 50) & (temp_df["Calculated_Score"].notna())]
            
            qoraman_df = pd.concat([ciccimoo, giddu, suuta])
            none_df = temp_df[temp_df["Calculated_Score"].isna()]

            dhiira_qoraman = len(qoraman_df[qoraman_df[gender_col].astype(str).str.contains("Dhi|M", case=False)])
            dhalaa_qoraman = len(qoraman_df[qoraman_df[gender_col].astype(str).str.contains("Dha|F", case=False)])
            waliigala_qoraman = dhiira_qoraman + dhalaa_qoraman

            dhiira_none = len(none_df[none_df[gender_col].astype(str).str.contains("Dhi|M", case=False)])
            dhalaa_none = len(none_df[none_df[gender_col].astype(str).str.contains("Dha|F", case=False)])
            waliigala_none = dhiira_none + dhalaa_none

            st.info(f"📊 **Xiinxala Gosa Barnootaa Kanaa ({subj}):**\n\n"
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

            st.markdown("---")

    # ==========================================
    # KAARDII BARATAA (STUDENT ID CARD)
    # ==========================================
    st.markdown("---")
    st.subheader("🪪 Kaardii Eenyummaa Barataa Qopheessuu (Student ID Card)")
    
    card_top_col1, card_top_col2 = st.columns(2)
    with card_top_col1:
        school_name_input = st.text_input("Maqaa Mana Barumsaa:", "MANA BARUMSAA SADARKAA 2FFAA", key="school_name_general_input")
    with card_top_col2:
        student_list = df[name_col].unique().tolist() if name_col in df.columns else []
        selected_student = st.selectbox("Barataa:", student_list if student_list else [""], key="id_card_student_select")
    
    uploaded_student_photo = st.file_uploader("🖼️ Suuraa Barataa Kanaaf Fe'i (Optional for ID Card)", type=["png", "jpg", "jpeg"], key="student_photo_upload_card")
    photo_html = "<div style='width:75px; height:90px; background:#ddd; border-radius:4px; display:inline-block; text-align:center; line-height:90px; font-size:10px; color:#555;'>Suuraa</div>"
    
    if uploaded_student_photo is not None:
        bytes_data = uploaded_student_photo.getvalue()
        base64_img = base64.b64encode(bytes_data).decode('utf-8')
        photo_html = f"<img src='data:image/png;base64,{base64_img}' style='width:75px; height:90px; object-fit:cover; border-radius:4px; border: 1.5px solid #1b5e20;'>"

    if student_list and selected_student:
        student_data = df[df[name_col] == selected_student].iloc[0]
        s_name = student_data[name_col]
        s_gender = student_data[gender_col] if gender_col in df.columns else "N/A"
        
        # Kutaa fi Daree iddoo Lakk ID cinaatti guutte irraa fudhata
        s_grade = manual_grade if manual_grade else "N/A"
        s_section = manual_section if manual_section else "N/A"
        
        s_id_num = student_data[id_num_col] if id_num_col != "Hin jiru" and id_num_col in df.columns else "N/A"
        
        card_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .card {{
                    width: 400px;
                    border: 2.5px solid #1b5e20;
                    border-radius: 12px;
                    padding: 15px;
                    font-family: 'Poppins', Arial, sans-serif;
                    background: #ffffff;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                    margin: auto;
                }}
                .flex-container {{ display: flex; align-items: center; gap: 15px; margin-top: 8px; }}
                .school-title {{ font-size: 15px; font-weight: bold; color: #1b5e20; text-align: center; text-transform: uppercase; }}
                .card-header {{ font-size: 11px; color: #555; text-align: center; margin-bottom: 5px; font-weight: 600; }}
                .student-info {{ font-size: 13px; margin: 3px 0; color: #222; }}
                .badge-box {{ background-color: #e8f5e9; padding: 4px 8px; border-radius: 6px; display: inline-block; font-weight: bold; color: #1b5e20; font-size: 12px; margin-top: 4px; }}
                .footer {{ margin-top: 10px; font-size: 9px; color: #777; border-top: 1px solid #ddd; padding-top: 5px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="school-title">🏫 {school_name_input}</div>
                <div class="card-header">KAARDII EENYUMMAA BARATAA (STUDENT ID CARD)</div>
                <hr style="border: 0.5px solid #1b5e20; margin: 6px 0;">
                <div class="flex-container">
                    <div>{photo_html}</div>
                    <div>
                        <div class="student-info"><b>Maqaa:</b> {s_name}</div>
                        <div class="student-info"><b>Saala:</b> {s_gender} | <b>Lakk ID:</b> {s_id_num}</div>
                        <div class="badge-box">Kutaa: {s_grade} &nbsp;|&nbsp; Daree: {s_section}</div>
                    </div>
                </div>
                <div class="footer">TRIAD Analytics App | Designed by Kitesa Negasa</div>
            </div>
        </body>
        </html>
        """
        
        st.components.v1.html(card_html, height=255)
        
        st.download_button(
            label=f"📥 Kaardii {s_name} Buusuu (Download Card HTML)",
            data=card_html.encode('utf-8'),
            file_name=f"Kaardii_{s_name}.html",
            mime="text/html",
            key=f"download_card_{s_name}"
        )

    # ==========================================
    # WARAQAA RAGAA BARATAA (REPORT CARD)
    # ==========================================
    st.markdown("---")
    st.subheader("📄 Waraqaa Ragaa Barataa Qopheessuu (Student Report Card)")

    if student_list and subject_cols:
        selected_student_rc = st.selectbox("Barataa Waraqaa Ragaa (Report Card) isaaf:", student_list, key="rc_student_select_dropdown")
        
        if selected_student_rc:
            rc_student_data = df[df[name_col] == selected_student_rc].iloc[0]
            rc_name = rc_student_data[name_col]
            rc_gender = rc_student_data[gender_col] if gender_col in df.columns else "N/A"
            rc_grade = manual_grade if manual_grade else "N/A"
            rc_section = manual_section if manual_section else "N/A"
            rc_id_num = rc_student_data[id_num_col] if id_num_col != "Hin jiru" and id_num_col in df.columns else "N/A"
            
            rc_records = []
            total_obtained_score = 0
            count_subjects = 0
            
            for subj in subject_cols:
                raw_val = rc_student_data[subj]
                try:
                    val_num = float(raw_val)
                    if use_scaling and max_score_input > 0:
                        scaled_val = (val_num / max_score_input) * 100
                    else:
                        scaled_val = val_num
                    rc_records.append({"Gosa Barnootaa": subj, "Qabxii Argame": raw_val, "Qabxii Sirreeffame (%)": f"{scaled_val:.1f}%"})
                    total_obtained_score += scaled_val
                    count_subjects += 1
                except:
                    rc_records.append({"Gosa Barnootaa": subj, "Qabxii Argame": str(raw_val), "Qabxii Sirreeffame (%)": "N/A"})
            
            rc_df = pd.DataFrame(rc_records)
            avg_score = (total_obtained_score / count_subjects) if count_subjects > 0 else 0
            
            if avg_score >= 80:
                status_text = "Ciccimoo (Excellent)"
            elif avg_score >= 50:
                status_text = "Giddu-galeeyyii (Medium)"
            else:
                status_text = "Suuta Barataa (Needs Support)"

            rc_table_html = rc_df.to_html(classes='table table-striped', index=False)
            
            report_card_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Report Card - {rc_name}</title>
                <style>
                    body {{ font-family: 'Poppins', Arial, sans-serif; margin: 20px; background: #fafafa; }}
                    .report-card {{
                        width: 620px;
                        border: 3px solid #1b5e20;
                        border-radius: 12px;
                        padding: 25px;
                        background: #ffffff;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                        margin: auto;
                    }}
                    .header-title {{ text-align: center; color: #1b5e20; font-size: 18px; font-weight: bold; }}
                    .header-sub {{ text-align: center; color: #555; font-size: 12px; margin-bottom: 10px; }}
                    .top-section {{ display: flex; justify-content: space-between; align-items: center; background: #f1f8e9; padding: 12px; border-radius: 8px; margin-bottom: 15px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 15px; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 13px; }}
                    th {{ background-color: #e8f5e9; color: #1b5e20; }}
                    .summary-box {{ font-size: 13px; font-weight: bold; margin-top: 10px; padding: 10px; background: #e8f5e9; border-radius: 6px; border-left: 4px solid #1b5e20; }}
                    .footer-note {{ text-align: center; font-size: 11px; color: #777; margin-top: 15px; border-top: 1px solid #ddd; padding-top: 8px; }}
                </style>
            </head>
            <body>
                <div class="report-card">
                    <div class="header-title">🏫 {school_name_input}</div>
                    <div class="header-sub">Waraqaa Ragaa Barataa (Student Academic Performance Report Card)</div>
                    <hr style="border: 0.5px solid #1b5e20;">
                    <div class="top-section">
                        <div>
                            <b>Maqaa Barataa:</b> {rc_name} <br>
                            <b>Saala:</b> {rc_gender} | <b>Lakk. ID:</b> {rc_id_num} <br>
                            <b>Kutaa:</b> {rc_grade} | <b>Daree:</b> {rc_section}
                        </div>
                        <div>{photo_html}</div>
                    </div>
                    <b>Qabxii Gosa Barnootaa:</b>
                    {rc_table_html}
                    <div class="summary-box">
                        Waliigala Giddu-galeessaa (Average Score): {avg_score:.1f}% <br>
                        Gita Dandeettii (Performance Level): {status_text}
                    </div>
                    <div class="footer-note">Designed & Developed by Kitesa Negasa (TRIAD Analytics App)</div>
                </div>
            </body>
            </html>
            """
            
            st.components.v1.html(report_card_html, height=520)
            
            rc_col1, rc_col2 = st.columns(2)
            with rc_col1:
                st.download_button(
                    label=f"📥 Waraqaa Ragaa {rc_name} Buusuu (Download HTML)",
                    data=report_card_html.encode('utf-8'),
                    file_name=f"ReportCard_{rc_name}.html",
                    mime="text/html",
                    key=f"download_rc_{rc_name}"
                )
            with rc_col2:
                st.components.v1.html(
                    f"""
                    <script>
                    function printReportCard() {{
                        var myWindow = window.open('', '', 'height=700,width=800');
                        myWindow.document.write(`{report_card_html}`);
                        myWindow.document.close();
                        myWindow.focus();
                        setTimeout(function() {{ myWindow.print(); }}, 500);
                    }}
                    </script>
                    <button onclick="printReportCard()" style="background-color: #1b5e20; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; width: 100%;">
                        🖨️ Kallattiin Print Godhuu (Print Report Card)
                    </button>
                    """,
                    height=50
                )
else:
    st.info("Maaloo jalqabaaf faayilii kee (Excel, CSV) ykn Suuraa (PNG/JPG) fe'i.")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Created with ❤️ by Kitesa Negasa | Educational Analytics App</p>",
    unsafe_allow_html=True,
)
