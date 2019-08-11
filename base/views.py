from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
import os
import requests
from django.conf import settings
import zipfile
from django.core.mail import EmailMessage
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders

class Process(APIView):
	def post(self, request):
		urlserialzer = UrlSerializer(data=request.data)
		file_dir = os.path.join(settings.BASE_DIR, 'resource')
		zip_file_dir = os.path.join(file_dir,"outzipfile.zip")
		zip = zipfile.ZipFile(zip_file_dir,'w')
		if urlserialzer.is_valid():
			urls = urlserialzer.data['urls']
			i = 0
			for url in urls:
				re = requests.get(url)
				filename = "test" + str(i) + ".html"
				file_path = os.path.join(file_dir,filename)
				file = open(file_path, 'w')
				file.write(str(re.content))
				file.close()
				i+=1
				zip.write(file_path, filename, compress_type=zipfile.ZIP_DEFLATED)
			zip.close()
			process_email(zip_file_dir, urlserialzer.data['email'])
			return Response(200)
		else:
			return Response(urlserialzer.errors)

def process_email(zip_file_dir, to_mail):
	print(zip_file_dir)
	print(to_mail)
	fromaddr = "iamsangeethms@gmail.com"
	toaddr = to_mail
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Zipped File of HTML files"
	body = "Hi,\n\nPlese check attachment\n\nSangeeth M S"
	msg.attach(MIMEText(body, 'plain'))
	filename = "outzipfile.zip"
	attachment = open(zip_file_dir, "rb")
	p = MIMEBase('application', 'octet-stream') 
	p.set_payload((attachment).read())
	encoders.encode_base64(p)
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	msg.attach(p)
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(fromaddr, "ymsowhvicennzoii")
	text = msg.as_string()
	s.sendmail(fromaddr, toaddr, text)
	s.quit()


