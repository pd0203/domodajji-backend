from rest_framework import serializers
from users.models import User 
from rest_framework.exceptions import ValidationError, NotFound
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password, check_password

class UserSignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User 
        fields = ['email', 'password', 'password2', 'name', 'phone_number']
    def create(self, validated_data):
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError('PASSWORD1 AND PASSWORD2 DO NOT MATCH')
        validated_data.pop('password2')
        encoded_password = make_password(password)
        validated_data['password'] = encoded_password
        return User.objects.create(**validated_data)
    def validate(self, data):
        user = User.objects.filter(email=data['email'])
        if user: 
           raise ValidationError('USER ALREADY REGISTERED')
        if len(data['phone_number']) != 11: 
           raise ValueError('PHONE NUMBER MUST BE 11 CHARACTERS')
        return data
    def validate_password(self, password):
        try:
           validate_password(password)
           return password
        except ValidationError as v:
            raise serializers.ValidationError(v.args)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True) 
    class Meta:
        model = User
        fields = ['email', 'password']
    def create(self, validated_data):
        return User.objects.filter(email=validated_data['email']).first
    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if not user: 
           raise NotFound('USER NOT FOUND')
        raw_password = data['password']
        encoded_password = user.password
        if check_password(raw_password, encoded_password) is False:
           raise ValidationError('PASSWORD IS INCORRECT') 
        return data 
    