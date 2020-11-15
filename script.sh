#!/bin/bash
 
FUNCTION_NAME=$1
echo "function_name: ${FUNCTION_NAME}"
echo "$FUNCTION_NAME"
zipfile=zip -r ${FUNCTION_NAME}.zip ./Lambdas/
echo "zip created with name: ${zipfile}"

