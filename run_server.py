import http.server
import socketserver
import webbrowser
import os
from weather_map import main as update_weather

# 날씨 데이터 업데이트
update_weather()

# 웹 서버 설정
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

# 웹 서버 시작
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"서버가 http://localhost:{PORT} 에서 실행 중입니다.")
    # 자동으로 브라우저 열기
    webbrowser.open(f'http://localhost:{PORT}')
    # 서버 실행
    httpd.serve_forever() 