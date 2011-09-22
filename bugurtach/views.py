from decorators import render_to

@render_to('home.html')
def homepage(request):
    return {'bug':'sdf'}