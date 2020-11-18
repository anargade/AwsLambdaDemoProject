pipeline {
	agent any
	
	stages{
		
		stage ('Test Stage') {
			steps {
				sh 'python3 main.py $Env $FUNCTION_NAME'
			}
		}
	}	
}
