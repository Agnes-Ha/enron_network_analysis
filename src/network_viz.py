import pandas as pd
import networkx as nx
import plotly
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# load data
kaminski_edges = pd.read_csv('./data/kaminski_edges.csv')
lay_edges = pd.read_csv('./data/lay_edges.csv')
skilling_edges = pd.read_csv('./data/skilling_edges.csv')


# create network graph for Kaminski
G_kam = nx.from_pandas_edgelist(kaminski_edges, 'sender', 'recipient', 
                                edge_attr='num_emails')
fig_kam = plt.figure(figsize=(20, 20))

# create a layout for the nodes
layout_kam = nx.spring_layout(G_kam, iterations=50)

# draw the edges
nx.draw_networkx_edges(G_kam, layout_kam, edge_color='#AAAAAA')

# create and draw sender nodes, sized according to their number of connections
sender_kam = [node for node in G_kam.nodes() if node in kaminski_edges['sender'].unique()]
size_kam = [G_kam.degree(node) * 80 for node in G_kam.nodes() if node in kaminski_edges['sender'].unique()]
nx.draw_networkx_nodes(G_kam, layout_kam, nodelist=sender_kam, node_size=size_kam, node_color='#8EB2A5')

# create and draw all recipient nodes
recipients_kam = [node for node in G_kam.nodes() if node in kaminski_edges['recipient'].unique()]
nx.draw_networkx_nodes(G_kam, layout_kam, nodelist=recipients_kam, node_size=100, node_color='#ACA9BB')

# create and draw popular recipients
high_degree_recipients_kam = [node for node in G_kam.nodes() if node in kaminski_edges['recipient'].unique() and G_kam.degree(node) > 1]
nx.draw_networkx_nodes(G_kam, layout_kam, nodelist=high_degree_recipients_kam, node_size=100, node_color='#474554')

# label the sender nodes
sender_dict_kam = dict(zip(sender_kam, sender_kam))
nx.draw_networkx_labels(G_kam, layout_kam, labels=sender_dict_kam)

plt.axis('off')
plt.title('Network of Vincent Kaminski\'s sent emails')
fig_kam.savefig('./plots/kaminski_network.png')