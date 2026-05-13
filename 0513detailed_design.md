# 詳細設計書

## 1. API仕様

### 1.1. POST /tasks タスクをJSONファイルに保存する

リクエスト：
```
POST http://localhost:8001/tasks
Content-Type: application/json
```

```json
{
    "content": "XXさんにoo時に電話をかける",
    "category": "仕事",
    "priority": "高",
}
```

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| content | 文字列 | ○ | 問い合わせ本文（空不可）|
| category | 文字列 | ○ | カテゴリ（仕事／プライベート／その他） |
| priority | 文字列 | ○ | 優先度（高／中／低） |

レスポンス（成功 201）:
```json
{
    "id": 0001,
    "created_at": "2026-05-11T10:00:00+09:00",
    "content": "XXさんにoo時に電話をかける",
    "category": "仕事",
    "priority": "高",
    "status": "未完了"
}
```

エラーレスポンス:
| ステータス | 発生条件 |
|---|---|
| 422 | JSONの内容が不正 |
| 500 | サーバーの内部のエラー |

### 1.2. GET /tasks タスク一覧を返す

リクエスト：
```
GET http://localhost:8001/tasks
```

レスポンス（成功 200）:
```json
[
    {
        "id": 0002,
        "created_at": "2026-05-11T10:00:00+09:10",
        "content": "PCパスワードを更新する",
        "category": "仕事",
        "priority": "高",
        "status": "未完了"
    },
    {
        "id": 0001,
        "created_at": "2026-05-11T10:00:00+09:00",
        "content": "XXさんにoo時に電話をかける",
        "category": "仕事",
        "priority": "高",
        "status": "未完了"
    }
]
```

エラーレスポンス:
| ステータス | 発生条件 |
|---|---|
| 500 | サーバーの内部のエラー |


### 1.3. GET /tasks/{id} 指定IDのタスク詳細を返す

リクエスト：
```
POST http://localhost:8001/tasks/0001
```

レスポンス（成功 200）:
```json
{
    "id": 0001,
    "created_at": "2026-05-11T10:00:00+09:00",
    "content": "XXさんにoo時に電話をかける",
    "category": "仕事",
    "priority": "高",
    "status": "未完了"
}
```

エラーレスポンス:
| ステータス | 発生条件 |
|---|---|
| 404 | そのIDのタスクがJSONファイル内に存在しない |
| 500 | サーバーの内部のエラー |


### 1.4. PUT /done タスクのステータスを完了にする

リクエスト：
```
POST http://localhost:8001/done
Content-Type: application/json
```

```json
{
    "id": 0001,
    "created_at": "2026-05-11T10:00:00+09:00",
    "content": "XXさんにoo時に電話をかける",
    "category": "仕事",
    "priority": "高",
    "status": "未完了"
}
```

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| id | 整数 | ○ | タスクID（自動採番） |
| created_at | 文字列（ISO 8601） | ○ | 登録日時 |
| content | 文字列 | ○ | 問い合わせ本文（空不可）|
| category | 文字列 | ○ | カテゴリ（仕事／プライベート／その他） |
| priority | 文字列 | ○ | 優先度（高／中／低） |
| status | 文字列 | ○ | ステータス（未完了／完了）ただしデフォルトは未完了 |

レスポンス（成功 200）:
```json
{
    "id": 0001,
    "created_at": "2026-05-11T10:00:00+09:00",
    "content": "XXさんにoo時に電話をかける",
    "category": "仕事",
    "priority": "高",
    "status": "完了"
}
```

エラーレスポンス:
| ステータス | 発生条件 |
|---|---|
| 404 | そのIDのタスクがJSONファイル内に存在しない |
| 422 | JSONの内容が不正 |
| 500 | サーバーの内部のエラー |

---

## 2. データモデル

```Python
from pydantic import BaseModel

class InquiryRequest(BaseModel):
    content: str           # POST リクエストボディ
    category: str
    priority: str

class InquiryRecord(BaseModel):
    id: int
    created_at: str
    content: str
    category: str
    priority: str
    status: str
```

---

## 3. データ操作処理

JSONファイルの読み込み・書き込みの処理手順を示す。

### 3.1. 全件読み込み

3.3., 3.4., 3.5.にて最初に行う全件読み込みの手順をこの項に示す。

1. DATA_FILE_PATH のファイルが存在するか確認する
2. 存在しない場合は空のリスト [] を返す
3. 存在する場合は json.load() で読み込んでリストを取得する
4. リストを返す

### 3.2. 一覧表示機能

1. DATA_FILE_PATH のファイルが存在するか確認する
2. 存在しない場合は空のリスト [] を返す
3. 存在する場合は json.load() で読み込んでリストを取得する
4. IDの降順（新しい順）に並べ替えてリストに再代入する
    （sorted(data, key=lambda x: x["ID"], reverse=True)を用いる）
5. リストを返す

### 3.3. タスク登録機能

1. 全件読み込みを行いリストを取得する。
2. 新しいレコードをリストの末尾に append する
3. json.dump() でファイルに上書き保存する
   （ensure_ascii=False, indent=2を用いる）

### 3.4. 詳細表示機能

1. 全件読み込みを行いリストを取得する
2. id が一致するレコードを検索する
3. 見つかれば返す。見つからなければ None を返す

### 3.5. 完了更新機能

1. 全件読み込みを行いリストを取得する
2. リストの中から、詳細画面で取得したレコードと同じ ID の辞書を探す
3. 該当IDの辞書に対して、"status"に対応する値を"完了"に更新する
4. 更新後のリストを json.dump() でファイルに上書き保存する
5. 更新した辞書を返す。見つからなければ None を返す

---

## 4. 画面詳細

### 4.1. サイドバー

```Python
st.sidebar.title("メニュー")
page = st.sidebar.radio("ページ", ["タスク入力画面","タスク一覧画面"])
```

### 4.2. タスク入力画面

```Python
if page == "タスク入力画面"
    st.title("タスク入力")

    content = st.text_area("タスクを入力してください", height=150)
    category = st.selectbox("カテゴリ", ["仕事", "プライベート", "その他"])
    priority = st.selectbox("優先度", ["高", "中", "低"])

    if st.button("登録する"):
        if content.strip() == "":
            st.error("空欄では登録できません。")
        else:
            response = POST /tasks に content, category, priority を送信
            if response.ok:
                data = response.json()
                st.success("登録が完了しました")
            else:
                st.error("登録に失敗しました。")
```

### 4.3. タスク一覧画面

```Python
if page == "タスク一覧画面":
    st.title("タスク一覧")
    response = GET /tasksに全タスクを取りに行く
    if response.status_code == 200:
        tasks = response.json
        if tasks:
            for record in tasks
                if st.button(record["content"]): # タスクのタイトルをボタンにが書いてある。もし押されたら
                    st.session_state.id = record["id"]
                    st.session_state.page = "タスク詳細画面" #タスク詳細画面に遷移
        else:
            st.write("まだタスクはありません")
```

### 4.4. タスク詳細画面

```Python
if st.session_state.page == "タスク詳細画面":
    st.title("タスク詳細")
    response = GET /tasksに全タスクを取りに行く
    if response.status_code == 200:
        tasks = response.json
        for record in tasks:
            if record["ID"] == st.session_state.page:
                st.write(f"ID: {record["ID"]}")
                st.write(f"日付: {record["created_at"]}")
                st.write(f"タイトル: {record["content"]}")
                st.write(f"カテゴリ: {record["category"]}")
                st.write(f"優先度: {record["category"]}")
                st.write(f"ステータス: {record["status"]}")
                if record["status"] == "未完了":
                    if st.button("✓ステータスを完了にする"):
                        ステータスを完了に更新
```

---

## 5. エラー処理一覧

| No | 発生箇所 | エラー内容 | 処理内容 | ユーザー表示 |
|---|---|---|---|---|
| 1 | Streamlit | タスクタイトルが空 | 登録せずに停止 | 「空欄では登録できません。」 |
| 2 | FastAPI | 登録時、FastAPIとStreamlit間の接続エラー | 接続できなかった場合の条件分岐にて処理。登録はしない | 「登録に失敗しました。」 |
| 3 | FastAPI | dataフォルダが存在しない | dataフォルダを新しく生成して処理を続行する | （エラーなし） |
| 4 | FastAPI | JSONファイルが存在しない | 空リストとして続行 | （エラーなし） |
| 5 | FastAPI | 指定IDが存在しない | 404 を返す | 「指定のタスクが見つかりません。」 |

---

## 6. テスト観点

### 6.1. 正常系テスト
| No | テスト内容 | 確認ポイント |
|---|---|---|
| 1 | タスクを登録する | 登録完了が表示されること |
| 2 | 登録後に一覧画面を表示する | 登録したタスクが、日付の降順に正しく表示されること　|
| 3 | 一覧画面から詳細画面を表示する | 全フィールドが正しく表示されること |
| 4 | 詳細画面から一覧画面を表示する | タスク一覧が正しく表示されること |
| 5 | 一覧画面から入力画面を表示する | 新規のタスク入力ができること |
### 6.2. 異常系テスト
| No | テスト内容  | 確認ポイント |
|---|---|---|
| 4 | 空のまま登録ボタンを押す | エラーメッセージが表示され、登録されないこと |
| 5 | JSONファイルがない状態で一覧を開く | エラーにならず「まだタスクはありません」と表示されること |
| 6 | JSONが空リストの状態で一覧を開く | 「まだタスクはありません」と表示されること |
### 6.3. 品質確認テスト


---