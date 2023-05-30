import scipy.io as sio
import torch
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    ld_edge_index = './data/graph15000_edge_index.mat'
    edge_index = sio.loadmat(ld_edge_index)
    edge_index = edge_index['edge_index'][0]

    ld_label = './data/graph15000_label.mat'
    label = sio.loadmat(ld_label)
    label = label['label']

    ld_positions = './data/graph15000_position.mat'
    positions = sio.loadmat(ld_positions)
    positions = positions['position'][0]

    G_index = 3213

    edge_index_G = np.array(edge_index[G_index][:, 0:2], dtype=int)
    edge_index_G = torch.tensor(edge_index_G, dtype=torch.long)

    G = nx.Graph()
    G.add_edges_from(edge_index_G.tolist())

    node_colors = [G.degree[node] for node in G.nodes()]

    pos = {node: positions[node][0] for node in G.nodes()}

    plt.figure(figsize=(8, 8))
    nx.draw_networkx_edges(G, pos=pos, edge_color='gray', alpha=0.2)
    plt.scatter(*zip(*pos.values()), c=node_colors, cmap='coolwarm', edgecolors='k', linewidths=0.5, alpha=0.8)
    plt.title(f'Graph Visualization - Label: {label[G_index]}')
    plt.colorbar(label='Node Degree')
    plt.show()
