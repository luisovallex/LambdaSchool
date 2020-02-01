# LambdaSchool

This repository contains the template for the Lambda School project. This template is in charge of stopping EC2, RDS and Sage Maker instaces when the estimated budget is reached.

## LambdaSchool Diagram

This is the structure of how Lambda School works:

## Infrastructure

This template was built using AWS Cloudformation Nested Stacks. The *master* files is in charge to create all the resources needed.

### Parameters

| Parameter        | Description           | Type    |
| ------------- |:-------------:| -----:|
| S3Bucket      | S3 Bucket where the template is hosted | String |
| MaxLambdaWaitTime      | Timeout for lambda functions  |   Number |
| WaitingTime | Time in minutes that the step function will wait berfore retrying      |    Number |
| EmailAddress | Email address to send notification when the cleaning process ends     |    Number |
| RetryTimes | The number of times the process will try to clean the resources     |    Number |
| BudgetAmout | Budget Treshold     |    Number |
| OwnerName | An arbitrary tag name for the owner of these resources    |    String |
| StackName | The name of the stack to which these resources belong      |    String |
| Environment | Environment name to append to resources names and tags     |    String |

### Stacks

#### LambdaStack
* Template in charge of creating lambda functions that will be used for state machine.

#### Parameters

| Parameter        | Description           | Type    |
| ------------- |:-------------:| -----:|

