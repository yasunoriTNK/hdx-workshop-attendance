import streamlit as st
import pandas as pd
import os

# =========================
# カスタムCSS
# =========================
st.markdown("""
<style>
/* 全体の背景色 */
.stApp {
    background-color: #f7f8fa;
    font-family: "Hiragino Sans", "Noto Sans JP", sans-serif;
}

/* タイトルデザイン */
h1 {
    color: #1a1a1a;
    text-align: center;
    font-size: 2.2rem !important;
    letter-spacing: 1px;
    margin-bottom: 1rem;
}

/* セクション見出し */
h3, h4 {
    color: #333333;
    border-left: 6px solid #005BAC;
    padding-left: 10px;
    margin-top: 2rem;
    margin-bottom: 0.8rem;
    font-weight: 600;
}

/* データフレーム（テーブル）の装飾 */
.dataframe {
    border-radius: 10px;
    overflow: hidden;
}

/* ボタンデザイン */
div[data-testid="stButton"] > button {
    background-color: #005BAC;
    color: white;
    border-radius: 10px;
    padding: 10px 24px;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    transition: background-color 0.2s ease;
}
div[data-testid="stButton"] > button:hover {
    background-color: #004080;
}

/* フッターテキスト */
.footer {
    text-align: center;
    font-size: 0.9rem;
    color: #777;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# アプリタイトル
# =========================
st.title("HD-Xワークショップ欠席管理")

st.write("#### 👥 全体の「欠席」を一覧で確認・編集できます。")
st.write("「欠席される方は」チェックボックスにチェックを入れて「保存」ボタンを押すと、自動的にデータが更新されます。")
st.markdown("---")

# =========================
# 名簿定義
# =========================
groups = {
    "1": ["木村儒宗", "田島美佑", "清水陽太", "岡村俊也", "光原聡人"],
    "2": ["大沼清子", "向田あづさ", "鈴木裕太", "宮崎真緒", "田上孝", "山邉雅仁"],
    "3": ["杉本進悟", "荻原幹", "土屋竜之介", "相馬伸広", "山下大輔", "大石信子"],
    "4": ["京黒光槻", "宮亮太", "原圭祐", "國府方奈緒", "荒島淳", "奥村有美子"],
    "5": ["梅田知佳", "待野健太郎", "三村勝洋", "高崎翔太", "阿部貴史", "富永峻史", "山口嘉之"],
}
sessions = [f"第{i}回" for i in range(1, 6)]
csv_file = "attendance_matrix.csv"

# =========================
# CSV 初期化 or 読み込み
# =========================
all_records = []
for g, members in groups.items():
    for m in members:
        record = {"グループ": g, "名前": m}
        for s in sessions:
            record[s] = False
        all_records.append(record)
df_template = pd.DataFrame(all_records)

if not os.path.exists(csv_file):
    df_template.to_csv(csv_file, index=False, encoding="utf-8-sig")

df_attendance = pd.read_csv(csv_file)

# =========================
# 入力テーブル表示
# =========================
st.markdown("### 📝 欠席回を入力")

edited_df = st.data_editor(
    df_attendance,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",
    disabled=["グループ", "名前"],
    key="attendance_editor",
)

st.markdown("")

# =========================
# 保存ボタン
# =========================
if st.button("💾 保存"):
    edited_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    st.success("✅ データを保存しました！")

# =========================
# 一覧表示（保存後も常時表示）
# =========================
st.markdown("### 📋 登録済みデータ（全体一覧）")
st.dataframe(edited_df, use_container_width=True)

# =========================
# フッター
# =========================
st.markdown('<div class="footer">© 2025 HD-X Workshop Attendance Manager</div>', unsafe_allow_html=True)
