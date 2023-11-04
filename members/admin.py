from django.contrib import admin
from .models import Users, ItemsOnBid, ItemsClaimed

# Register your models here.
admin.site.register(Users)
admin.site.register(ItemsOnBid)
admin.site.register(ItemsClaimed)
