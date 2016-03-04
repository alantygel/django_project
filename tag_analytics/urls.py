#/tag_analytics/
#>> show all ODPs, with rounds

#/tag_analytics/load_odps
#>> load odps from instances

#/tag_analytics/x/load
#>> load odp next round

#/tag_analytics/x/load/x
#>> reload odp next for the spec. round

#/tag_analytics/x
#>> ODP details

#/tag_analytics/x/detail/9
#>> ODP/round details


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^load_odps/$', views.load_odps, name='load_odps'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<open_data_portal_id>[0-9]+)/load/(?P<rnumber>[0-9]+)$', views.load_metadata, name='load'),
    url(r'^(?P<open_data_portal_id>[0-9]+)/load/$', views.load_metadata, name='load'),
    url(r'^load_all/$', views.load_all, name='load'),
]


