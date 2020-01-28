import json
import boto3
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    try:
        response = {}
        ec2 = boto3.client('ec2')
        # ----- EC2 -----------------------------
        #Filtering the instances to avoid errors...
        ec2_result = ec2.describe_instances(Filters=[{'Name':'instance-state-name','Values':['running','pending']}])
        instances = []
        for reservation in ec2_result['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance['InstanceId'])
        # Stopping EC2 instances at once
        result = ec2.stop_instances(InstanceIds=instances)

        # ----- RDS -----------------------------
        rds = boto3.client('rds')
        rds_result = rds.describe_db_instances()
        for rdsi in rds_result['DBInstances']:
            try:
                rds.stop_db_instance(DBInstanceIdentifier=rdsi['DBInstanceIdentifier'])
            except Exception as err:
                logger.info('RDS Instance: '+rdsi['DBInstanceIdentifier']+" error while trying to stop it: "+err)
        
        # ------ SAGE MAKER ----------------------
        sage = boto3.client('sagemaker')
        # -- listing in service Sage Maker Instances
        sage_result_service = sage.list_notebook_instances(StatusEquals='InService')
        for n_insta in sage_result_service['NotebookInstances']:
            try:
                sage.stop_notebook_instance(NotebookInstanceName=n_insta['NotebookInstanceName'])
            except Exception err:
                logger.info('Sage Maker Instance: '+n_insta['NotebookInstanceName']+" error while trying to stop it: "+err)
        # -- listing pending Sage Maker Instances
        sage_result_pending = sage.list_notebook_instances(StatusEquals='Pending')
        for n_insta in sage_result_pending['NotebookInstances']:
            try:
                sage.stop_notebook_instance(NotebookInstanceName=n_insta['NotebookInstanceName'])
            except Exception err:
                logger.info('Sage Maker Instance: '+n_insta['NotebookInstanceName']+" error while trying to stop it: "+err)

    except Exception as e:
        response["errorMessage"] = str(e)
        return response