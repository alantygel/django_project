from tag_analytics.models import OpenDataPortal, Tag, Dataset, Group, TagDataset, GroupDataset

import model
import cPickles as pickle
from django.utils import timezone


with open('ODP.pkl', 'rb') as input:
	ODP =  pickle.load(input)

for o in ODP:
	odp = OpenDataPortal(name=o.name, url=o.url, insert_date=timezone.now())
	odp.save();
	for t in o.tags:
		odp.tag_set.create(name=t.name, ckan_id=t.tag_id,insert_date=timezone.now())

	for d in o.datasets:
		odp.dataset_set.create(name=d.name, ckan_id=d.dataset_id,insert_date=timezone.now())

	for g in o.groups:
		odp.group_set.create(name=g.name, ckan_id=0,insert_date=timezone.now())

