from django.db import models

# Create your models here.
class Client(models.Model):
    """
    """
    client_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    api_key = models.CharField(max_length=32, null=True,
                               blank=True, db_index=True)

class UserInfo(models.Model):
    """
    """
    username = models.CharField(max_length=255)
    email = models.EmailField()
    name = models.CharField(max_length=500, null=True, blank=True)
    client = models.ForeignKey(Client, null=True)

class SessionInfo(models.Model):
    """
    """
    sessionkey = models.CharField(max_length=32, null=True,
                                  blank=True)
    login_at = models.DateTimeField(null=True)
    logout_at = models.DateTimeField(null=True)

class Location(models.Model):
    """
    """
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

class ClientData(models.Model):
    """
    """
    page_name = models.CharField(max_length=500)
    timestamp = models.DateTimeField(null=True)
    location = models.ForeignKey(Location)
    user = models.ForeignKey(UserInfo)
    session = models.ForeignKey(SessionInfo)
    client = models.ForeignKey(Client)
