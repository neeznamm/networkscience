from email.utils import getaddresses, parseaddr
import mailbox

import matplotlib.pyplot as plt
import networkx as nx


# unix mailbox recipe
# see https://docs.python.org/3/library/mailbox.html


def mbox_graph():
    mbox = mailbox.mbox("enron.baughman-d.power.legal_agreements")  # parse unix mailbox

    G = nx.MultiDiGraph()  # create empty graph

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

# print edges with message subject
for (u, v, d) in G.edges(data=True):
    print(f"From: {u} To: {v} Subject: {d['message']['Subject']}")

pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=4, alpha=0.1, edge_color="g")
ax = plt.gca()
ax.margins(0.08)
plt.show()
