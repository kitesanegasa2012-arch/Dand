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

profile_pic_path = "qixxeessaa.jpg"
if os.path.exists(profile_pic_path):
    st.sidebar.image(profile_pic_path, caption="Qixxeessaa Nagaasaa (KN)", use_container_width=True)
else:
    st.sidebar.warning("Suuraan 'qixxeessaa.jpg' jedhu hin argamne. Maaloo foldera koodii kana wajjin jiru keessa kaa'i.")

st.sidebar.markdown("### 📝 Seensa  (Introduction)")
st.sidebar.write(
    "Baga Nagaan Gara  TRIAD appilikeeshiniikootti nagaan Dhuftan! Ani barsiisaa Qixxeessaa Nagaasaa Jedhama.Mogaasni maqaa appikoo TRIAD jedhu Afaan Ingiliffaan (Tracking Rates in Academic Development)itti hiikama, "
    "Kunis,Baratoota Dandeetti Sadiin Suuta baratoo,Giddugaleeyyii fi ciccimoo jennee Qabxii isaani gosa barnootan battalleen ykn qormaata giddugaleessaan ykn semisteeran adda baasnee deggeruuf kan tajaajiludha.Appiinkun Kutaalee Gurguddoo kudhan(10) kan of keessaa qabuu fi manneen barnotaa sadarkaa 1ffaa(1-6),sadarkaa giddugaleessaa(7-8) fi sadarkaa 2ffaa(9-12) keessatti tajaajila kennuu kan danda'udha."
)

st.sidebar.markdown("### 🎯 Kaayyoo Appichaa (App Objective)")
st.sidebar.write(
    "Kaayyoon Guddaan kalaqa appi kana daree barnootaa keessatti barattoota dandeett isaanitiin adda baasuun deggersa barbaachisaa kennuun qabxii barattoota foyyeessuuf kan kalaqamedha, "
)

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

@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en'])

st.sidebar.markdown("---")
st.sidebar.subheader("🗄️ Madda Ragaa Filadhu")
madda_ragaa = st.sidebar.radio(
    "Filannoo kee:",
    ["📤 Ragaa Haaraa Fe'uu (Upload)", "📁 Ragaa Kuufame Filachuu (Saved)"]
)

df = None
file_extension = ""
image_to_process = None

if madda_ragaa == "📤 Ragaa Haaraa Fe'uu (Upload)":
    st.subheader("📂 Step 1: Faayila (Excel/CSV) ykn Suuraa (Image) Fe'i")
    uploaded_file = st.file_uploader(
        "Faayilii qabxii barattootaa ykn suuraa filadhu", 
        type=["csv", "xlsx", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if st.button("💾 Faayilii Kana Kuusi (Save File)"):
            file_path = os.path.join(SAVE_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Faayiliin '{uploaded_file.name}' milkaa'inaan kuufameera!")

        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
            st.success("Faayiliin kee milkaa'inaan fe'ameera!")
        elif file_extension == 'xlsx':
            xls = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Sheet Excel filadhu:", xls.sheet_names)
            skip = st.number_input("Sarara irraa kaafamu (Header Row Index):", min_value=0, max_value=10, value=0)
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
        selected_file = st.selectbox("Faayilii barbaaddu filadhu:", saved_files)
        file_path = os.path.join(SAVE_DIR, selected_file)
        file_extension = selected_file.split('.')[-1].lower()

        if st.button("🗑️ Faayilii Kana Haqi (Delete)"):
            os.remove(file_path)
            st.success(f"Faayiliin '{selected_file}' haqameera!")
            st.rerun()

        if os.path.exists(file_path):
            if file_extension == 'csv':
                df = pd.read_csv(file_path)
            elif file_extension == 'xlsx':
                xls = pd.ExcelFile(file_path)
                sheet_name = st.selectbox("Sheet Excel filadhu:", xls.sheet_names)
                skip = st.number_input("Sarara irraa kaafamu (Header Row Index):", min_value=0, max_value=10, value=0)
                df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skip)
            elif file_extension in ['png', 'jpg', 'jpeg']:
                image_to_process = Image.open(file_path)
                st.image(image_to_process, caption="Suuraa Kuufame", use_container_width=True)

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

if df is not None:
    st.subheader("⚙️ Step 2 & 3: Qindaa'ina Kolomanii fi Daataa Waliigalaa")
    all_columns = df.columns.tolist()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        name_col = st.selectbox("Kolomanii Maqaa Barataa qabatee jiru:", all_columns, index=0)
    with col_b:
        gender_col = st.selectbox("Kolonii Saala (Gender):", all_columns, index=1 if len(all_columns) > 1 else 0)
    with col_c:
        subject_cols = st.multiselect("Kolomanii Gosa Barnootaa Waliigalaa qabatee jiru:", [col for col in all_columns if col not in [name_col, gender_col]])

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

    if subject_cols and name_col and gender_col:
        
        # ==========================================
        # 1. WARAQAA EENYUMMAA BARATAA (STUDENT ID CARD)
        # ==========================================
        st.markdown("---")
        st.subheader("🪪 Kaardii Eenyummaa Barataa Qopheessuu (Student ID Card)")
        
        student_list = df[name_col].unique().tolist()
        selected_id_student = st.selectbox("Barataa Kaardii Eenyummaaf barbaaddu filadhu:", student_list, key="id_card_select")
        
        if selected_id_student:
            id_s_row = df[df[name_col] == selected_id_student].iloc[0]
            id_s_name = id_s_row[name_col]
            id_s_gender = id_s_row[gender_col]
            
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
                    <div class="student-info"><b>Maqaa:</b> {id_s_name}</div>
                    <div class="student-info"><b>Saala:</b> {id_s_gender}</div>
                    <div class="student-info"><b>Daree:</b> Barataa/tuu Qormaataa</div>
                    <div class="footer">Designed & Developed by Kitesa Negasa</div>
                </div>
            </body>
            </html>
            """
            st.components.v1.html(card_html, height=260)
            st.download_button(
                label=f"📥 Kaardii {id_s_name} Buusuu (Download ID Card HTML)",
                data=card_html.encode('utf-8'),
                file_name=f"Kaardii_Eenyummaa_{id_s_name}.html",
                mime="text/html",
                key="download_id_btn"
            )

        # ==========================================
        # 2. WARAQAA RAGAA BARATAA GUUTUU (FULL REPORT CARD)
        # ==========================================
        st.markdown("---")
        st.subheader("📋 Waraqaa Ragaa Barataa Guutuu (Full Report Card - Sem 1 & Sem 2)")
        
        school_name_input = st.text_input("Maqaa Mana Barumsaa (School Name):", value="Mane Barumsaa Sadarkaa 1ffaa & 2ffaa TRIAD")
        
        selected_rep_student = st.selectbox("Barataa Waraqaa Ragaa (Report Card) isaaf qopheessuuf barbaaddu filadhu:", student_list, key="report_select")
        
        if selected_rep_student:
            s_row = df[df[name_col] == selected_rep_student].iloc[0]
            s_name = s_row[name_col]
            s_gender = s_row[gender_col]
            
            col_rc1, col_rc2 = st.columns(2)
            with col_rc1:
                student_conduct = st.selectbox("Amala Barataa (Conduct):", ["Baayyee Gaarii (Very Good)", "Gaarii (Good)", "Giddu-galeessa (Satisfactory)", "Fooyya'uu qaba (Needs Improvement)"])
            with col_rc2:
                days_absent = st.number_input("Guyyaa Haftee (Days Absent):", min_value=0, value=0)

            # Kolomii Semisteera 1ffaa fi 2ffaa adda baasuu ykn herreguu
            st.markdown("### ⚙️ Qindaa'ina Qabxii Semisteera 1ffaa fi 2ffaa")
            col_sem1, col_sem2 = st.columns(2)
            with col_sem1:
                sem1_cols = st.multiselect("Kolomanii Qabxii Semisteera 1ffaa (Sem 1 Subjects):", subject_cols, default=subject_cols[:len(subject_cols)//2] if len(subject_cols)>1 else subject_cols)
            with col_sem2:
                sem2_cols = st.multiselect("Kolomanii Qabxii Semisteera 2ffaa (Sem 2 Subjects):", subject_cols, default=subject_cols[len(subject_cols)//2:] if len(subject_cols)>1 else subject_cols)

            # Herrega Semisteera 1ffaa, 2ffaa, Avireejii fi Rank
            temp_calc_df = df.copy()
            
            for sc in subject_cols:
                temp_calc_df[sc] = pd.to_numeric(temp_calc_df[sc], errors='coerce').fillna(0)
            
            if sem1_cols:
                temp_calc_df['Sem1_Total'] = temp_calc_df[sem1_cols].sum(axis=1)
                temp_calc_df['Sem1_Avg'] = temp_calc_df[sem1_cols].mean(axis=1)
            else:
                temp_calc_df['Sem1_Total'] = 0
                temp_calc_df['Sem1_Avg'] = 0

            if sem2_cols:
                temp_calc_df['Sem2_Total'] = temp_calc_df[sem2_cols].sum(axis=1)
                temp_calc_df['Sem2_Avg'] = temp_calc_df[sem2_cols].mean(axis=1)
            else:
                temp_calc_df['Sem2_Total'] = 0
                temp_calc_df['Sem2_Avg'] = 0

            temp_calc_df['Annual_Avg'] = (temp_calc_df['Sem1_Avg'] + temp_calc_df['Sem2_Avg']) / 2
            temp_calc_df['Rank'] = temp_calc_df['Annual_Avg'].rank(ascending=False, method='min').astype(int)
            
            curr_stat = temp_calc_df[temp_calc_df[name_col] == selected_rep_student].iloc[0]
            sem1_avg = curr_stat['Sem1_Avg']
            sem2_avg = curr_stat['Sem2_Avg']
            annual_avg = curr_stat['Annual_Avg']
            st_rank = curr_stat['Rank']
            
            # Table subjects rows for report card
            subjects_html = ""
            for subj in subject_cols:
                val = s_row[subj]
                subjects_html += f"<tr><td>{subj}</td><td>{val}</td><td>100</td><td>Gaarii</td></tr>"

            report_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 0; padding: 10px; background: #f9f9f9; }}
                    .report-card {{
                        width: 100%;
                        max-width: 650px;
                        margin: auto;
                        border: 3px solid #1b5e20;
                        border-radius: 10px;
                        padding: 20px;
                        background: #ffffff;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    }}
                    .header {{ text-align: center; color: #1b5e20; margin-bottom: 10px; }}
                    .header h2 {{ margin: 0; font-size: 19px; }}
                    .header h3 {{ margin: 5px 0; font-size: 15px; color: #2e7d32; }}
                    .header p {{ margin: 2px 0; font-size: 12px; color: #555; }}
                    .student-info {{
                        display: flex;
                        justify-content: space-between;
                        background: #e8f5e9;
                        padding: 10px;
                        border-radius: 6px;
                        font-size: 14px;
                        margin-bottom: 15px;
                    }}
                    table {{ width: 100%; border-collapse: collapse; margin-bottom: 15px; }}
                    th, td {{ border: 1px solid #c8e6c9; padding: 8px; text-align: left; font-size: 13px; }}
                    th {{ background-color: #2e7d32; color: white; }}
                    .summary-box {{
                        background: #f1f8e9;
                        padding: 10px;
                        border-radius: 6px;
                        font-size: 14px;
                        margin-bottom: 15px;
                    }}
                    .footer-note {{
                        display: flex;
                        justify-content: space-between;
                        font-size: 13px;
                        margin-top: 25px;
                        border-top: 1px dashed #aaa;
                        padding-top: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="report-card">
                    <div class="header">
                        <h2>🏫 {school_name_input}</h2>
                        <h3>Waraqaa Ragaa Barataa (Student Report Card)</h3>
                        <p>Semisteera 1ffaa & 2ffaa</p>
                    </div>
                    <hr style="border: 1px solid #1b5e20;">
                    <div class="student-info">
                        <div><b>Maqaa:</b> {s_name}</div>
                        <div><b>Saala:</b> {s_gender}</div>
                    </div>
                    <table>
                        <tr>
                            <th>Gosa Barnootaa (Subjects)</th>
                            <th>Qabxii Argame</th>
                            <th>Qabxii Waliigalaa</th>
                            <th>Ibsaa (Remark)</th>
                        </tr>
                        {subjects_html}
                    </table>
                    <div class="summary-box">
                        <div><b>📊 Avireejii Semisteera 1ffaa (1st Semester Average):</b> {sem1_avg:.2f}%</div>
                        <div><b>📊 Avireejii Semisteera 2ffaa (2nd Semester Average):</b> {sem2_avg:.2f}%</div>
                        <div><b>📈 Avireejii Waliigalaa / Annual Average:</b> {annual_avg:.2f}%</div>
                        <div><b>🏆 Sadarkaa (Rank):</b> {st_rank} / {len(df)}</div>
                        <div><b>⭐ Amala (Conduct):</b> {student_conduct}</div>
                        <div><b>📅 Guyyaa Haftee (Days Absent):</b> {days_absent}</div>
                    </div>
                    <div class="footer-note">
                        <div>Mallattoo Barsiisaa Daree: ____________</div>
                        <div>Mallattoo Bulchiinsaa: ____________</div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            st.components.v1.html(report_html, height=560, scrolling=True)
            
            st.download_button(
                label=f"📥 Waraqaa Ragaa {s_name} Buusuu (Download Report Card HTML)",
                data=report_html.encode('utf-8'),
                file_name=f"ReportCard_{s_name}.html",
                mime="text/html",
                key="download_report_btn"
            )

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Created with ❤️ by Kitesa Negasa | Educational Analytics App</p>",
    unsafe_allow_html=True,
)
