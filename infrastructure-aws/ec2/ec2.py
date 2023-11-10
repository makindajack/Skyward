import pulumi
import pulumi_aws as aws
import base64


user_data_script = """
                    #!/bin/bash 
                    sudo apt update
                    echo "Hello, World!" > index.html
                    nohup python -m SimpleHTTPServer 80 &
                    """
user_data_base64 = base64.b64encode(user_data_script.encode()).decode()


def launch_template(custom_sg_id):
    """
    Create Auto Scaling Launch Template
    """
    return aws.ec2.LaunchTemplate(
        "patatte-LT",
        image_id="ami-053b0d53c279acc90",
        instance_type="t2.micro",
        vpc_security_group_ids=[custom_sg_id],
        user_data=user_data_base64,
        # key_name="test-keypair"
    )



def create_auto_scaling_group(launch_temp, subnet_ids):
    """Create an autoscaling group in Pulumi"""
    asg = aws.autoscaling.Group(
        "patatte-asg",
        launch_template={
            "id": launch_temp.id,
            "version": launch_temp.latest_version,
        },
        min_size=1,
        max_size=3,
        desired_capacity=2,
        termination_policies=["OldestInstance"],
        vpc_zone_identifiers=subnet_ids,
    )


 

    pulumi.export("autoscaling_group_name", asg.name)



# Export the autoscaling group name
