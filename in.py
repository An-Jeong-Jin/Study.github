import networkx as nx
import matplotlib.pyplot as plt
import math

def execute_first_code():
    ###
    #### 최종1층임
    import networkx as nx
    import matplotlib.pyplot as plt
    import math

    # 좌표 설정
    coordinates = {
        1: (179, 215), 2: (145, 218), 3: (170, 165),
        4: (260, 160), 5: (305, 155), 6: (340, 153),
        7: (375, 152), 8: (400, 150), 9: (435, 146.4),
        10: (470, 143), 11: (500, 141), 12: (530, 139),
        13: (560, 136), 14: (598, 134), 15: (179, 535),
        16: (150, 535), 17: (179, 565), 18: (150, 605),
        19: (230, 559), 20: (260, 559), 21: (290, 559),
        22: (290, 559), 23: (320, 559), 24: (360, 559),
        25: (395, 559), 26: (420, 559), 27: (450, 559),
        28: (490, 559), 29: (525, 558), 30: (550, 558),
        31: (585, 558), 32: (625, 558), 33: (655, 558),
        34: (625, 575), 35: (95, 380), 36: (150, 380), 
        37: (220, 162), 38: (146, 300), 39:(120, 380),
        40: (150, 400), 41: (150, 420), 42: (150, 450),
        43: (150, 480), 44: (210, 560)
    }

    TT = []
    # 그래프 생성
    G = nx.Graph()

    # 노드 추가
    for node, coord in coordinates.items():
        G.add_node(node, pos=coord)

    # 각 노드에 대해 가장 가까운 두 개의 이웃 찾기
    for node1 in G.nodes:
        distances = [(node2, math.sqrt((coordinates[node1][0] - coordinates[node2][0])**2 + (coordinates[node1][1] - coordinates[node2][1])**2)) for node2 in G.nodes if node1 != node2]
        closest_neighbors = sorted(distances, key=lambda x: x[1])[:2]
        for neighbor, distance in closest_neighbors:
            G.add_edge(node1, neighbor, weight=distance)

    # 수동으로 시작 노드 선택
    start_node = int(input("Enter the starting node: "))

    # 지하 1층 목적지 여부 확인
    is_b1_destination = int(input("Is the destination in 1? (1 for Yes, 0 for No): "))

    if is_b1_destination:
        # 직접 목적지 입력
        end_node = int(input("Enter the destination node: "))
        
        # 최단 경로 찾기
        shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
        print("Follow this path:")
        print(shortest_path)
    else:
        # 1층 목적지가 없는 경우 가장 가까운 엘베나 계단으로 안내
        stairs_and_elevator_nodes = [14, 1, 3, 15]
        closest_stairs_or_elevator = min(stairs_and_elevator_nodes, key=lambda x: nx.shortest_path_length(G, source=start_node, target=x, weight='weight'))
        
        # 안내
        print(f"Navigate to the nearest stairs or elevator (Node {closest_stairs_or_elevator}) first.")
        shortest_path_to_stairs_or_elevator = nx.shortest_path(G, source=start_node, target=closest_stairs_or_elevator, weight='weight')
        print("Follow this path:")
        print(shortest_path_to_stairs_or_elevator)

    # 이미지 읽기
    image_path = '디지털관 1층.jpg'
    image = plt.imread(image_path)

    # 이미지 표시
    plt.imshow(image)

    # 간선 추가
    for edge in G.edges:
        node1, node2 = edge
        plt.plot([coordinates[node1][0], coordinates[node2][0]], [coordinates[node1][1], coordinates[node2][1]], color="gray", linewidth=2, alpha=0.5)

    # 최단 경로 추가
    if is_b1_destination:
        for i in range(len(shortest_path) - 1):
            node1, node2 = shortest_path[i], shortest_path[i + 1]
            plt.plot([coordinates[node1][0], coordinates[node2][0]], [coordinates[node1][1], coordinates[node2][1]], color="blue", linewidth=2.5)
        TT.append(end_node)  # 목적지 노드 추가
    else:
        for i in range(len(shortest_path_to_stairs_or_elevator) - 1):
            node1, node2 = shortest_path_to_stairs_or_elevator[i], shortest_path_to_stairs_or_elevator[i + 1]
            plt.plot([coordinates[node1][0], coordinates[node2][0]], [coordinates[node1][1], coordinates[node2][1]], color="blue", linewidth=2.5)
        TT.append(closest_stairs_or_elevator)  # 엘베나 계단 노드 추가

    # 시작 노드와 목표 노드 추가
    plt.scatter(coordinates[start_node][0], coordinates[start_node][1], color='green', s=100, marker='o', label='Start Node')
    if is_b1_destination:
        plt.scatter(coordinates[end_node][0], coordinates[end_node][1], color='red', s=100, marker='x', label='Destination Node')
    else:
        plt.scatter(coordinates[closest_stairs_or_elevator][0], coordinates[closest_stairs_or_elevator][1], color='red', s=100, marker='x', label='Nearest Stairs or Elevator')

    # 레이블 표시
    plt.legend()

    plt.show()
    print(TT)

    ###
    print("Executing the first code...")

def execute_second_code():
    ###
    ## 최종입 지하 1층
    import networkx as nx
    import matplotlib.pyplot as plt
    import math

    # 좌표 설정
    coordinates = {
        1: (165, 180), 2: (170, 525), 3: (165, 470), 4: (130, 525), 5: (130, 450), 
        6: (135, 350), 7: (175, 350), 8: (171, 265), 9: (170, 555), 10: (220, 555), 
        11: (255, 555), 12: (290, 555), 13: (320, 555), 14: (375, 555), 15: (410, 555), 
        16: (440, 555), 17: (470, 555), 18: (515, 555), 19: (550, 555), 20: (580, 555), 
        21: (620, 555), 22: (660, 555), 23: (700, 555), 24: (158, 120), 25: (188, 120), 
        26: (280, 125), 27: (320, 124), 28: (350, 122), 29: (440, 113), 30: (515, 110), 
        31: (590, 105), 32: (630, 105), 33: (645, 85), 34: (240, 120), 35: (240, 100), 
        36: (175, 300), 37: (175, 330), 38: (160, 350), 39: (148, 350), 40: (148, 370),
        41: (148, 390), 42: (148, 420), 43: (148, 460), 44: (148, 480), 45: (148, 510),
        46: (148, 550), 47: (148, 530), 48: (148, 470), 49: (148, 490), 50: (148, 500),
        51: (148, 510), 52: (148, 520), 53: (148, 540), 54: (155, 552), 55: (148, 430),
        56: (148, 440), 57: (148, 450), 58: (148, 410), 59: (148, 400), 60: (148, 380),
        61: (170, 220), 62: (170, 235), 63: (170, 250), 64: (173, 280)
    }

    TT = []
    # 그래프 생성
    G = nx.Graph()

    # 노드 추가
    for node, coord in coordinates.items():
        G.add_node(node, pos=coord)

    # 각 노드에 대해 가장 가까운 두 개의 이웃 찾기
    for node1 in G.nodes:
        distances = [(node2, math.sqrt((coordinates[node1][0] - coordinates[node2][0])**2 + (coordinates[node1][1] - coordinates[node2][1])**2)) for node2 in G.nodes if node1 != node2]
        closest_neighbors = sorted(distances, key=lambda x: x[1])[:2]
        for neighbor, distance in closest_neighbors:
            G.add_edge(node1, neighbor, weight=distance)

    # 수동으로 시작 노드 선택
    start_node = int(input("Enter the starting node: "))

    # 지하 1층 목적지 여부 확인
    is_b1_destination = int(input("Is the destination in 1? (1 for Yes, 0 for No): "))

    if is_b1_destination:
        # 직접 목적지 입력
        end_node = int(input("Enter the destination node: "))
        
        # 최단 경로 찾기
        shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
        print("Follow this path:")
        print(shortest_path)
    else:
        # 1층 목적지가 없는 경우 가장 가까운 엘베나 계단으로 안내
        stairs_and_elevator_nodes = [33, 1, 25, 3, 2, 22]
        closest_stairs_or_elevator = min(stairs_and_elevator_nodes, key=lambda x: nx.shortest_path_length(G, source=start_node, target=x, weight='weight'))
        
        # 안내
        print(f"Navigate to the nearest stairs or elevator (Node {closest_stairs_or_elevator}) first.")
        shortest_path_to_stairs_or_elevator = nx.shortest_path(G, source=start_node, target=closest_stairs_or_elevator, weight='weight')
        print("Follow this path:")
        print(shortest_path_to_stairs_or_elevator)

    # 이미지 읽기
    image_path = '디지털관 지하 1층.jpg'
    image = plt.imread(image_path)

    # 이미지 표시
    plt.imshow(image) 

    # 간선 추가
    for edge in G.edges:
        node1, node2 = edge
        plt.plot([coordinates[node1][0], coordinates[node2][0]], [coordinates[node1][1], coordinates[node2][1]], color="gray", linewidth=2, alpha=0.5)

    # 최단 경로 추가
    if is_b1_destination:
        for i in range(len(shortest_path) - 1):
            node1, node2 = shortest_path[i], shortest_path[i + 1]
            plt.plot([coordinates[node1][0], coordinates[node2][0]], [coordinates[node1][1], coordinates[node2][1]], color="blue", linewidth=2.5)
        TT.append(end_node)  # 목적지 노드 추가
    else:
        for i in range(len(shortest_path_to_stairs_or_elevator) - 1):
            node1, node2 = shortest_path_to_stairs_or_elevator[i], shortest_path_to_stairs_or_elevator[i + 1]
            plt.plot([coordinates[node1][0], coordinates[node2][0]], [coordinates[node1][1], coordinates[node2][1]], color="blue", linewidth=2.5)
        TT.append(closest_stairs_or_elevator)  # 엘베나 계단 노드 추가

    # 시작 노드와 목표 노드 추가
    plt.scatter(coordinates[start_node][0], coordinates[start_node][1], color='green', s=100, marker='o', label='Start Node')
    if is_b1_destination:
        plt.scatter(coordinates[end_node][0], coordinates[end_node][1], color='red', s=100, marker='x', label='Destination Node')
    else:
        plt.scatter(coordinates[closest_stairs_or_elevator][0], coordinates[closest_stairs_or_elevator][1], color='red', s=100, marker='x', label='Nearest Stairs or Elevator')

    # 레이블 표시
    plt.legend()
    
    #plt.show()
    print(TT)

    ###
    print("Executing the second code...")

while True: 
    user_input = input("Enter '1' to execute the first code, '2' to execute the second code, or 'quit' to exit: ")

    if user_input.lower() == 'quit':
        break
    elif user_input == '1':
        execute_first_code()
    elif user_input == '2':
        execute_second_code()
    else:
        print("Invalid input. Please enter '1', '2', or 'quit'.")
