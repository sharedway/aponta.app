
from rest_framework import serializers
from notifications.models import NotificationTokenModel

class NotificationTokenModelSerializer(serializers.ModelSerializer):   
    def create(self, validated_data):        
        criado_por = self.context.get('criado_por',None)
        if criado_por:
            validated_data.update({
                'criado_por':criado_por
            })
            
        instance = NotificationTokenModel.objects.create(**validated_data)       
        return instance

    class Meta:
        model = NotificationTokenModel
        fields = NotificationTokenModel.SERIALIZABLES
        if NotificationTokenModel.READ_ONLY_FIELDS:
            read_only_fields =NotificationTokenModel.READ_ONLY_FIELDS
