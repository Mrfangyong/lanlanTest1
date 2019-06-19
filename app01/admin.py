from django.contrib import admin
from app01.models import User,content_table,article_type_table,crawler_data,IMG


# Register your models here.


admin.site.register(User)
admin.site.register(content_table)
admin.site.register(article_type_table)
admin.site.register(crawler_data)
admin.site.register(IMG)