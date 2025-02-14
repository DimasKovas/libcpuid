#!/usr/bin/env python3

import os, sys, re

args = sys.argv

if len(args) != 3:
	print("Usage: create_test.py <rawdata file> <report file>")
	print("The .test file is written to stdout.")
	sys.exit(1)

def readRawFile():
	rawdata = []
	for line in open(args[1], "rt").readlines():
		lookfor = ["basic_cpuid", "ext_cpuid", "intel_fn4", "intel_fn11", "amd_fn8000001dh", "Logical CPU", "CPUID"]
		ignore  = ["MSR Register"]
		good = False
		for match in lookfor:
			if line.find(match) != -1:
				good = True
				break
		for match in ignore:
			if line.find(match) != -1:
				good = False
				break
		if good:
			rawdata.append(line.strip())
	return rawdata

def readResultFile():
	repdata = []
	rexp = re.compile('(-?[0-9]+).*')
	for line in open(args[2], "rt").readlines():
		s = line.strip()
		if s.find(":") == -1:
			continue
		numeric = ["family", "model", "stepping", "ext_family", "ext_model",
				"num_cores", "num_logical",
				"L1 D cache",  "L1 I cache",  "L2 cache",   "L3 cache",   "L4 cache",
				"L1D assoc.",  "L1I assoc.",  "L2 assoc.",  "L3 assoc.",  "L4 assoc.",
				"L1D line sz", "L1I line sz", "L2 line sz", "L3 line sz", "L4 line sz",
				"L1D inst.",   "L1I inst.",   "L2 inst.",   "L3 inst.",   "L4 inst.",
				]
		field = s[:s.find(":")].strip()
		if field in numeric:
			value = s[s.find(":")+1:].strip()
			if not rexp.match(value):
				raise "Bad format of value: [%s]" % s
			repdata.append(rexp.findall(value)[0])
		if "CPU Info for type" in field:
			repdata.append(delimiter)
		if field == "arch":
			value = s[s.find(":") + 2:]
			repdata.append(value)
		if field == "purpose":
			value = s[s.find(":") + 2:]
			repdata.append(value)
		if field == "code name":
			value = s[s.find("`") + 1: s.find("'")]
			repdata.append(value)
		if field == "features":
			value = s[s.find(":") + 2:]
			repdata.append(value)
		if field == "SSE units":
			value = s[s.find(":") + 2:]
			# the value here is something like "XX bits (authoritative)". We remove the "bits" part:
			i = value.find("bits")
			if i != -1:
				value = value[:i] + value[i + 5:]
			repdata.append(value)
	return repdata

delimiter = "-" * 80
lines = readRawFile() + readResultFile()
sys.stdout.writelines([s + "\n" for s in lines])
