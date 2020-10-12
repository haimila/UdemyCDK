from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ssm as ssm
    )


class VPCStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self, "Vpc",
            cidr='10.0.0.0/16',
            max_azs=2,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="IsolatedSubnet",
                    subnet_type=ec2.SubnetType.ISOLATED,
                    cidr_mask=24
                )
            ],
            nat_gateways=1
        )

        private_subnet_ids = [subnet.subnet_id for subnet in self.vpc.private_subnets]

        count = 1

        for privatesubnet in private_subnet_ids:
            ssm.StringParameter(
                self, "private-subnet-"+str(count),
                string_value=privatesubnet,
                parameter_name='/private-subnet-'+str(count)
            )
            count += 1


