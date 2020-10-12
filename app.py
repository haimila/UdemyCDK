#!/usr/bin/env python3

from aws_cdk import core

from stacks.VPCstack import VPCStack
from stacks.SecurityStack import SecurityStack
from stacks.BastionStack import BastionStack

environment = core.Environment(region='eu-central-1')

app = core.App()
vpc_stack = VPCStack(app, "vpc-stack", env=environment)
security_stack = SecurityStack(app, "security-stack", vpc=vpc_stack.vpc, env=environment)
bastion_stack = BastionStack(app, "bastion-stack", vpc=vpc_stack.vpc, sg=security_stack.bastion_host_security_group, env=environment)

app.synth()
