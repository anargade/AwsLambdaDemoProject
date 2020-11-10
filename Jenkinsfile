pipeline {
	agent any
	
	stages{
		stage ('Test Stage') {
			steps {
				sh 'python main.py ${Env} ${Lambda}'
			}
		}
	}	
}
