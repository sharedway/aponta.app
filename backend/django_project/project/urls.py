from django.contrib import admin
from django.urls import path, include, converters
from django.conf import settings
from .views import CustomAuthToken
from project.admin import project_admin_site, project_dashboard_site

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),

    path("manager/", 
            include(
            [             
                path("", project_dashboard_site.urls)                
            ]
        ),    
    ),    
    path(r"api-token-auth/", CustomAuthToken.as_view(), name="get-token-auth"),
   

    # path("manager/",include([
    #     path("", include("dashboard.urls")),
    #     path("central/", include("central.urls")),        
    #     path("entidades/", include("entidades.urls")),
    #     path("equipamentos/", include("equipamentos.urls")),
    #     path("chips/", include("chips.urls")),
    #     path("veiculos/", include("veiculos.urls")), 
    #     path("atendimentos/", include("atendimentos.urls")),                    
    #     path("relatorios/", include("relatorios.urls")),
    #     path("organizacoes/", include("organizacoes.urls")),                      
    # ])
    # ),
    path(
        "accounts/",
        include(
            [
                path("", include("accounts.urls")),
                path("", include("django.contrib.auth.urls")),
            ]
        ),
    ),
    path(
        "web/api/v1/",
        include(
            [
                path("equipamentos/", include("equipamentos.urls")),         
                path("simcards/", include("chips.urls")),                               
            ]
        ),
    ),
    path(
        "web/app/v1/",
        include(
            [         
                path("veiculos/", include("veiculos.app_routes.web.v1.routes")),
                path("contatos/", include("contatos.app_routes.web.v1.routes")),                               
            ]
        ),
    ),



    path(
        "rest-api/v1/admin/",
        include(
            [          
                path("equipamentos/", include("equipamentos.rest_urls")),
                path("simcards/", include("chips.rest_urls")),
                path("entidades/", include("entidades.rest_urls")),  
                path("veiculos/", include("veiculos.rest_urls")),
                path("aplicativos/", include("aplicativos.rest_urls")), 
                path("central/", include("central.rest_urls")),                             
            ]
        ),
    ),
    path(
        "rest-api/v1/app/",
        include(
            [
                path("", include("accounts.rest_urls")),
                path("veiculos/", include("veiculos.app_routes.veiculos")),
                path("contatos/", include("contatos.rest_urls")),
                path("notifications/", include("notifications.rest_urls")),                
                path("aplicativos/", include("aplicativos.rest_urls")),                               
            ]
        ),
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("django.contrib.flatpages.urls")),
]
