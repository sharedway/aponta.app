
from rest_framework import serializers
from notifications.models import NotificationModel

class NotificationModelSerializer(serializers.ModelSerializer):   
    def create(self, validated_data):        
        criado_por = self.context.get('criado_por',None)
        if criado_por:
            validated_data.update({
                'criado_por':criado_por
            })
            
        instance = NotificationModel.objects.create(**validated_data)       
        return instance

    class Meta:
        model = NotificationModel
        fields = NotificationModel.SERIALIZABLES
        if NotificationModel.READ_ONLY_FIELDS:
            read_only_fields =NotificationModel.READ_ONLY_FIELDS
