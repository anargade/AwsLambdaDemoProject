#!/bin/bash
 
FUNCTION_NAME=$1
echo "function_name: ${FUNCTION_NAME}"
echo "$FUNCTION_NAME"
zipfile=zip ${FUNCTION_NAME}.zip src/main/Lambdas/
echo "zip created with name: ${zipfile}"

