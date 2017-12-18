import re 

file_path = "/home/kristoforus/compbio/updating_scobra/scobra/classes/model.py"

file = enumerate(open(file_path))

p = '\s*def (.*)\(.*'

def get_function_names(file): 
	thelist = []
	for i, line in file:
		if re.match(p, line) != None: 
			thelist.append(re.match(p, line).group(1))
		else: 
			pass
	return thelist


