
# coding: utf-8

# In[10]:


import re 


# In[11]:




p = '\s*def (.*)\(.*'
p_easy = '\s*def (.*)\(self*'
p_self = '\s*def (.*)\(self\).*'


# In[12]:


def get_function_names(file): 
	thelist = []
	for i, line in file:
		if re.match(p, line) != None: 
			thelist.append(re.match(p, line).group(1))
		else: 
			pass
	print thelist
	return thelist

def get_function_names_easy(file): 
	thelist = []
	for i, line in file:
		if re.match(p_easy, line) != None: 
			thelist.append(re.match(p_easy, line).group(1))
		else: 
			pass
	print thelist
	return thelist

def get_functions_self_only(file): 
	self_only = []
	more = []
	for i, line in file: 
		if re.match(p_self, line) != None: 
			self_only.append(re.match(p_self,line).group(1))
		elif re.match(p, line) != None: 
			more.append(re.match(p, line).group(1))
		else: 
			pass
	return self_only, more
	

