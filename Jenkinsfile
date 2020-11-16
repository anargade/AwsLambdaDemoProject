pipeline {
	agent any
	
	stages{
		stage ('Test Stage') {
			steps {
				sh 'javac CreateLambdaFunction.java java CreateLambdaFunction -Dparam1=$FUNCTION_NAME'
			}
		}
	}	
}
