pipeline {
	agent any
	
	stages{
		stage ('Test Stage') {
			steps {
				sh 'chmod 0755 script.sh'
				sh './script.sh $FIRST_NAME $LAST_NAME $SHOW'
			}
		}
	}	
}
