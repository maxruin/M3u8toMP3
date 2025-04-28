from flask import Flask, Response, stream_with_context, request, redirect, url_for, render_template_string
import subprocess
import os
import threading
import Functions as func
import StreamList as sl
import FetchRadioUrl as fetch


# 外部 HTML 模板檔案
TEMPLATE_FILE = 'setting/setting.html'

# 若 stream name 在此列表中，啟用 HTTP 持久連線
PERSISTENT_NAMES = [
    'BestRadio 台中好事 903',
    # 可在此添加其他名稱
]

# 抓取最新串流 URL
fetch.fetch_all()
# 廣播列表
streams = sl.load_streams()
# 當前播放的 URL
active_url = streams[0]['url'] if streams else None


app = Flask(__name__)
@app.route('/')
def audio_feed():
    global active_url
    url = active_url or (streams[0]['url'] if streams else None)
    if not url:
        return "<p>尚未設定任何串流，請先在 <a href='/settings.html'>設定頁面</a> 新增。</p>", 400

    # 根據 active_url 找到對應名稱
    active_name = None
    for s in streams:
        if s.get('url') == url:
            active_name = s.get('name')
            break

    # 建構 ffmpeg cmd
    cmd = ["ffmpeg", "-re"]
    # 如果名稱在 PERSISTENT_NAMES，加入 http_persistent 參數
    if active_name in PERSISTENT_NAMES:
        cmd.extend(["-http_persistent", "1"])
    cmd.extend([
        # 不顯示 banner
        "-hide_banner",
        # 只輸出錯誤訊息，忽略 warning/info/log
        "-loglevel", "info",
        # 不印出進度統計
        "-nostats",
        
        # 強制無限迴圈（如果 playlist 真的是 finite，可以用這招不讓它結束）
        # "-stream_loop", "-1",                          # :contentReference[oaicite:0]{index=0}

        # 協議白名單
        # "-protocol_whitelist", "file,http,https,tcp,tls",

        # HLS demuxer 選項（要放在 -i 前面才管用）
        # "-allowed_extensions", "ALL",                  # 允許所有副檔名載入段檔 :contentReference[oaicite:1]{index=1}
        # "-live_start_index", "0",                      # 從最舊 segment 開始讀 :contentReference[oaicite:2]{index=2}
        # "-max_reload", "999999",                       # 重試重新載入 playlist 的次數（預設 1000）&#8203;:contentReference[oaicite:3]{index=3}
        # "-http_multiple", "1",                         # 多連線下載 segment :contentReference[oaicite:4]{index=4}
        # "-http_seekable", "0",                         # 關閉 partial request，強制整段下載 :contentReference[oaicite:5]{index=5}

        # 增大解碼隊列，避免 I/O 阻塞
        # "-thread_queue_size", "4096",

        # 低延遲模式：不額外緩衝、直接寫入
        "-fflags", "nobuffer+genpts",
        "-flags", "low_delay",
        "-avioflags", "direct",

        # 使用牆時鐘作為時間戳，讓重連時 pts 連續
        "-use_wallclock_as_timestamps", "1",

        # 讀檔逾時（微秒）
        "-rw_timeout", "5000000",

        # 重連設定
        "-reconnect", "1",
        "-reconnect_streamed", "1",
        "-reconnect_at_eof", "1",
        "-reconnect_delay_max", "2",

        # 輸入串流網址
        "-i", url,

        # 不要影像
        "-vn",

        # 音訊輸出選項
        "-ar", "44100",         # 重新採樣到 44.1kHz
        "-ac", "2",             # 立體聲
        "-f", "mp3",
        "-codec:a", "libmp3lame",
        "-b:a", "128k",

        # 輸出到 stdout
        "-"
    ])

    flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=flags,
        bufsize=0
    )

    # 啟動 ffmpeg 日誌輸出線程
    threading.Thread(target=func.log_ffmpeg, args=(proc.stderr,), daemon=True).start()

    def generate():
        try:
            while True:
                chunk = proc.stdout.read(4096)
                if not chunk:
                    break
                yield chunk
        finally:
            proc.kill()

    return Response(
        stream_with_context(generate()),
        mimetype='audio/mpeg'
    )

@app.route('/settings.html')
def settings():
    if not os.path.exists(TEMPLATE_FILE):
        return f"<p>未找到模板檔：{TEMPLATE_FILE}</p>", 500
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()
    return render_template_string(template, streams=streams, active=active_url)

@app.route('/add_stream', methods=['POST'])
def add_stream():
    global streams, active_url
    name = request.form['name'].strip()
    url = request.form['url'].strip()
    if name and url and not any(s['url'] == url for s in streams):
        streams.append({'name': name, 'url': url})
        sl.save_streams(streams)
        if active_url is None:
            active_url = url
    return redirect(url_for('settings'))

@app.route('/delete_stream', methods=['POST'])
def delete_stream():
    global streams, active_url
    url = request.form['url']
    streams = [s for s in streams if s['url'] != url]
    sl.save_streams(streams)
    if active_url == url:
        active_url = streams[0]['url'] if streams else None
    return redirect(url_for('settings'))

@app.route('/edit_stream', methods=['POST'])
def edit_stream():
    global streams, active_url
    old = request.form['old_url']
    new_name = request.form['new_name'].strip()
    new_url = request.form['new_url'].strip()
    for s in streams:
        if s['url'] == old:
            s['name'] = new_name or s['name']
            s['url'] = new_url or s['url']
            break
    sl.save_streams(streams)
    if active_url == old:
        active_url = new_url
    return redirect(url_for('settings'))

@app.route('/select_stream', methods=['POST'])
def select_stream():
    global active_url
    url = request.form['url']
    if url:
        active_url = url
    return redirect(url_for('settings'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3378, threaded=True)
