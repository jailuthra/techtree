import urllib.request
from bs4 import BeautifulSoup
import networkx as nx
# import matplotlib.pyplot as plt

class Course():
    prereq = []
    def __init__(self, id, title):
        self.id = id
        self.title = title
    def __repr__(self):
        return "<Course object>"
    def __str__(self):
        return self.id + '\n' + self.title

with urllib.request.urlopen('http://sites.iiitd.ac.in/courserepo/') as res:
    html = res.read() 

soup = BeautifulSoup(html, 'html.parser')

exTitle = lambda title: title.string.split('Title: ')[1][:-1]
exId = lambda id: id.string.split('(')[0][:-1]
exPRId = lambda pr_id: pr_id.string.strip(' ')

# print(soup.prettify())
titles = soup.find_all(attrs={'class': 'title'})
ids = soup.find_all(attrs={'class': 'number'})

prereqs = {}

for id in ids:
    pr_row = id.parent.parent.next_sibling.next_sibling.next_sibling.next_sibling
    if 'Pre-requisite:' in str(pr_row):
        prereqs[exId(id)] = [exPRId(pr_id) for pr_id in pr_row.find_all('a')]

# print(prereqs)


# titles = [exTitle(title) for title in titles]
# ids = [exId(id) for id in ids]

titles = map(exTitle, titles)
ids = map(exId, ids)

courses = []

for t, i in zip(titles, ids):
    course = Course(i, t)
    if i in prereqs.keys():
        course.prereq = prereqs[i]
    courses.append(course)

# for course in courses:
    # print(course)

# GRAPH

#nodes = [course.id for course in courses]
edges = []

for course in courses:
    if course.prereq != []:
        for pr in course.prereq:
            try:
                pr_course = [p for p in courses if pr in p.id][0]
                edges.append((pr_course, course))
            except:
                print(pr, '\'s course name not found')
                edges.append((pr, course))

nodes = set([n1 for n1,n2 in edges] + [n2 for n1,n2 in edges])
G = nx.DiGraph()
for node in nodes:
    G.add_node(node)
for edge in edges:
    G.add_edge(edge[0], edge[1])
nx.write_dot(G, "graph.dot")
# pos = nx.spring_layout(G)
# nx.draw(G, pos)
# plt.show()
