from groceryapp.models import User
from rest_framework import serializers




""" User Registration"""
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password','is_enduser','is_grocery')
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
          
""" Admin Registration"""
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        
    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)
    
    
class UserManageSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ('id','username','email', 'firstname', 'lastname','age','gender','address','is_enduser','is_grocery','is_active','is_staff','is_superuser')
        
        
     def update(self, instance, validated_data):
           instance.username=validated_data.get('username',instance.username)
           instance.email=validated_data.get('email',instance.email)
           instance.firstname=validated_data.get('firstname',instance.firstname)
           instance.lastname=validated_data.get('lastname',instance.lastname)
           instance.age=validated_data.get('age',instance.age)
           instance.gender=validated_data.get('gender',instance.gender)
           instance.address=validated_data.get('address',instance.address)
           instance.save()
           return instance
            

""" ProfileSerializer """
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields=('id','firstname', 'lastname', 'age','gender','address')
      
      
   
    def update(self, instance, validated_data):
      instance.firstname=validated_data.get('firstname',instance.firstname)
      instance.lastname=validated_data.get('lastname',instance.lastname)
      instance.age=validated_data.get('age',instance.age)
      instance.gender=validated_data.get('gender',instance.gender)
      instance.address=validated_data.get('address',instance.address)
      instance.save()
      return instance

        