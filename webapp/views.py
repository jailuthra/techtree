from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

import pygraphviz as pgv

from .models import Course

def index(request):
    courses = Course.objects.all().order_by('id')
    context = {'courses': courses}
    return render(request, 'webapp/index.html', context)

def graph(request):
    return render(request, 'webapp/graph.html') 

def add_edges(course, edges):
    prereqs = course.prereq.all()
    if prereqs == []:
        return
    else:
        for pr in prereqs:
            edges.append((pr, course))
            add_edges(pr, edges)
        return

@require_POST
def subgraph(request):
    courses = []
    ids = request.POST.getlist('course')
    print(ids)
    for course_id in ids:
        try:
            courses.append(Course.objects.get(id=course_id))
        except ObjectDoesNotExist:
            print(course_id, 'not found in the database')
    edges = []
    for course in courses:
        add_edges(course, edges)
    nodes = set([n1 for n1, n2 in edges] + [n2 for n1, n2 in edges] + courses)
   
    G = pgv.AGraph(directed=True)
    for node in nodes:
        G.add_node(node, label=node.id + '\n' + node.title, id=node.id)

    for edge in edges:
        G.add_edge(edge[0], edge[1])

    svg_data = G.draw(prog='dot', format='svg')
    return HttpResponse(svg_data, content_type='image/svg+xml')
