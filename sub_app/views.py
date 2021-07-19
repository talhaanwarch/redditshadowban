from django.shortcuts import render
from .forms import TextForm,FileForm
from django.conf import settings
import requests
import os



def code(username):
	url = "https://www.reddit.com/user/" + username
	html_content = requests.get(url,headers=headers).text
	if not "Something went wrong" in html_content:
        # the given sentence appears only if the user is banned or does not exist
		if "Sorry, nobody on Reddit goes by that name." in html_content:
			return('The account ' + username +
      ' does not exists, or it is shadowbanned. ')
		elif '"profileSuspended":true' in html_content:
			return ('Account {} is suspended'.format(username))
		else:
			return('Everything looks fine for ' + username )
	else:
		return 1
    
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# Create your views here.
def home(request):
	form=TextForm()
	if request.method=='POST':
		form=TextForm(request.POST)
		
		if form.is_valid():
			form.save()

		error=True
		while error:
		    username=request.POST['username']
		    res=code(username)
		    print(res)
		    if res==1:
		        print('retrying')
		        error=True
		    else:
		        return render(request,'home.html',{'output':res,'form':form})
		        error=False
		
	return render(request,'home.html',{'form':form})


def filehome(request):
	print(request.method)
	if request.method == 'POST':
		myform = FileForm(request.POST,request.FILES)
		if myform.is_valid():
			myform.save()
			banned,notbanned=[],[]
			for line in request.FILES['fileupload']:
				username = line.decode()  
				error=True
				while error:
					res=code(username)
					print(res)
					if 'shadowbanned' in res:
						banned.append(username)
						error=False
					elif res==1:
						print('retrying')
						error=True
					else:
						notbanned.append(username)
						error=False
			path=os.path.join(settings.BASE_DIR,'sub_app','static','banfile.txt')
			print(path)
			banfile = open(path, "w")
			banfile.write(''.join(banned))
			banfile.close()
			path=os.path.join(settings.BASE_DIR,'sub_app','static','notbanfile.txt')
			notbanfile = open(path, "w")
			notbanfile.write(''.join(notbanned))
			notbanfile.close()

			return render(request,'uploadfile.html',{'fileform':FileForm(),'banned':len(banned),'other':len(notbanned)})		
	else:			
		form = FileForm()
		context={'fileform':form}
		return render(request,'uploadfile.html',context)
