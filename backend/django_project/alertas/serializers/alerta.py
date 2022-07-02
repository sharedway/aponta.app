
from rest_framework import serializers
from alertas.models import AlertaModel

class AlertaModelSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        modificado_por = self.context.get('modificado_por',None)
        if modificado_por:
            validated_data.update({
                'modificado_por':modificado_por
            })        
        instance = super().update(instance, validated_data)
        return instance

    def create(self, validated_data):        
        criado_por = self.context.get('criado_por',None)
        if criado_por:
            validated_data.update({
                'criado_por':criado_por
            })
            
        instance = AlertaModel.objects.create(**validated_data)       
        return instance

    class Meta:
        model = AlertaModel
        fields = AlertaModel.SERIALIZABLES
        if AlertaModel.READ_ONLY_FIELDS:
            read_only_fields =AlertaModel.READ_ONLY_FIELDS
