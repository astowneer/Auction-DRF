from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password", "password2", "first_name", "last_name")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True}
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password didn't match"})
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        user.set_password(validated_data["password"])
        user.save()

        return user
    

class ChangePassswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attr):
        if attr["password"] != attr["password2"]:
            raise serializers.ValidationError({"password": "Password didn't match"})
        
        return attr
    
    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old password", "Old password not correct"})

        return value
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()

        return instance
    

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True}
        }

        def validate_email(self, value):
            user = self.context["request"].user
            if User.objects.exclude(pk=user.id).filter(email=value).exists():
                raise serializers.ValidationError({"email": "Email is already exists"})
            
            return value

        def update(self, instance, validated_data):
            instance.first_name = validated_data["first_name"]
            instance.last_name = validated_data["last_name"]
            instance.email = validated_data["email"]
            instance.save()

            return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token["username"] = user.username
        return token
    
