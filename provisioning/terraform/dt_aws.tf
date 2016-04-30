# Configure the AWS Provider
provider "aws" {
    access_key = "NOPE"
    secret_key = "NOPE"
    region = "us-east-1"
}

resource "aws_instance" "dt_web" {
    ami = "ami-6d1c2007"
    instance_type = "t2.medium"
    security_groups = ["comcast_from_house"]
    key_name = "victors_keypair"
    instance_initiated_shutdown_behavior = "terminate"
    root_block_device {
        delete_on_termination = true
    }
    tags {
        Name = "Django Template Server"
    }
}