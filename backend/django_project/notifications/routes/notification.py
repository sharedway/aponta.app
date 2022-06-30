
from django.urls import path,include, re_path
from notifications.views import NotificationModelTemplateView,NotificationModelDetailView, NotificationModelListView, NotificationModelUpdateView, NotificationModelDeleteView, NotificationModelCreateView

urlpatterns = [    
    path("", NotificationModelTemplateView.as_view(), name="notificationmodel-index"),    
    path("collection/", NotificationModelListView.as_view(), name="notificationmodel-list"),
    path("collection/<int:pk>/", NotificationModelDetailView.as_view(), name='notificationmodel-detail'),
    path("collection/<int:pk>/editar/", NotificationModelUpdateView.as_view(), name='notificationmodel-update'),
    path("collection/<int:pk>/remover/", NotificationModelDeleteView.as_view(), name='notificationmodel-delete'),    
    path("collection/adicionar/", NotificationModelCreateView.as_view(), name='notificationmodel-create'),
]