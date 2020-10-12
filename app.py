#!/usr/bin/env python3

from aws_cdk import core

from cdk_udemy.cdk_udemy_stack import CdkUdemyStack


app = core.App()
CdkUdemyStack(app, "cdk-udemy")

app.synth()
