from tortoise import models
from tortoise import fields
import uuid

class User(models.Model):
    id = fields.UUIDField(default=uuid.uuid4(), primary_key=True)
    username = fields.CharField(max_length=128)
    email = fields.CharField(max_length=128, unique=True)
    first_name = fields.CharField(null=True, blank_re=True, max_length=128)
    last_name = fields.CharField(null=True, blank_re=True, max_length=128)
    is_active = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"