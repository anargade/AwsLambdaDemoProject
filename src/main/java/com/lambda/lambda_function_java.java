package com.lambda;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

public class lambda_function_java implements RequestHandler<Object, Object>{

	@Override
	public Object handleRequest(Object input, Context context) {
		System.out.println("welcome to lambda function");
		return null;
	}
}
