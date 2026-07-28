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
    page_title="Appii Qoodinsa Qabxii (Save/Delete)",
    page_icon="📚",
    layout="wide",
)

st.title("🏫 Appii Qoodinsa Qabxii Barattootaa")
st.markdown("### Daataa Fe'uu, Kuusuu (Save) fi Haquu (Delete)")
st.sidebar.info("Designed & Developed by **KN (Kitesa Negasa)**")

@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en'])

# Sidebar - Madda Ragaa Filachuu
st.sidebar.markdown("---")
st.sidebar.subheader("🗄️ Madda Ragaa Filadhu")
madda_ragaa = st.sidebar.radio(
    "Filannoo kee:",
    ["📤 Ragaa Haaraa Fe'uu (Upload)", "📁 Ragaa Kuufame Fayyadamuu (Saved)"]
)

df = None
file_extension = ""
image_to_process = None

# ==========================================
# FILANNOO 1: RAGAA HAARAA FE'UU
# ==========================================
if madda_ragaa == "📤 Ragaa Haaraa Fe'uu (Upload)":
    st.subheader("📂 Faayilii (Excel/CSV) ykn Suuraa (Image) Fe'aa")
    uploaded_file = st.file_uploader(
        "Faayilii filadhu", type=["csv", "xlsx", "png", "jpg", "jpeg"]
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
        elif file_extension == 'xlsx':
            xls = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox('Sheet Excel filadhu:', xls.sheet_names)
            skip = st.number_input('Sarara irraa kaafamu (Header Row):', min_value=0, max_value=10, value=0)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=skip)
        elif file_extension in ['png', 'jpg', 'jpeg']:
            image_to_process = Image.open(uploaded_file)
            st.image(image_to_process, caption='Suuraa Fe’ame', use_container_width=True)

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
            st.rerun()  # Fuula appichaa haaromsuuf (refresh)

        # Daataa Dubbisuu
        if os.path.exists(file_path):
            if file_extension == 'csv':
                df = pd.read_csv(file_path)
            elif file_extension == 'xlsx':
                xls = pd.ExcelFile(file_path)
                sheet_name = st.selectbox('Sheet Excel filadhu:', xls.sheet_names)
                skip = st.number_input('Sarara irraa kaafamu (Header Row):', min_value=0, max_value=10, value=0)
                df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skip)
            elif file_extension in ['png', 'jpg', 'jpeg']:
                image_to_process = Image.open(file_path)
                st.image(image_to_process, caption='Suuraa Kuufame', use_container_width=True)

# ==========================================
# SUURAA (IMAGE) IRRAA DUBBISUU (OCR)
# ==========================================
if image_to_process is not None:
    st.info('Suuraa irraa barreeffama dubbisuu (OCR) eegalaara... Maaloo xiqqoo turi!')
    with st.spinner('Suuraa irraa daataa baasaa jira...'):
        image_np = np.array(image_to_process)
        reader = load_ocr_reader()
        results = reader.readtext(image_np)
        extracted_texts = [res[1] for res in results]

        if extracted_texts:
            st.success('Daataan suuraa irraa milkaa\'inaan dubbifameera!')
            st.write('**Barreeffama Argame:**', extracted_texts)
        else:
            st.error('Barreeffama dubbisuun hin danda\'amne.')

# ==========================================
# GAMAAGGAMA FI QOODINSA QABXII (EXCEL/CSV)
# ==========================================
if df is not None:
    st.markdown("---")
    st.subheader('⚙️ Qindaa\'ina Kolonootaa fi Ulaagaa')
    all_columns = df.columns.tolist()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        name_col = st.selectbox('Kolonii Maqaa Barataa:', all_columns)
    with col_b:
        gender_col = st.selectbox('Kolonii Saala (Gender):', all_columns, index=1 if len(all_columns) > 1 else 0)
    with col_c:
        subject_cols = st.multiselect('Kolonoota Gosa Barnootaa:', [col for col in all_columns if col not in [name_col, gender_col]])

    # Scaling to 100%
    st.markdown('---')
    use_scaling = st.checkbox('Qabxii Qorannoo (Quiz) gara 100tti jijjiiruu (Scale to 100%)')
    max_score_input = 100
    if use_scaling:
        max_score_input = st.number_input('Qabxii Waliigalaa (Fkn: 10, 20):', min_value=1, value=10)

    if subject_cols and name_col and gender_col:
        st.markdown('---')
        st.subheader('🔍 Barbaacha (Search) fi Qoodinsa')
        search_query = st.text_input('🔍 Maqaa Barataa Barbaadi:')

        filtered_main_df = df.copy()
        if search_query:
            filtered_main_df = filtered_main_df[filtered_main_df[name_col].astype(str).str.contains(search_query, case=False, na=False)]
            st.dataframe(filtered_main_df, use_container_width=True, hide_index=True)

        for subj in subject_cols:
            st.markdown(f'### 📖 Gosa Barnootaa: **{subj}**')
            scores = pd.to_numeric(df[subj], errors='coerce')

            if use_scaling and max_score_input > 0:
                scores = (scores / max_score_input) * 100

            temp_df = df.copy()
            temp_df['Calculated_Score'] = scores

            ciccimoo = temp_df[temp_df['Calculated_Score'] >= 80]
            giddu = temp_df[(temp_df['Calculated_Score'] >= 50) & (temp_df['Calculated_Score'] < 80)]
            suuta = temp_df[(temp_df['Calculated_Score'] < 50) & (temp_df['Calculated_Score'].notna())]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label='🌟 Ciccimoo (≥ 80%)', value=f'{len(ciccimoo)}')
                if not ciccimoo.empty:
                    st.dataframe(ciccimoo[[name_col, gender_col, subj]], use_container_width=True, hide_index=True)
            with col2:
                st.metric(label='📊 Giddu-galeeyyii (50-79.9%)', value=f'{len(giddu)}')
                if not giddu.empty:
                    st.dataframe(giddu[[name_col, gender_col, subj]], use_container_width=True, hide_index=True)
            with col3:
                st.metric(label='⚠️ Suuta (< 50%)', value=f'{len(suuta)}')
                if not suuta.empty:
                    st.dataframe(suuta[[name_col, gender_col, subj]], use_container_width=True, hide_index=True)
            st.markdown('---')
