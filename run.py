  """
  	Ditch ButterKnife
  	A script to remove ButterKnife code and use Android Built-in methods instead

    Copyright (C) 2017 Aung Thiha

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

 """

import fnmatch
import os
import sys
import re

field_pattern = r"@BindView\((.*?)\) (.*?) (.*?);"
butter_pattern = r"\n(.*?)ButterKnife.bind\((.*?)\);"
butter_regex = re.compile(butter_pattern)

class resources():
    butter_replacement = ''
    space = ''
    suffix = ''
    support26 = False

def replace_content(match):
	# remove Access Modifiers for assigments inside methods
	splits = match.group(3).split(' ')
	variable_name = splits[1] if len(splits) > 1 else splits[0]
	# check if we need type casting
	# if resources.support26 is true, we only empty string that means no type casting
	# if the type is View, we don't need type casting, obviously
	should_type_cast = resources.suffix or resources.support26 or match.group(2) == 'View'
	suffix = resources.suffix if should_type_castelse "({0}) {1}".format(match.group(2), resources.suffix)
	# save text to replace ButterKnife.Bind. This replacement text is variable assigments.
	resources.butter_replacement += "{0}{1} = {2}findViewById({3});\n".format(resources.space, variable_name, suffix, match.group(1))
	return "{0} {1};".format(match.group(2), match.group(3))

def process_file(abs_path):

	f = open(abs_path, 'r')
	content = f.read()
	f.close()

	# check if the file use ButterKnife
	result = butter_regex.search(content)
	if result:
		# indentation that needs for variable assignment statements
		resources.space = result.group(1)
		# check if we need to add "view.".
		# In activity, we don't need it.
		# If the ButterKnife.bind has two argvs, that means it's not activity
		argvs = result.group(2).split(',')
		resources.suffix = argvs[1].strip() + "." if len(argvs) > 1 else ""
		# re initiage butter_replacement for next file
		resources.butter_replacement = '\n\n'
		# replace fields
		content = re.sub(field_pattern, replace_content, content)
		# replace ButterKnife.Bind with variable assignments
		content = re.sub(butter_pattern, resources.butter_replacement, content)

		f = open(abs_path, 'w')
		f.write(content)
		f.close()

	
def main(filedir):
	for root, dirnames, filenames in os.walk(filedir):
	    for filename in fnmatch.filter(filenames, '*.java'):
	    	abs_path = os.path.join(root, filename)
	    	process_file(abs_path)
	    for dirname in dirnames:
	    	main(dirname)

if __name__ == '__main__':
	print('')
	if len(sys.argv) > 1:
		# check if there's an argv to command omitting type casting
		if len(sys.argv) > 2:
			resources.support26 = sys.argv[2] == '26' 
		main(sys.argv[1])
	else:
		main('.')
