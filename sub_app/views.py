from django.shortcuts import render
from .forms import TextForm

import requests
import os


# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 01:28:54 2021

@author: TAC
"""


import requests
import os


def code(username):
	url = "https://www.reddit.com/user/" + username
	html_content = requests.get(url,headers=headers).text
	if not "Something went wrong" in html_content:
        # the given sentence appears only if the user is banned or does not exist
		if "Sorry, nobody on Reddit goes by that name." in html_content:
			return('The account ' + username +
      'does not exists, or it is shadowbanned. Please don\'t kill me...')
		else:
			return('Everything looks fine for ' + username +
      '. Heartbeats back to normal...')
	else:
		return 1
    
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# Create your views here.
def home(request):
	form=TextForm()
	if request.method=='POST':
		form=TextForm(request.POST)
		
		if form.is_valid():
			print('saving')
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


