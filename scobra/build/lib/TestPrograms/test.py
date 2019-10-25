import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import timeit 

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def test(FCA=False):
	start = timeit.default_timer()
	blockPrint()
	try:
		print('executing Model')
		path = os.path.join(currentdir, "Model.py")
		command = 'python %s' % (path)
		os.system(command)
	except Exception as e:
		print(e) 
	try:
		print('executing MOMA and ROOM')
		import MOMA_and_ROOM
	except Exception as e:
		print(e) 
	try:
		print('executing FVA')
		path = os.path.join(currentdir, "FVA.py")
		command = 'python %s' % (path)
		os.system(command)
	except Exception as e:
		print(e) 
	try:
		print('executing Scan')
		import Scan
	except Exception as e:
		print(e) 
	if FCA: 
		try:
			print('executing FCA')
			import FCA
		except Exception as e:
			print(e) 
	end  = timeit.default_timer()
	time_taken = end - start
	enablePrint()
	print("Test completed in %s seconds" % (time_taken))
