from django.contrib import admin
from .models import Session, Weights, Calisthenics, Cardio
# Register your models here.

admin.site.register(Session)
admin.site.register(Weights)
admin.site.register(Calisthenics)
admin.site.register(Cardio)