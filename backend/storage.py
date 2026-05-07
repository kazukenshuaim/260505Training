import json
from pathlib import Path
from datetime import datetime

DATA_PATH = Path("data/inquiries.json")  # プロジェクトルートからの相対パス.
    # data/inquiries.jsonをPathオブジェクトとして使い、これに問い合わせ履歴を蓄積
    # 「POST で JSON が来たら、その中に question という文字列があるはずだよ」とFastAPIにおしえる

def load_inquiries(): #JSONファイルから問い合わせ履歴を読み込む関数
    if not DATA_PATH.exists(): #ファイルがなければ空リストを
        return []
    with DATA_PATH.open("r", encoding="utf-8") as f: # "r"：読み込みモードでファイルを開く
        return json.load(f) #JSONをPythonのリストに変換して返す(例：[{"id":1, "question":"..."}]


def save_inquiry(question, category, priority, answer): #JSONに新しいデータを追加して保存
    inquiries = load_inquiries() #既存問い合わせ一覧取得
    new_id = len(inquiries) + 1 #新ID作成
    item = {                    #保存するデータを辞書形式で
        "id": new_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "category": category,
        "priority": priority,
        "answer": answer,
    }
    inquiries.append(item) #新しい問い合わせを既存の問い合わせ一覧に追加
    DATA_PATH.parent.mkdir(exist_ok=True)   #dataフォルダがなければ作る
        # exist_ok=True → 既にあってもエラーにしない
    with DATA_PATH.open("w", encoding="utf-8") as f:   # "w"：書き込みモードでファイルを開く
        json.dump(inquiries, f, ensure_ascii=False, indent=2)   # PythonのリストをJSONに変換して保存(ensure_ascii=False → 日本語をそのまま保存)
    return item #呼び出し元に「保存したデータ」を返す