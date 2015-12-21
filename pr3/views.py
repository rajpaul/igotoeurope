from django.shortcuts import render_to_response, render

def home(request):
	
	return render(request, "home.html", {})
