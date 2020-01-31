import json
import botocore
import boto3
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
  try:
    response = {}
    Iteration = event['Iteration']
    logger.info('Clean >> Starting...')
    clean_up()
    if check():
        response = {"statusCode": 200,"Message": "Succesful", "Iteration": Iteration, "Stopped": 1}
        logger.info('Clean >> All resources are stopped')
    else:
        response = {"statusCode": 200,"Message": "Succesful", "Iteration": Iteration, "Stopped": 0}
        logger.info('Clean >> Resources are still running...')
    return response
  except Exception as e:
    logger.info('Error while executing Cleaning: '+str(e))
    response = {"statusCode": 500,"Message": str(e), "Iteration": event['Iteration']}
    return response

def clean_up():
    try:
        # Cleaning EC2...
        ec2s = listing_ec2(['pending', 'running'])
        if len(ec2s) > 0:
            logger.info('Cleaning >> Stopping EC2 Instances')
            stopping_ec2(ec2s)

        # Cleaning RDS
        rdss = listing_rds('available')
        if len(rdss) > 0:
            logger.info('Cleaning >> Stopping RDS Instances')
            stopping_rds(rdss)

        # Cleaning Clusters
        clusters = listing_rds_cluster('available')
        if len(clusters) > 0:
            logger.info('Cleaning >> Stopping RDS Aurora Clusters')
            stopping_rds_clusters(clusters)
        
        # Cleaning Sage Maker
        sms = listing_sm('InService')
        if len(sms) > 0:
            logger.info('Cleaning >> Stopping Sage Maker Instances')
            stopping_sm(sms)

    except Exception as e:
        logger.info('Error while executing Cleaning: '+str(e))

def check():
    try:
        # checking instances status..
        return check_ec2_stopped() and check_rds_clusters() and check_rds_stopped() and check_sm_stopped()
    except Exception as e:
        logger.info('Error while executing Check: '+str(e))

def listing_ec2(ec2_states):
  try:
    instances = []
    ec2 = boto3.client('ec2')
    ec2_result = ec2.describe_instances(Filters=[{'Name':'instance-state-name','Values':ec2_states}])
    for reservation in ec2_result['Reservations']:
      for instance in reservation['Instances']:
        instances.append(instance['InstanceId'])
    #instances = ['i-037c369dd9b7510ec', 'i-070b04d8f0f9f680c','i-0aaf513951e58821b']
    return instances
  except botocore.exceptions.ClientError as e:
    logger.info('Cleaning >> Error Listing EC2 Instances: '+str(e.response['Error']['Message']))
    return []

def stopping_ec2(instances):
  try:
    ec2 = boto3.client('ec2')
    for instance in instances:
      try:
        result = ec2.stop_instances(InstanceIds=[instance])
        logger.info('Cleaning >> Stopping EC2 Instance: '+str(instance))
      except botocore.exceptions.ClientError as err:
        logger.info('Cleaning >> Error Stopping ec2 Instance '+str(instance)+': '+err.response['Error']['Message'])
  except botocore.exceptions.ClientError as e:
    logger.info('Cleaning >> Error Stopping EC2 Instances: '+str(e.response['Error']['Message']))

def listing_rds(status):
  try:
    instances = []
    rds = boto3.client('rds')
    rds_result = rds.describe_db_instances()
    for rdsi in rds_result['DBInstances']:
      if rdsi['DBInstanceStatus'] == 'available':
        instances.append(rdsi['DBInstanceIdentifier'])
    #instances = ['test-lambda-rc3', 'test-lambda-rc5']
    return instances
  except botocore.exceptions.ClientError as err:
    logger.info('Cleaning >> Error Listing RDS Instances: '+str(err.response['Error']['Message']))
    return []

def stopping_rds(instances):
  try:
    rds = boto3.client('rds')
    for instance in instances:
      try:
        rds.stop_db_instance(DBInstanceIdentifier=instance)
        logger.info('Cleaning >> Stopping RDS Instance: '+instance)
      except botocore.exceptions.ClientError as e:
        logger.info('Cleaning >> Error Stopping RDS Instance '+str(instance)+': '+e.response['Error']['Message'])
  except botocore.exceptions.ClientError as err:
    logger.info('Cleaning >> Error Stopping RDS Instances: '+str(err.response['Error']['Message']))

def listing_sm(status):
  try:
    instances = []
    sage = boto3.client('sagemaker')
    sage_result_service = sage.list_notebook_instances(StatusEquals=status)
    for n_insta in sage_result_service['NotebookInstances']:
      instances.append(n_insta['NotebookInstanceName'])
    #instances = ['test-lambda-rc6', 'test-lambda-rc4']
    return instances
  except botocore.exceptions.ClientError as err:
    logger.info('Cleaning >> Error stopping Sage Maker Instances: '+str(err.response['Error']['Message']))
    return []

def stopping_sm(instances):
  try:
    sage = boto3.client('sagemaker')
    for instance in instances:
      try:
        sage.stop_notebook_instance(NotebookInstanceName=instance)
        logger.info('Cleaning >> Stopping Sage Maker Instance: '+instance)
      except botocore.exceptions.ClientError as e:
        logger.info('Cleaning >> Error Stopping Sage Maker Instance: '+instance+" : "+str(e.response['Error']['Message']))
  except botocore.exceptions.ClientError as err:
    logger.info('Cleaning >> Error stopping Sage Maker Instances: '+str(err.response['Error']['Message']))

def listing_rds_cluster(status):
  try:
    clusters = []
    rds = boto3.client('rds')
    cluster_result = rds.describe_db_clusters()
    for cluster in cluster_result['DBClusters']:
      if cluster['Status'] == status:
        clusters.append(cluster['DBClusterIdentifier'])
    #clusters = ['test-lambda-cluster']
    return clusters
  except botocore.exceptions.ClientError as err:
    logger.info('Cleaning >> Error Listing RDS Clusters: '+str(err.response['Error']['Message']))
    return []

def stopping_rds_clusters(clusters):
  try:
    rds = boto3.client('rds')
    for cluster in clusters:
      try:
        rds.stop_db_cluster(DBClusterIdentifier=cluster)
        logger.info('Cleaning >> Stopping RDS Cluster: '+cluster)
      except botocore.exceptions.ClientError as e:
        logger.info('Cleaning >> Error Stopping RDS Cluster '+str(cluster)+': '+e.response['Error']['Message'])
  except botocore.exceptions.ClientError as err:
    logger.info('Cleaning >> Error Stopping RDS Clusters: '+str(err.response['Error']['Message']))

def check_ec2_stopped():    
  try:
    logger.info('Cleaning >> Checking EC2 Instances State... ')
    ec2 = boto3.client('ec2')
    ec2_result = ec2.describe_instances()
    for reservation in ec2_result['Reservations']:
      for instance in reservation['Instances']:
        if instance['State']['Name'] != 'stopped' and instance['State']['Name'] != 'terminated':
            logger.info('Cleaning >> EC2 Instance in '+str(instance['State']['Name'])+' status...')
            return False
    return True
  except botocore.exceptions.ClientError as err:
    logger.info('Cleaning >> Error Checking all EC2 Instances: '+str(err.response['Error']['Message']))
    return False

def check_rds_stopped():
  try:
    logger.info('Cleaning >> Checking RDS Instances State... ')
    rds = boto3.client('rds')
    rds_result = rds.describe_db_instances()
    for rdsi in rds_result['DBInstances']:
      if rdsi['DBInstanceStatus'] != 'stopped':
          logger.info('Cleaning >> RDS Instance in '+rdsi['DBInstanceStatus']+' status...')
          return False
    return True
  except botocore.exceptions.ClientError as err:
    logger.info('Cleaning >> Error Checking all RDS Instances: '+str(err.response['Error']['Message']))
    return False

def check_sm_stopped():
  try:
    logger.info('Cleaning >> Checking Sage Maker Instances State... ')
    sage = boto3.client('sagemaker')
    sage_result_service = sage.list_notebook_instances()
    for n_insta in sage_result_service['NotebookInstances']:
      if n_insta['NotebookInstanceStatus'] != 'Stopped':
          logger.info('Cleaning >> Sagemaker Instance in '+n_insta['NotebookInstanceStatus']+' status...')
          return False
    return True
  except botocore.exceptions.ClientError as err:
    logger.info('Cleaning >> Error Checking all SM Instances: '+str(err.response['Error']['Message']))
    return False

def check_rds_clusters():
  try:
    logger.info('Cleaning >> Checking RDS Clusters State... ')
    rds = boto3.client('rds')
    cluster_result = rds.describe_db_clusters()
    for cluster in cluster_result['DBClusters']:
      if cluster['Status'] != 'stopped':
          logger.info('Cleaning >> RDS Aurora Cluster in '+cluster['Status'] +' status...')
          return False
    return True
  except botocore.exceptions.ClientError as err:
    logger.info('Cleaning >> Error Checking all RDS Clusters: '+str(err.response['Error']['Message']))
    return False