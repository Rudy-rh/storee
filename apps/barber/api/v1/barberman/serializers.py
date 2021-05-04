from rest_framework import serializers
from utils.generals import get_model

BranchBarberman = get_model('barber', 'BranchBarberman')


class BarbermanSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()
    name = serializers.CharField(source='user.name')

    class Meta:
        model = BranchBarberman
        fields = '__all__'

    def get_picture(self, instance):
        request = self.context.get('request')
        picture = instance.user.profile.picture
        if picture:
            return request.build_absolute_uri(picture.url)
        return None
