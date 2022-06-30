from django.contrib import admin
from django.utils.translation import gettext as _, gettext_lazy
from django.conf import settings
from project.views import BaseEntidadeView,BaseChipView,BaseEquipamentoView,BaseVeiculoView,BaseOrganizacaoView
# def get_app_list(self, request):
#     app_dict = self._build_app_dict(request)
#     from django.contrib.admin.sites import site
#     for app_name in app_dict.keys():
#         app = app_dict[app_name]
#         model_priority = {
#             model['object_name']: getattr(
#                 site._registry[apps.get_model(app_name, model['object_name'])],
#                 'admin_priority',
#                 20
#             )
#             for model in app['models']
#         }
#         app['models'].sort(key=lambda x: model_priority[x['object_name']])
#         yield app

# admin.AdminSite.get_app_list = get_app_list

class BaseModelAdmin(admin.ModelAdmin):
    # add_form_template = 'admin/auth/user/add_form.html'
    # change_form_template = 'tabbed_admin/change_form.html'
    # change_list_template = 'admin/change_list.htm'
    

    #add_form_template = None
    #change_form_template = None
    
    # change_list_template = None
    # delete_confirmation_template = None
    # delete_selected_confirmation_template = None
    # object_history_template = None
    # popup_response_template = None


    admin_priority = 20
    default_lon = -5372220.98 
    default_lat = -2413950.78
    map_width = 800
    map_height = 600
    default_zoom = 8
    save_on_top = True
    date_hierarchy = "created"
    list_per_page = 200
    list_max_show_all = 300
    actions_on_bottom = True
    EXCLUDE_FROM_ADMIN = []    
    exclude = [
         "criado_por","modificado_por","removido_por","isRemoved",
        "isActive", "isDone", "isComplete", "isPublic", "isProcessed","alterado_por"]

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class BaseModelAdminTabular(admin.TabularInline):
    ""


class ProjectAdminSite(admin.AdminSite,BaseVeiculoView):
    site_header = "Api Wamove"
    site_title = "Wamove Dashboard"
    enable_nav_sidebar = True
    index_template = "admin/admin_api/index.html"
    app_index_template = "admin/admin_api/app_index.html"


    def each_context(self, request):
        self.request= request
        contexto = super().each_context(request)

        contexto.update({
            "map_credits":'Desenvolvido por <a href="https://www.sharedway.app/copyright">SharedWAY&copy;</a> aplicativos e sistemas de alta disponibilidade  Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            "rest_api_address":f"{settings.REST_API_ADDRESS}",
            "socket_api_address":f"{settings.SOCKET_API_ADDRESS}",   
        })
        return contexto

    
project_admin_site = ProjectAdminSite(name="admin")



class ProjectDashBoardSite(admin.AdminSite,BaseEntidadeView,BaseChipView,BaseEquipamentoView,BaseVeiculoView,BaseOrganizacaoView):
    site_header = "Wamove"   
    enable_nav_sidebar = True
    site_title = gettext_lazy('Wamove')
    index_title = gettext_lazy('Dashboard')    



    def each_context(self, request):
        self.request= request
        contexto = super().each_context(request)
        contexto.update({          
            "body_class":"manager",    
            "map_credits":'Desenvolvido por <a target="_sharedway" href="https://www.sharedway.app">SharedWAY&copy;</a> aplicativos e sistemas de alta disponibilidade  Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',              
            "rest_api_address":f"{settings.REST_API_ADDRESS}",
            "socket_api_address":f"{settings.SOCKET_API_ADDRESS}",   
        })
        if request.user.is_authenticated:
            contexto.update({
                "veiculos": self.veiculos_associados_query,          
                "ultima_hora":self.total_transmissoes_ultima_hora,
                "entre_1_e_6": self.total_transmissoes_entre_1_e_6,
                "entre_6_e_24":self.total_transmissoes_entre_6_e_24,
                "entre_24_e_48":self.total_transmissoes_entre_24_e_48,
                "acima_de_48":self.total_transmissoes_acima_de_48,            
                "total_entidades":self.get_total_entidades,
                "total_veiculos":self.get_total_veiculos,
                "total_chips":self.get_total_chips,
                "total_equipamentos":self.get_total_equipamentos,
                "organizacoes":self.organizacoes_query,
                "entidades":self.entidades_query,
                "total_transmissoes_ultima_hora":self.total_transmissoes_ultima_hora,
                "total_transmissoes_entre_1_e_6":self.total_transmissoes_entre_1_e_6,
                "total_transmissoes_entre_6_e_24":self.total_transmissoes_entre_6_e_24, 
                "total_transmissoes_acima_de_48":self.total_transmissoes_acima_de_48,
                "total_transmissoes_entre_24_e_48":self.total_transmissoes_entre_24_e_48,            
            })
        return contexto


project_dashboard_site = ProjectDashBoardSite(name="painel")
