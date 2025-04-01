import networkx as nx
import matplotlib.pyplot as plt

pair_counts = {
    ("himalayan bluetail", "hume's warbler"): 319,
    ("tytler's leaf warbler", "western crowned warbler"): 82,
    ("variegated laughingthrush", "western crowned warbler"): 73,
    ("greenish warbler", "hume's warbler"): 48,
    ("hume's warbler", "variegated laughingthrush"): 33,
    ("hume's warbler", "western crowned warbler"): 11,
    ("himalayan monal", "hume's warbler"): 11,
    ("common rosefinch", "hume's warbler"): 5,
    ("hume's warbler", "slaty-blue flycatcher"): 3,
    ("hume's warbler", "tickell's leaf warbler"): 3,
    ("hume's warbler", "large-billed leaf warbler"): 2,
    ("buff-barred warbler", "hume's warbler"): 2,
    ("hume's warbler", "pink-browed rosefinch"): 1,
    ("greenish warbler", "himalayan bluetail"): 1,
}

# Create graph
G = nx.Graph()
for (sp1, sp2), weight in pair_counts.items():
    G.add_edge(sp1, sp2, weight=weight)

# Draw
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, k=1.8, seed=42)  # layout
weights = [G[u][v]['weight'] / 10 for u, v in G.edges()]  # scale for visibility

nx.draw(
    G, pos,
    with_labels=True,
    node_color="skyblue",
    node_size=1500,
    edge_color="gray",
    width=weights,
    font_size=10
)

plt.title("Hume's Warbler Interaction Network", fontsize=16)
plt.savefig("vanessa_plots/humes_social_network.png", bbox_inches="tight", dpi=300)
plt.show()

# NOTES #
# Each node is a bird species.
# An edge means the two species were heard in the same 3-second audio chunk.
# This implies either vocal overlap or presence in the same area at the same time.
# Thicker edges mean more frequent co-detections.