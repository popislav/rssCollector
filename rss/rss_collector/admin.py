from django.contrib import admin

# Register your models here.

from .models import Sources
from .models import Feeds

admin.site.register(Sources)

admin.site.register(Feeds)