import streamlit as st
import pandas as pd
import numpy as np

# ユーザー入力の初期値
if 'data' not in st.session_state:
    st.session_state['data'] = {
        'ジョッシュ強': 0, 'エクセラ強': 0, 'CZ後ステージ': '',
        '白ナビ': 0, '青ナビ': 0, 'CHANCEアイコン': 0,
        'ターゲッティング演出': 0, 'フラッシュ演出': 0,
        'クリスアクション': {'汗ぬぐい': 0, 'リロード': 0, '見回す': 0, 'ストレッチ': 0},
        'ステージ移動': [], 'レア役履歴': []
    }

# 画像の表に基づく確率データ（仮定値なし）
ACTION_PROB = {
    '汗ぬぐい': {'LOW': 60.0, 'MID': 13.3, 'HI': 11.1, 'SP': 11.1},
    'リロード': {'LOW': 13.3, 'MID': 60.0, 'HI': 11.1, 'SP': 11.1},
    '見回す': {'LOW': 13.3, 'MID': 13.3, 'HI': 60.0, 'SP': 11.1},
    '銃回し': {'LOW': 13.3, 'MID': 13.3, 'HI': 11.1, 'SP': 54.2},
    'ストレッチ': {'LOW': 0, 'MID': 0, 'HI': 6.7, 'SP': 12.5}
}

STAGE_TRANSITION_PROB = {
    'LOW': {'集会場': 0, '大湿原': 86.67, '遺跡': 13.33, '始祖': 0},
    'MID': {'集会場': 0, '大湿原': 80.0, '遺跡': 20.0, '始祖': 0},
    'HI': {'集会場': 0, '大湿原': 20.0, '遺跡': 80.0, '始祖': 0},
    'SP': {'集会場': 0, '大湿原': 6.67, '遺跡': 13.33, '始祖': 80.0}
}

# モード確率計算関数（画像の表に基づく）
def calculate_mode_probabilities():
    prob = {'LOW': 25, 'MID': 25, 'HI': 25, 'SP': 25}
    
    # クリスアクションの影響（累積）
    for action, count in st.session_state['data']['クリスアクション'].items():
        for mode in prob.keys():
            prob[mode] += ACTION_PROB[action][mode] * count
    
    # ステージ移動の影響（累積）
    for move in st.session_state['data']['ステージ移動']:
        for mode in prob.keys():
            if move in STAGE_TRANSITION_PROB[mode]:
                prob[mode] += STAGE_TRANSITION_PROB[mode][move]
    
    # 正規化
    total = sum(prob.values())
    for key in prob:
        prob[key] = round(prob[key] / total * 100, 1)
    
    return prob

# タイトル
st.title('スマスロ バイオハザード5 モード判別ツール')

# クリスアクション入力
st.subheader('クリスアクション（累積）')
for action in st.session_state['data']['クリスアクション'].keys():
    if st.button(action):
        st.session_state['data']['クリスアクション'][action] += 1
    st.write(f"{action}: {st.session_state['data']['クリスアクション'][action]}")

# ステージ移動入力
st.subheader('ステージ移動（累積）')
new_stage_move = st.selectbox('ステージ間の移動を選択', ['', '集会場 → 大湿原', '大湿原 → 遺跡', '遺跡 → 始祖'])
if new_stage_move and new_stage_move not in st.session_state['data']['ステージ移動']:
    st.session_state['data']['ステージ移動'].append(new_stage_move)
st.write("ステージ移動履歴:", st.session_state['data']['ステージ移動'])

# モード確率の表示
st.subheader('現在のモード判別結果')
mode_probs = calculate_mode_probabilities()
st.write(mode_probs)

# 入力データ表示
st.subheader('入力データ一覧')
st.write(pd.DataFrame([st.session_state['data']]))
