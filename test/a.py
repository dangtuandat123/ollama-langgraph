import plotly.graph_objects as go
import networkx as nx

# Tạo đồ thị
G = nx.DiGraph()
G.add_edges_from([(1, 2), (2, 3), (3, 4), (2, 5)])

# Vị trí của các node trong không gian 2D
pos = nx.spring_layout(G)

# Danh sách các node và edges
nodes = list(G.nodes)
edges = list(G.edges)

# Tạo các điểm và kết nối
node_x = []
node_y = []
for node in nodes:
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

edge_x = []
edge_y = []
for edge in edges:
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_y.append(y0)
    edge_y.append(y1)

# Tạo đồ họa
fig = go.Figure()

# Vẽ các edge
fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=2, color='gray')))

# Vẽ các node
fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers', marker=dict(size=10, color='blue', line=dict(width=2, color='black'))))

# Hiệu ứng sáng lên node khi workflow chạy
def update_node_highlight(node_index, color='yellow'):
    # Cập nhật node sáng lên
    fig.data[1].marker.color = [color if i == node_index else 'blue' for i in range(len(node_x))]
    fig.show()

# Hiển thị đồ họa ban đầu
fig.update_layout(title="Dynamic Flowchart", showlegend=False, xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
fig.show()

# Cập nhật node sáng lên theo workflow (ví dụ: khi workflow chạy đến node 2)
update_node_highlight(1)  # Đánh dấu node thứ 2 (index 1)
