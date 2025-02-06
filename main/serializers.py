from rest_framework import serializers
from .models import *


class GetUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'date_joined', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def get_role(self, obj):
        """
        Roleni aniqlash:
        - Agar foydalanuvchi Mentor bo‘lsa, 'mentor' qaytadi.
        - Agar foydalanuvchi Student bo‘lsa, 'student' qaytadi.
        - Agar ikkalasiga ham aloqador bo‘lmasa, 'unknown' qaytadi.
        """
        if hasattr(obj, 'mentor'):
            return 'mentor'
        elif hasattr(obj, 'student'):
            return 'student'
        return 'unknown'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class MentorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Mentor
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['birth_date', 'image', 'bio','phone_number']  # Student'lar faqat shularni o'zgartira oladi


class PointTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointType
        fields = '__all__'


class GivePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = GivePoint
        fields = '__all__'



class GetPointSerializer(serializers.ModelSerializer):
    student=StudentSerializer()
    class Meta:
        model = GivePoint
        fields = '__all__'

class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = '__all__'

class NewsReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsReadStatus
        fields = ['id', 'user', 'news', 'is_read']

