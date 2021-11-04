import boto3
import json

def lambda_handler(event, context):
    
    #SQS msg processing and getting file name
    
    sqs = boto3.resource('sqs') 
    queue = sqs.get_queue_by_name(QueueName='QUEUE_NAME')
    message = queue.receive_messages(WaitTimeSeconds=3)
    msgbody = json.loads(message[0].body)
    objname = msgbody["Records"][0]["s3"]["object"]["key"]
    response = queue.delete_messages(Id=message['MessageId'])
    
    #getting metadata of the file uploaded to s3
    
    s3 = boto3.client('s3')
    s3head = s3.head_object(Bucket='BUCKETNAME', Key=objname)
    metadata = s3head["Metadata"]
    moviename = metadata["movie-name"]
    filename = metadata["movid"]
    releaseyear = metadata["ryear"]
    producer = metadata["prod"]
    director = metadata["dir"]
    review = metadata["rtext"]
    username = metadata["uname"]
    sqlhost = 'RDS-HOST'
    sqluser = 'RDS-USER'
    sqlsec = 'RDS-PW'
    sqldb = 'RDS-DB'
    
    #Run ECS task for each sqs msg
    
    client = boto3.client('ecs')
    response = client.run_task(
    cluster='CLUSTER_NAME', # name of the cluster
    launchType = 'FARGATE',
    taskDefinition='DEF_NAME', # replace with your task definition name and revision
    count = 1,
    platformVersion='LATEST',
    networkConfiguration={
         'awsvpcConfiguration': {
             'subnets': [
                 'subnet-', # replace with your public subnet or a private with NAT
             ],
             'assignPublicIp': 'ENABLED'
        }
     },
    overrides={
        'containerOverrides': [
            {
                'name': 'CONTAINER_NAME',
                'environment': [
                    {
                        'name': 'UserName',
                        'value': username
                    },
                                        {
                        'name': 'MovieName',
                        'value': moviename
                    },
                                        {
                        'name': 'ReleaseYear',
                        'value': releaseyear
                    },
                                        {
                        'name': 'Producer',
                        'value': producer
                    },
                                        {
                        'name': 'Director',
                        'value': director
                    },
                                        {
                        'name': 'SEQTOLANG_TEXT',
                        'value': review
                    },
                                        {
                        'name': 'FileName',
                        'value': filename
                    },
                                         {
                        'name': 'sqlhost',
                        'value': sqlhost
                    },
                                         {
                        'name': 'sqluser',
                        'value': sqluser
                    },
                                         {
                        'name': 'sqlsec',
                        'value': sqlsec
                    },
                                         {
                        'name': 'sqldb',
                        'value': sqldb
                    }
                ]
            }
        ]
    }
   )
