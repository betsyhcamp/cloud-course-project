# clean previous artifacts
rm -rf lambda-env || true
rm -r lambda.zip || true
rm -r lambda-layer.zip || true

# install packages in new virtual environment directory ./lambda-env
mkdir -p lambda-env/python
uv pip install --target ./lambda-env/python requests fastapi

# change directory to zip lambda handler and zip virtual environment w/ lambda layer
cd lambda-env
zip -r ../lambda-layer.zip ./

cd ../scripts
zip -r ../lambda.zip ./

cd ..

# set environment variables
export AWS_PROFILE=cloud-course
export AWS_REGION=us-east-1

###### lambda_function.py file contents #######
## import json
## import os
## import requests
## def lambda_handler(event:dict, context):
##   return event

# publish lambda.zip to AWS Lambda service
aws lambda update-function-code \
    --function-name demo-func \
    --zip-file fileb://./lambda.zip \
    --output json | cat

# publish lambda-env.zip as a layer AWS Lambda service
LAYER_VERSION_ARN=$(aws lambda publish-layer-version \
    --layer-name cloud-course-project-python-deps \
    --compatible-runtimes python3.13 --zip-file fileb://./lambda-layer.zip \
    --compatible-architectures arm64 \
    --query 'LayerVersionArn' \
    --output text | cat)

echo $LAYER_VERSION_ARN

# update lambda function to use lambda layer
aws lambda update-function-configuration \
    --function-name demo-func \
    --layers $LAYER_VERSION_ARN \
    --output json | cat
