from encodings import utf_8
from urllib import response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from accounts.serializers import ProfileSerializer
from rest_framework.renderers import JSONRenderer
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from entidades.models import EntidadeModel
from chips.models import Chip
from equipamentos.models import Equipamento, Position
from organizacoes.models import Organizacao
from django.conf import settings
from veiculos.models import VeiculoModel, UnidadeDoVeiculo, SituacaoAdministrativa
from django.utils.functional import cached_property
from django.db.models import Count
from datetime import datetime,timedelta
from django.db.models import Q,F

class CommonBaseView:
    def get_qs_value(self,key_name):       
        return self.request.GET.get(f'{key_name}', None)

    def get_bool_qs_value_or_none(self,key_name):        
        try:
            key_value = bool(int(self.get_qs_value(key_name)))
        except:
            key_value=None


        if isinstance(key_value,(bool)):
            return key_value
        return None


    def get_int_qs_value_or_default(self,key_name,default_value):
        key_value = self.get_qs_value(key_name)
        if isinstance(key_value,(int)):
            return key_value
        return default_value


    def get_string_qs_value_or_none(self,key_name):
        key_value = self.get_qs_value(key_name)
        if isinstance(key_value,(str)):
            return key_value
        return None


    def get_int_qs_value_or_none(self,key_name):
        
        key_value = self.get_qs_value(key_name)

        if key_value:
            key_value = int(key_value)

        if isinstance(key_value,(int)):
            return key_value
        return None

    @property
    def chatroom_id(self):
        return self.get_int_qs_value_or_none("chatroom_id")        

    @property
    def next(self):
        return self.get_qs_value('next')

    @property
    def page(self):
        return self.get_int_qs_value_or_default('page',1)
        
    @property
    def page_size(self):
        return self.get_int_qs_value_or_default('page_size',100)

    @property
    def offset(self):
        if int(self.page) > 1:
            return self.page_size * self.page
        return 0

    @property
    def organizacao_id(self):   
        ident = self.get_int_qs_value_or_none('organizacao')
        if not ident:
            ident = self.get_int_qs_value_or_none('organizacao_id')

        return ident

    @property
    def entidade_id(self):
        return self.get_int_qs_value_or_none('entidade_id')


    @property
    def modelo_id(self):
        return self.get_int_qs_value_or_none('modelo_id')

    @property
    def position_id(self):
        return self.get_int_qs_value_or_none('position_id')

    @property
    def veiculo_id(self):
        return self.get_int_qs_value_or_none('veiculo_id')


    @property
    def unidade_do_veiculo_id(self):
        return self.get_int_qs_value_or_none('unidade_do_veiculo_id')

    @property
    def situacao_administrativa_do_veiculo_id(self):
        return self.get_string_qs_value_or_none('situacao_administrativa_id')

    @property
    def ignicao_status(self):
        return self.get_string_qs_value_or_none('ignicao_status')

    @property
    def placa_do_veiculo(self):
        return self.get_string_qs_value_or_none('placa_do_veiculo')


    def filtrar_veiculo_por_placa(self,qs):   
        """"
        Filtrar por entidade e organizacao
        """
        if self.placa_do_veiculo:       
            qs = qs.filter(placa=self.placa_do_veiculo)
        return qs


    def filtrar_veiculo_por_unidade(self,qs):   
        """"
        Filtrar por entidade e organizacao
        """
        if self.unidade_do_veiculo_id:
            qs = qs.filter(unidade_do_veiculo__id__in=[self.unidade_do_veiculo_id])
        return qs


    def filtrar_veiculo_por_status_da_ignicao(self,qs):
        if self.ignicao_status:                      
            if self.ignicao_status in ['LIGADA']:
                qs = qs.filter(ignition=True)
            if self.ignicao_status in ['DESLIGADA']:
                qs = qs.filter(ignition=False)
        return qs

    def filtrar_veiculo_por_situacao_administrativa(self,qs):
        if self.situacao_administrativa_do_veiculo_id:
            qs = qs.filter(situacao_administrativa__id__in=[self.situacao_administrativa_do_veiculo_id])
        return qs




    def filtrar_por_organizacao(self,qs):   
        """"
        Filtrar por entidade e organizacao
        """
        if self.organizacao_id:          
            qs = qs.filter(organizacao__id__in=[self.organizacao_id])   
        return qs

    def filtrar_por_entidade(self,qs):   
        """"
        Filtrar por entidade
        """
        if self.entidade_id:
            qs = qs.filter(entidade__id__in=[self.entidade_id])   
        return qs




class BasePositionView(CommonBaseView):
    @cached_property
    def positions_query(self):
        positions = Position.objects.all()
        return positions

 

class BaseUnidadesDosVeiculosView(CommonBaseView):
    @cached_property
    def unidades_dos_veiculos_query(self):        
        return self.filtrar_por_organizacao(self.filtrar_por_entidade(UnidadeDoVeiculo.objects.all()))
        

class BaseSituacaoAdministrativaDosVeiculosView(CommonBaseView):
    @cached_property
    def situacao_administrativa_dos_veiculos_query(self):        
        return SituacaoAdministrativa.objects.all()        


class BaseVeiculoView(CommonBaseView):  


    @property
    def veiculos_query(self):
        qs=VeiculoModel.objects.filter(isActive=True,entidade__conta_de_entidade=self.request.user)
        if self.request.user.is_superuser:  
            qs= VeiculoModel.objects.filter(isActive=True)
        return self.filtrar_veiculo_por_status_da_ignicao(
            self.filtrar_veiculo_por_situacao_administrativa(self.filtrar_por_organizacao(self.filtrar_por_entidade(self.filtrar_veiculo_por_unidade(self.filtrar_veiculo_por_placa(qs))))))

        

    @property
    def veiculos_associados_query(self):
        return self.veiculos_query.annotate(equipamentos=Count('lista_de_equipamentos_associados_com_esse_veiculo')).filter(equipamentos__gt=0)


    @property
    def get_total_veiculos(self):
        return  self.veiculos_query.count()



class BaseOrganizacaoView(CommonBaseView):
    @cached_property
    def organizacoes_query(self):        
        return Organizacao.objects.all()
                
    @cached_property
    def get_total_organizacoes(self):
        return  self.organizacoes_query.count()


class BaseEntidadeView(CommonBaseView):    
    @property
    def entidades_query(self):        
        return self.filtrar_por_organizacao(EntidadeModel.objects.all())
        
    @cached_property
    def get_total_entidades(self):
        return  self.entidades_query.count()


class BaseChipView(CommonBaseView):
    @property
    def chips_query(self):        
        return self.filtrar_por_organizacao(Chip.objects.all())
        
    @property
    def get_total_chips(self):
        return  self.chips_query.count()


class BaseEquipamentoView(CommonBaseView):
    @property
    def equipamentos_query(self): 
        qs = self.filtrar_por_organizacao(Equipamento.objects.all().order_by('created'))
        return qs


    @property
    def equipamentos_na_expedicao_query(self):         
        qs = self.equipamentos_query.annotate(total_veiculos=Count('lista_de_veiculos_associados_com_esse_equipamento')).filter(total_veiculos__lt=1)
        
        return qs


    @cached_property
    def get_total_equipamentos(self):
        return self.equipamentos_query.count()


    @cached_property
    def get_all_equipamentos_page(self):        
        return self.equipamentos_query[self.offset:self.page_size]

    @cached_property
    def get_active_equipamentos_page(self):
        return self.equipamentos_query.annotate(ativos=Count('positions')).filter(ativos__gt=0)[self.offset:self.page_size]

    @cached_property
    def equipamentos_associados_query(self):    
        try:
            resposta = self.equipamentos_query.annotate(veiculos=Count('lista_de_veiculos_associados_com_esse_equipamento')).filter(veiculos__gt=0)
        except Exception as e:
            print(e.__repr__())
            resposta = self.equipamentos_query
        return resposta

    @cached_property
    def total_equipamentos_associados(self):
        return self.equipamentos_associados_query.count()


    @cached_property
    def equipamentos_associados_page(self):
        return self.equipamentos_associados_query[self.offset:self.page_size]

    @cached_property
    def total_transmissoes_ultima_hora(self):
        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now() - timedelta(hours=1)
        

        return {
            "total":self.equipamentos_associados_query.filter(positions__created__gt=start_time).count(),
            "de":self.total_equipamentos_associados
        }
        

    @cached_property
    def total_transmissoes_entre_1_e_6(self):
        agora = datetime.now()
        start_time =  agora - timedelta(hours=6)
        end_time = agora - timedelta(hours=1)
        return {
            "total":self.equipamentos_associados_query.filter(positions__created__gt=start_time,positions__created__lt=end_time).count(),
            "de":self.total_equipamentos_associados
        }

       

    @cached_property
    def total_transmissoes_entre_6_e_24(self):
        agora = datetime.now()
        start_time =  agora - timedelta(hours=24)
        end_time = agora - timedelta(hours=6)
        return {
            "total":self.equipamentos_associados_query.filter(positions__created__gt=start_time,positions__created__lt=end_time).count(),
            "de":self.total_equipamentos_associados
        }

    @cached_property
    def total_transmissoes_entre_24_e_48(self):
        agora = datetime.now()
        start_time =  agora - timedelta(hours=48)
        end_time = agora - timedelta(hours=25)
        return {
            "total":self.equipamentos_associados_query.filter(positions__created__gt=start_time,positions__created__lt=end_time).count(),
            "de":self.total_equipamentos_associados
        }





    @cached_property
    def total_transmissoes_acima_de_48(self):
        agora = datetime.now()
        start_time =  agora - timedelta(hours=48)
        return {
            "total":self.equipamentos_associados_query.filter(positions__created__gt=start_time).count(),
            "de":self.total_equipamentos_associados
        }



class CustomBaseView(CommonBaseView):       
    context_response = {}

    @cached_property
    def cache_context(self):
        response = {
            "map_credits":'<a target="_sharedway" href="https://www.sharedway.app">SharedWAY&copy;</a> sistemas de alta disponibilidade  Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',              
            "rest_api_address":f"{settings.REST_API_ADDRESS}",
            "socket_api_address":f"{settings.SOCKET_API_ADDRESS}",               
            "page":self.page,            
            "qs":self.request.GET,
            "page_size":self.page_size,
            "site":self.request.site,
            "hostname":self.request.headers.get('host')
        }
        return response 


    def common_context(self):          
        response = self.cache_context      
        if self.next:
            response.update({
                "next":self.next
            })
    
        return response







class CustomBaseListView(ListView, CustomBaseView):
    def list_context(self):
        return {}


class CustomBaseDetailView(DetailView, CustomBaseView):
    def detail_context(self):
        return {}

class CustomBaseFormView(FormView, CustomBaseView):
    def form_context(self):
        return {}

class CustomBaseCreateView(CreateView, CustomBaseView):
    def create_context(self):
        return {}


class CustomBaseUpdateView(UpdateView, CustomBaseView):
    def update_context(self):
        return {}


class CustomBaseDeleteView(DeleteView, CustomBaseView):
    def delete_context(self):
        return {}


class BaseTemplateView(TemplateView,CustomBaseView):
    def template_context(self):
        return {
            "site":self.request.site
        }



class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_data = ProfileSerializer(user)
        return Response(user_data.data)
