from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

# Serializador para devolver información del usuario (incluyendo is_staff)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}, # La contraseña solo se escribe, no se lee
            'is_staff': {'read_only': True}, # El usuario no puede autoasignarse como staff
            'is_superuser': {'read_only': True} # El usuario no puede autoasignarse como superuser
        }
    def create(self, validated_data):
        # Crear el usuario con la contraseña hasheada
        user = User.objects.create_user(
            username=validated_data['email'], # Usaremos el email como username para simplificar
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Por defecto, los usuarios registrados no son staff ni superusuarios
        return user

# Serializador para la gestión de usuarios por un administrador
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False, 'style': {'input_type': 'password'}},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
            # El admin sí puede modificar estos campos
            'is_staff': {'required': False},
            'is_superuser': {'required': False},
            'is_active': {'required': False},
        }

    def create(self, validated_data):
        # El admin puede establecer is_staff e is_superuser directamente
        # Asegurarse de que la contraseña se provea para la creación
        password = validated_data.pop('password') # Si no hay password, esto dará KeyError, lo cual es bueno para la creación
        user = User.objects.create_user(
            username=validated_data['email'], # Usamos email como username
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=validated_data.get('is_staff', False),
            is_superuser=validated_data.get('is_superuser', False),
            is_active=validated_data.get('is_active', True)
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        if 'email' in validated_data and instance.email != validated_data['email']:
            instance.username = validated_data['email'] # Actualizar username si el email cambia
        return super().update(instance, validated_data)

# Serializador para validar las credenciales de login (similar al de DRF)
class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'No se pudo iniciar sesión con las credenciales proporcionadas.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Debe incluir "username" y "password".'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs