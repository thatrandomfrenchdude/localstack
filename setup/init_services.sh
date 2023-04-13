# create queue called test
awslocal sqs create-queue --queue-name test

# create bucket called test
awslocal s3api create-bucket --bucket test --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2