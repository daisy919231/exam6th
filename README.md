Today I have learned that through related name I get all instances of the same class , not for example product's. But I can I access through fileld names too, like here below:
Yes, there are a couple of issues in the provided code snippet that need to be addressed:

1. Typo in Template Loop: In the template code, you have a typo in the variable name. You are using produc_attribute instead of product_attribute. It should be:
   
   {% for product_attribute in product.product_values.values.all %}
     {{ product_attribute.name }}
   {% endfor %}
   

2. Model Method Naming: The __str__ method in both Attribute and AttributeValue classes is incorrectly defined. It should be __str__ (with double underscores) instead of str. Here’s the corrected version:
   
   class Attribute(BaseModel):
       name = models.CharField(max_length=255, null=True, blank=True)

       def __str__(self):
           return self.name

   class AttributeValue(BaseModel):
       value = models.CharField(max_length=255, null=True, blank=True)
       attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True, related_name='values')
       product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_values', null=True, blank=True)

       def __str__(self):
           return self.value
   

3. Accessing Attribute Name: In your template, you are trying to access product_attribute.name, but product_attribute is an instance of AttributeValue, not Attribute. You should access the related Attribute to get the name. Assuming you want to display the name of the attribute associated with the value, you would do something like this:
   
   {% for product_attribute in product.product_values.all %}
     {{ product_attribute.attribute.name }}
   {% endfor %}
   

With these corrections, the logic should work as intended.

In Django, the ability to easily access related objects is due to the powerful ORM (Object-Relational Mapping) system that Django provides. Here's how it works in your case:

1. ForeignKey Relationships: In your AttributeValue model, you have a ForeignKey relationship to the Attribute model. This means that each AttributeValue instance is linked to a specific Attribute instance. The ForeignKey creates a reverse relationship that allows you to access the related Attribute from an AttributeValue.

   
   class AttributeValue(BaseModel):
       ...
       attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True, related_name='values')
   

2. Related Name: The related_name='values' in the ForeignKey definition allows you to access all AttributeValue instances related to a specific Attribute instance using the values attribute. This is useful for querying and accessing related data.

3. Accessing Related Objects: When you have an instance of AttributeValue, you can access its related Attribute instance directly through the attribute defined in the ForeignKey. For example, if you have an AttributeValue instance called product_attribute, you can access the related Attribute instance like this:

   
   product_attribute.attribute
   

4. Template Rendering: In your template, when you loop through product.product_values.all(), each product_attribute is an instance of AttributeValue. You can easily access the related Attribute name using:

   
   {{ product_attribute.attribute.name }}
   

This design pattern allows for clean and efficient access to related data, making it easy to work with complex data models in Django. The ORM handles the underlying SQL queries for you, so you can focus on working with Python objects instead of writing raw SQL.

So I am hopefully never going to confuse the related name to the class it does not belong. It's owner is where it is living!
