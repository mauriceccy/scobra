
import os


import scobra

def TestModel():

	# usual flux bounds are already added in the model

	m = scobra.ModelTest(os.path.dirname(__file__)+'/sample_chloroplast.xls') # loading the model

	# model will load with the flux bounds provided within

	m.SetConstraint('chl_Star_tx',-1,-1) # one unit of starch biosynthesis


	m.Solve() #solving the problem

	sol = m.GetSol() # getting the flux distribution

	#print sol 


	for reac in sol:
	    print reac,sol[reac]


def AllBiomassSyn():

    m = scobra.ModelTest(os.path.dirname(__file__)+'/sample_chloroplast.xls')


    io = ['Photon', 'CO2', 'O2']

    for tx in m.Reactions():
        if '_tx' in tx and tx.split('_')[1] not in io:
            m.SetFixedFlux({tx:-1})

            
    m.Solve()
    sol = m.GetSol()
    for reac in sol:
        print reac,sol[reac]

    
        
