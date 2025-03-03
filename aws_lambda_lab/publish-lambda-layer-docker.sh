# clean previous artifacts
rm -rf lambda-env || true
rm -r lambda.zip || true
rm -r lambda-layer.zip || true

# install dependancies with Docker
docker logout || true # logout of dockerhub so can use AWS Public ECR
docker pull public.ecr.aws/lambda/python:3.13-arm64

docker run --rm \
    --volume $(pwd):/out \
    --entrypoint /bin/bash \
    public.ecr.aws/lambda/python:3.13-arm64 \
    -c ' \
    pip install \
        -r /out/requirements.txt \
        --target /out/lambda-env/python \
    '

# change directory to zip lambda handler and zip virtual environment w/ lambda layer
cd lambda-env
zip -r ../lambda-layer.zip ./

cd ../scripts
zip -r ../lambda.zip ./

cd ..

# set environment variables
export AWS_PROFILE=cloud-course
export AWS_REGION=us-east-1

# publish lambda.zip to AWS Lambda service
aws lambda update-function-code \
    --function-name demo-func \
    --zip-file fileb://./lambda.zip \
    --output json | cat

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
