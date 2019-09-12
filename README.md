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
ranges_in_use_file=/tmp/subnets-$vpc_id-in-use.txt

aws ec2 describe-subnets \
--filter "Name=vpc-id,Values=$vpc_id" \
--query "Subnets[*].CidrBlock" \
| jq -r ".[]" \
| sort > ${ranges_in_use_file}
```

## Get subnet in use (GCP example)

```shell
NETWORK_NAME=<your_network_name>
PROJECT_ID=<your_project_id>
subnet_file=/tmp/subnets-${PROJECT_ID}-${NETWORK_NAME}.json

gcloud compute networks subnets list \
--network=${NETWORK_NAME} \
--project=${PROJECT_ID} \
--format json > ${subnet_file}

ranges_in_use_file=/tmp/ranges-in-use-${PROJECT_ID}-${NETWORK_NAME}.txt

jq -r '.[]|.secondaryIpRanges[]?|.ipCidrRange' \
${subnet_file} \
> ${ranges_in_use_file}

jq -r '.[]|.ipCidrRange' \
${subnet_file} \
>> ${ranges_in_use_file}
```

## List available ranges in the VPC

```shell
vpc_range=10.169.0.0/20
pipenv run python3 available_range.py \
--vpc_range ${vpc_range} \
--used_cidrs_path ${ranges_in_use_file}
```

### Sample output

```text
VPC Range 10.169.0.0/20
Used CIDRS file ${ranges_in_use_file}
--------
vpc SIZE=[4096]
unavailable SIZE=[2944]
available SIZE=[1152]
10.169.9.0/24
10.169.10.0/23
10.169.12.0/24
10.169.15.128/25
```
