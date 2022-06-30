
from rest_framework import serializers
from aplicativos.models import AppImagem

class AppImagemSerializer(serializers.ModelSerializer):   
    def create(self, validated_data):        
        criado_por = self.context.get('criado_por',None)
        if criado_por:
            validated_data.update({
                'criado_por':criado_por
            })
            
        instance = AppImagem.objects.create(**validated_data)       
        return instance

    class Meta:
        model = AppImagem
        fields = AppImagem.SERIALIZABLES
        if AppImagem.READ_ONLY_FIELDS:
            read_only_fields =AppImagem.READ_ONLY_FIELDS
