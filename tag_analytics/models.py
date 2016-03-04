from __future__ import unicode_literals
from datetime import datetime
from django.db import models

class OpenDataPortal(models.Model):
	url = models.CharField(max_length=200)
	insert_date = models.DateTimeField('insert date', default=datetime.now)

	def __str__(self):
		return self.url

class LoadRound(models.Model):
	open_data_portal = models.ForeignKey(OpenDataPortal, on_delete=models.CASCADE)
	roundn = models.IntegerField(null=False,blank=False)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	success = models.IntegerField(default=1, null=False,blank=False)

	def __str__(self):
		return self.open_data_portal.url + '-' + str(self.roundn)

class ODPMetadata(models.Model):
	site_title = models.CharField(max_length=200, null=True,blank=True)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	ckan_version = models.CharField(max_length=200, null=True,blank=True)
	site_description = models.CharField(max_length=2000, null=True,blank=True)
	locale_default = models.CharField(max_length=10, null=True, blank=True)
	load_round = models.ForeignKey(LoadRound, on_delete=models.CASCADE)
	

	def __str__(self):
		return self.load_round.open_data_portal.url

class Group(models.Model):
	name = models.CharField(max_length=200)
	display_name = models.CharField(max_length=200,null=True,blank=True)
	ckan_id = models.CharField(max_length=200)
	load_round = models.ForeignKey(LoadRound, on_delete=models.CASCADE)
	insert_date = models.DateTimeField('insert date', default=datetime.now)

	def __unicode__(self):
		return self.name

class Dataset(models.Model):
	name = models.CharField(max_length=200)
	display_name = models.CharField(max_length=200,null=True,blank=True)
	ckan_id = models.CharField(max_length=200)
	load_round = models.ForeignKey(LoadRound, on_delete=models.CASCADE)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	metadata_modified = models.DateTimeField('metadata_modified')
	groups = models.ManyToManyField(Group, blank=True)

	def __unicode__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=200)
	display_name = models.CharField(max_length=200,blank=True,null=True)
	ckan_id = models.CharField(max_length=200)
	translation = models.CharField(max_length=200)
	load_round = models.ForeignKey(LoadRound, on_delete=models.CASCADE)
	insert_date = models.DateTimeField('insert date', default=datetime.now)
	datasets = models.ManyToManyField(Dataset, blank=True)

	def __unicode__(self):
		return self.name

