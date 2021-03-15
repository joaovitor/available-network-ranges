package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"

	"inet.af/netaddr"
)

func main() {
	var ip_set_builder netaddr.IPSetBuilder
	var vpc_range string
	var used_cidrs_path string
	flag.StringVar(&vpc_range, "vpc_range", "10.0.0.0/8", "VPC Range.")
	flag.StringVar(&used_cidrs_path, "used_cidrs_path", "/tmp/ranges_in_use.txt", "File with used CIDR ranges.")
	flag.Parse()

	ip_set_builder.AddPrefix(netaddr.MustParseIPPrefix(vpc_range))

	f, err := os.Open(used_cidrs_path)
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if err = f.Close(); err != nil {
			log.Fatal(err)
		}
	}()
	s := bufio.NewScanner(f)
	for s.Scan() {
		ip_set_builder.RemovePrefix(netaddr.MustParseIPPrefix(s.Text()))
	}
	err = s.Err()
	if err != nil {
		log.Fatal(err)
	}
	ip_set := ip_set_builder.IPSet()
	fmt.Println(ip_set.Ranges())
	fmt.Println(ip_set.Prefixes())
}
