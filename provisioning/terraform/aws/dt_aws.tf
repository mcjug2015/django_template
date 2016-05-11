# Configure the AWS tf

variable "access_key" {
  description = "Your amazon access key"
  default = "NOPE"
}

variable "secret_key" {
  description = "Your amazon secret key"
  default = "NOPE"
}

variable "region_name" {
  description = "Name of the amazon region"
  default = "us-east-1"
}

variable "local_ip" {
  description = "Your local ip for aws security group"
  default = "73.133.230.159/32"
}

variable "vpc_cidr" {
  description = "The cidr to use for dt_vpc"
  default = "172.32.0.0/16"
}

variable "subnet_cidr" {
  description = "The cidr to use for dt_subnet"
  default = "172.32.0.0/20"
}

variable "pem_key_name" {
  description = "Name of the key for your aws .pem file"
  default = "victors_keypair"
}


provider "aws" {
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
    region = "${var.region_name}"
}

resource "aws_vpc" "dt_vpc" {
    cidr_block = "${var.vpc_cidr}"
    instance_tenancy = "default"
    enable_dns_hostnames = true

    tags {
        Name = "dt_vpc"
    }
}

resource "aws_internet_gateway" "dt_igw" {
    vpc_id = "${aws_vpc.dt_vpc.id}"

    tags {
        Name = "dt_igw"
    }
}

resource "aws_route_table" "dt_route_table" {
    depends_on = ["aws_internet_gateway.dt_igw"]
    vpc_id = "${aws_vpc.dt_vpc.id}"
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = "${aws_internet_gateway.dt_igw.id}"
    }

    tags {
        Name = "dt_route_table"
    }
}

resource "aws_main_route_table_association" "dt_vpc_to_route" {
    depends_on = ["aws_vpc.dt_vpc", "aws_route_table.dt_route_table"]
    vpc_id = "${aws_vpc.dt_vpc.id}"
    route_table_id = "${aws_route_table.dt_route_table.id}"
}


resource "aws_subnet" "dt_subnet" {
    vpc_id = "${aws_vpc.dt_vpc.id}"
    cidr_block = "${var.subnet_cidr}"
    map_public_ip_on_launch = true

    tags {
        Name = "dt_subnet"
    }
}

resource "aws_security_group" "ssh_and_http" {
  name = "ssh_and_http"
  description = "Allows all outbound traffic, all http inbound, ssh inbound from defined ip"
  vpc_id = "${aws_vpc.dt_vpc.id}"

  ingress {
      from_port = 80
      to_port = 80
      protocol = "TCP"
      cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
      from_port = 443
      to_port = 443
      protocol = "TCP"
      cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
      from_port = 22
      to_port = 22
      protocol = "TCP"
      cidr_blocks = ["${var.local_ip}"]
  }

  egress {
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "dt_web" {
    depends_on = ["aws_internet_gateway.dt_igw"]
    ami = "ami-6d1c2007"
    instance_type = "t2.medium"
    subnet_id = "${aws_subnet.dt_subnet.id}"
    vpc_security_group_ids = ["${aws_security_group.ssh_and_http.id}"]
    associate_public_ip_address = true
    key_name = "${var.pem_key_name}"
    instance_initiated_shutdown_behavior = "terminate"
    root_block_device {
        delete_on_termination = true
    }
    tags {
        Name = "Django Template Server"
    }
    user_data = "${file("./../cloud_init.txt")}"
}