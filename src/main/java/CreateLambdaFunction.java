import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;

import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.lambda.LambdaClient;
import software.amazon.awssdk.services.lambda.model.CreateFunctionRequest;
import software.amazon.awssdk.services.lambda.model.CreateFunctionResponse;
import software.amazon.awssdk.services.lambda.model.FunctionCode;
import software.amazon.awssdk.services.lambda.model.LambdaException;
import software.amazon.awssdk.services.lambda.model.Runtime;

public class CreateLambdaFunction {

	public static void testFunction(String[] args) {
		
		String function_name = System.getProperty("param1");
		System.out.println("function_name:--->    "+function_name);
		final String USAGE = "\n" +
                "Usage:\n" +
                "    CreateFunction <functionName><filePath><role><handler> \n\n" +
                "Where:\n" +
                "    functionName - the name of the Lambda function \n"+
                "    filePath - the path to the ZIP or JAR where the code is located \n"+
                "    role - the role ARN that has Lambda permissions \n"+
                "    handler - the fully qualifed method name (for example, example.Handler::handleRequest)  \n";

          //if (args.length < 4) {
              System.out.println(USAGE);
            //  System.exit(1);
         // }

        /* Read the name from command args*/
        String functionName = "lambda-test-function";
        String filePath = "src\\main\\Lambdas\\mylambda.jar";
        String role = "arn:aws:iam::137479420152:role/aws-lambda-demo-role";
        String handler = "mylambda.my_handler";

        Region region = Region.US_EAST_1;
        LambdaClient awsLambda = LambdaClient.builder()
                .region(region)
                .build();

        /* Read the name from command args*/
        createLambdaFunction(awsLambda, functionName, filePath, role, handler);

	}

	  // snippet-start:[lambda.java2.create.main]
    public static void createLambdaFunction(LambdaClient awsLambda,
                                            String functionName,
                                            String filePath,
                                            String role,
                                            String handler) {

        try {
            // Create a SdkBytes object that represents the Lambda code
            InputStream is = new FileInputStream(filePath); 
            SdkBytes fileToUpload = SdkBytes.fromInputStream(is);

            // Create a FunctionCode object
            FunctionCode code = FunctionCode.builder()
                .zipFile(fileToUpload)
                .build();

            CreateFunctionRequest functionRequest = CreateFunctionRequest.builder()
                .functionName(functionName)
                .description("Created by the Lambda Java API")
                .code(code)
                .handler(handler)
                .runtime(Runtime.PYTHON2_7)
                .role(role)
                .build();

            CreateFunctionResponse functionResponse = awsLambda.createFunction(functionRequest);
            System.out.println("The function ARN is "+functionResponse.functionArn());

        } catch(LambdaException | FileNotFoundException e) {
            System.err.println(e.getMessage());
            System.exit(1);
        }
    }
    // snippet-end:[lambda.java2.create.main]
}
