from django.conf.urls import url
from tutorials import views

urlpatterns = [
    # function based view

    # url(r'^api/tutorials$', views.tutorial_list),
    # url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
    # url(r'^api/tutorials/published$', views.tutorial_list_published)

    # Class based views + generics
    url(r'^api/tutorials$', views.tutorial_list_view_generic.as_view()),
    url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail_view_generic.as_view()),
    url(r'^api/tutorials/published$', views.tutorial_list_published_view_generics.as_view())
]