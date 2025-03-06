from .models import Category

def menu_list(request):
  links = Category.objects.all()
  return {'links':links} #return as dictionary


