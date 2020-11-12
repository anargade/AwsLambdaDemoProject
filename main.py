import string
import sys
import os
import zipfile

import boto3

def print_hi(env, lname):

	print('Hi, There')
	print('Arguments from the Jenkins Job: ' + str(sys.argv[1]), str(sys.argv[2]))
	print('Method Parameters: ' + env +' '+lname)

	folder_to_be_ziped = 'Lambdas'
	with zipfile.ZipFile(lname+'.zip', 'w', zipfile.ZIP_DEFLATED) as lnamezip:
		for dirpath, dirnames, files in os.walk(folder_to_be_ziped):
			for file in files:
				lnamezip.write(os.path.join(dirpath, file))
	s3_bucket_obj = boto3.resource('s3',aws_access_key_id='AKIASAATJPD4OY7M2E4X',aws_secret_access_key='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')
	for each_buk in s3_bucket_obj.buckets.all():
		print("Bucket: "+each_buk.name)
		if(each_buk.name == 'ft-demo-bucket'):
			s3 = boto3.resource('s3',aws_access_key_id='AKIASAATJPD4OY7M2E4X',aws_secret_access_key='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')
			s3.meta.client.upload_file('lambda1.zip' ,'ft-demo-bucket' ,'lambda1.zip')
			print("Done")



#s3 = boto3.client('s3')
#s3.upload_file('lambda1.zip', 'mybucket', 'lambda1.zip')



	#handle = zipfile.ZipFile('allpy.zip', 'w')

	#for x in os.listdir():
	#	if x.endswith('.py'):
	#		handle.write(x, compress_type=zipfile.ZIP_DEFLATED)
	#		handle.close()



if __name__ == '__main__':
    print_hi(str(sys.argv[1]), str(sys.argv[2]))





