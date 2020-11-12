pipeline {
	agent any
	
	stages{
		stage ('Test Stage') {
			steps {
				sh 'python3 main.py ${Env} ${Lambda}'
			}
		}
		stage ('Import Boto Stage') {
			steps {
				git 'https://github.com/boto/boto3.git'
				sh 'pip install --user .'
			}
		}
	}	
}
