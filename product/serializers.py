from rest_framework import serializers

from groceryapp.models import User
from groceryapp.serializers import RegistrationSerializer
from.models import Cart, Product, Product_category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
      model = Product_category
      fields = ('id','category_name',)
       
    def create(self, validated_data):
        user=self.context["user"]
        print(user)
        return Product_category.objects.create(user=user,**validated_data)
      
    def update(self, instance, validated_data):
      instance.category_name=validated_data.get('category_name',instance.category_name)
      instance.save()
      return instance
    
# Using Admin view all Category
class CategorySerializers(serializers.ModelSerializer):
    user=RegistrationSerializer()
    class Meta:
      model = Product_category
      fields = ('id','category_name','user')
       


class ProductSerializer(serializers.ModelSerializer):
  class Meta:
        model =Product
        fields = ('product_name', 'description', 'price', 'category')  
  def create(self, validated_data):
        user=self.context["user"]
        return Product.objects.create(user=user,**validated_data)
  
  def update(self, instance, validated_data):
      instance.product_name=validated_data.get('product_name',instance.product_name)
      instance.description=validated_data.get('description',instance.description)
      instance.price=validated_data.get('price',instance.price)
      instance.category=validated_data.get('category',instance.category)
      instance.save()
      return instance
    
    
  def validate(self,data):
      cat=data['category']
      user = self.context['user']
      try:
        obj=Product_category.objects.filter(user=user)
        if obj:
          for obj in obj:
            if obj == cat:
              return super().validate(data)
          else:
            raise serializers.ValidationError('This category not found')
      except Product_category.DoesNotExist:
         raise serializers.ValidationError('This category do exist.')
     
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id','item','quantity','user')

    def create(self, validated_data):
        user=self.context["user"]
        print(user)
        return Cart.objects.create(user=user,**validated_data)
      
      
class PaymentMethodSerializer(serializers.Serializer):
    card_number=serializers.CharField(required=True)
    exp_month= serializers.CharField(required=True)
    exp_year= serializers.CharField(required=True)
    cvc= serializers.CharField(required=True)
    
    
class UserInvoiceSerializer(serializers.Serializer):
  class Meta:
        model = Cart
        fields = ('user','item','price','is_active')
        
        
# Admin Product update      
class UpdateProductSerializer(serializers.ModelSerializer):
  class Meta:
        model =Product
        fields = ('product_name', 'description', 'price', 'category')   

  def update(self, instance, validated_data):
      instance.product_name=validated_data.get('product_name',instance.product_name)
      instance.description=validated_data.get('description',instance.description)
      instance.price=validated_data.get('price',instance.price)
      instance.category=validated_data.get('category',instance.category)
      instance.save()
      return instance