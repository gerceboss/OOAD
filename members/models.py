from unittest.util import _MAX_LENGTH
from django.db import models
#import datetime

class Users(models.Model):
  wallet_addr=models.CharField(max_length=42,default="0x0")
  username = models.CharField(max_length=255)
  role = models.BooleanField()
  password = models.CharField(max_length=500)
  email = models.CharField(max_length=50)
  balance = models.IntegerField()


class ItemsOnBid(models.Model):
  # wallet_addr=models.CharField(max_length=42,default="0x0")
  item_name=models.CharField(max_length=255)
  item_descr=models.CharField(max_length=255)
  item_picture=models.CharField(max_length=255)
  highest_bid=models.IntegerField()
  highest_bidder_username=models.CharField(max_length=255)
  owner_username=models.CharField(max_length=255)
  valid=models.BooleanField()
  initial_time=models.IntegerField(default=0)
  time_left=models.IntegerField(default=0)
  hours=models.IntegerField(default=0)
  minutes=models.IntegerField(default=0)
  

class ItemsClaimed(models.Model):
  # item_id=models.BigIntegerField()
  item_name=models.CharField(max_length=255)
  item_descr=models.CharField(max_length=255)
  item_picture=models.CharField(max_length=255)
  owner_username=models.CharField(max_length=255)
  highest_bidder_username=models.CharField(max_length=255,default="")
  highest_bid=models.IntegerField(default=0)
  # to_address=models.CharField(max_length=42,default="0x0")
