pipeline {
	agent any
	
	stages{
		stage ('Import Boto Stage') {
			steps {
				git 'https://github.com/boto/boto3.git'
				sh 'pip install --user .'
			}
		}
		stage ('Test Stage') {
			steps {
				sh 'python3 main.py $Env $FUNCTION_NAME'
			}
		}
	}	
}
