import pulumi
import pulumi_aws as aws

# --- AWS Deployment ---
# Example: provision an S3 bucket for CodexDominion archives
archive_bucket = aws.s3.Bucket("codexdominion-archive")

# Export AWS context
pulumi.export("awsRegion", aws.config.region)
pulumi.export("awsAccountId", aws.get_caller_identity().account_id)

# Note: Grafana resources are not supported in Python. For Grafana integration, use Pulumi TypeScript or YAML.
