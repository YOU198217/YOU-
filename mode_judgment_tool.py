import streamlit as st
import pandas as pd

# ユーザー入力の初期値
if 'data' not in st.session_state:
    st.session_state['data'] = {
        'ジョッシュ強': 0, 'エクセラ強': 0, 'CZ後ステージ': '',
        '白ナビ': 0, '青ナビ': 0, 'CHANCEアイコン': 0,
        'ターゲッティング演出': 0, 'フラッシュ演出': 0
    }

# タイトル
st.title('スマスロ バイオハザード5 モード判別ツール')

# セリフ入力
st.subheader('セリフ履歴')
col1, col2 = st.columns(2)
with col1:
    if st.button('ジョッシュ強'):
        st.session_state['data']['ジョッシュ強'] += 1
    st.write(f"ジョッシュ強: {st.session_state['data']['ジョッシュ強']}")
with col2:
    if st.button('エクセラ強'):
        st.session_state['data']['エクセラ強'] += 1
    st.write(f"エクセラ強: {st.session_state['data']['エクセラ強']}")

# CZ・ART後のステージ入力
st.subheader('CZ・ART終了後のステージ')
st.session_state['data']['CZ後ステージ'] = st.selectbox('最初のステージを選択', ['', '集会場', '大湿原', '遺跡', '始祖'])

# ナビ色・CHANCEアイコン
st.subheader('ナビ色 & CHANCEアイコン')
col3, col4, col5 = st.columns(3)
with col3:
    if st.button('白ナビ'):
        st.session_state['data']['白ナビ'] += 1
    st.write(f"白ナビ: {st.session_state['data']['白ナビ']}")
with col4:
    if st.button('青ナビ'):
        st.session_state['data']['青ナビ'] += 1
    st.write(f"青ナビ: {st.session_state['data']['青ナビ']}")
with col5:
    if st.button('CHANCEアイコン'):
        st.session_state['data']['CHANCEアイコン'] += 1
    st.write(f"CHANCEアイコン: {st.session_state['data']['CHANCEアイコン']}")

# 演出カウント
st.subheader('ターゲッティング演出 & フラッシュ演出')
col6, col7 = st.columns(2)
with col6:
    if st.button('ターゲッティング演出'):
        st.session_state['data']['ターゲッティング演出'] += 1
    st.write(f"ターゲッティング演出: {st.session_state['data']['ターゲッティング演出']}")
with col7:
    if st.button('フラッシュ演出'):
        st.session_state['data']['フラッシュ演出'] += 1
    st.write(f"フラッシュ演出: {st.session_state['data']['フラッシュ演出']}")

# 入力データ表示
st.subheader('入力データ一覧')
st.write(pd.DataFrame([st.session_state['data']]))
