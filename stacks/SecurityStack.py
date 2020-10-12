from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm
    )

class SecurityStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_security_group = ec2.SecurityGroup(
            self, "LambdaSG",
            security_group_name="lambda-sg",
            vpc=vpc,
            description="security group for lambda functions",
            allow_all_outbound=True
        )

        self.bastion_host_security_group = ec2.SecurityGroup(
            self, "BastionSG",
            security_group_name="bastion-host-sg",
            vpc=vpc,
            description="security group for bastion host",
            allow_all_outbound=True
        )

        self.bastion_host_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "SSH Access"
        )

        lambda_role = iam.Role(
            self, 'LambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            role_name='lambda-role',
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                managed_policy_name='service-role/AWSLambdaBasicExecutionRole'
            )]
        )

        lambda_role.add_to_policy(
            statement=iam.PolicyStatement(
                actions=['s3:*', 'rds:*'],
                resources=['*']
            )
        )

        ssm.StringParameter(
            self, "lambda-sg-parameter",
            parameter_name='/lambda-sg',
            string_value=lambda_security_group.security_group_id
        )

        ssm.StringParameter(
            self, "lambda-rolearn-parameter",
            parameter_name='/lambda-role-arn',
            string_value=lambda_role.role_arn
        )

        ssm.StringParameter(
            self, "lambda-rolename-parameter",
            parameter_name='/lambda-role-name',
            string_value=lambda_role.role_name
        )