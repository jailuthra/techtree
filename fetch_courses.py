import django
import os
import urllib.request
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechTree.settings')
django.setup()

from webapp.models import Course

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

titles = list(map(exTitle, titles))
ids = list(map(exId, ids))

assert(len(titles) == len(ids))

for t, i in zip(titles, ids):
    course = Course.objects.get_or_create(id=i, title=t)[0]
    # if i in prereqs.keys():
        # course.prereq = prereqs[i]
    course.save()

for i in prereqs.keys():
    course = Course.objects.get(pk=i)
    for prereq in prereqs[i]:
        try:
            pr = Course.objects.get(pk=prereq)
            course.prereq.add(pr)
        except django.core.exceptions.ObjectDoesNotExist:
            print(prereq, "not found, skipping...")
    course.save()
