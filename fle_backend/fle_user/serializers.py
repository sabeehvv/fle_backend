from rest_framework import serializers, validators
from .models import Account
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = ["id", "first_name", "last_name", "email",
                  "mobile", "password", "place", "occupation", "picture"]

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    UniqueValidator(
                        queryset=Account.objects.all(),
                        message='A user with this email already exists. Please try with another one.'
                    )
                ]
            },
            'mobile': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    UniqueValidator(
                        queryset=Account.objects.all(),
                        message='A user with this mobile number already exists. Please try with another one.'
                    )
                ]
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password', 'email_token')


class UserInfoUpdatedSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    def get_profile_picture_url(self, obj):
        if obj.picture:
            return self.context['request'].build_absolute_uri(obj.picture.url)
        return None

    class Meta:
        model = Account

        fields = ['id', 'first_name', 'email',
                  'is_superuser', 'profile_picture_url']


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = ["id", "first_name", "last_name", "email", "mobile",
                  "place", "occupation", "picture", 'is_superuser']
