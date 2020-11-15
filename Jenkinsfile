pipeline {
	agent any
	
	stages{
		stage ('Test Stage') {
			steps {
				sh './script.sh $FIRST_NAME @LAST_NAME $SHOW'
			}
		}
	}	
}
