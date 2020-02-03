# LambdaSchool

This repository contains the template for the Lambda School project. This template is in charge of stopping EC2, RDS and Sage Maker instaces when the estimated budget is reached.

## LambdaSchool Diagram

This is the structure of how the template works:

![Inf Diagram](/img/Diagram.png)

### Elements

* Budget Treshold: budget definition for the student, this will trigger an SNS Message to start the cleaning process

* SNS Budget Trigger: SNS element that will publish a message to start the execution of the cleaning proccess

* State Machine Execution: Lambda in charge of executing the process in the state machine (Step Functions)

* State Machine: Lambda functions orchestration to start the process of stopping EC2, RDS and Sage Maker instaces.

* SNS User Email Notification: notification to the user about the results of the process.

### State Machine

States Diagram:

![Inf Diagram](/img/StateMachine.png)

* Params: pass type state to initialize parameters for the state machine executions

* Clean: Lambda function in charge of stopping instances and checking their status

* Decision: choice type state in charge of deciding if the process should wait for instaces that are still running

* SnsNotification: Lambda function that sends information to user email about the result of the process


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

