import scobra
from scobra.classes.matrix import matrix
from scobra.classes.reaction import Reaction

mToy = scobra.Model()

# H2, H20, H2C03, ACE

mToy.AddReaction('reduct_ket_to_alc', {'OXA': -1, 'H2': -1, 'MAL': 1})
mToy.AddReaction('dehydration', {'MAL': -1, 'FUM': 1, 'H2O': 1})
mToy.AddReaction('reduct_cdouble_to_csingle', {'FUM': -1, 'H2': -1, 'SUC': 1})
mToy.AddReaction('addition_co2_h2', {
                 'SUC': -1, 'H2CO3': -1, 'H2': -1, 'AKG': 1, 'H2O': 1})
mToy.AddReaction('addition_co2', {'AKG': -1, 'H2CO3': -1, 'OXS': 1, 'H2O': 1})
mToy.AddReaction('ket_to_alc_2', {'OXS': -1, 'H2': -1, 'ISC': 1})
mToy.AddReaction('dehydration_cis', {'ISC': -1, 'CAC': 1, 'H2O': 1})
mToy.AddReaction('hydration_to_alcohol', {'CAC': -1, 'H2O': -1, 'CIT': 1})
mToy.AddReaction('split', {'CIT': -1, 'OXA': 1, 'ACE': 1})

mToy.SetDefaultKinetics()
mToy.SetRateEquation('addition_co2_h2', 'H2CO3 ** 1 *SUC ** 1 * H2 ** 1')
mToy.AddExchangeReactions({"exchange_h2": "H2", "exchange_h2o": "H2O",
                           "exchange_h2co3": "H2CO3", "exchange_ace": "ACE"})

# mToy.PrintExchangeReactions()
mToy.SetRateConstants({
    'reduct_ket_to_alc': 0.0001,
    'dehydration': 0.0001,
    'reduct_cdouble_to_csingle': 0.0001,
    'addition_co2_h2': 0.0001,
    'addition_co2': 0.0001,
    'ket_to_alc_2': 0.0001,
    'dehydration_cis': 0.0001,
    'hydration_to_alcohol': 0.0001,
    'split': 0.0001
})

print(mToy.Metabolites())

concDict = {
    'OXA': 100,
    'H2': 10000,
    'MAL': 100,
    'FUM': 100,
    'H2O': 10000,
    'SUC': 100,
    'H2CO3': 10000,
    'AKG': 100,
    'OXS': 100,
    'ISC': 100,
    'CAC': 100,
    'CIT': 100,
    'ACE': 0}

mToy.SetConcentrations(concDict)
mToy.SetObjective('split')
mToy.SetObjDirec('Max')

sim = mToy.DFBASimulation(20, zeroLB=True, minFluxSolve=False)

sim[0].to_csv('concTest.csv', index=False)
sim[1].to_csv('fluxTest.csv', index=False)

mToy.WriteModel("test.xls", "excel")

mExcel = scobra.Model("test_formose1.xml")
mExcel.WriteModel("withoutReaction.xls", "excel")

mExcel.DelReactions(['Out3k', 'Out4k', 'OutPdt',
                     'Out2', 'Out3a', 'Out4a', 'Form1'])
mExcel.SetDefaultKinetics()

mExcel.AddExchangeReactions()

mExcel.GetExchangeReactions()
mExcel.PrintExchangeReactions()
mExcel.SetRateConstants({
    'Form2': 0.0001,
    'Form3': 0.0001,
    'Isom3': 0.0001,
    'Isom4': 0.0001,
    'Form4': 0.0001,
    'Ring4': 0.0001,
    'Split4': 0.0001
})

concDict = {
    'C1': 1000,
    'C2': 0,
    'C3ald': 0,
    'C4ket': 0,
    'C3ket': 0,
    'C4ald': 0,
    'C4fur': 0
}

mExcel.SetConcentrations(concDict)
mExcel.SetConstrFromRateEquation(zeroLB=False)
mExcel.SetObjective(['Split4'])
mExcel.SetObjDirec('Max')

sim = mExcel.DFBASimulation(20, zeroLB=False, minFluxSolve=True)

sim[0].to_csv('conc.csv', index=False)
sim[1].to_csv('flux.csv', index=False)
mExcel.WriteModel("formoseOut.xls", "excel")

# Add ExchangeReaction at DFBA.py

# H2O_tx, O2_tx, CO2_tx, GLC_tx, Biomass_tx as exchange reaction.
# GLC_tx | Biomass * GLC / (1 + GLC)
# Catabolism: GLC + 6O2 -> 6CO2 + 6H2O + energy
# Anabolism: GLC + energy -> Biomass
# Track only GLC and Biomass
# Biomass: 1, GLC: 100, H2O, O2, CO2: non-0
# Biomass constraint: (None, 0)

# Only Excel export is available --> Later on can work on other things
# Lack of concentrations at metabolite section of output
