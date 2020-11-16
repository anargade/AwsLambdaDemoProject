pipeline {
	agent any
	
	stages{
		stage ('Test Stage') {
			steps {
				sh 'javac src/main/java/CreateLambdaFunction.java java src/main/java/CreateLambdaFunction -Dparam1=$FUNCTION_NAME'
			}
		}
	}	
}
