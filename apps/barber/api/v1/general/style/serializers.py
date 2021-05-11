from rest_framework import serializers
from utils.generals import get_model

StyleCategory = get_model('barber', 'StyleCategory')
StyleItem = get_model('barber', 'StyleItem')
StyleAttachment = get_model('barber', 'StyleAttachment')
StyleOfTheYear = get_model('barber', 'StyleOfTheYear')


class ListStyleAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleAttachment
        fields = ('label', 'image',)


class ListStyleItemSerializer(serializers.ModelSerializer):
    attachments = ListStyleAttachmentSerializer(many=True)

    class Meta:
        model = StyleItem
        fields = ('uuid', 'label', 'attachments',)
        depth = 1


class ListStyleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='barber_api:general:style-detail',
                                               lookup_field='uuid', read_only=True)
    items = ListStyleItemSerializer(many=False)

    class Meta:
        model = StyleCategory
        fields = '__all__'


class RetrieveStyleSerializer(serializers.ModelSerializer):
    items = ListStyleItemSerializer(many=False)

    class Meta:
        model = StyleCategory
        fields = '__all__'


class ListStyleOfTheYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleOfTheYear
        fields = '__all__'
