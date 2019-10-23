from scobra.classes import db, fca, flux, fva, matrix, model, pareto 

m1 = ("sample/testmodel.xls")
m2 = ("sample/testmodel2.xls")

def CompareModel_test():
    assert model.CompareModel(m1,m1) == 
    assert model.CompareModel(m1,m2)