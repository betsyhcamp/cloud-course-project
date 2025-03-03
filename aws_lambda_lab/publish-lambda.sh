# clean previous artifacts
rm -rf lambda-env || true
rm -r lambda.zip || true

# install packages in new virtual environment directory ./lambda-env
uv pip install --target ./lambda-env requests fastapi

# copy lambda handler function into virtual environment directory
cp ./lambda_function.py ./lambda-env/lambda_function.py

# change directory and zip virtual environment w/ lambda handler
cd lambda-env
zip -r ../lambda.zip ./

# set environment variables
export AWS_PROFILE=cloud-course
export AWS_REGION=us-east-1

# lambda_function.py
# import json
# import os
# import requests
# def lambda_handler(event:dict, context):
#   return event

# publish .zip to AWS Lambda service
aws lambda update-function-code --function-name demo-func --zip-file fileb://../lambda.zip
