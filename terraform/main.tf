terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">=1.2.0"

  backend "s3" {
    bucket         = "my-devops-tf-state-johny"
    key            = "global/s3/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "tf-state-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-0f58b397bc5c1f2e8"
  instance_type = "t2.micro"
  key_name      = "my-devops-key"

  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name = "my-devops-server"
  }
}

resource "aws_security_group" "web_sg" {
  name        = "my-devops-sg"
  description = "Allow SSH, HTTP, Prometheus, Grafana"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["157.48.0.0/14"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["157.48.0.0/14"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "server_public_ip" {
  description = "Public IP of the server"
  value       = aws_instance.app_server.public_ip
}
