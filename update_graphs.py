import django
import os
import json
from networkx.readwrite import json_graph
import networkx as nx
import pygraphviz as pgv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechTree.settings')
django.setup()

from webapp.models import Course

courses = Course.objects.all()

edges = []

for course in courses:
    prereqs = course.prereq.all()
    if prereqs != []:
        for pr in prereqs:
            edges.append((pr, course))

nodes = set([n1 for n1, n2 in edges] + [n2 for n1,n2 in edges])

# Using pygraphviz to generate a dot file

G = pgv.AGraph(directed=True)

for node in nodes:
    G.add_node(node, label=node.id + '\n' + node.title)

for edge in edges:
    G.add_edge(edge[0], edge[1])

static_path = 'webapp/static/webapp/'
G.write('graph.dot')

# Generating basic svg 
G.draw(path=static_path + 'graph.svg', prog='dot')

# Generating .dot with coordinate information for nodes
os.system("ccomps -x graph.dot | dot -Nshape=point -Granksep=1.0 -Gnodesep=1.0 -Gsize=10 | gvpack -array1 | neato -Tdot -n2 -o graphcoord.dot")

# Generating JSON from graph with coordinates
G = pgv.AGraph('graphcoord.dot')
nx_G = nx.from_agraph(G)
graph_json = json_graph.node_link_data(nx_G)
with open(static_path + 'graph.json', 'w') as f:
    json.dump(graph_json, f, indent=1)

# Cleaning up
os.remove('graph.dot')
os.remove('graphcoord.dot')
