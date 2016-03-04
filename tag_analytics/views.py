from django.http import HttpResponse,Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from datetime import datetime

from .models import OpenDataPortal

import lib
import json

class IndexView(generic.ListView):
    template_name = 'tag_analytics/index.html'
#    context_object_name = 'open_data_portal_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return OpenDataPortal.objects.all()

class DetailView(generic.DetailView):
    model = OpenDataPortal
    template_name = 'tag_analytics/detail.html'

#def show_odp(request,open_data_portal_id):
#	try:
#		o = OpenDataPortal.objects.get(id=open_data_portal_id)
#	except OpenDataPortal.DoesNotExist:
#		raise Http404("Question does not exist")
#	context = {'open_data_portal': o}
#	return render (request,'tag_analytics/index.html',context)

def load_odps(request):
	"Reads the instance files, and initialize a list of ODP objects"

	with open("/home/alan/Dropbox/Alan - Doutorado/ODP_tag_analysis/django_project/tag_analytics/instances.json", 'r') as f:
		instances = json.loads(f.read())

	print 'Number of instances: ' + str(len(instances))

	for i in instances:
		if 'url-api' in i:
			odp_url = i['url-api']
		else:
			odp_url = i['url']
	
		o = OpenDataPortal(url=odp_url)
		o.save()

	return render (request,'tag_analytics/index.html')

def load_all(request):
	odps = OpenDataPortal.objects.all()
	for o in odps:
		print o.url
		load_metadata(request,o.id,None)

	return render (request,'tag_analytics/index.html')

def load_metadata(request, open_data_portal_id,rnumber=None):

	try:
		o = OpenDataPortal.objects.get(id=open_data_portal_id)
	except:
		return
		raise Http404("No ODP with id " + open_data_portal_id)
	## create round or laod
	if rnumber is not None:
		try:
			lr = o.loadround_set.get(roundn = rnumber)
		except:
			raise Http404("No round with this number: " + rnumber)
		lr.delete()
		lr = o.loadround_set.create(roundn = rnumber)
	else:
		if o.loadround_set.count() > 0:
			rnumber = o.loadround_set.last().roundn + 1
		else:
			rnumber = 1
		lr = o.loadround_set.create(roundn = rnumber)

	## get metadata
	metadata_response = 0
	try:		
		metadata_response = lib.urlopen_with_retry(o.url + '/api/3/action/status_show')
	except:
		lr.success = 0
		lr.save()
		return
#		raise Http404("Website not available while getting metadata")


	lr.success = 1
	if metadata_response:
		try: 
			metadata_dict = json.loads(metadata_response.read())	
			metadata = metadata_dict['result']
		except:
			raise Http404("No results")

		lr.odpmetadata_set.create(site_title = metadata['site_title'], ckan_version=metadata['ckan_version'], site_description=metadata['site_description'], locale_default=metadata['locale_default'])

	## get tags
	tag_list_response = 0
	tag_list = 0
	try:		
		tag_list_response = lib.urlopen_with_retry(o.url + '/api/3/action/tag_list?all_fields=True')
	except:
		raise Http404("Website not available while getting tags")

	if tag_list_response: 
		try: 
			tag_list_dict = json.loads(tag_list_response.read())	
			tag_list = tag_list_dict['result']
		except:
			raise Http404("No results")

		for tag in tag_list:
			lr.tag_set.create(name=tag['name'],display_name=tag['display_name'], ckan_id = tag['id'])

	## get groups
	group_list_response = 0
	group_list = 0
	try:		
		group_list_response = lib.urlopen_with_retry(o.url + '/api/3/action/group_list?all_fields=True')
	except:
		raise Http404("Website not available while getting groups")

	if group_list_response: 
		try: 
			group_list_dict = json.loads(group_list_response.read())	
			group_list = group_list_dict['result']
		except:
			print("No results")

		for group in group_list:
			lr.group_set.create(name=group['name'],display_name=group['display_name'], ckan_id = group['id'])


	## get datasets
	LIMIT = 50
	START = 0
	dataset_list_response = 0
	dataset_list = []
	keeploading = True

	print o.url + '/api/3/action/package_search?rows='+str(LIMIT)+'&start='+str(START)

	while keeploading:
		try:
			dataset_list_response = lib.urlopen_with_retry(o.url + '/api/3/action/package_search?rows='+str(LIMIT)+'&start='+str(START))
		except:
			raise Http404("Website not available while getting datasets")

		if dataset_list_response: 
			dataset_list_dict = json.loads(dataset_list_response.read())	
			dataset_list += dataset_list_dict['result']['results']

			print o.url + '/api/3/action/package_search?rows='+str(LIMIT)+'&start='+str(START)
			print len(dataset_list_dict['result']['results'])
			print dataset_list_dict['result']['count']
			print len(dataset_list)
			print "---"
			if len(dataset_list) >= int(dataset_list_dict['result']['count']):
				keeploading = False
			else:
				START += LIMIT

	for dataset in dataset_list:
		dataset_response = 0
		if type(dataset['title']) is dict:
			dataset_name = dataset['title'].values()[0]
		else:
			dataset_name = dataset['title']
		print "dataset name: " + dataset_name
		d = lr.dataset_set.create(name=dataset['name'],display_name=dataset_name, ckan_id = dataset['id'], metadata_modified = dataset['metadata_modified'])
		d.save()


		for tag in dataset['tags']:
			print ">> " + tag['name']
			t = lr.tag_set.filter(name=tag['name']).first()
			d.tag_set.add(t)
		print "---"

		for group in dataset['groups']:
			print ">> " + group['name']
			g = lr.group_set.filter(name=group['name']).first()
			d.groups.add(g)
		print "---"

	lr.save()

	return HttpResponse("bla")

