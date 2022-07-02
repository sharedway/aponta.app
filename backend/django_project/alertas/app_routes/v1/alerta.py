
from django.urls import path,include, re_path
from alertas.views import AlertaModelTemplateView,AlertaModelDetailView, AlertaModelListView, AlertaModelUpdateView, AlertaModelDeleteView, AlertaModelCreateView

urlpatterns = [    
    path("", AlertaModelTemplateView.as_view(template_name="alertamodel/app_templates/v1/alertamodel_index.html"), name="alertamodel-index"),
    path("collection/", AlertaModelListView.as_view(template_name = "alertamodel/app_templates/v1/alertamodel_list.html"), name="alertamodel-list"),
    path("collection/<int:pk>/", AlertaModelDetailView.as_view(template_name = "alertamodel/app_templates/v1/alertamodel_detail.html"), name='alertamodel-detail'),
    path("collection/<int:pk>/editar/", AlertaModelUpdateView.as_view(template_name = "alertamodel/app_templates/v1/alertamodel_update.html"), name='alertamodel-update'),
    path("collection/<int:pk>/remover/", AlertaModelDeleteView.as_view(template_name = "alertamodel/app_templates/v1/alertamodel_delete.html"), name='alertamodel-delete'),    path("collection/adicionar/", AlertaModelCreateView.as_view(template_name = "alertamodel/app_templates/v1/alertamodel_create.html"), name='alertamodel-create'),
]