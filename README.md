Serverless Machine Learning pipeline (s3->sqs->lambda->ECS fargate->rds):

This is a simple serverless pipeline that translates English text to deutch or french language using ML modules in python.

Upload file to s3 then trigger a s3 event on file upload.

Send the event to sqs for processing and our processor here is a lambda function.

Read the msg from sqs and extract the file name then gets the uploaded file's Metadata
for later processing in ECS Fargate.

Insert the file's metadata and the translated text to an mysql rds instance.
