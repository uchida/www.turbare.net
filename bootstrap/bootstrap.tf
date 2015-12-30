variable "aws_access_key" {
  description = "AWS access key"
}

variable "aws_secret_key" {
  description = "AWS secret access key"
}

variable "aws_region" {
  description = "AWS region"
}

provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region = "${var.aws_region}"
}

resource "aws_iam_user" "terraform" {
  name = "terraform-www.turbare.net"
  path = "/www.turbare.net/"
}

resource "template_file" "terraform" {
  template = "${path.module}/terraform-policy.json"
}

resource "aws_iam_user_policy" "terraform" {
  name = "terraform-www.turbare.net"
  user = "${aws_iam_user.terraform.name}"
  policy = "${template_file.terraform.rendered}"
}

resource "aws_iam_access_key" "terraform" {
  user = "${aws_iam_user.terraform.name}"
}
