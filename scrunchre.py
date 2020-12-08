#!/usr/bin/env python

# Copyright 2013 Martin Planer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sre_parse import *
import argparse
import itertools

def re_iter(t):
	type = t[0]
	spec = t[1]
	if(type == LITERAL):
		return literal_iter(spec)
	if(type == IN):
		return in_iter(spec)
	if(type == MAX_REPEAT):
		return maxrepeat_iter(spec)

def literal_iter(s):
	return iter(chr(s))

def in_iter(spec):
	return iter(spec_list(spec))

def maxrepeat_iter(spec):
        # (0, 2, [('in', [('range', (97, 99))])])
	min = spec[0]
	max = spec[1]
	if spec[2][0][0] == IN:
		speclist = spec_list(spec[2][0][1])
	else:
		speclist = spec_list(spec[2])
	rng = range(min, max+1)
	iters = map(lambda x: itertools.product(speclist, repeat = x), rng)
	for it in iters:
	        for element in it:
	            yield "".join(element)

def spec_list(l):
	all = []
	for i in l:
		type = i[0]
		spec = i[1]
		if(type == LITERAL):
			all.append(chr(spec))
		if(type == RANGE):
			all.extend(map(chr, range(spec[0], spec[1]+1)))
	return all

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("regex",
                        help="Regex Pattern to use")
    parser.add_argument("-f", "--file",
                        help="Save result to a file")
    args = parser.parse_args()
    return args

def main():
    args = getArgs()
    pattern_string = args.regex

    pattern = parse(pattern_string)

    iters = map(lambda x: re_iter(x), pattern)

    if args.file:
        with open(args.file, "w") as out_file:
            for i in itertools.product(*iters):
                out_file.write("".join(i) + "\n")
        print("[+] Created file {}".format(args.file))
    else:
        for i in itertools.product(*iters):
            print "".join(i)

if __name__ == "__main__":
    main()
