import folium
import networkx as nx
import math
import time
from IPython.display import display, clear_output
import requests
import re

# 두 좌표 사이의 조건에 따라 새로운 좌표를 찾는 함수
def find_point_with_condition(point_A, point_B, ratio=0.8):
    if point_A[0] > point_B[0] and point_A[1] < point_B[1]:
        new_point_A = (
            point_A[0] - ratio * (point_A[0] - point_B[0]),
            point_A[1] + ratio * (point_B[1] - point_A[1])
        )
    elif point_A[0] > point_B[0]:
        new_point_A = (
            point_A[0] - ratio * (point_A[0] - point_B[0]),
            point_A[1] - ratio * (point_A[1] - point_B[1])
        )
    elif point_A[0] < point_B[0] and point_A[1] > point_B[1]:
        new_point_A = (
            point_A[0] + ratio * (point_B[0] - point_A[0]),
            point_A[1] - ratio * (point_A[1] - point_B[1])
        )
    else:
        new_point_A = (
            point_A[0] + ratio * (point_B[0] - point_A[0]),
            point_A[1] + ratio * (point_B[1] - point_A[1])
        )
    return new_point_A

# Waypoints의 좌표 설정
coordinates = {
    1: (36.14393, 128.3935),
    2: (36.143805, 128.394),
    3: (36.14354, 128.3932),
    4: (36.14578, 128.3926),
    5: (36.14595, 128.3929),
    6: (36.14621, 128.3926),
    7: (36.14609, 128.392),
    8: (36.14536, 128.3932),
    9: (36.14534, 128.392838),
    10: (36.14555, 128.39323),
    11: (36.14597, 128.39316),
    12: (36.14327, 128.39408),
    13: (36.14329, 128.39348),
    14: (36.14345, 128.39408),
    15: (36.14376, 128.39416),
    16: (36.14343, 128.39313),
    17: (36.14465, 128.39226),
    18: (36.14451, 128.39334),
    19: (36.144907, 128.39327634),
    20: (36.14364, 128.3928),
    21: (36.1438, 128.39257),
    22: (36.14425, 128.39238),
    23: (36.14394, 128.39247),
    24: (36.14531, 128.392068),
    25: (36.145685, 128.392),
    'db_2': (36.14548, 128.3928),
    27: (36.14311, 128.39374),
    28: (36.14667, 128.39165),
    29: (36.14667, 128.39155),
    30: (36.14605, 128.39188),
    31: (36.14620, 128.3924),
    32: (36.14628, 128.3931),
    33: (36.14613, 128.393155),
    34: (36.14626, 128.3929),
    35: (36.14571, 128.3923),
    36: (36.145685, 128.392),
    37: (36.14571, 128.3923),
    38: (36.14531, 128.392508),
    39: (36.14531, 128.392400),
    40 : (36.14498, 128.3922),
    41 :(36.14558, 128.3920),
    42: (36.14558, 128.3922),
    43: (36.14566, 128.3921),
    44: (36.14360, 128.3941),
    45: (36.14372, 128.3942),
    46: (36.14335, 128.3933),
    47: (36.14359, 128.3930)
   
}
# 그래프 생성
G = nx.Graph()

# 노드 추가
for node, coord in coordinates.items():
    G.add_node(node, pos=coord)

# 각 노드에 대해 가장 가까운 이웃을 찾아 간선 추가
for node1 in G.nodes:
    distances = [
        (node2, math.sqrt((coordinates[node1][0] - coordinates[node2][0])**2 + (coordinates[node1][1] - coordinates[node2][1])**2))
        for node2 in G.nodes if node1 != node2
    ]
    closest_neighbors = sorted(distances, key=lambda x: x[1])[:2]

    for neighbor, distance in closest_neighbors:
        # 조건이 만족되면 간선 추가
        if node1 not in [4, 5, 6, 25, 26, 35, 7, 38, 24, 42] or neighbor not in [4, 5, 6, 7, 25, 26, 35, 38, 24, 42]:
            G.add_edge(node1, neighbor, weight=distance)

# 목적지와 중심점 설정
end_node = 1
center = [36.14540, 128.3916]

# 초기 설정
start_node = 3
shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
center_lat, center_lon = sum(coord[0] for coord in coordinates.values()) / len(coordinates), sum(coord[1] for coord in coordinates.values()) / len(coordinates)
mymap = folium.Map(location=[center_lat, center_lon], zoom_start=15)

# GPS 좌표에서 가장 가까운 노드를 찾는 함수
def find_closest_node(gps_node, coordinates):
    min_distance = float('inf')
    closest_node = None
    for node, coord in coordinates.items():
        distance = math.sqrt((gps_node[0] - coord[0])**2 + (gps_node[1] - coord[1])**2)
        if distance < min_distance:
            min_distance = distance
            closest_node = node
    return closest_node

# Google Geolocation API를 사용하여 현재 위치를 가져오는 함수
def get_geolocation():
    GOOGLE_API_KEY = "AIzaSyC6HoA5U0zlPfJzP7vXWAzqjggPzaMzYMQ"
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}'
    data = {'considerIp': True}
    result = requests.post(url, data).text
    return result

# Google Geolocation API 결과를 파싱하는 함수
def parse_geolocation(result):
    coordinates = [float(re.sub("[^0-9.]", "", i)) for i in result.split("\n") if "lat" in i or "lng" in i]
    return coordinates

# 지도를 업데이트하고 현재 위치를 표시하는 함수
def update_map(mymap, G, coordinates, start_node, end_node, gps_node):
    mymap = folium.Map(location=[center_lat, center_lon], zoom_start=15)

    # 회색으로 간선 그리기
    for edge in G.edges:
        node1, node2 = edge
        folium.PolyLine([coordinates[node1], coordinates[node2]], color="gray", weight=2, opacity=0.5).add_to(mymap)

    # 파란색으로 현재 경로 그리기
    for i in range(len(shortest_path) - 1):
        node1, node2 = shortest_path[i], shortest_path[i + 1]
        folium.PolyLine([coordinates[node1], coordinates[node2]], color="blue", weight=2.5).add_to(mymap)

    # 빨간색 마커로 GPS 노드 표시
    folium.Marker(gps_node, popup='GPS Node', icon=folium.Icon(color='red')).add_to(mymap)

    # Waypoints에 대한 마커 표시
    for waypoint, coord in coordinates.items():
        folium.Marker(coord, popup=f'Waypoint {waypoint}').add_to(mymap)

    # 업데이트된 지도 표시
    display(mymap)

# GPS 노드가 목적지에 가까울 때까지 업데이트 루프 실행
try:
    while True:
        # 현재 GPS 위치 가져오기
        result = get_geolocation()
        gps_loc = parse_geolocation(result)

        # GPS 노드를 중심으로 가장 가까운 좌표를 찾아서 최종 현재 위치로 설정
        closest_node = find_closest_node(gps_loc, coordinates)
        final_loc = coordinates[closest_node]

        # 시작 노드 업데이트
        start_node = closest_node

        # 현재 시작 노드가 목적지와 동일한지 확인
        if start_node == end_node:
            print("목적지에 도착했습니다. 루프를 종료합니다.")
            break

        # 업데이트된 시작 노드로 최단 경로 찾기
        shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')

        # 지도 업데이트 및 표시
        update_map(mymap, G, coordinates, start_node, end_node, final_loc)

        # 20초 대기
        time.sleep(20)
        clear_output(wait=True)
except KeyboardInterrupt:
    pass  # 키보드 인터럽트를 처리하여 루프를 중지합니다.
