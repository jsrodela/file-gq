from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'fileapp/index.html', {
    'hello': 'world',
  })

def send(request):
  return render(request, 'fileapp/send.html', {
    
  })

def receive(request):
  return render(request, 'fileapp/receive.html', {
    
  })
