from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm
    )

class BastionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)