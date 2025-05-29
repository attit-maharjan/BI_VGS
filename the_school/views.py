from django.shortcuts import Render 

def homePage(Request):
      return render("shared/index.htm", request)

def abouteUs(req):
    render("shared/about.html")

def privacyPolcy(request): 
  return render(request, "shared/privacy.html") 

def Terms(request):  
    return render(request,"shared/terms_of_service.htm")  

def accredations(req):
 return render(req,"shared/accred.html")  

def contactPage(r): 
    return Render(r,"shared/contact.html")

