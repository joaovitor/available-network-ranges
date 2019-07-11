# Available ranges in a VPC

Did you ever needed to create a subnet and didn't knew which subnet range were available?
With this helper you can discover unused ipranges from a bigger cidr.

## Python setup

```shell
asdf install python 3.7.3
pip install --upgrade pip
pip install pipenv
asdf reshim python 3.7.3
pipenv install
```

## Get subnet in use (AWS example)

```shell
vpc_id=<your-vpc-id>
aws ec2 describe-subnets \
--filter "Name=vpc-id,Values=$vpc_id" \
--query "Subnets[*].CidrBlock" \
| jq -r ".[]" \
| sort > /tmp/subnets-$vpc_id-in-use.txt
```

## List available ranges in the VPC

```shell
pipenv run python3 available_range.py \
--vpc_range 10.169.0.0/20 \
--used_cidrs_path /tmp/subnets-$vpc_id-in-use.txt
```

### Sample output

```text
VPC Range 10.169.0.0/20
Used CIDRS file /tmp/subnets-$vpd_id-in-use.txt
--------
vpc SIZE=[4096]
unavailable SIZE=[2944]
available SIZE=[1152]
10.169.9.0/24
10.169.10.0/23
10.169.12.0/24
10.169.15.128/25
```
