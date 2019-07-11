#!/usr/bin/env python3

import click
from netaddr import IPSet, IPNetwork

@click.command()
@click.option('--vpc_range', help='VPC Range. This can be read from VERIFIER_VPC_RANGE')
@click.option('--used_cidrs_path', help='File with used CIDR ranges. This can be read from VERIFIER_USED_CIDRS_PATH')
def available_range(vpc_range, used_cidrs_path):
    """Verify if a given range is available in a range."""
    click.echo('VPC Range %s' % vpc_range)
    click.echo('Used CIDRS file %s' % used_cidrs_path)
    click.echo('--------')

    vpc = IPSet([vpc_range])

    unavailable = IPSet([])
    with open(used_cidrs_path) as fp:  
        for cnt, line in enumerate(fp):
            unavailable.add(line.strip())

    available = vpc.difference(unavailable)

    __print_set_size("vpc", vpc)
    __print_set_size("unavailable", unavailable)
    __print_set("available", available)

def __print_set_size(description, ip_set):
    click.echo("{} SIZE=[{}]".format(description, len(ip_set)))


def __print_set(description, ip_set):
    __print_set_size(description, ip_set)
    for cidr in ip_set.iter_cidrs():
        click.echo(cidr)

if __name__ == '__main__':
    available_range(auto_envvar_prefix='VERIFIER')