# www.turbare.net

Contents are

- generated from [`website`](./website) by [Pelican](http://getpelican.com)
- deliver via [AWS S3](https://aws.amazon.com/s3/) bucket built from [`terraform`](terraform) by [Atlas](https://atlas.hashicorp.com) and [Terraform](https://terraform.io)
- triggered to update by [CircleCI](https://circleci.com) with [`circle.yml`](./circle.yml)

[`bootstrap`](./bootstrap) is to generate bootstrap AWS IAM key for [Terraform](https://terraform.io) in [Atlas](https://atlas.hashicorp).

## Setup

- To setup, generate limited access keys for
[Terraform](https://terraform.io) in [Atlas](https://atlas.hashicorp.com).
```console
$ cd bootstrap
$ edit terraform.tfvars # Write your AWS access keys
$ terraform plan
$ terraform apply
```
- Fill `terraform/terraform.tfvars` from `bootstrap/terraform.tfstate`
- Initial push [`terraform`](./terraform) to [Terraform](https://terraform.io) in [Atlas](https://atlas.hashicorp.com)
```
$ (cd terraform; terraform push --name uchida/www.turbare.net)
```
- set environment variables to CircleCI project
  - `ATLAS_TOKEN`: for deploy to [Atlas](https://atlas.hashicorp.com)
  - `AWS_ACCESS_KEY_ID`: for test `terraform` and deploy to [AWS S3](https://aws.amazon.com/s3/)
  - `AWS_SECRET_KEY_ID`: for test `terraform` and deploy to [AWS S3](https://aws.amazon.com/s3/)
  - `AWS_DEFAULT_REGION`: to deploy to [AWS S3](https://aws.amazon.com/s3/)

## License

- Contents in [website/contents](./website/contents) are licensed
under the [![CC-BY 4.0](https://i.creativecommons.org/l/by/4.0/80x15.png "CC-BY-4.0")](http://creativecommons.org/licenses/by/4.0/).
- Others are dedicated to [![CC0](http://i.creativecommons.org/p/zero/1.0/80x15.png "CC0")](https://creativecommons.org/publicdomain/zero/1.0/).
