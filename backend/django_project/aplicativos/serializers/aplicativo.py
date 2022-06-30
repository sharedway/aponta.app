
from rest_framework import serializers
from aplicativos.models import AplicativoModel
from .app_imagem import AppImagemSerializer

class AplicativoModelSerializer(serializers.ModelSerializer):
    imagens_de_capa = AppImagemSerializer(many=True)


    def create(self, validated_data):        
        criado_por = self.context.get('criado_por',None)
        if criado_por:
            validated_data.update({
                'criado_por':criado_por
            })
            
        instance = AplicativoModel.objects.create(**validated_data)       
        return instance

    class Meta:
        model = AplicativoModel
        fields = AplicativoModel.SERIALIZABLES
        if AplicativoModel.READ_ONLY_FIELDS:
            read_only_fields =AplicativoModel.READ_ONLY_FIELDS
