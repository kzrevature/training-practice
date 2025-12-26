# AWS EMR Manual Setup - "Alanna"

Basic overview of how to set up a minimal working EMR Cluster on AWS.
Alanna is just a placeholder name to avoid confusion with other projects.

Everything was done on the **us-east-1** (N. Virginia) region.

## Resource Creation

### VPC:

Create a VPC `alanna-vpc` with default settings.

Create a subnet `alanna-subnet` inside the VPC.
I actually made three subnets `alanna-subnet-1a`, `alanna-subnet-1b`, `alanna-subnet-1f`
(with corresponding availability zones `us-east-1a`, `us-east-1b`,  `us-east-1f`)
but this is unnecessary.
I just wanted to match the cheapest pricing locations for different EMR instance types.

Create an internet gateway `alanna-igw` and attached it to the VPC.
Add `0.0.0.0/0 → IGW` to the route table.

### S3:

Create a bucket `alanna-s3` with default settings.

### EMR:

Version: `emr-7.12.0`

Application Bundle: `Spark 3.5.6` (everything else deselected)

Instance Groups:
 - Primary: `r8g.xlarge`
 - Core: `r8g.xlarge`
 - No task instances

Networking: `alanna-vpc`, `alanna-subnet-1f`

Cluster Logs:
 - I pointed this at a logs directory in my s3 bucket: `s3://alanna-s3/logs`
 - The default bucket 'elasticmapreduce' doesn't exist/work.

IAM Service Role:
 - Use the default 'Create a service role.' This role includes two policies:
   - A default `AmazonEMRServicePolicy_v2`
   - A custom `AmazonEMR-ServiceRole-Policy-<timestamp>`
 - Alternatively, you could create a custom role (e.g. `AlannaEMRServiceRole`):
   - Setting "Service" to "EMR" and "Use Case" to "EMR" adds `AmazonEMRServicePolicy_v2`.
   - The custom permissions need to be added manually since they include cluster-specific details.
      Specifically, you'll need to provide ARNs for your VPC, subnet, security group, and the IAM instance role.
   - Refer to `iam-emr-service-role-policy.json`
 - Setting the correct policy permissions is very important, the cluster will crash during startup without them.

IAM Instance Role:
 - Use the default 'Create an instance profile'
 - Alternatively, make a custom role (e.g. `AlannaEMRInstanceRole`).
   It basically just needs access to S3.
   Refer to `iam-emr-service-role-policy.json`.

### Misc/Troubleshooting:

Cluster provisioning took about 10 minutes.

"The specified location-constraint is not valid" - the region and availability zones for EMR, VPC, and S3 have to match.
This includes the bucket for cluster logs.

"Terminated with errors: Service role arn:aws:iam::\<role name\> has insufficient EC2 permissions" - 
The specified IAM role doesn't have the right permissions (probably missing a subnet).

"Terminated with errors: An internal error occurred." -
Try using a bigger instance (the default `r8g.xlarge` works fine).

## Running a task

### Python

Create a Python script with simple Spark workload (see `spark_step.py` for an example) and upload it to S3.

### spark-submit

Create a spark-submit script and upload it to S3 (see `spark_run.sh`).

```spark-submit s3://alanna-s3/spark_step.py```

### EMR

Select the cluster, click "Add step",
pick the option that runs a shell script,
and point it at the spark-submit uploaded in S3.

## Cost Management

All the EMR stuff is quite expensive, take it down once it's done.
Note that instances that are cheaper by the hour might not be optimized for EMR.
For example: `c1.medium` is 50% cheaper than `r8g.xlarge` but takes 6x as long to instantiate,
so it ends up being 3x as expensive.
I'd stick with the defaults.

S3 is very cheap.

VPC also takes your money for some (??) reason but it's also fairly cheap.