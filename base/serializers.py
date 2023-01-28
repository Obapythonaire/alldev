from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Advocate, Company

class CompanySerializer(ModelSerializer):
    employee_count = SerializerMethodField(read_only=True)
    class Meta:
        model = Company
        fields = '__all__'

    def get_employee_count(self, obj):
        count = obj.advocate_set.count()
        return count

class AdvocateSerializer(ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Advocate
        fields = ['name', 'username','joined', 'followers', 'bio', 'company', 'profile_pic']
    
    # def create(self, validated_data):
    #     username = validated_data['username']
    #     if Advocate.objects.filter(username=username).exists():
    #         raise ValidationError("User Already Exists.")
    #     return Advocate.objects.create(**validated_data)
