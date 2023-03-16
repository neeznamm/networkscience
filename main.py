from email.utils import getaddresses, parseaddr
import mailbox

import matplotlib.pyplot as plt
import networkx as nx


# unix mailbox recipe
# see https://docs.python.org/3/library/mailbox.html

def mbox_graph():
    mbox = mailbox.mbox("enron.baughman-d.power.legal_agreements")  # parse unix mailbox

    G = nx.Graph()  # create empty graph

    # parse each messages and build graph
    for msg in mbox:  # msg is python email.Message.Message object
        (source_name, source_addr) = parseaddr(msg["From"])  # sender
        # get all recipients
        # see https://docs.python.org/3/library/email.html
        tos = msg.get_all("to", [])
        ccs = msg.get_all("cc", [])
        resent_tos = msg.get_all("resent-to", [])
        resent_ccs = msg.get_all("resent-cc", [])
        all_recipients = getaddresses(tos + ccs + resent_tos + resent_ccs)
        # now add the edges for this mail message
        for (target_name, target_addr) in all_recipients:
            G.add_edge(source_addr, target_addr, message=msg)

    return G


G = mbox_graph()

# Remove self-loops
G.remove_edges_from(nx.selfloop_edges(G))

# print edges with message subject
for (u, v, d) in G.edges(data=True):
    print(f"From: {u} To: {v} Subject: {d['message']['Subject']}")

pos = nx.spring_layout(G)
sizes = [v * 10 for v in dict(G.degree()).values()]
nx.draw(G, pos, node_size=sizes, edge_color="grey", alpha=0.5)
ax = plt.gca()
ax.margins(0.08)
plt.show()

# plot node degrees
plt.figure(figsize=(10,6))
plt.subplots_adjust(bottom=0.2)
degree_sequence = sorted([(n, d) for n, d in G.degree()], key=lambda x: x[1], reverse=True)
top_nodes = [n for n, d in degree_sequence[:5]]
x_ticks = top_nodes
degree_sequence = [d for n, d in degree_sequence if n in top_nodes]
plt.bar(x_ticks, degree_sequence)
plt.ylabel('Degree')
plt.title('Degree distribution of 5 nodes with highest degree')
plt.xticks(rotation=20, fontsize=10)
plt.show()

# calculate the degree histogram and plot it
dh = nx.degree_histogram(G)
dgs = list(range(0,len(dh)))
plt.bar(dgs, dh)
plt.xlabel('Degree')
plt.ylabel('Number of Nodes')
plt.title('Degree distribution of graph')
plt.show()

# loglog plot of the degree frequencies
plt.loglog(dgs,dh)
plt.title("Loglog plot of degree frequencies")
plt.show()

print("\nThe graph has a clustering coefficient of", nx.average_clustering(G),
      "an average shortest path length of", nx.average_shortest_path_length(G),
      "and a density of", nx.density(G))
