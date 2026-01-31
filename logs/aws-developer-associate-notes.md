# AWS Certified Developer Associate - Study Notes

> My learning path and key concepts for the AWS CDA certification.

---

## Certification Overview

The **AWS Certified Developer - Associate (DVA-C02)** validates proficiency in:
- Developing and maintaining AWS-based applications
- Writing code that interacts with AWS services
- Understanding CI/CD pipelines
- Security best practices

## Core Services to Master

### 1. Compute

#### Lambda
- Serverless compute service
- Pay per invocation (first 1M requests free)
- Max execution time: 15 minutes
- Memory: 128MB to 10GB

```python
# Simple Lambda handler
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
```

#### EC2
- Virtual servers in the cloud
- Instance types: t2, t3, m5, c5, etc.
- Know the difference between On-Demand, Reserved, and Spot instances

### 2. Storage

#### S3
- Object storage with 99.999999999% durability
- Storage classes: Standard, IA, Glacier
- Bucket policies vs IAM policies

#### DynamoDB
- Fully managed NoSQL database
- Key concepts: Partition Key, Sort Key, GSI, LSI
- Read/Write Capacity Units

### 3. Messaging

#### SQS (Simple Queue Service)
- Fully managed message queuing
- Standard vs FIFO queues
- Visibility timeout, Dead Letter Queues

#### SNS (Simple Notification Service)
- Pub/Sub messaging
- Push notifications, SMS, Email
- Fan-out pattern with SQS

### 4. Security

#### IAM (Identity and Access Management)
- Users, Groups, Roles, Policies
- Always follow least privilege principle
- Never use root account for daily tasks

#### Cognito
- User authentication and authorization
- User Pools vs Identity Pools
- Integration with social identity providers

## Study Resources

1. **AWS Official Documentation** - Always the primary source
2. **Stephane Maarek's Course** - Comprehensive Udemy course
3. **AWS Skill Builder** - Free labs and learning paths
4. **Practice Exams** - Essential for exam readiness

## My Study Plan

| Week | Focus Area |
|------|------------|
| 1-2 | IAM, EC2, VPC basics |
| 3-4 | S3, DynamoDB |
| 5-6 | Lambda, API Gateway |
| 7-8 | SQS, SNS, Step Functions |
| 9-10 | CI/CD, CloudFormation |
| 11-12 | Review + Practice Exams |

## Key Exam Tips

- Read questions **carefully** - AWS loves tricky wording
- Eliminate obviously wrong answers first
- Look for keywords: "most cost-effective", "highly available", "least operational overhead"
- Time management: ~2 minutes per question

---

*Status: In Progress*
*Last Updated: 2025-11-15*
