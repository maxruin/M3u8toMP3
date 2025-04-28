import re

# 先在外面定義好要過濾的模式
IGNORE_PATTERNS = [
    re.compile(r'Queue input is backward in time'),
    re.compile(r'non monotonically increasing dts'),
    re.compile(r'Last message repeated'),
]

# 讀取並輸出 ffmpeg 狀態到 console
def log_ffmpeg(stderr_pipe):
    for raw in stderr_pipe:
        try:
            line = raw.decode('utf-8', errors='ignore').strip()
        except AttributeError:
            line = str(raw).strip()

        # 如果符合任何一個過濾模式，就跳過不印
        if any(p.search(line) for p in IGNORE_PATTERNS):
            continue

        print(line)