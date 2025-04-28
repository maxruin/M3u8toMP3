import os, json

# 存放串流設定的 JSON 檔案
JSON_FILE = 'setting/radio.json'

# 載入 streams 設定
def load_streams():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# 將 streams 寫回 JSON
def save_streams(streams):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(streams, f, ensure_ascii=False, indent=2)