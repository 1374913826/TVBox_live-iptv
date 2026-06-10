import http.server
import socketserver
import urllib.request
import os

# 1. 定义需要自动拉取的 16 个直播源链接
URLS = [
    "https://gh-proxy.com/raw.githubusercontent.com/alenin-zhang/IPTV/master/lenin.txt",
    "https://gh-proxy.com/raw.githubusercontent.com/develop202/migu_video/refs/heads/main/interface.txt",
    "http://rihou.cc:555/gggg.nzk",
    "http://tvv.tw/github.com/fafa002/yf2025/blob/main/yiyifafa.txt",
    "https://d.kstore.dev/download/8344/1电信酒店.txt",
    "https://40.tv1288.xyz/",
    "https://php.946985.filegear-sg.me/jackTV.m3u",
    "http://iptv.4666888.xyz/FYTV.txt",
    "https://gh-proxy.com/raw.githubusercontent.com/Jsnzkpg/Jsnzkpg/Jsnzkpg/Jsnzkpg1.m3u",
    "http://ge.html-5.me//ii/黄蚂蚁先锋推流源.txt",
    "https://2026.tv1288.xyz",
    "https://gitee.com/OscarWilde/itv/raw/master/tv.txt",
    "https://live.ottiptv.cc/iptv.m3u?userid=7601455084&sign=8d90bbf8aeac077cf2f4cc84a6a67a9ef5cdf776237a4c716b75a37c33c5c3044f0630b937bb210c795ead158d3bf3fdc9ef716881d7f57e146ae978afcc3e31526b2cdae71fd0&auth_token=47968e58f2b34cace69dbe0d0fc69b93",
    "https://123.tv1288.xyz/jav.txt",
    "https://gh-proxy.com/raw.githubusercontent.com/alenin-zhang/IPTV/master/10000.txt",
    "https://gh-proxy.com/raw.githubusercontent.com/alenin-zhang/IPTV/master/30000.txt"
]

def update_live_txt():
    """自动拉取所有源并合并保存到 live.txt"""
    print("🔄 开始拉取网络直播源...")
    all_content = ""
    
    for url in URLS:
        try:
            # 模拟浏览器请求，防止有些网站拦截
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=8) as response:
                # 获取网页内容并解码
                content = response.read().decode('utf-8', errors='ignore')
                all_content += content + "\n"
                print(f"✅ 成功拉取: {url[:40]}...")
        except Exception as e:
            print(f"❌ 拉取失败: {url[:40]}... 原因: {e}")
            
    # 把所有拉取到的内容写入到 live.txt 文件中（覆盖写入）
    with open("live.txt", "w", encoding="utf-8") as f:
        f.write(all_content)
    print("💾 live.txt 更新并保存成功！\n")

class MyHandler(http.server.SimpleHTTPRequestHandler):
    """网页展示逻辑（保留你中午的功能）"""
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # 读取刚刚更新好的 live.txt
            live_data = ""
            if os.path.exists("live.txt"):
                with open("live.txt", "r", encoding="utf-8") as f:
                    live_data = f.read()
            
            # 简易的网页 HTML 模板
            html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Web TV 直播源</title></head>
            <body>
                <h1>🎬 我的电视直播源 (已自动更新)</h1>
                <hr>
                <pre>{live_data}</pre>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            # 其他静态文件请求
            super().do_GET()

if __name__ == "__main__":
    # 第一步：先拉取更新数据
    update_live_txt()
    
    # 第二步：启动网页服务器
    PORT = 8000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"🚀 Web TV 服务器已启动！请在浏览器访问: http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 服务器已关闭。")
