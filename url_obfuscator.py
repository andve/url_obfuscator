#!/usr/bin/env python

import getopt
import re
import socket
import sys

def get_scheme(url: str) -> str:
	"""Return the scheme of the URL."""
	scheme = re.search(r'^http(s)?(:)?\/\/?', url)
	return scheme.group() if scheme != None else ""

def get_path(url: str) -> str:
	"""Return the path of the URL."""
	url_no_scheme = re.sub(r'^http(s)?(:)?\/\/?', "", url)
	path = re.search(r'(\/.*)', url_no_scheme)
	return path.group() if path != None else ""

def get_host(url: str) -> str:
	"""Return the host of the URL"""
	return re.sub(r'^http(s)?(:)?\/\/?|(\/.*)?', "", url)

def get_ip(url: str) -> str:
	"""Translate the URL host name to IPv4."""
	host = get_host(url)
	ip = ""
	try:
		ip = socket.gethostbyname(host)
	except socket.gaierror as e:
		print("error: name resolution failed")
		sys.exit(1)
	return ip

def ip_to_hexa(ip: str) -> str:
	"""Convert the IPv4 address to hexadecimal."""
	ip = ip.split(".")
	#hexa_ip_list = [hex(int(x)).replace("o", "") for x in ip]
	#hexa_ip = f"{hexa_ip_list[0]}.{hexa_ip_list[1]}.{hexa_ip_list[2]}.{hexa_ip_list[3]}"
	hexa_ip = "0x"
	for i in ip:
		hexa_ip += hex(int(i))[2:]
	return hexa_ip

def ip_to_octal(ip: str) -> str:
	"""Convert the IPv4 address to octal."""
	ip = ip.split(".")
	octal_ip_list = [oct(int(i)).replace("o", "") for i in ip]
	octal_ip = f"{octal_ip_list[0]}.{octal_ip_list[1]}.{octal_ip_list[2]}.{octal_ip_list[3]}"
	return octal_ip

def path_to_hexa(path: str) -> str:
	"""Convert the characters of the path to hexadecimal."""
	hexa_path = "/"
	for i in path[1:]:
		if i != "=" and i != "&" and i != "/":
			hexa_path += hex(ord(i)).replace("0x", "%")
		else:
			hexa_path += i
	return hexa_path

def print_usage():
	print(f"usage: {sys.argv[0]} [<url> | -h]")

def main():
	url = ""
	to_remove = []
	for opt in sys.argv:
		if "-" != opt[0] and opt != sys.argv[0]:
			to_remove.append(opt)

	for opt in to_remove:
		url = opt.strip()
		sys.argv.remove(opt)

	try:
		opts, args = getopt.getopt(sys.argv[1:], "h")
	except getopt.GetoptError as e:
		print(f"error: {e}")
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			print_usage()
			sys.exit()
		else:
			assert False, "unhandled option"

	if url == "":
		print("error: no url provided")
		print_usage()
		sys.exit(2)

	if len(opts) == 0 and url == "":
		print("error: no options given")
		print_usage()
		sys.exit(2)

	scheme = "https://" if (s := get_scheme(url)) == "" else s
	host = get_host(url)
	path = get_path(url)
	ip = get_ip(host)

	print(f"{scheme}{ip}{path}")
	print(f"{scheme}{ip_to_hexa(ip)}{path}")
	print(f"{scheme}{ip_to_octal(ip)}{path}")
	if path != "":
		print(f"{scheme}{ip_to_hexa(ip)}{path_to_hexa(path)}")
		print(f"{scheme}{ip_to_octal(ip)}{path_to_hexa(path)}")

if __name__ == "__main__":
	main()
