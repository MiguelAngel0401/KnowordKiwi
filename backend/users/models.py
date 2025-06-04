import uuid
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255, null=False, blank=False)
    password_hash = models.CharField(max_length=255, null=False, blank=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    real_name = models.CharField(max_length=100, null=False, blank=False)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    email_verification_expires_at = models.DateTimeField(blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_expires_at = models.DateTimeField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    

