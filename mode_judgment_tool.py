import streamlit as st
import pandas as pd
import numpy as np

# ユーザー入力の初期値
if 'data' not in st.session_state:
    st.session_state['data'] = {
        'ジョッシュ強': 0, 'エクセラ強': 0, 'CZ後ステージ': '',
        '白ナビ': 0, '青ナビ': 0, 'CHANCEアイコン': 0,
        'ターゲッティング演出': 0, 'フラッシュ演出': 0,
        'クリスアクション': '', 'ステージ移動': '', 'レア役履歴': []
    }

# モード確率計算関数
def calculate_mode_probabilities():
    prob = {'LOW': 25, 'MID': 25, 'HI': 25, 'SP': 25}
    
    # セリフの影響
    prob['MID'] += st.session_state['data']['ジョッシュ強'] * 5
    prob['SP'] += st.session_state['data']['エクセラ強'] * 10
    
    # CZ後のステージ影響
    if st.session_state['data']['CZ後ステージ'] == '集会場':
        prob['LOW'] += 10
    elif st.session_state['data']['CZ後ステージ'] == '大湿原':
        prob['MID'] += 10
    elif st.session_state['data']['CZ後ステージ'] == '遺跡':
        prob['HI'] += 10
    elif st.session_state['data']['CZ後ステージ'] == '始祖':
        prob['SP'] = 100
    
    # ナビ色の影響
    prob['LOW'] += st.session_state['data']['白ナビ'] * 2
    prob['HI'] += st.session_state['data']['青ナビ'] * 3
    prob['SP'] += st.session_state['data']['青ナビ'] * 5
    
    # CHANCEアイコン影響
    prob['MID'] += st.session_state['data']['CHANCEアイコン'] * 5
    prob['HI'] += st.session_state['data']['CHANCEアイコン'] * 8
    prob['SP'] += st.session_state['data']['CHANCEアイコン'] * 10
    
    # クリスアクションの影響
    if st.session_state['data']['クリスアクション'] == '汗ぬぐい':
        prob['LOW'] += 10
    elif st.session_state['data']['クリスアクション'] == 'リロード':
        prob['MID'] += 10
    elif st.session_state['data']['クリスアクション'] == '見回す':
        prob['HI'] += 10
    elif st.session_state['data']['クリスアクション'] == 'ストレッチ':
        prob['SP'] += 10
    
    # ステージ移動の影響
    if st.session_state['data']['ステージ移動'] == '集会場 → 大湿原':
        prob['MID'] += 10
    elif st.session_state['data']['ステージ移動'] == '大湿原 → 遺跡':
        prob['HI'] += 10
    elif st.session_state['data']['ステージ移動'] == '遺跡 → 始祖':
        prob['SP'] = 100
    
    # レア役の影響
    for rare in st.session_state['data']['レア役履歴']:
        if rare == '弱チェリー':
            prob['MID'] += 5
        elif rare == '強チェリー':
            prob['HI'] += 10
        elif rare == '単チェリー':
            prob['SP'] += 20
    
    # 正規化
    total = sum(prob.values())
    for key in prob:
        prob[key] = round(prob[key] / total * 100, 1)
    
    return prob

# タイトル
st.title('スマスロ バイオハザード5 モード判別ツール')

# 入力フォーム
st.subheader('クリスアクション')
st.session_state['data']['クリスアクション'] = st.selectbox('クリスのアクションを選択', ['', '汗ぬぐい', 'リロード', '見回す', 'ストレッチ'])

st.subheader('ステージ移動')
st.session_state['data']['ステージ移動'] = st.selectbox('ステージ間の移動を選択', ['', '集会場 → 大湿原', '大湿原 → 遺跡', '遺跡 → 始祖'])

st.subheader('レア役履歴')
if st.button('弱チェリー'):
    st.session_state['data']['レア役履歴'].append('弱チェリー')
if st.button('強チェリー'):
    st.session_state['data']['レア役履歴'].append('強チェリー')
if st.button('単チェリー'):
    st.session_state['data']['レア役履歴'].append('単チェリー')

# モード確率の表示
st.subheader('現在のモード判別結果')
mode_probs = calculate_mode_probabilities()
st.write(mode_probs)

# 入力データ表示
st.subheader('入力データ一覧')
st.write(pd.DataFrame([st.session_state['data']]))
