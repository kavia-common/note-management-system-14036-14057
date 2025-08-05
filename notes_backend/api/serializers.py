from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

# PUBLIC_INTERFACE
class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label='Confirm password',
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

# PUBLIC_INTERFACE
class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note model.
    """

    class Meta:
        model = Note
        fields = ["id", "user", "title", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
