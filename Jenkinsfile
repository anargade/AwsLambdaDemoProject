pipeline {
	agent any
	
	stages{
		stage ('Lambda Deployment Stage') {
			steps {
				sh 'python3 main.py $FUNCTION_NAME $ENV'
			}
		}
		
	}	
}
