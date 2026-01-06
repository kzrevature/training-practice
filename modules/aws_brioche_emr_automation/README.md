# Automated EMR Deployments - 'Brioche'

This document contains commands which automate the deployment of an EMR cluster.
- Setting up permissions
- Creating the EMR cluster

"But in the real world most of this work would be handled by an orchestration tool–"
and I do not care.
If you think slogging through setup commands is a waste of time
you are more than welcome to stop reading.

'Brioche' is a placeholder name to avoid confusion with other projects.

## Prerequisites

I made a VPC `brioche-vpc` with a single subnet routed to an internet gateway.
The VPC has one (default) security group.

I also made an S3 bucket `brioche-s3`.
The bucket contains a `log` directory for logging
and a simple spark script.

```aws s3 cp spark_step.py s3://brioche-s3/spark_step.py```

## Policies and Permissions

**Resources have Roles. Roles contain Policies. Policies grant Permissions.**

A **permission** covers any kind of action that can be performed in AWS:
listing objects in an S3 bucket, running a Lambda function, deleting an EC2 instance, etc.

A **policy** is a specially formatted JSON file which grants or denies a set of permissions.
It also specifies how and to which resources these permissions are attached
(e.g. deny inserts to DatabaseXYZ, allow read requests only from VPC-123).

A **role** is a grouping of one or more policies.

A **resource** is any AWS service capable of action: SQS, Lambda, etc.

A **trust policy** (aka 'assume role policy') is a specialized policy attached to a role
which describes which resources are allowed to take on said role.
Every role has with exactly 1 trust policy.
Note that trust policies *don't actually assign any roles*;
it's just another level of safeguarding.

A **instance profile** is a extra layer for attaching roles to EC2 instances.
It is mostly pointless (see comments at the end of this doc).

### EMR/EC2 Instance Role

For this module, my EC2 instances (used by EMR) need read/write access to an S3 bucket.
`instance-profile.json` contains those permissions.

Instructions:
1. Create an IAM policy `BriocheInstanceProfilePolicy` with the JSON.
    ```
    aws iam create-policy \
        --policy-name BriocheInstanceProfilePolicy \
        --policy-document file://instance-profile-policy.json
    ```
2. Create an IAM role `BriocheInstanceProfile` for EC2 instances.
    ```
    aws iam create-role \
        --role-name BriocheInstanceProfile \
        --assume-role-policy-document file://instance-profile-assume-role.json
    ```
4. Create an instance profile `BriocheInstanceProfile` (same name) for EC2 instances.
    ```
    aws iam create-instance-profile \
        --instance-profile-name BriocheInstanceProfile
    ```
3. Attach the policy to the role.
    ```
    aws iam attach-role-policy \
        --role-name BriocheInstanceProfile \
        --policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/BriocheInstanceProfilePolicy
    ```
    Note: `<ACCOUNT_ID>` is a placeholder for your 12-digit AWS account id.
    (it's attached to every resource you should see it everywhere).
5. Attach the role to the profile.
    ```
    aws iam add-role-to-instance-profile \
        --instance-profile-name BriocheInstanceProfile \
        --role-name BriocheInstanceProfile
    ```

Later, nodes in the EMR Cluster will be assigned `BriocheInstanceProfile`,
granting access to various actions on the S3 bucket.

### EMR Service Role

AWS needs an 'oversight' role to set up the EMR cluster.
This role needs permission to provision EC2 instances, manage security groups,
assign the just-created instance role, etc.

`emr-service-policy.json` contains these permissions.
Note that the file contains placeholders for the VPC, security group, etc which need to be filled in.

Instructions:
1. Create an IAM policy `BriocheServiceRolePolicy` with the JSON.
    ```
    aws iam create-policy \
        --policy-name BriocheServiceRolePolicy \
        --policy-document file://service-role-policy.json
    ```
    Note: this file contains placeholders for vpc, etc. that must be set manually.
2. Create an IAM role `BriocheServiceRole` for the EMR service.
    ```
    aws iam create-role \
        --role-name BriocheServiceRole \
        --assume-role-policy-document file://service-role-assume-role.json
    ```
3. Attach `BriocheServiceRolePolicy` to the role.
    ```
    aws iam attach-role-policy \
        --role-name BriocheServiceRole \
        --policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/BriocheServiceRolePolicy
    ```
4. Attach `AmazonEMRServicePolicy_v2` to the role
    ```
    aws iam attach-role-policy \
        --role-name BriocheServiceRole \
        --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEMRServicePolicy_v2
    ```

## Scripts

From here on out it's just single commands.
These eliminate the the hassle of finagling with the console GUI.

### Starting the cluster

```
aws emr create-cluster \
    --name BriocheAutoCluster \
    --release-label emr-7.12.0 \
    --os-release-label 2023.9.20251117.1 \
    --instance-type r6g.xlarge \
    --instance-count 2 \
    --applications Name=Spark \
    --ec2-attributes \
        '{
            "SubnetId": "'$BRIOCHE_SUBNET'",
            "InstanceProfile": "BriocheInstanceProfile",
            "EmrManagedMasterSecurityGroup": "'$BRIOCHE_SG'",
            "EmrManagedSlaveSecurityGroup": "'$BRIOCHE_SG'"
        }' \
    --service-role BriocheServiceRole \
    --log-uri s3://brioche-s3/log \
    --tags for-use-with-amazon-emr-managed-policies=true \
    --auto-termination-policy IdleTimeout=60
```

Notes:
 - Application versions are fixed for each EMR release (e.g. emr-7.12.0 sets the Spark version to 3.5.6).
 - AWS infers how many cluster nodes are created based on `--instance-count` (2 instances = 1 worker, 1 master).
 - 'Structure'-type args can be passed either as JSON (`--ec2-attributes`)
    or comma-separated key-value pairs (`--tags`).
 - The `--auto-termination-policy` flag is used to terminate the cluster after 60 seconds of inactivity.
 - The `--tags` flag is used to match some conditions in `AmazonEMRServicePolicy_v2`.
    If you look inside this policy you'll find that many permissions are restricted
    to resources tagged with `for-use-with-amazon-emr-managed-policies`.
    *Using the 'Create a service role' option in the AWS console will set the tag automatically.* 

### Running a step

As with *Alanna*, steps can be executed by invoking `spark-submit` with `command-runner.jar`.

```
aws emr add-steps \
    --cluster-id <CLUSTER_ID> \
    --steps \
        '[
            {
                "Type": "CUSTOM_JAR",
                "Name": "BriocheSparkStep",
                "ActionOnFailure": "CONTINUE",
                "Jar": "command-runner.jar",
                "Args": ["spark-submit", "s3://brioche-s3/spark_step.py"]
            }
        ]'
```

Unlike the web console, the CLI allows you to queue steps before the cluster is ready.
This is very convenient.

### Stopping the cluster

Not needed since the clusters are configured to terminate after a minute of inactivity.
There's definitely a command for this though.

## Misc

The [AWS CLI docs](https://docs.aws.amazon.com/cli/latest/reference/iam) are really good.

Errors that happen during the instantiation process of the EMR cluster
might not appear in the normal cluster logs
(because the cluster doesn't exist yet).
You can instead find them in Cloudtrail.

### Policy files

The `"Version": "2012-10-17"` line in every policy file
specifies the *policy format*, not the date of creation.
There are only two options: "2012-10-17" and "2008-10-17"

Note that some policies contains separate lists of actions with redundant entries.
AWS does this by default, presumably to improve clarity.
I am following their convention.

### Instance Profiles (are stupid)

Every instance profile is associated with exactly one role.
This makes it entirely superfluous.
In fact, the AWS web console straight-up hides the distinction and collapses 
instance profiles and roles into a singular entity.
[Unfortunately the CLI is stuck with the legacy model](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#ec2-instance-profile).

There is no way to directly access instance profiles in the AWS console.
You can sorta see that they exist and are attached to IAM roles
(in the GUI for each role),
but if multiple instance profiles have the same role,
only one will be shown.

Instance profiles created in the console ("Create a service role" option in the EMR setup GUI)
will be auto-deleted with their corresponding role.

Instance profiles created in the CLI must be detached and deleted
manually, also through the CLI.