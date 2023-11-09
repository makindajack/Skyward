import pulumi
import pulumi_aws as aws


def create_custom_vpc_and_subnets():
    """Define your custom VPC and subnets here"""

    custom_vpc = aws.ec2.Vpc(
        "patatte_custom-vpc1",
        cidr_block="10.0.0.0/16",
        enable_dns_support=True,
        enable_dns_hostnames=True,
    )

    subnet_a = aws.ec2.Subnet(
        "ec2-public-subnet",
        cidr_block="10.0.3.0/24",
        tags={"Name": "ec2-subnetA"},
        vpc_id=custom_vpc.id,
        availability_zone="us-east-1d",
    )

    subnet_b = aws.ec2.Subnet(
        "ec2-public-subnetB",
        cidr_block="10.0.4.0/24",
        tags={"Name": "ec2-subnetB"},
        vpc_id=custom_vpc.id,
        availability_zone="us-east-1f",
    )

    igw = aws.ec2.InternetGateway(
        "ec2-igw",
        vpc_id=custom_vpc.id,
    )

    route_table = aws.ec2.RouteTable(
        "ec2-route-table",
        vpc_id=custom_vpc.id,
        routes=[{"cidr_block": "0.0.0.0/0", "gateway_id": igw.id}],
    )

    rt_assoc_a = aws.ec2.RouteTableAssociation(
        "ec2-rtaA", route_table_id=route_table.id, subnet_id=subnet_a.id
    )

    rt_assoc_b = aws.ec2.RouteTableAssociation(
        "ec2-rtaB", route_table_id=route_table.id, subnet_id=subnet_b.id
    )

    custom_sg = aws.ec2.SecurityGroup(
        "custom-sg",
        description="Custom Security Group",
        tags={
            "Name": "custom-sg",
            },
        ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": [
                "0.0.0.0/0"
            ],  # Adjust this to your preferred SSH access
        },
        {
            "protocol": "tcp",
            "from_port": 9000,
            "to_port": 9000,
            "cidr_blocks": [
                "0.0.0.0/0"
            ],  # Adjust this to your preferred HTTP access
        },
        {
            "protocol": "tcp",
            "from_port": 5436,
            "to_port": 5436,
            "cidr_blocks": [
                "0.0.0.0/0"
            ],  # Adjust this to your preferred HTTP access
        },
    ],
    egress=[
        {
            "protocol": "-1",  # -1 means all protocols
            "from_port": 0,  # All ports
            "to_port": 0,  # All ports
            "cidr_blocks": [
                "0.0.0.0/0"
            ],  # Allow all outbound traffic to any destination
        },
    ],
    vpc_id=custom_vpc.id,
    )  # type: ignore
    
    pulumi.export("VPC ID", subnet_a.id)
    pulumi.export("subnet_a ID", subnet_a.id)
    pulumi.export("subnet_b ID", subnet_b.id)
    pulumi.export("Custom Security Group ID", custom_sg.id)
    return (
        custom_vpc,
        subnet_a,
        subnet_b,
        igw,
        route_table,
        rt_assoc_a,
        rt_assoc_b,
        custom_sg
    )
