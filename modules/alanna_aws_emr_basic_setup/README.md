# Basic EMR Setup - 'Alanna'

Overview of how to set up a minimal working EMR cluster on AWS,
and then how to run a PySpark workload on that cluster.

'Alanna' is a placeholder name to avoid confusion with other projects.

## Resource Creation

Everything was done on the **us-east-1** (N. Virginia) region.

### VPC:

You can probably skip this entire section and use the default VPC,
but making a new one is easy enough.

Create a VPC `alanna-vpc` with default settings.

Create a subnet `alanna-subnet` inside the VPC.
I actually made like four subnets `alanna-subnet-1a`, `alanna-subnet-1b`, ...
(with corresponding availability zones `us-east-1a`, `us-east-1b`,  ...)
to match the lowest spot pricing for different instance types,
but this should be unnecessary.

Create an internet gateway `alanna-igw` and attached it to the VPC.
Add `0.0.0.0/0 → IGW` to the route table.

### S3:

Create a bucket `alanna-s3` with default settings.

### EMR:

Version: `emr-7.12.0`

Application Bundle: `Spark 3.5.6` (everything else deselected)

OS: `Amazon Linux release` (with auto-updates)

Instance Groups:
 - Primary: `r6g.xlarge`
 - Core: `r6g.xlarge`
 - No task instances

Networking: `alanna-vpc`, `alanna-subnet-1f`

Cluster Logs:
 - I pointed this at a logs directory in my s3 bucket: `s3://alanna-s3/logs`
 - The default bucket 'elasticmapreduce' doesn't exist/work.

IAM Service Role: Use the default 'Create a service role.'

IAM Instance Role: Use the default 'Create an instance profile' and make sure it has access to S3

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

```
aws s3 cp spark_step.py s3://alanna-s3/spark_step.py
```

### EMR Add Step

I found two configurations which work for running PySpark workloads.
They both use `spark-submit` to run a Python file.

**Custom JAR** just needs the following settings
 - JAR location: `command-runner.jar`
 - Arguments: `spark-submit s3://alanna-s3/spark_step.py`

**Shell Script**:
 - Upload a script containing the `spark-submit` command to S3 (see `spark_run.sh`)
 - Point "Shell Script location" at wherever you uploaded the script (e.g. `s3://alanna-s3/spark_run.sh`)

### Logs

Logs will appear at the location specified during the earlier "Cluster Logs" setting.
In my case this is `s3://alanna-s3/logs`.

The full path for Step logging will be `s3://alanna-s3/<CLUSTER-ID>/steps/<STEP-ID>/`.
The useful ones are `stdout.gz` and `stderr.gz`.
Click 'Open' to view them directly.

`stdout` from my cluster:
```
Downloading 's3://alanna-s3/spark_run.sh' to '/mnt/var/lib/hadoop/steps/s-03377232BWHRHR709FEG/.'
Sum of 1000 random numbers (using PySpark RDD):  504.5137461759091
Sum of 1000 random numbers (basic Python sum):   504.5137461759091
```

## Cost Management

All the EMR stuff is quite expensive so take it down once you're done.
Note that instances which are cheaper by the hour might not be optimized for EMR.
For example: `c1.medium` is 40% cheaper than `r6g.xlarge` but takes 10x as long to instantiate,
so it ends up being way more expensive.
I'd stick with the defaults, but anything in the `r` family of instances should get the job done.

S3 is extremely cheap.

VPC (with the setup I described) should have zero overhead costs.