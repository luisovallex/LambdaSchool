# LambdaSchool

This repository contains the template for the Lambda School project. This template is in charge of stopping EC2, RDS and SageMaker instaces when the estimated budget is reached.

## LambdaSchool Flowchart

<p align="center">
  <img src="img/LambdaSchool.png"/>
</p>

* **AWS Budgets**: Allows the students define a budget. It's set to send a notification to all the subscribers when the cost of the other services exceed the 100% of the defined amount of money. This resource reset's the first day of everý month.

* **Amazon SNS**: Amazon Simple Notification Service creates a Topic and publish there, every resources subscribed to that Topic will receive a notification when the SNS get triggered.

* **Lamda Function and State Machine**: Lambda in charge of executing the process in the state machine (Step Functions). Lambda functions orchestration to start the process of stopping EC2, RDS and Sage Maker instaces.

* **SNS and Email Notification**: As is writted before, SNS creates a Topic and all the resources subscribed can get a notification, in this case every email selected is going to receive a message when the budget is reached and all the instaces are off.

* **AWS CloudWatch**: 

### How it works?

The *AWS Budget* resource it's created to stablish a maximum amount of money that can be spent. When the cost of the resources exceed the 100% of the stablished budget, it would activate the *AWS SNS* to create a *Topic* and publish notifications in all the subscribers, in this case a *Lambda Function* is going to be the subscriber. 

The *Lambda Function* works like that:

Finally, it's important to say that at the moment all the infrastructure was created *AWS SNS* is going to send an email to the students with a subscription request. If the subscription request was accepted, the students will receive an alert telling that the EC2, the RDS and the SageMaker instances are off.


## Infrastructure

The following template creates the following resources

<p align="center">
  <img src="img/Infra_Lambda_School.jpeg"/>
</p>

* Budget-Notification: is an SNS Topic in charge of triggering the lambda to start the process

* CallStepFunction: Lambda function that starts the state machine execution.

* Cleaning_Lambda: Lambda function that lists Instances and tries to stop them. It also checks the state of the instaces.

* Notify_Lambda: Lambda function in charge of sending the notification about the process to the specified email address.

* Process-Notification: SNS Topic that publishes a message to the specified email address.

### Parameters

<center>

| Parameter        | Description           | Type    |
| ------------- |:-------------:| -----:|
| S3Bucket      | S3 Bucket where the template is hosted | String |
| WaitingTime | Time in seconds that will wait until retrying again      |    Number |
| EmailAddress | Email address to send notification when the cleaning process ends     |    Number |
| RetryTimes | The number of times the process will try to clean the resources if they are still running  |    Number |
| BudgetAmout | Budget amount that will trigger the clean up process, if the billing goes higher than the amount    |    Number |
| OwnerName   | Name of the owner of the resources, this will be used to tag resources that will be created | String
| StackName   | Name of the stack, this will be used to tag resources that will be created | String


</center>

