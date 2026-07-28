import easyocr
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# App Configuration
st.set_page_config(
    page_title="Appii Qoodinsa Qabxii Barattootaa (Suuraa & Excel)",
    page_icon="📚",
    layout="wide",
)

# Header & Creator Info
st.title("🏫 Appii Qoodinsa Qabxii Barattootaa (Excel & Suuraa)")
st.markdown(
    "### Gamaaggama Dandeettii Barattootaa fi Qoodinsa Koorniyaan (OCR dabalataatiin)"
)
st.sidebar.info("Designed & Developed by **KN (Kitesa Negasa)**")

# Sidebar - Qajeelfama
st.sidebar.markdown("---")
st.sidebar.subheader("📖 Qajeelfama Itti Fayyadamaa")
st.sidebar.markdown(
    """
1. **Faayilii ykn Suuraa Fe'i:** Excel, CSV ykn Suuraa waraqaa qabxii (PNG/JPG) upload godhi.
2. **OCR (Suuraa irraa dubbisuu):** Suuraa yoo feite, appichi keessaa barreeffama baasee daataatti jijjiira.
3. **Qindaa'ina:** Kolonii maqaa, saala, fi gosa barnootaa filadhu.
4. **Bu'aa Ilaali:** C我们会iccimoo, Giddu-galeeyyii, fi Suuta barattootaa koorniyaan argadhu!
"""
)

# Cache OCR reader to avoid reloading
@st.cache_resource
def load_ocr_reader():
  return easyocr.Reader(['en'])


# Faayilii ykn Suuraa Fe'uu (Upload)
st.subheader(
    "📂 Step 1: Faayilii (Excel/CSV) ykn Suuraa Qabxii (Image) Fe'aa"
)
uploaded_file = st.file_uploader(
    "Faayilii Excel/CSV ykn Suuraa (PNG, JPG, JPEG) filadhu",
    type=["csv", "xlsx", "png", "jpg", "jpeg"],
)

df = None

if uploaded_file is not None:
  file_extension = uploaded_file.name.split('.')[-1].lower()

  if file_extension == 'csv':
    df = pd.read_csv(uploaded_file)
    st.success("Faayiliin CSV milkaa'inaan fe'ameera!")

  elif file_extension == 'xlsx':
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox('Sheet Excel filadhu:', xls.sheet_names)
    skip = st.number_input(
        'Sarara irraa kaafamu (Header Row Index):',
        min_value=0,
        max_value=10,
        value=0,
    )
    df = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=skip)
    st.success("Faayiliin Excel milkaa'inaan fe'ameera!")

  elif file_extension in ['png', 'jpg', 'jpeg']:
    st.image(
        uploaded_file, caption='Suuraa Fe’ame (Uploaded Image)', use_width=True
    )
    st.info(
        'Suuraa irraa barreeffama dubbisuu (OCR) eegalaara... Maaloo xiqqoo'
        ' turi!'
    )

    with st.spinner('Suuraa irraa daataa baasaa jira...'):
      image = Image.open(uploaded_file)
      image_np = np.array(image)

      reader = load_ocr_reader()
      results = reader.readtext(image_np)

      # Barreeffamoota suuraarra jiran walitti qabuu
      extracted_texts = [res[1] for res in results]

      if extracted_texts:
        st.success('Daataan suuraa irraa milkaa'inaan dubbifameera!')
        st.write('Barreeffama Suuraa keessaa argame:', extracted_texts)
        # Hubachiisa: Suuraan bifa waraqaa irraa dhufeef dataframe qindeessuun
        # akkaataa teessoo waraqaa sanaatiin murtaa'a.
        st.warning(
            'Hubachiisa: Suuraa irraa daataan sirriitti akka hojjetuuf,'
            ' barreeffamni suuraarratti jiru ifaa fi qajeelaa ta'uu qaba.'
        )
      else:
        st.error(
            'Suuraa kana irraa barreeffama argachuu hin danda’amne. Maaloo'
            ' suuraa ifaa ta’e deebisanii fe’aa.'
        )

  # Step 2: Daataa Preview (Yoo Excel/CSV ta'e)
  if df is not None:
    st.subheader('👀 Step 2: Daataa Jalqabaa (Raw Data Preview)')
    st.dataframe(df.head(), use_container_width=True)

    # Step 3: Qindaa'ina Kolonootaa
    st.subheader('⚙️ Step 3: Qindaa\'ina Kolonootaa fi Ulaagaa')
    all_columns = df.columns.tolist()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
      name_col = st.selectbox('Kolonii Maqaa Barataa:', all_columns)
    with col_b:
      gender_col = st.selectbox(
          'Kolonii Saala (Gender) - [Fkn: Dhi/Dha ykn M/F]:',
          all_columns,
          index=1 if len(all_columns) > 1 else 0,
      )
    with col_c:
      subject_cols = st.multiselect(
          'Kolonoota Gosa Barnootaa:',
          [col for col in all_columns if col not in [name_col, gender_col]],
      )

    # Quiz Qabxii Gara 100tti jijjiiruu (Scaling option)
    st.markdown('---')
    use_scaling = st.checkbox(
        'Qabxii Qorannoo Xiqqaa (Fkn: 10 ykn 20) gara 100tti jijjiiruu (Scale'
        ' to 100%)'
    )
    max_score_input = 100
    if use_scaling:
      max_score_input = st.number_input(
          'Qabxii Waliigalaa (Maximum Possible Score, fkn: 10, 20, 50):',
          min_value=1,
          value=10,
      )

    if subject_cols and name_col and gender_col:
      st.markdown('---')
      st.subheader('🔍 Step 4: Barbaacha (Search) fi Qoodinsa Gosa Barnootaan')

      # Search Bar
      search_query = st.text_input(
          '🔍 Maqaa Barataa Barbaadi (Barbaachaaf asitti barreessi):'
      )

      filtered_main_df = df.copy()
      if search_query:
        filtered_main_df = filtered_main_df[
            filtered_main_df[name_col]
            .astype(str)
            .str.contains(search_query, case=False, na=False)
        ]
        st.info(f"Bu'aa barbaacha barataa: '{search_query}'")
        st.dataframe(filtered_main_df, use_container_width=True, hide_index=True)
        st.markdown('---')

      # Gosa barnootaan qooduu fi koorniyaan ibsuu
      for subj in subject_cols:
        st.markdown(f'### 📖 Gosa Barnootaa: **{subj}**')

        scores = pd.to_numeric(df[subj], errors='coerce')

        if use_scaling and max_score_input > 0:
          scores = (scores / max_score_input) * 100

        temp_df = df.copy()
        temp_df['Calculated_Score'] = scores

        ciccimoo = temp_df[temp_df['Calculated_Score'] >= 80]
        giddu = temp_df[
            (temp_df['Calculated_Score'] >= 50)
            & (temp_df['Calculated_Score'] < 80)
        ]
        suuta = temp_df[
            (temp_df['Calculated_Score'] < 50)
            & (temp_df['Calculated_Score'].notna())
        ]

        col1, col2, col3 = st.columns(3)

        with col1:
          st.metric(
              label='🌟 Ciccimoo (≥ 80%)', value=f'{len(ciccimoo)} Barattoota'
          )
          if not ciccimoo.empty:
            dhiira_c = len(
                ciccimoo[
                    ciccimoo[gender_col]
                    .astype(str)
                    .str.contains('Dhi|M', case=False)
                ]
            )
            dhalaa_c = len(
                ciccimoo[
                    ciccimoo[gender_col]
                    .astype(str)
                    .str.contains('Dha|F', case=False)
                ]
            )
            st.caption(f'👥 Dhiira: {dhiira_c} | Dhalaa: {dhalaa_c}')
            st.dataframe(
                ciccimoo[[name_col, gender_col, subj]],
                use_container_width=True,
                hide_index=True,
            )

        with col2:
          st.metric(
              label='📊 Giddu-galeeyyii (50-79.9%)',
              value=f'{len(giddu)} Barattoota',
          )
          if not giddu.empty:
            dhiira_g = len(
                giddu[
                    giddu[gender_col]
                    .astype(str)
                    .str.contains('Dhi|M', case=False)
                ]
            )
            dhalaa_g = len(
                giddu[
                    giddu[gender_col]
                    .astype(str)
                    .str.contains('Dha|F', case=False)
                ]
            )
            st.caption(f'👥 Dhiira: {dhiira_g} | Dhalaa: {dhalaa_g}')
            st.dataframe(
                giddu[[name_col, gender_col, subj]],
                use_container_width=True,
                hide_index=True,
            )

        with col3:
          st.metric(
              label='⚠️ Suuta Barattoota (< 50%)',
              value=f'{len(suuta)} Barattoota',
          )
          if not suuta.empty:
            dhiira_s = len(
                suuta[
                    suuta[gender_col]
                    .astype(str)
                    .str.contains('Dhi|M', case=False)
                ]
            )
            dhalaa_s = len(
                suuta[
                    suuta[gender_col]
                    .astype(str)
                    .str.contains('Dha|F', case=False)
                ]
            )
            st.caption(f'👥 Dhiira: {dhiira_s} | Dhalaa: {dhalaa_s}')
            st.dataframe(
                suuta[[name_col, gender_col, subj]],
                use_container_width=True,
                hide_index=True,
            )

        st.markdown('---')

else:
  st.info(
      'Maaloo jalqabaaf faayilii kee (Excel/CSV) ykn Suuraa (PNG/JPG) fe’i!'
  )

# Footer
st.markdown('---')
st.markdown(
    "<p style='text-align: center; color: gray;'>Created with ❤️ by KN (Kitesa"
    " Negasa) | Educational Analytics App</p>",
    unsafe_allow_html=True,
)
