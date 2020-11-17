pipeline {
	agent any
	
	stages{
		stage ('Test Stage') {
			steps {
				sh 'main.py $Env $FUNCTION_NAME'
			}
		}
	}	
}
