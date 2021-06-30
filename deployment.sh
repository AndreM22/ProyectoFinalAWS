
#!/bin/bash
DEPLOYMENT_BUCKET="test-bank-project"
STACK_NAME="bank-stack-test"

while getopts ":bdpc" OPTION; do
    case $OPTION in
    d)
      DEPLOY=1
      ;;
    p)
      PACKAGE=1
      ;;
    b)
      BUILD=1
      ;;
    c)
      DATA_BASE=1
      ;;
    *)
      ;;
    esac
done

if [[ $BUILD == 1 ]]
then
    pip3 install --target package -r requirements.txt
    cp -a src/. package/
    # zip -r9 ../function.zip .
    # cd ../src
    # zip -g ../function.zip *
fi

if [[ $PACKAGE == 1 ]]
then
    aws cloudformation package --template-file template.yaml --s3-bucket $DEPLOYMENT_BUCKET --output-template-file packaged-template.json
fi

if [[ $DEPLOY == 1 ]]
then
    aws cloudformation deploy --template-file packaged-template.json --stack-name $STACK_NAME --capabilities CAPABILITY_NAMED_IAM
fi
if [[ $DATA_BASE == 1 ]]
then
    aws s3 cp TablaEmpresas.csv s3://bucket-prueba-company-1/TableEmpresas.csv
    # aws s3 cp test.txt s3://mybucket/test2.txt
fi