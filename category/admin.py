from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('category_name', 'slug', 'created_at')
  prepopulated_fields = {'slug': ('category_name',)}


# you can you this line of code below to register the Model (Category) or use Decorator
# admin.site.register(Category,  CategoryAdmin)
