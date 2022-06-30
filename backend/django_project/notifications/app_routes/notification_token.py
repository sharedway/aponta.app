
from django.urls import path,include, re_path
from notifications.views import NotificationTokenModelTemplateView,NotificationTokenModelDetailView, NotificationTokenModelListView, NotificationTokenModelUpdateView, NotificationTokenModelDeleteView, NotificationTokenModelCreateView

urlpatterns = [    
    path("", NotificationTokenModelTemplateView.as_view(template_name="notificationtokenmodel/app_templates/notificationtokenmodel_index.html"), name="notificationtokenmodel-index"),    
    path("collection/", NotificationTokenModelListView.as_view(template_name = "notificationtokenmodel/app_templates/notificationtokenmodel_list.html"), name="notificationtokenmodel-list"),
    path("collection/<int:pk>/", NotificationTokenModelDetailView.as_view(template_name = "notificationtokenmodel/app_templates/notificationtokenmodel_detail.html"), name='notificationtokenmodel-detail'),
    path("collection/<int:pk>/editar/", NotificationTokenModelUpdateView.as_view(template_name = "notificationtokenmodel/app_templates/notificationtokenmodel_update.html"), name='notificationtokenmodel-update'),
    path("collection/<int:pk>/remover/", NotificationTokenModelDeleteView.as_view(template_name = "notificationtokenmodel/app_templates/notificationtokenmodel_delete.html"), name='notificationtokenmodel-delete'),    
    path("collection/adicionar/", NotificationTokenModelCreateView.as_view(template_name = "notificationtokenmodel/app_templates/notificationtokenmodel_create.html"), name='notificationtokenmodel-create'),
]