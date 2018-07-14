import xml.etree.ElementTree as ET
import argparse
import os
import locale

#	 TAG_PATH, ATTRIB CONDITION, ATTRIBS TO CONVERT, CONVERSION LIMIT
fucked_up_items = [
	["producer", None, "in,out", None],
	["producer/property", "name=length", None, None],
	["producer/property", "name=warp_speed", None, None],
	["producer/property", "name=resource", None, ":"],
	["producer/filter", None, "in,out", None],
	["producer/filter/property", "name=geometry", None, None],
	["producer/filter/property", "name=av.h", None, None],
	["producer/filter/property", "name=av.b", None, None],
	["producer/filter/property", "name=av.s", None, None],
	["producer/filter/property", "name=level", None, None],
	["playlist/entry", None, "in,out", None],
	["playlist/blank", None, "length", None],
	["tractor", None, "in,out", None],
	["tractor/track", None, "in,out", None],
	["tractor/transition", None, "in,out", None],
	["tractor/property", "name=shotcut:scaleFactor", None, None],
]

separator_from = ""
separator_to = ""

def replace(what, limit):
	if limit:
		if type(limit) is int:
			return what.replace(separator_from, separator_to, limit)
		elif type(limit) is str:
			# Find the limit character
			limchar = what.find(limit)
			if limchar != -1:
				return what[0:limchar].replace(separator_from, separator_to) + what[limchar:]
			else:
				return what
		else:
			print("FAIL!")
	else:
		return what.replace(separator_from, separator_to)

def repair_project(file_path):
	tree = ET.parse(file_path)
	root = tree.getroot()
	
	for item in fucked_up_items:
		path, conditions, attributes, replacement_limit = item
		
		elements = root.findall(path)
		for element in elements:
			passed = True
			if conditions:
				for condition in conditions.split(","):
					attrib,value = condition.split("=")
					if str(element.get(attrib)) != value:
						passed = False
						break
			
			if not passed:
				continue
			
			if attributes:
				for attrib in attributes.split(","):
					if element.get(attrib):
						element.set(attrib, replace(element.get(attrib), replacement_limit))
			else:
				element.text = replace(element.text, replacement_limit)
				
	tree.write(file_path)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', help='The decimal separator to convert from', default='.')
	parser.add_argument('-o', help='The decimal separator to convert to', default=',')
	args = parser.parse_args()
	
	separator_from = args.i
	separator_to = args.o
	
	for path in os.listdir("."):
		if path.endswith(".mlt"):
			repair_project(path)