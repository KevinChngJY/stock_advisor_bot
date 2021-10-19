from django.contrib import admin
from .models import userdatabase, bursalist, option1_selection, option3_stock_monitoring,sentimentanalysistop10

# Register your models here.
admin.site.register(userdatabase)
admin.site.register(bursalist)
admin.site.register(option1_selection)
admin.site.register(option3_stock_monitoring)
admin.site.register(sentimentanalysistop10)
