import requests, re
import StreamList as sl
import utils.HttpUtil as httpUtil

# 廣播列表
streams = sl.load_streams()

# 更新串流 URL
def update_streams(new_url, name):
    if new_url:
        updated = False
        for s in streams:
            if s.get('name') == name:
                if s.get('url') != new_url:
                    s['url'] = new_url
                    updated = True
                break
        if not updated and not any(s.get('name') == name for s in streams):
            streams.append({'name': name, 'url': new_url})
            updated = True
        if updated:
            sl.save_streams(streams)

# BestRadio 好事 最新串流 URL
def fetch_best_radio_url(channel):
    try:
        name = ''
        pattern = ''
        if channel == '1':
            name = '台北好事 989'
            pattern = r'https://bestradiow-hichannel\.cdn\.hinet\.net/live/RA000013/playlist\.m3u8[^" ]*'
        elif channel == '2':
            name = '台中好事 903'
            pattern = r'https://bestradiow-hichannel\.cdn\.hinet\.net/live/RA000010/playlist\.m3u8[^" ]*'
        resp = requests.get('http://www.bestradio.com.tw/', timeout=5)
        text = resp.text
        # print("BestRadio 網頁內容：", text)  # Debug: 印出網頁內容
        match = re.search(pattern, text)
        if match:
            new_url = match.group(0)
            print(f"{name} 最新串流 URL: {new_url}")
            return new_url
        else:
            print("無法找到 {name} 最新串流 URL")
    except Exception as e:
        print(f"Fetch {name} 失敗: {e}")
    return None

# BestRadio HitFM 最新串流 URL
def fetch_hit_radio_url(channel):
    try:
        name = 'HitFM'
        if channel == '1':
            name = 'HitFM 北部'
        elif channel == '2':
            name = 'HitFM 中部'
        print(f"{channel=} {name=}")
        resp = httpUtil.post('https://www.hitoradio.com/newweb/hichannel.php', {'channelID': channel, 'action': 'getLIVEURL'})
        if resp:
            new_url = resp
            print(f"{name} 最新串流 URL: {new_url}")
            return new_url
        else:
            print("無法找到 {name} 最新串流 URL")
    except Exception as e:
        print(f"Fetch {name} 失敗: {e}")
    return None

# Kiss 最新串流 URL
def fetch_kiss_radio_url():
    try:
        name = 'Kiss'
        pattern = r'https://kissradiow-hichannel\.cdn\.hinet\.net/live/RA000040/playlist\.m3u8[^" ]*'
        resp = requests.get('https://www.kiss.com.tw/test/hichannel2.php?api=1', timeout=5)
        text = resp.text
        match = re.search(pattern, text)
        if match:
            new_url = match.group(0)
            print(f"{name} 最新串流 URL: {new_url}")
            return new_url
        else:
            print("無法找到 {name} 最新串流 URL")
    except Exception as e:
        print(f"Fetch {name} 失敗: {e}")
    return None

# 中廣音樂網 i radio 最新串流 URL
def fetch_i_radio_url():
    try:
        name = '中廣音樂網 i radio'
        data = httpUtil.get_cffi('https://api.instant.audio/data/streams/142/i-bcc-music-network')
        url = data.get('result').get('streams')[1].get('url')
        if url:
            print(f"{name} 最新串流 URL: {url}")
            return url
        else:
            print("無法找到 {name} 最新串流 URL")
    except Exception as e:
        print(f"Fetch {name} 失敗: {e}")
    return None

def fetch_all():
    update_streams(fetch_best_radio_url('1'), 'BestRadio 台北好事 989')
    update_streams(fetch_best_radio_url('2'), 'BestRadio 台中好事 903')
    update_streams(fetch_hit_radio_url('1'), 'HitFM 北部')
    update_streams(fetch_hit_radio_url('2'), 'HitFM 中部')
    update_streams(fetch_kiss_radio_url(), 'Kiss')
    update_streams(fetch_i_radio_url(), '中廣音樂網 i radio')


if __name__ == "__main__":
    fetch_all()