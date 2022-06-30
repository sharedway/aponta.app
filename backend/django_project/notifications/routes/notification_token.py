
from django.urls import path,include, re_path
from notifications.views import NotificationTokenModelTemplateView,NotificationTokenModelDetailView, NotificationTokenModelListView, NotificationTokenModelUpdateView, NotificationTokenModelDeleteView, NotificationTokenModelCreateView

urlpatterns = [    
    path("", NotificationTokenModelTemplateView.as_view(), name="notificationtokenmodel-index"),    
    path("collection/", NotificationTokenModelListView.as_view(), name="notificationtokenmodel-list"),
    path("collection/<int:pk>/", NotificationTokenModelDetailView.as_view(), name='notificationtokenmodel-detail'),
    path("collection/<int:pk>/editar/", NotificationTokenModelUpdateView.as_view(), name='notificationtokenmodel-update'),
    path("collection/<int:pk>/remover/", NotificationTokenModelDeleteView.as_view(), name='notificationtokenmodel-delete'),    
    path("collection/adicionar/", NotificationTokenModelCreateView.as_view(), name='notificationtokenmodel-create'),
]