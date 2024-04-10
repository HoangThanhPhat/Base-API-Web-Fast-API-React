from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class User(Model):
    id                = fields.IntField(pk = True)
    name              = fields.CharField(max_length=50)
    password          = fields.CharField(max_length=50)
    phone_number      = fields.CharField(max_length=50)
    email             = fields.CharField(max_length=254)
    address           = fields.CharField(max_length=350)
    roleID            = fields.IntField(default=0)
    

    
#Create pydantic models
user_pydantic   = pydantic_model_creator(User, name="User")
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
