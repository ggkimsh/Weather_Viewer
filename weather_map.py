import requests
import folium
from folium.plugins import HeatMap
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# 기상청 API 키를 환경 변수에서 로드
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

def get_weather_data():
    """기상청 API를 통해 전국 날씨 데이터를 가져옵니다."""
    # 기상청 API 엔드포인트
    url = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getAsosHourlyInfo"
    
    # 현재 시간 기준으로 데이터 요청
    now = datetime.now()
    params = {
        'serviceKey': API_KEY,
        'pageNo': '1',
        'numOfRows': '100',
        'dataType': 'JSON',
        'dataCd': 'ASOS',
        'dateCd': 'HR',
        'startDt': now.strftime('%Y%m%d'),
        'startHh': '00',
        'endDt': now.strftime('%Y%m%d'),
        'endHh': '23',
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 데이터 추출 및 가공
        weather_data = []
        for item in data['response']['body']['items']['item']:
            if 'tm' in item and 'ta' in item and 'hm' in item and 'stnNm' in item:
                weather_data.append({
                    'station': item['stnNm'],
                    'temperature': float(item['ta']),
                    'humidity': float(item['hm']),
                    'time': item['tm']
                })
        
        return weather_data
    except Exception as e:
        print(f"날씨 데이터를 가져오는 중 오류 발생: {e}")
        return []

def create_weather_map(weather_data):
    """날씨 데이터를 지도에 시각화합니다."""
    # 한국 중심 좌표로 지도 생성
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    
    # 기상 관측소 좌표 데이터
    station_coords = {
        '서울': [37.5665, 126.9780],
        '부산': [35.1796, 129.0756],
        '인천': [37.4563, 126.7052],
        '대구': [35.8714, 128.6014],
        '광주': [35.1595, 126.8526],
        '대전': [36.3504, 127.3845],
        '울산': [35.5384, 129.3114],
        '세종': [36.4801, 127.2892],
        '경기': [37.4138, 127.5183],
        '강원': [37.8228, 128.1555],
        '충북': [36.6357, 127.4914],
        '충남': [36.6588, 126.6728],
        '전북': [35.8242, 127.1480],
        '전남': [34.8161, 126.4629],
        '경북': [36.5760, 128.5059],
        '경남': [35.2382, 128.6924],
        '제주': [33.4996, 126.5312]
    }
    
    # 각 관측소의 날씨 정보를 지도에 표시
    for data in weather_data:
        station = data['station']
        if station in station_coords:
            lat, lon = station_coords[station]
            temp = data['temperature']
            humidity = data['humidity']
            
            # 팝업 내용 생성
            popup_content = f"""
            <div style="font-family: 'Noto Sans KR', sans-serif;">
                <h4 style="margin-bottom: 10px;">{station}</h4>
                <p style="margin: 5px 0;">🌡️ 온도: {temp}°C</p>
                <p style="margin: 5px 0;">💧 습도: {humidity}%</p>
                <p style="margin: 5px 0; font-size: 0.8em; color: #666;">
                    업데이트: {data['time']}
                </p>
            </div>
            """
            
            # 마커 생성
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
    
    # 지도를 HTML 파일로 저장
    m.save('map.html')
    print("지도가 'map.html' 파일로 저장되었습니다.")

def main():
    # 날씨 데이터 가져오기
    weather_data = get_weather_data()
    
    if weather_data:
        # 지도 생성
        create_weather_map(weather_data)
    else:
        print("날씨 데이터를 가져오지 못했습니다.")

if __name__ == "__main__":
    main() 