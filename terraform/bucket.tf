variable "aws_access_key" {
  description = "AWS access key"
}

variable "aws_secret_key" {
  description = "AWS secret access key"
}

variable "aws_region" {
  description = "AWS region"
}

variable "bucket" {
  description = "AWS S3 bucket"
}

provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region = "${var.aws_region}"
}

resource "aws_s3_bucket" "main" {
  bucket = "${var.bucket}"
  acl = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  tags {
    Name = "${var.bucket}"
    Environment = "www.turbare.net"
  }
}

resource "aws_iam_user" "main" {
    name = "circleci-www.turbare.net"
    path = "/www.turbare.net/"
}

resource "aws_iam_access_key" "main" {
    user = "${aws_iam_user.main.name}"
}

resource "template_file" "policy" {
  template = "${path.module}/s3-sync-policy.json"
  vars {
    bucket = "${aws_s3_bucket.main.id}"
  }
}

resource "aws_iam_user_policy" "main" {
    name = "s3-sync-www.turbare.net"
    user = "${aws_iam_user.main.name}"
    policy = "${template_file.policy.rendered}"
}
