import json
import urllib.request
from bs4 import BeautifulSoup
import networkx as nx
from networkx.readwrite import json_graph
import pygraphviz as pgv

class Course():
    prereq = []
    def __init__(self, id, title):
        self.id = id
        self.title = title
    def __repr__(self):
        return "<Course object>"
    def __str__(self):
        return self.id + ': ' + self.title

with urllib.request.urlopen('http://sites.iiitd.ac.in/courserepo/') as res:
    html = res.read() 

soup = BeautifulSoup(html, 'html.parser')

exTitle = lambda title: title.string.split('Title: ')[1][:-1]
exId = lambda id: id.string.split('(')[0][:-1]
exPRId = lambda pr_id: pr_id.string.strip(' ')

titles = soup.find_all(attrs={'class': 'title'})
ids = soup.find_all(attrs={'class': 'number'})

prereqs = {}

for id in ids:
    pr_row = id.parent.parent.next_sibling.next_sibling.next_sibling.next_sibling
    if 'Pre-requisite:' in str(pr_row):
        prereqs[exId(id)] = [exPRId(pr_id) for pr_id in pr_row.find_all('a')]

titles = map(exTitle, titles)
ids = map(exId, ids)

courses = []

for t, i in zip(titles, ids):
    course = Course(i, t)
    if i in prereqs.keys():
        course.prereq = prereqs[i]
    courses.append(course)


# GRAPH

edges = []

for course in courses:
    if course.prereq != []:
        for pr in course.prereq:
            edges.append((pr, course.id))

nodes = set([n1 for n1,n2 in edges] + [n2 for n1,n2 in edges])

### Commented for legacy purposes
# G = nx.DiGraph()
# for node in nodes:
    # G.add_node(node)
# for edge in edges:
    # G.add_edge(edge[0], edge[1])
# nx.write_dot(G, "graph.dot")

# pos = nx.spring_layout(G)
# nx.draw(G, pos)
# plt.show()

# Using pygraphviz library to generate svg and dot file
G = pgv.AGraph(directed=True)
for node in nodes:
    node_object = next((c for c in courses if node in c.id), None)
    if node_object:
        label = node_object.id + '\n' + node_object.title
    else:
        label = node
    G.add_node(node, label=label)
for edge in edges:
    G.add_edge(edge[0], edge[1])
G.write('graph.dot')

# Generating JSON from graph
graph_json = json_graph.node_link_data(nx.from_agraph(G))

with open('graph.json', 'w') as f:
    json.dump(graph_json, f, indent=1)

# Generating .svg from graph
G.draw(path='graph.svg', prog='dot')
