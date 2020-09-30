# "Reaction",    # Function/pathway    # Information on SUBA (MS and/or GFP)    # Reference
# Reactions with a "#" in front represent dead reactions (reactions that cannot carry a non-zero flux), therefore not in the compartmented model

#_p
Plastid = [

"PSII-RXN",		# Light reaction	# 22 genes, 110 MSp
"RXN490-3650",		# Light reaction	# 16 genes, 98 MSp
"PLASTOQUINOL--PLASTOCYANIN-REDUCTASE-RXN",	# Light reaction	# no genes ##########
"1.18.1.2-RXN",		# Light reaction	# 5 genes, 20 MSp, (1 GFPm)
#"FLAVONADPREDUCT-RXN",	# Light reaction	# 2 genes, 19 MSp

"RXN0-5184",		# Starch	# 2 genes, 6 MSp
"RXN-1827",		# Starch	# 8 genes, 5 MSp, 1 GFPp
"MALTODEXGLUCOSID-RXN",	# Starch	# 5 genes, 2 MSp
"GLYCOGENSYN-RXN",	# Starch	# 3 genes, 5 MSp
"GLUC1PADENYLTRANS-RXN",	# Starch synthesis	# 6 genes, 11 MSp
"PGLUCISOM-RXN",		# Starch synthesis	# 2 genes, 6 MSp
"PHOSPHOGLUCMUT-RXN",	# Starch synthesis + degradation	# 4 genes, 10 MSp, (1 MSm, 1 GFPc)
"RXN0-5182",		# Starch degradation	# no genes # maltotetraose
"AMYLOMALT-RXN",	# Starch degradation	# 2 genes, 3 MSp, (1 GFPc)
"RXN0-5181",		# Starch degradation	# 3 genes, 3 MSp, 1 GFPp
"ALPHA-AMYL-RXN",	# Starch degradation	# 3 genes, 3 MSp, 1 GFPp
"RXN-2141",		# Amylase	# 4 genes, 2 MSp
"RXN-10770",		# ADP-glucose	# 1 gene, 3 MSp

"RIBULOSE-BISPHOSPHATE-CARBOXYLASE-RXN",	# Calvin Cycle	# 5 genes, 46 MSp, 2 GFPp
"PHOSPHORIBULOKINASE-RXN",	# Calvin Cycle	# 1 gene, 10 MSp
"PHOSGLYPHOS-RXN",		# Calvin Cycle	# 3 genes, 15 MSp, 2 GFPp, (2 MSm, 1 GFPc)
"RIB5PISOM-RXN",		# Calvin Cycle + PPP	# 3 genes, 8 MSp, (2 GFPc)
"RIBULP3EPIM-RXN",		# Calvin Cycle + PPP	# 3 genes, 7 MSp
"1TRANSKETO-RXN",		# Calvin Cycle + PPP	# 2 genes, 9 MSp
"2TRANSKETO-RXN",		# Calvin Cycle + PPP	# 2 genes, 9 MSp
"1.2.1.13-RXN",			# Calvin Cycle	# 3 genes, 23 MSp
"TRIOSEPISOMERIZATION-RXN",	# Calvin Cycle	# 2 genes, 9 MSp, 1 GFPp, (2 MSm, 1 GFPc)
"F16ALDOLASE-RXN",		# Calvin Cycle	# 9 genes, 32 MSp, 3 GFPp, (3 MSm)
"SEDOHEPTULOSE-BISPHOSPHATASE-RXN",	# Calvin Cycle	# 1 gene, 8 MSp
"F16BDEPHOS-RXN",		# Calvin Cycle	# 3 genes, 10 MSp
"SEDOBISALDOL-RXN",		# Calvin Cycle	# no genes ##########

"RXN-961",		# Photorespiration	# 5 genes, 46 MSp, 2 GFPp
"GPH-RXN",		# Photorespiration	# 3 genes, 8 MSp, (1 GFPc)
"GLY3KIN-RXN",		# Photorespiration	# 1 gene, 2 MSp

"HYDROXYPYRUVATE-REDUCTASE-RXN-(NADP)",	# Photorespiration	# 2 genes, 5 MSp, 1 GFPp, (4 MSx)	# Timm et al., 2011
"GLYOXYLATE-REDUCTASE-NADP+-RXN",	# Photorespiration	# 1 gene, 3 MSp, 1 GFPp	# Timm et al., 2011

"6PGLUCONDEHYDROG-RXN",		# OPPP	# 3 genes, 4 MSp, (1 MSm, 3 MSx, 1 GFPc)
"6PGLUCONOLACT-RXN",		# OPPP	# 3 genes ##########
"GLU6PDEHYDROG-RXN",		# OPPP	# 5 genes, 5 MSp

"TRANSALDOL-RXN",	# PPP	# no genes ##########
"6PFRUCTPHOS-RXN",	# glycolysis	# 7 genes, 2 MSp	# Mustroph et al., 2007
"GAPOXNPHOSPHN-RXN",	# glycolysis	# 10 genes, 40 MSp, (4 MSm, 1 GFPc)	# Munoz-Bertomeu et al., 2009
"3PGAREARR-RXN",	# glycolysis	# 3 genes, 1 MSp, 1 GFPp	# Andriotis et al., 2010
"2PGADEHYDRAT-RXN",	# glycolysis	# 3 genes, 2 MSp, 2 GFPp, (4 GFPc)	# Andriotis et al., 2010
"PEPDEPHOS-RXN",	# glycolysis	# 13 genes, 10 MSp, 2 GFPp	# Andriotis et al., 2010
"GLUCOKIN-RXN",		# hexokinase	# 6 genes, 1 MSp, (4 MSm, 1 GFPm) ##########	# Claeyssen, 2007


"GLYOHMETRANS-RXN",	# Serine	# 7 genes, 7 MSp, 1 GFPp, (4 MSm)	# Zhang et al., 2010
"PGLYCDEHYDROG-RXN",	# Serine biosynthesis	# 4 genes, 8 MSp, (1 MSm, 4 MSx)	# Ho and Saito, 2001
"PSERTRANSAM-RXN",	# Serine biosynthesis	# 2 genes, 5 MSp, 1 GFPp	# Ho and Saito, 2001
"RXN0-5114",		# Serine biosynthesis	# 1 gene, 2 MSp			# Ho and Saito, 2001

#"TRYPSYN-RXN",		# Tryptophan biosynthesis	# 5 genes, 7 MSp

"DAHPSYN-RXN",				# shikimate pathway	# 3 genes, 3 MSp
"3-DEHYDROQUINATE-SYNTHASE-RXN",	# shikimate pathway	# 1 gene ##########
"3-DEHYDROQUINATE-DEHYDRATASE-RXN",	# shikimate pathway	# no genes ##########
"SHIKIMATE-5-DEHYDROGENASE-RXN",	# shikimate pathway	# 1 gene, 2 MSp
"SHIKIMATE-KINASE-RXN",			# shikimate pathway	# no genes ##########
"2.5.1.19-RXN",				# shikimate pathway	# 2 genes, 5 MSp, 1 GFPp
"CHORISMATE-SYNTHASE-RXN",		# shikimate pathway	# 1 gene, 2 MSp
"CHORISMATEMUT-RXN",			# Phenylalanine and Tyrosine biosynthesis	# 1 gene ##########
"PREPHENATE-TRANSAMINE-RXN",		# Phenylalanine and Tyrosine biosynthesis	# no genes ##########
"RXN-5682",				# Tyrosine biosynthesis	# 2 genes, 1 MSp, 2 GFPp
"TYRAMINOTRANS-RXN",			# Tyrosine biosynthesis	# 4 genes, 1 MSp
"PREPHENATEDEHYDROG-RXN",		# Tyrosine biosynthesis	# no genes
"PREPHENATE-DEHYDROGENASE-NADP+-RXN",	# Tyrosine biosynthesis	# 1 gene, 1 MSp, 1 GFPp
"CARBOXYCYCLOHEXADIENYL-DEHYDRATASE-RXN",	# Phenylalanine biosynthesis	# 6 genes, 1 MSp, 6 GFPp

"ANTHRANSYN-RXN",			# Tryptophan biosynthesis	# 10 genes, 5 MSp, 1 GFPp
"PRTRANS-RXN",				# Tryptophan biosynthesis	# 1 gene, 4 MSp
"PRAISOM-RXN",				# Tryptophan biosynthesis	# 3 genes, 2 MSp
"IGPSYN-RXN",				# Tryptophan biosynthesis	# 2 genes, 7 MSp
"RXN0-2381",				# Tryptophan biosynthesis	# 1 gene ##########
"RXN0-2382",				# Tryptophan biosynthesis	# 5 genes, 7 MSp

#"ACETATE--COA-LIGASE-ADP-FORMING-RXN",	# fatty acid synthesis	# 2 genes, (2 MSx)	# Lin and Oliver, 2008
"PYRUVDEH-RXN",				# fatty acid synthesis	# 2 genes, 4 MSp, (5 MSm)
"ACETATE--COA-LIGASE-RXN",	# S fix + fatty acid synthesis	# 4 genes, 5 MSp, (6 MSx) ##########
"ACETYL-COA-CARBOXYLTRANSFER-RXN",	# fatty acid synthesis	# 6 genes, 18 MSp
"MALONYL-COA-ACP-TRANSACYL-RXN",	# fatty acid synthesis	# 1 gene, 4 MSp
"2.3.1.180-RXN",			# fatty acid synthesis	# 1 gene, 2 MSp
"RXN-9514",				# fatty acid synthesis	# 1 gene, 3 MSp
"4.2.1.58-RXN",				# fatty acid synthesis	# 1 gene, 3 MSp
"RXN-9657",				# fatty acid synthesis	# no genes
"RXN-9516",				# fatty acid synthesis	# 3 genes, 7 MSp, (1 GFPm)
"RXN-9518",				# fatty acid synthesis	# 1 gene, 3 MSp
"RXN-9520",				# fatty acid synthesis	# no genes
"RXN-9658",				# fatty acid synthesis	# no genes
"RXN-9523",				# fatty acid synthesis	# 3 genes, 7 MSp, (1 GFPm)
"RXN-9524",				# fatty acid synthesis	# 1 gene, 3 MSp
"4.2.1.59-RXN",				# fatty acid synthesis	# no genes
"RXN-9659",				# fatty acid synthesis	# no genes
"RXN-9527",				# fatty acid synthesis	# 3 genes, 7 MSp, (1 GFPm)
"RXN-9528",				# fatty acid synthesis	# 1 gene, 3 MSp
"RXN-9655",				# fatty acid synthesis	# no genes			
"RXN-9660",				# fatty acid synthesis	# no genes
"RXN-9531",				# fatty acid synthesis	# 3 genes, 7 MSp, (1 GFPm)
"RXN-9532",				# fatty acid synthesis	# 1 gene, 3 MSp
"RXN-9533",				# fatty acid synthesis	# no genes
"RXN-9661",				# fatty acid synthesis	# no genes
"RXN-9535",				# fatty acid synthesis	# 3 genes, 7 MSp, (1 GFPm)
"RXN-9536",				# fatty acid synthesis	# 1 gene, 3 MSp
"RXN-9537",				# fatty acid synthesis	# no genes
"RXN-9662",				# fatty acid synthesis	# no genes
"RXN-9539",				# fatty acid synthesis	# 3 genes, 7 MSp, (1 GFPm)
"RXN-9540",				# fatty acid synthesis	# 1 gene, 3 MSp
"4.2.1.61-RXN",				# fatty acid synthesis	# no genes
"RXN-9663",				# fatty acid synthesis	# no genes
"RXN-9549",				# fatty acid synthesis	# no genes

#"RXN-9538",	# ACPs	# 1 gene, 8 MSp
"RXN-9652",	# ACPs	# 3 genes, 7 MSp
#"RXN-9526",	# ACPs	# 1 gene, 8 MSp
"RXN-9650",	# ACPs	# 3 genes, 7 MSp
#"RXN-9534",	# ACPs	# 1 gene, 8 MSp
"RXN-9648",	# ACPs	# 3 genes, 7 MSp
#"RXN-9521",	# ACPs	# 1 gene, 8 MSp
#"RXN-9515",	# ACPs	# 1 gene, 8 MSp
#"RXN-9530",	# ACPs	# 1 gene, 8 MSp
"RXN-9654",	# ACPs	# 3 genes, 7 MSp
#"RXN-9542",	# ACPs	# 1 gene, 8 MSp
"RXN-9651",	# ACPs	# 3 genes, 7 MSp
"RXN-9653",	# ACPs	# 3 genes, 7 MSp



"PRPPSYN-RXN",	# PRPP		# 5 genes, 2 MSp, (1 GFPc)
"ATPPHOSPHORIBOSYLTRANS-RXN",	# Histidine biosynthesis	# 2 genes, 5 MSp
"HISTPRATPHYD-RXN",		# Histidine biosynthesis	# 1 gene, 3 MSp
"HISTCYCLOHYD-RXN",		# Histidine biosynthesis	# 1 gene, 3 MSp
"PRIBFAICARPISOM-RXN",		# Histidine biosynthesis	# 1 gene, 3 MSp
"GLUTAMIDOTRANS-RXN",		# Histidine biosynthesis	# 1 gene, 3 MSp
"IMIDPHOSDEHYD-RXN",		# Histidine biosynthesis	# no genes
"HISTAMINOTRANS-RXN",		# Histidine biosynthesis	# 2 genes, 1 MSp
"HISTIDPHOS-RXN",		# Histidine biosynthesis	# no genes
"HISTOLDEHYD-RXN",		# Histidine biosynthesis	# 1 gene, 2 MSp
"HISTALDEHYD-RXN",		# Histidine biosynthesis	# 1 gene, 2 MSp
"RXN-8001",			# Histidine biosynthesis	# 1 gene, 2 MSp	# redundant

"GLUTKIN-RXN",			# Proline biosynthesis	# 2 genes, 1 MSp, 2 GFPp, (2 GFPc)	# Funck et al., 2010
"GLUTSEMIALDEHYDROG-RXN",	# Proline biosynthesis	# 2 genes, 1 MSp, 2 GFPp, (2 GFPc)	# Funck et al., 2010
"PROLINE-MULTI",		# Proline biosynthesis	# no genes ##########	# Verbruggen, 2008
"SPONTPRO-RXN",			# Proline biosynthesis + degradation	# no genes ##########	# Verbruggen, 2008
"PYRROLINECARBREDUCT-RXN-(NAD)",	# Proline biosynthesis	# 1 gene ##########	# Verbruggen, 2008
"PYRROLINECARBREDUCT-RXN-(NADP)",	# Proline biosynthesis	# 1 gene ##########	# Verbruggen, 2008

"N-ACETYLTRANSFER-RXN",		# Arginine biosynthesis	# no genes ##########	# Slocum 2005
"ACETYLGLUTKIN-RXN",		# Arginine biosynthesis	# 4 genes, 6 MSp	# Slocum 2005
"N-ACETYLGLUTPREDUCT-RXN",	# Arginine biosynthesis	# 3 genes, 4 MSp	# Slocum 2005
"ACETYLORNTRANSAM-RXN",		# Arginine biosynthesis	# 1 gene, 5 MSp	# Slocum 2005
"ACETYLORNDEACET-RXN",		# Arginine biosynthesis	# no genes ##########	# Slocum 2005
"GLUTAMATE-N-ACETYLTRANSFERASE-RXN",	# Arginine biosynthesis	# no genes ##########	# Slocum 2005
"ORNCARBAMTRANSFER-RXN",	# Arginine biosynthesis	# 1 gene, 3 MSp	# Slocum 2005
"CARBPSYN-RXN",			# Arginine + pyrimidine biosynthesis	# 2 genes, 7 MSp
"6.3.4.16-RXN",			# carbamoylphosphate synthase	# 2 genes, 7 MSp	# Potel et al., 2009

"ASPARTATEKIN-RXN",		# Asp aa biosynthesis	# 6 genes, 5 MSp	# Galili 1995
"ASPARTATE-SEMIALDEHYDE-DEHYDROGENASE-RXN",	# Asp aa biosynthesis	# 1 gene, 3 MSp	# Galili 1995

"DIHYDRODIPICSYN-RXN",		# Lysine biosynthesis	# 2 genes, 1 MSp	# Galili 1995
"DIHYDROPICRED-RXN-(NADP)",	# Lysine biosynthesis	# 2 genes, 2 MSp	# Galili 1995
"DIHYDROPICRED-RXN-(NAD)",	# Lysine biosynthesis	# 2 genes, 2 MSp	# Galili 1995
"RXN-7737",			# Lysine biosynthesis	# 1 gene, 4 MSp	# Galili 1995
"DIAMINOPIMEPIM-RXN",		# Lysine biosynthesis	# 1 gene, 2 MSp	# Galili 1995
"DIAMINOPIMDECARB-RXN",		# Lysine biosynthesis	# 2 genes, 4 MSp	# Galili 1995

"HOMOSERDEHYDROG-RXN-(NAD)",	# Thr + Met biosynthesis	# 3 genes, 3 MSp	# Galili 1995
"HOMOSERDEHYDROG-RXN-(NADP)",	# Thr + Met biosynthesis	# 3 genes, 3 MSp	# Galili 1995
"HOMOSERKIN-RXN",		# Thr + Met biosynthesis	# 1 gene, 3 MSp	# Galili 1995
"THRESYN-RXN",			# Thr biosynthesis	# 2 genes, 4 MSp	# Galili 1995

"THREDEHYD-RXN",		# Isoleucine biosynthesis	# 1 gene, 1 MSp	# Binder et al., 2007
"ACETOOHBUTSYN-RXN",		# Isoleucine biosynthesis	# 1 gene, 2 MSp	# Binder et al., 2007
"ACETOOHBUTREDUCTOISOM-RXN",	# Isoleucine biosynthesis	# no genes ##########	# Binder et al., 2007
"DIHYDROXYMETVALDEHYDRAT-RXN",	# Isoleucine biosynthesis	# no genes ##########	# Binder et al., 2007
"BRANCHED-CHAINAMINOTRANSFERILEU-RXN",	# Isoleucine biosynthesis	# 5 genes, 5 MSp, 3 GFPp, (1 MSm, 1 GFPm)	# Binder et al., 2007

"ACETOLACTSYN-RXN",		# Val + Leu biosynthesis	# 1 gene, 2 MSp	# Binder et al., 2007
"ACETOLACTREDUCTOISOM-RXN",	# Val + Leu biosynthesis	# no genes ##########	# Binder et al., 2007
"DIHYDROXYISOVALDEHYDRAT-RXN",	# Val + Leu biosynthesis	# no genes ##########	# Binder et al., 2007
"BRANCHED-CHAINAMINOTRANSFERVAL-RXN",	# Valine biosynthesis	# 5 genes, 5 MSp, 3 GFPp, (1 MSm, 1 GFPm)	# Binder et al., 2007

"2-ISOPROPYLMALATESYN-RXN",	# Leucine biosynthesis	# 2 genes, 4 MSp	# Binder et al., 2007
"3-ISOPROPYLMALISOM-RXN",	# Leucine biosynthesis	# no genes ##########	# Binder et al., 2007
"RXN-8991",			# Leucine biosynthesis	# no genes ##########	# Binder et al., 2007
"3-ISOPROPYLMALDEHYDROG-RXN",	# Leucine biosynthesis	# 4 genes, 13 MSp	# Binder et al., 2007
"RXN-7800",			# Leucine biosynthesis	# no genes ##########	# Binder et al., 2007
"BRANCHED-CHAINAMINOTRANSFERLEU-RXN",	# Leucine biosynthesis	# 7 genes, 5 MSp, 3 GFPp, (1 MSm, 1 GFPm)	# Binder et al., 2007

"ASPAMINOTRANS-RXN",		# Aspartate	# 7 genes, 9 MSp, 1 GFPp, (3 MSm, 3 MSx, 1 GFPx)	# Wadsworth, 1997

"SULFATE-ADENYLYLTRANS-RXN",	# S fix	# 4 genes, 8 MSp, 1 GFPp, (1 MSm)	# Rotte and Leustek, 2000
"1.8.4.9-RXN",			# S fix	# 3 genes, 3 MSp	# Rotte and Leustek, 2000
"SULFITE-REDUCTASE-FERREDOXIN-RXN",	# S fix	# 1 gene, 7 MSp
"SERINE-O-ACETTRAN-RXN",	# S fix + Cys biosynthesis	# 5 genes, 1 GFPp, (3 GFPc, 1 GFPm) ##########	# Noji et al., 1998
"ACSERLY-RXN",			# S fix + Cys biosynthesis	# 9 genes, 17 MSp, (5 MSm, 2 MSx)	# Wirtz et al., 2004

"CYSPH-RXN",			# Methionine biosynthesis	# no genes ##########	# Heese 2003
"CYSTATHIONINE-BETA-LYASE-RXN",	# Methionine biosynthesis	# 4 genes, 2 MSp	# Heese 2003
"HOMOCYSMETB12-RXN",		# Methionine biosynthesis	# 1 gene, 1 MSp, 1 GFPp	# Wirtz and Droux, 2005
#"O-SUCCHOMOSERLYASE-RXN",	# Methionine biosynthesis	# 2 genes, 3 MSp ##########
#"METBALT-RXN",			# Methionine biosynthesis	# 2 genes, 3 MSp ##########

"CYSTATHIONINE-BETA-SYNTHASE-RXN",	# Homocysteine and cysteine interconversion	# no genes ##########
"CYSTAGLY-RXN",				# Homocysteine and cysteine interconversion	# no genes ##########

"FERREDOXIN--NITRITE-REDUCTASE-RXN",	# N fix	# 1 gene, 6 MSp, (1 MSm)
"GLUTAMINESYN-RXN",			# N fix	# 6 genes, 12 MSp, 1 GFPp, (1 MSc, 1 GFPc, 1 GFPm)	# Suzuki and Knaff, 2005
"GLUTAMATE-SYNTHASE-FERREDOXIN-RXN",	# N fix	# 1 gene, 6 MSp				# Suzuki and Knaff, 2005
"GLUTAMATE-SYNTHASE-NADH-RXN",		# Glutamate synthase	# 3 genes, 13 MSp	# Suzuki and Knaff, 2005


"ASPCARBTRANS-RXN",		# Pyrimidine biosynthesis	# 1 gene, 3 MSp	# Zrenner et al., 2006
"DIHYDROOROT-RXN",		# Pyrimidine biosynthesis	# 1 gene, 3 MSp	# Zrenner et al., 2006
"OROPRIBTRANS-RXN",		# Pyrimidine biosynthesis	# 1 gene ##########	# Zrenner et al., 2006
"OROTPDECARB-RXN",		# Pyrimidine biosynthesis	# 1 gene ##########	# Zrenner et al., 2006

"PRPPAMIDOTRANS-RXN",		# Purine biosynthesis	# 3 genes, 3 MSp	# Zrenner et al., 2006
"GLYRIBONUCSYN-RXN",		# Purine biosynthesis	# 1 gene, 4 MSp	# Zrenner et al., 2006
"GART-RXN",			# Purine biosynthesis	# 4 genes, 2 MSp	# Zrenner et al., 2006
"GARTRANSFORMYL2-RXN",		# Purine biosynthesis	# 1 gene, 2 MSp	##########
"FGAMSYN-RXN",			# Purine biosynthesis	# 1 gene, 4 MSp, 1 GFPp, (1 MSm, 1 GFPm)	# Zrenner et al., 2006
"AIRS-RXN",			# Purine biosynthesis	# 1 gene, 2 MSp, (1 MSm)	# Zrenner et al., 2006
"AIRCARBOXY-RXN",		# Purine biosynthesis	# 1 gene, 3 MSp	# Zrenner et al., 2006
"SAICARSYN-RXN",		# Purine biosynthesis	# 1 gene, 2 MSp	# Zrenner et al., 2006
"AICARSYN-RXN",			# Purine biosynthesis	# 2 genes, 6 MSp	# Zrenner et al., 2006
"AICARTRANSFORM-RXN",		# Purine biosynthesis	# no genes ##########	# Zrenner et al., 2006
"IMPCYCLOHYDROLASE-RXN",	# Purine biosynthesis	# 1 gene, 4 MSp	# Zrenner et al., 2006
"ADENYLOSUCCINATE-SYNTHASE-RXN",	# Purine biosynthesis	# 1 gene, 5 MSp	# Zrenner et al., 2006
"AMPSYN-RXN",			# Purine biosynthesis	# 2 genes, 6 MSp	# Zrenner et al., 2006


"MALIC-NADP-RXN",			# malic enzyme	# 6 genes, 3 MSp, (4 MSm) # Wheeler et al., 2008
"MALATE-DEHYDROGENASE-NADP+-RXN",	# malate dehydrogenase (NADP)	# 1 gene, 6 MSp, (1 MSm)
"MALATE-DEH-RXN",	# malate dehydrogenase (NAD)	# 8 genes, 14 MSp, (9 MSm, 9 MSx)	# Berkemeyer et al., 1998
"OXALODECARB-RXN",	# oxaloacetate decarboxylase	# no genes ##########	# Trukhina et al., 2002

"RXN0-5224",		# carbonic anhydrase	# 11 genes, 19 MSp, 2 GFPp, (11 MSm, 2 GFPc, 1 GFPm) # Fabre et al., 2007
"INORGPYROPHOSPHAT-RXN",	# PPiase	# 9 genes, 10 MSp, (1 MSm)	# Schulze et al., 2004
"PYRUVATEORTHOPHOSPHATE-DIKINASE-RXN",	# PPDK	# 1 gene, 5 MSp, 1 GFPp	# Parsley and Hibberd, 2006
#"ISOCITDEH-RXN",	# ICDH	# 3 genes, 3 MSp, (1 MSm, 4 MSx, 1 GFPx)	# Hodges et al., 2003
"1.2.1.2-RXN",		# formate dehydrogenase	# 2 genes, 3 MSp, (6 MSm)	# Herman et al., 2002
"RXN-6903",		# succinic semialdehyde reductase isoforms	# no genes	# Shelp et al.., 2012


"THIOREDOXIN-REDUCT-NADPH-RXN",	# thioredoxin reductase	# 4 genes, 5 MSp, (1 MSx)	# Serrato et al., 2004

"ADENYL-KIN-RXN",		# adenylate kinase	# 8 genes, 8 MSp, 1 GFPp, (6 MSm)	# Zrenner et al., 2006
"UMPKI-RXN",			# uridine monophosphate kinase	# 4 genes, 1 MSp, (1 GFPc)	# Zrenner et al., 2006
"CMPKI-RXN",	# uridine monophosphate kinase	# 3 genes, (1 MSc, 1 GFPc)	# Zrenner et al., 2006
"CDPKIN-RXN",	# nucleoside diphosphate kinase	# 4 genes, 7 MSp, 1 GFPp, (5 MSm, 1 MSx, 1 GFPc, 1 GFPm, 1 GFPx)	# Zrenner et al., 2006
"UDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 7 MSp, 1 GFPp, (5 MSm, 1 MSx, 1 GFPc, 1 GFPm, 1 GFPx)	# Zrenner et al., 2006
"GDPKIN-RXN",	# nucleoside diphosphate kinase	# 1 gene, 5 MSp, 1 GFPp	# Zrenner et al., 2006
"DUDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 7 MSp, 1 GFPp, (5 MSm, 1 MSx, 1 GFPc, 1 GFPm, 1 GFPx)	# Zrenner et al., 2006
"DADPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 7 MSp, 1 GFPp, (5 MSm, 1 MSx, 1 GFPc, 1 GFPm, 1 GFPx)	# Zrenner et al., 2006
"DGDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 7 MSp, 1 GFPp, (5 MSm, 1 MSx, 1 GFPc, 1 GFPm, 1 GFPx)	# Zrenner et al., 2006
"DCDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 7 MSp, 1 GFPp, (5 MSm, 1 MSx, 1 GFPc, 1 GFPm, 1 GFPx)	# Zrenner et al., 2006
"DTDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 7 MSp, 1 GFPp, (5 MSm, 1 MSx, 1 GFPc, 1 GFPm, 1 GFPx)	# Zrenner et al., 2006

"GLUTCYSLIG-RXN",		# glutathione biosynthesis	# 1 gene, 5 MSp	# Wirtz and Droux, 2005
"GLUTATHIONE-SYN-RXN",		# glutathione biosynthesis	# 1 gene ##########	# Wirtz and Droux, 2005
"GLUTATHIONE-REDUCT-NADPH-RXN",	# GSH recycling + GSH-ascorbate cycle	# 2 genes, 5 MSp, (2 MSm, 3 MSx, 1 GFPm)	# Marty et al., 2009
"RXN-3521",	# GSH-ascorbate cycle	# 3 genes, 4 MSp, (1 MSm, 5 MSm, 1 GFPx)	# Chew et al., 2003
"RXN-3522",	# GSH-ascorbate cycle	# 10 genes, 4 MSp, (4 MSx)	# Chew et al., 2003
"RXN-3523",	# GSH-ascorbate cycle	# no genes, non-enzymatic	# Chew et al., 2003
"1.8.5.1-RXN",	# GSH-ascorbate cycle	# 4 genes, 7 MSp, 1 GFPp, (1 MSm, 1 MSx, 1 GFPc, 1 GFPx)	# Chew et al., 2003
"L-ASCORBATE-PEROXIDASE-RXN",	# GSH-ascorbate cycle	# 2 genes, 1 MSp	# Chew et al., 2003	# redundant

"SUPEROX-DISMUT-RXN",	# SOD	# 9 genes, 21 MSp, (7 MSm, 2 MSx)	# Alscher et al., 2002

"L-ASPARTATE-OXID-RXN",		# NAD biosynthesis	# 1 gene, 1 GFPp	# Katoh et al., 2006
"QUINOLINATE-SYNTHA-RXN",	# NAD biosynthesis	# 1 gene, 1 GFPp	# Katoh et al., 2006
"QUINOPRIBOTRANS-RXN",		# NAD biosynthesis	# 1 gene, 2 MSp, 1 GFPp	# Katoh et al., 2006

"NAD-KIN-RXN",		# NADP biosynthesis	# 3 genes, 2 MSp, 2 GFP, (1 GFPc, 1 GFPx)	# Hashida et al., 2009

"GLURS-RXN",		# Chlorophyll biosynthesis	# 2 genes, 3 MSp, 2 GFPp, (2 GFPm)	# Eckhardt et al., 2004
"GLUTRNAREDUCT-RXN",	# Chlorophyll biosynthesis	# 3 genes, 1 MSp	# Eckhardt et al., 2004
"GSAAMINOTRANS-RXN",	# Chlorophyll biosynthesis	# 2 genes, 12 MSp, 1 GFPp	# Eckhardt et al., 2004
"PORPHOBILSYNTH-RXN",	# Chlorophyll biosynthesis	# 1 gene, 5 MSp	# Eckhardt et al., 2004
"OHMETHYLBILANESYN-RXN",	# Chlorophyll biosynthesis	# 1 gene, 5 MSp	# Eckhardt et al., 2004
"UROGENIIISYN-RXN",	# Chlorophyll biosynthesis	# 1 gene, 3 MSp, 1 GFPp	# Eckhardt et al., 2004
"UROGENDECARBOX-RXN",	# Chlorophyll biosynthesis	# 2 genes, 8 MSp	# Eckhardt et al., 2004
"RXN0-1461",		# Chlorophyll biosynthesis	# 2 genes, 6 MSp, 1 GFPp	# Eckhardt et al., 2004
"PROTOPORGENOXI-RXN",	# Chlorophyll + heme biosynthesis	# 2 genes, 7 MSp	# Eckhardt et al., 2004
"RXN-9259",		# Chlorophyll + heme biosynthesis	# 2 genes, 7 MSp ##########
"RXN1F-20",		# Chlorophyll biosynthesis	# 4 genes, 13 MSp, 2 GFPp, (1 MSm)	# Eckhardt et al., 2004
"RXN-MG-PROTOPORPHYRIN-METHYLESTER-SYN",	# Chlorophyll biosynthesis	# 1 gene, 4 MSp	# Eckhardt et al., 2004
"RXN-5282",		# Chlorophyll biosynthesis	# 1 gene, 5 MSp	# Eckhardt et al., 2004
"RXN-5283",		# Chlorophyll biosynthesis	# 1 gene, 5 MSp	# Eckhardt et al., 2004
"RXN-5284",		# Chlorophyll biosynthesis	# 1 gene, 5 MSp	# Eckhardt et al., 2004
"RXN1F-72",		# Chlorophyll biosynthesis	# 1 gene, 4 MSp	# Eckhardt et al., 2004
"RXN1F-10",		# Chlorophyll biosynthesis	# 3 genes, 15 MSp, 2 GFPp	# Eckhardt et al., 2004
"RXN1F-66",		# Chlorophyll biosynthesis + cycle	# 1 gene, 2 MSp	# Eckhardt et al., 2004
"RXN-7663",		# Chlorophyll biosynthesis	# 1 gene, 2 MSp	# Eckhardt et al., 2004
"RXN-7664",		# Chlorophyll biosynthesis	# 1 gene, 7 MSp	# Keller et al., 1998
"RXN-7665",		# Chlorophyll biosynthesis	# 1 gene, 7 MSp	# Keller et al., 1998
"RXN-7666",		# Chlorophyll biosynthesis	# 1 gene, 7 MSp	# Keller et al., 1998
"RXN-7676",		# Chlorophyll cycle	# 1 gene, 2 GFPp	# Eckhardt et al., 2004
"RXN-7677",		# Chlorophyll cycle	# 2 genes, 2 MSp, 2 GFPp	# Eckhardt et al., 2004
"RXN-7674",		# Chlorophyll cycle	# 1 gene, 2 GFPp	# Eckhardt et al., 2004
"RXN-7678-(NAD)",	# Chlorophyll cycle	# 2 genes, 2 MSp	# Eckhardt et al., 2004
"RXN-7678-(NADP)",	# Chlorophyll cycle	# 2 genes, 2 MSp	# Eckhardt et al., 2004
"RXN-7679",		# Chlorophyll cycle	# no genes	# Eckhardt et al., 2004

#"RXN-7738",		# Chlorophyll degradation	##### SUBA ######		# Eckhardt et al., 2004
#"RXN-7739",		# Chlorophyll degradation	##### SUBA ######		# Eckhardt et al., 2004
#"RXN-7740",		# Chlorophyll degradation	##### SUBA ######		# Eckhardt et al., 2004
#"RXN-7741",		# Chlorophyll degradation	##### SUBA ######		# Eckhardt et al., 2004

"PABASYN-RXN",		# THF biosynthesis	# 1 gene, 1 GFPp	# Basset et al., 2003
"ADCLY-RXN",		# THF biosynthesis	# 1 gene, 3 MSp, 1 GFPp	# Basset et al., 2004

"ADENYLYLSULFKIN-RXN",	# PAPS biosynthesis	# 4 genes	# Mugford et al., 2009

"DXS-RXN",		# isoprenoid biosynthesis	# 3 genes, 2 MSp, 1 GFPp	# Laule et al., 2003
"DXPREDISOM-RXN",	# isoprenoid biosynthesis	# 1 gene, 2 MSp, 1 GFPp	# Laule et al., 2003
"2.7.7.60-RXN",		# isoprenoid biosynthesis	# 1 gene, 4 MSp, 1 GFPp	# Laule et al., 2003
"2.7.1.148-RXN",	# isoprenoid biosynthesis	# 5 genes, 46 MSp, 2 GFPp	# Laule et al., 2003
"RXN0-302",		# isoprenoid biosynthesis	# 1 gene, 3 MSp	# Laule et al., 2003
"RXN0-882",		# isoprenoid biosynthesis	# 1 gene, 6 MSp	# Laule et al., 2003
"RXN0-884-(NAD)",	# isoprenoid biosynthesis	# 1 gene, 1 MSp	# Laule et al., 2003
"RXN0-884-(NADP)",	# isoprenoid biosynthesis	# 1 gene, 1 MSp	# Laule et al., 2003
"ISPH2-RXN-(NAD)",	# isoprenoid biosynthesis	# 1 gene, 1 MSp	# Laule et al., 2003
"ISPH2-RXN-(NADP)",	# isoprenoid biosynthesis	# 1 gene, 1 MSp	# Laule et al., 2003
"IPPISOM-RXN",		# isoprenoid biosynthesis	# 3 genes, 5 MSp, 1 GFPp, (2 MSc, 1 GFPm)	# Laule et al., 2003
"GPPSYN-RXN",		# isoprenoid biosynthesis	# 3 genes, (2 MSc)	# Laule et al., 2003
"FPPSYN-RXN",		# isoprenoid biosynthesis	# 6 genes, 3 MSp, 2 GFPp, (2 MSc)	# Laule et al., 2003
"FARNESYLTRANSTRANSFERASE-RXN",	# isoprenoid biosynthesis	# 13 genes, 3 MSp, 3 GFPp, (2 GFPm)	# Laule et al., 2003
"RXN-7658",		# isoprenoid biosynthesis	# 1 gene, 7 MSp	# Laule et al., 2003
"RXN-7659",		# isoprenoid biosynthesis	# 1 gene, 7 MSp	# Laule et al., 2003
"RXN-7660",		# isoprenoid biosynthesis	# 1 gene, 7 MSp	# Laule et al., 2003

"GLYC3PDEHYDROGBIOSYN-RXN",	# glycerol-3-phosphate dehydrogenase	# 4 genes, 1 MSp, 1 GFPp	# Wei et al., 2001

#"ATP-CITRATE-PRO-S--LYASE-RXN",	# ATP:citrate lyase	# 6 genes, 1 MSp, (4 MSm)	#  Rangasamy and Ratledge, 2000

#"RXN-5061",	# folate transformation	# no genes ##########
"FORMYLTHFDEFORMYL-RXN",	# folate transformation	# no genes ##########
"FORMATETHFLIG-RXN",		# folate transformation # 5 genes, 5 MSp	# Hanson and Roje, 2001
"METHENYLTHFCYCLOHYDRO-RXN",	# folate transformation # no genes	# Hanson and Roje, 2001

"RXN-1407",	# Auxin biosynthesis	# no genes ##########
"RXN-1408",	# Auxin biosynthesis	# no genes ##########

"RXN-7978",	# xanthophyll cycle	# 1 gene, 4 MSp	# Jahns et al., 2009
"RXN-7979",	# xanthophyll cycle	# 1 gene, 4 MSp	# Jahns et al., 2009
"RXN-7984",	# xanthophyll cycle	# 1 gene, 4 MSp	# Jahns et al., 2009
"RXN-7985",	# xanthophyll cycle	# 1 gene, 4 MSp	# Jahns et al., 2009


"CARBAMATE-KINASE-RXN",		# Citrulline degradation	# no genes	# Ludwig, 1993
]


#_m
Mitochondria = [

"NADH-DEHYDROG-A-RXN",		# Oxidative Phosphorylation	# 37 genes, 135 MSm, 2 GFPm, (9 MSp)
"1.10.2.2-RXN",			# Oxidative Phosphorylation	# 3 genes, 7 MSm
"CYTOCHROME-C-OXIDASE-RXN",	# Oxidative Phosphorylation	# 13 genes, 19 MSm, (3 MSp)
"RXN0-5330-(NAD)",		# Alternative NADPH dehydrogenase	# 36 genes, 132 MSm, 2 GFPm, (9 MSp)
"RXN0-5330-(NADP)",		# Alternative NADPH dehydrogenase	# 36 genes, 132 MSm, 2 GFPm, (9 MSp)
"RXN-6883",			# Alternative oxidase	# 5 genes, 4 MSm, 1 GFPm, (1 MSp)
"RXN-6884",			# Alternative oxidase	# 5 genes, 4 MSm, 1 GFPm, (1 MSp)


"GCVMULTI-RXN",		# Photorespiration	# 2 genes, 4 MSm, (2 MSp)
"GLYOHMETRANS-RXN",	# Photorespiration	# 7 genes, 4 MSm, (7 MSp, 1 GFPp)


"PYRUVDEH-RXN",		# acetyl-CoA synthesis # 2 genes, 5 MSm, (4 MSp)

"CITSYN-RXN",		# TCA cycle	# 5 genes, 5 MSm, (1 MSp, 5 MSx)
"ACONITATEDEHYDR-RXN",	# TCA cycle	# 4 genes, 11 MSm, (7 MSp)
"ACONITATEHYDR-RXN",	# TCA cycle	# 4 genes, 11 MSm, (7 MSp)
"ISOCITRATE-DEHYDROGENASE-NAD+-RXN",	# TCA cycle	# 5 genes, 7 MSm, 1 GFPm, (1 MSp)
"2OXOGLUTARATEDEH-RXN",	# TCA cycle	# no genes ##########
"SUCCCOASYN-RXN",	# TCA cycle	# 3 genes, 15 MSm
"SUCCINATE-DEHYDROGENASE-UBIQUINONE-RXN",	# TCA cycle	# 11 genes, 31 MSm
"FUMHYDR-RXN",		# TCA cycle	# 2 genes, 6 MSm, 1 GFPm, (1 GFPc)	# Sweetlove et al., 2010
"MALATE-DEH-RXN",	# TCA cycle	# 8 genes, 9 MSm, (14 MSp, 9 MSx)

"SUCCINATE--COA-LIGASE-GDP-FORMING-RXN",	# TCA cycle	# no genes ##########
"SUCCINYL-COA-HYDROLASE-RXN",			# TCA cycle	# no genes ##########
#"MALATE-DEHYDROGENASE-ACCEPTOR-RXN",		# Quinol-MalateDH	# no genes ##########
"MALIC-NAD-RXN",	# malic enzyme	# no genes ##########

"GLUTAMATE-DEHYDROGENASE-RXN",	# GLT dehydrogenase (NADH)	# 3 genes, 12 MSm
#"GLUTDEHYD-RXN",		# GLT dehydrogenase (NADPH)	# 3 genes, 6 MSm

"GLUTAMINESYN-RXN",		# N fix + GLN synthesis	# 6 genes, 1 GFPm, (1 MSc, 12 MSp, 1 GFPc, 1 GFPp)	# Taira et al., 2004

"SPONTPRO-RXN",			# Proline biosynthesis + degradation	# no genes ##########	# Verbruggen, 2008
"RXN-821",			# Proline degradation	# 2 genes, 1 GFPm, (1 GFPp)	# Funck et al., 2010
"RXN-7183-(NAD)",		# Proline degradation	# 1 gene, 2 MSm, (1 MSp)	# Funck et al., 2010
"RXN-7183-(NADP)",		# Proline degradation	# 1 gene, 2 MSm, (1 MSp)	# Funck et al., 2010
"ORNITHINE-GLU-AMINOTRANSFORASE-RXN",	# Proline biosynthesis + degradation	# 2 genes, (5 MSp) ##########	# Verbruggen, 2008

"ACSERLY-RXN",			# S fix + Cys biosynthesis	# 9 genes, 5 MSm, (17 MSp, 2 MSx)	# Wirtz et al., 2004
"SERINE-O-ACETTRAN-RXN",	# S fix + Cys biosynthesis	# 5 genes, 1 GFPm, (3 GFPc, 1 GFPp) ##########	# Noji et al., 1998

"ALANINE-AMINOTRANSFERASE-RXN",	# Alanine	# 6 genes, 5 MSm, (3 MSp, 8 MSx, 1 GFPc, 1 GFPx)	# Miyashita et al., 2007
"ASPAMINOTRANS-RXN",		# Aspartate	# 7 genes, 3 MSm, (9 MSp, 3 MSx, 1 GFPp, 1 GFPx)	# Wadsworth, 1997

#"DIHYDROOROTATE-DEHYDROGENASE-RXN",	# Pyrimidine biosynthesis	# 1 gene, 2 MSm	# Zrenner et al., 2006
"ADENYL-KIN-RXN",		# adenylate kinase	# 8 genes, 6 MSm, (8 MSp, 1 GFPp)	# Zrenner et al., 2006
"CDPKIN-RXN",	# nucleoside diphosphate kinase	# 4 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"UDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"GDPKIN-RXN",	# nucleoside diphosphate kinase	# 1 gene, (5 MSp, 1 GFPp)	# Zrenner et al., 2006
"DUDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"DADPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"DGDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"DCDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"DTDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006

"ARGINASE-RXN",	# Arginine catabolism	# 2 genes, 1 MSm, (2 MSp) ##########	# Funck et al., 2008
"ORNCARBAMTRANSFER-RXN",	# Urea cycle	# 1 gene, (3 MSp) ##########
"CARBAMATE-KINASE-RXN",		# Citrulline degradation	# no genes ##########

"GABATRANSAM-RXN",	# GABA	# no genes ##########	# Bouche and Fromm, 2004
"RXN-6902",		# GABA	# 1 gene, 2 MSm	# Bouche and Fromm, 2004
"SUCCINATE-SEMIALDEHYDE-DEHYDROGENASE-RXN",	# GABA	# 1 gene, 2 MSm, (2 MSp)	# Bouche and Fromm, 2004


"GLUTATHIONE-REDUCT-NADPH-RXN",	# GSH recycling + GSH-ascorbate cycle	# 2 genes, 2 MSm, 1 GFPm, (5 MSp, 3 MSx)	# Marty et al., 2009
"RXN-3521",	# GSH-ascorbate cycle	# 3 genes, 1 MSm, (4 MSp, 5 MSm, 1 GFPx)	# Chew et al., 2003
"RXN-3522",	# GSH-ascorbate cycle	# 10 genes, (4 MSp, 4 MSx) ##########	# Chew et al., 2003
"RXN-3523",	# GSH-ascorbate cycle	# no genes, non-enzymatic	# Chew et al., 2003
"1.8.5.1-RXN",	# GSH-ascorbate cycle	# 4 genes, 1 MSm, (7 MSp, 1 GFPp, 1 MSx, 1 GFPc, 1 GFPx)	# Chew et al., 2003
"L-ASCORBATE-PEROXIDASE-RXN",	# GSH-ascorbate cycle	# 2 genes, (1 MSp)	# Chew et al., 2003	# redundant

"SUPEROX-DISMUT-RXN",	# SOD	# 9 genes, 7 MSm, (21 MSp, 2 MSx)	# Alscher et al., 2002

"THIOREDOXIN-REDUCT-NADPH-RXN",	# thioredoxin reductase	# 4 genes, (5 MSp, 1 MSx)	# Serrato et al., 2004
"ISOCITDEH-RXN",	# ICDH	# 3 genes, 1 MSm, (3 MSp, 4 MSx, 1 GFPx)	# Hodges et al., 2003
"RXN0-5224",		# carbonic anhydrase	# 11 genes, 11 MSm, 1 GFPm (19 MSp, 2 GFPp, 2 GFPc) # Fabre et al., 2007
"RXN66-3",		# aldehyde dehydrogenase	# 1 gene, 4 MSm, (1 MSp)	# Kirch et al., 2004
#"ACETALD-DEHYDROG-RXN",	# aldehyde dehydrogenase	# no genes	# Kirch et al., 2004
#"GLYC3PDEHYDROG-RXN",	# FAD-GPDH	# 1 gene, 1 MSm	# Shen et al., 2003
#"RXN-6841",		# FAD-GPDH	# 1 gene, 1 MSm	# Shen et al., 2003

"BRANCHED-CHAINAMINOTRANSFERLEU-RXN",	# Leucine degradation	# 7 genes, 1 MSm, 1 GFPm, (5 MSp, 3 GFPp) 	# Schuster and Binder, 2005
"2KETO-4METHYL-PENTANOATE-DEHYDROG-RXN",	# Leucine degradation	# 4 genes, 12 MSm, (1 MSp)	# Schuster and Binder, 2005
"RXN0-2301",				# Leucine degradation	# 1 gene, 4 MSm, 1 GFPm	# Daschner et al., 2001
"ISOVALERYL-COA-FAD-RXN",		# Leucine degradation	# 1 gene, 4 MSm, 1 GFPm	# Daschner et al., 2001
"METHYLCROTONYL-COA-CARBOXYLASE-RXN",	# Leucine degradation	# 2 genes, 3 MSm	# Schuster and Binder, 2005
"METHYLGLUTACONYL-COA-HYDRATASE-RXN",	# Leucine degradation	# no genes	# Schuster and Binder, 2005
#"HYDROXYMETHYLGLUTARYL-COA-LYASE-RXN",	# Leucine degradation	######### SUBA ########## # Schuster and Binder, 2005

"BRANCHED-CHAINAMINOTRANSFERVAL-RXN",	# Valine degradation	# 5 genes, 1 MSm, 1 GFPm, (5 MSp, 3 GFPp) 	# Schuster and Binder, 2005
"1.2.1.25-RXN",				# Valine degradation 	# 4 genes, 12 MSm, (1 MSp)	# Schuster and Binder, 2005
"MEPROPCOA-FAD-RXN",			# Valine degradation	# 1 gene, 4 MSm, 1 GFPm	# Daschner et al., 2001
"METHYLACYLYLCOA-HYDROXY-RXN",		# Valine degradation	# 5 genes, (1 MSp, 9 MSx, 5 GFPx) ##########
"3-HYDROXYISOBUTYRYL-COA-HYDROLASE-RXN",	# Valine degradation	# 6 genes, 2 MSm, (1 MSc, 1 MSp, 2 MSx) ##########
"3-HYDROXYISOBUTYRATE-DEHYDROGENASE-RXN",	# Valine degradation	# no genes ##########
#"1.2.1.27-RXN",				# Valine degradation	# 5 genes, 8 MSm, (1 MSp) ##########
"RXN-11213",				# Valine degradation	# 5 genes, 8 MSm, (1 MSp) ##########

"BRANCHED-CHAINAMINOTRANSFERILEU-RXN",	# Isoleucine degradation	# 5 genes, 1 MSm, 1 GFPm, (5 MSp, 3 GFPp) 	# Schuster and Binder, 2005
"2KETO-3METHYLVALERATE-RXN",		# Isoleucine degradation	# 4 genes, 12 MSm, (1 MSp)	# Schuster and Binder, 2005
"2-MEBUCOA-FAD-RXN",			# Isoleucine degradation	# no genes ##########
"TIGLYLCOA-HYDROXY-RXN",		# Isoleucine degradation	# 5 genes, (1 MSp, 9 MSx, 5 GFPx) ##########
"1.1.1.178-RXN",			# Isoleucine degradation	# no genes ##########
"METHYLACETOACETYLCOATHIOL-RXN",	# Isoleucine degradation	# 2 genes, (1 MSc, 2 MSx, 2 GFPc) ##########

"PROTOPORGENOXI-RXN",	# Chlorophyll + heme biosynthesis	# 2 genes, (7 MSp)	# Eckhardt et al., 2004
"RXN-9259",		# Chlorophyll + heme biosynthesis	# 2 genes, (7 MSp) ##########

"GALACTONOLACTONE-DEHYDROGENASE-RXN",	# Ascorbate biosynthesis	# 1 gene, 4 MSm	# Linster and Clarke, 2008

"H2PTERIDINEPYROPHOSPHOKIN-RXN",	# THF biosynthesis	# 2 genes	# Hanson and Gregory, 2002
"H2PTEROATESYNTH-RXN",			# THF biosynthesis	# 2 genes	# Hanson and Gregory, 2002
"DIHYDROFOLATESYNTH-RXN",		# THF biosynthesis	# 1 gene, 1 MSm	# Hanson and Gregory, 2002
"DIHYDROFOLATEREDUCT-RXN",		# THF biosynthesis	# 3 genes	# Hanson and Gregory, 2002

"THYMIDYLATESYN-RXN",	# dTMP biosynthesis	# 3 genes	# Neuburger et al., 1996

"NITRIC-OXIDE-SYNTHASE-RXN",		# Nitric oxide	# no genes	# Guo and Crawford, 2005

"PROPCOASYN-RXN",	# beta-alanine biosynthesis	# 1 gene, (2 MSx) ##########
"RXN-6383",		# beta-alanine biosynthesis	# 5 genes, (1 MSp, 9 MSx, 5 GFPx) ##########
"RXN-6384",		# beta-alanine biosynthesis	# 6 genes, 2 MSm, (1 MSc, 1 MSp, 2 MSx) ##########

#"GLUTARYL-COA-DEHYDROG-RXN",	# Lysine degradation	# no genes ##########

"ACETYL-COA-HYDROLASE-RXN",	# Acetyl-CoA hydrolase	# no genes ##########

"1.2.1.2-RXN",		# formate dehydrogenase	# 2 genes, 6 MSm, (3 MSp)	# Herman et al., 2002
"FORMATETHFLIG-RXN",	# folate transformation # 5 genes, (5 MSp)	# Hanson and Roje, 2001
"METHENYLTHFCYCLOHYDRO-RXN",	# folate transformation # no genes	# Hanson and Roje, 2001

"1.5.5.1-RXN",		# electron-transferring-flavoprotein dehydrogenase	# 1 gene, 1 MSm, 1 GFPm ##########
]


#_x
Peroxisome = [

"RXN-969",			# Photorespiration	# 6 genes, 11 MSx, (3 MSp, 1 MSm)
"GLYCINE-AMINOTRANSFERASE-RXN",	# Photorespiration	# 3 genes, 11 MSx, (4 MSp)
"SERINE-GLYOXYLATE-AMINOTRANSFERASE-RXN",	# Photorespiration	# 1 gene, 3 MSx, (2 MSp)
"HYDROXYPYRUVATE-REDUCTASE-RXN-(NAD)",	# Photorespiration	# 1 gene, 4 MSx, (2 MSp)

"MALATE-DEH-RXN",	# Redox	# 8 genes, 9 MSm, (14 MSp, 9 MSx)

"CATAL-RXN",	# Photorespiration	# 3 genes, 12 MSx, (7 MSp, 3 MSm)

"ALANINE-AMINOTRANSFERASE-RXN",	# Alanine	# 6 genes, 8 MSm, 1 GFPx, (3 MSp, 5 MSm, 1 GFPc)	# Miyashita et al., 2007
"ASPAMINOTRANS-RXN",		# Aspartate	# 7 genes, 3 MSx, 1 GFPx, (9 MSp, 3 MSm, 1 GFPp)	# Wadsworth, 1997


"CITSYN-RXN",		# glyoxylate cycle	# 5 genes, 5 MSx, (1 MSp, 5 MSm)	# Kunze et al., 2006
"MALSYN-RXN",		# glyoxylate cycle	# 1 gene, 1 MSx	# Kunze et al., 2006
"ISOCIT-CLEAV-RXN",	# glyoxylate cycle	# 3 genes, 1 GFPx, (5 MSp)	# Kunze et al., 2006

"GLUTATHIONE-REDUCT-NADPH-RXN",	# GSH recycling + GSH-ascorbate cycle	# 2 genes, 3 MSx, (5 MSp, 2 MSm, 1 GFPm)	# Kataya, 2010
"RXN-3521",	# GSH-ascorbate cycle	# 3 genes, 5 MSx, 1 GFPx, (4 MSp, 1 MSm)	# Narendra et al, 2006
"RXN-3522",	# GSH-ascorbate cycle	# 10 genes, 4 MSx, (4 MSp)	# Lisenbee et al., 2005
"RXN-3523",	# GSH-ascorbate cycle	# no genes, non-enzymatic	# Chew et al., 2003
"1.8.5.1-RXN",	# GSH-ascorbate cycle	# 4 genes, 1 MSx, 1 GFPx, (7 MSp, 1 MSm, 1 GFPc, 1 GFPp)
"1.6.5.4-RXN",	# GSH-ascorbate cycle	# 10 genes, 4 MSx, (4 MSp)	# Lisenbee et al., 2005
"L-ASCORBATE-PEROXIDASE-RXN",	# GSH-ascorbate cycle	# 2 genes, (1 MSp)	# Chew et al., 2003

"SUPEROX-DISMUT-RXN",	# SOD	# 9 genes, 2 MSx, (21 MSp, 7 MSm)	# Alscher et al., 2002

"ALANINE--GLYOXYLATE-AMINOTRANSFERASE-RXN",	# Photorespiration	# 6 genes, 11 MSx, 2 GFPx, (4 MSp, 4 MSm, 1 GFPm)	# Liepman and Olsen, 2003
"ISOCITDEH-RXN",	# ICDH	# 3 genes, 4 MSx, 1 GFPx, (3 MSp, 1 MSm)	# Hodges et al., 2003
"SULFITE-OXIDASE-RXN",	# sulfite oxidase	# 1 gene, 3 MSx, 2 GFPx, (1 MSm)	# Hansch et al., 2006

"ACETATE--COA-LIGASE-RXN",	# S fix + fatty acid synthesis	# 4 genes, 6 MSx, (5 MSp) ##########

"NADH-KINASE-RXN",	# NADH kinase	# 2 genes, 1 GFPx, (1 GFPc)	# Waller et al., 2010

"URATE-OXIDASE-RXN",	# purine degradation	# 1 gene, 3 MSx	# Werner and Witte, 2011
"3.5.2.17-RXN",		# purine degradation	# 8 genes, 1 MSx	# Werner and Witte, 2011
"RXN-6201",		# purine degradation	# no genes	# Werner and Witte, 2011

"PHOSPHOMEVALONATE-KINASE-RXN",		# mevalonate pathway	# no genes	# Simkin et al., 2011
"DIPHOSPHOMEVALONTE-DECARBOXYLASE-RXN",	# mevalonate pathway	# 2 genes, (1 MSc)	# Simkin et al., 2011
"IPPISOM-RXN",		# mevalonate pathway	# 3 genes, (2 MSc, 5 MSp)	# Simkin et al., 2011

"GLUTACONYL-COA-DECARBOXYLASE-RXN",	# lysine degradation	# no genes ##########
"3-HYDROXBUTYRYL-COA-DEHYDRATASE-RXN",	# lysine degradation	# 2 genes, 6 MSx, 3 GFPx, (1 MSp)
"BHBDCLOS-RXN",				# lysine degradation	# 2 genes, 6 MSx, 4 GFPx
"ACETYL-COA-ACETYLTRANSFER-RXN",	# lysine degradation	# 2 genes, 2 MSx, (1 MSc, 2 GFPc)

"INORGPYROPHOSPHAT-RXN",	# PPiase	# 9 genes, (10 MSp, 1 MSm)	##########

]


#_c
Cytosol = [	# Reactions in other compartments and also in cytosol

"GLUCOKIN-RXN",			# hexokinase	# 6 genes, 1 MSp, (4 MSm, 1 GFPm) ##########	# Claeyssen, 2007
"PGLUCISOM-RXN",		# glycolysis	# 2 genes, 6 MSp
"6PFRUCTPHOS-RXN",		# glycolysis	# 7 genes, 2 MSp	# Mustroph et al., 2007
"F16ALDOLASE-RXN",		# glycolysis	# 9 genes, 32 MSp, 3 GFPp, (3 MSm)
"TRIOSEPISOMERIZATION-RXN",	# glycolysis	# 2 genes, 9 MSp, 1 GFPp, (2 MSm, 1 GFPc)
"PHOSGLYPHOS-RXN",		# glycolysis	# 3 genes, 15 MSp, 2 GFPp, (2 MSm, 1 GFPc)
"GAPOXNPHOSPHN-RXN",		# glycolysis	# 10 genes, 40 MSp, (4 MSm, 1 GFPc)	# Munoz-Bertomeu et al., 2009
"3PGAREARR-RXN",		# glycolysis	# 3 genes, 1 MSp, 1 GFPp	# Andriotis et al., 2010
"2PGADEHYDRAT-RXN",		# glycolysis	# 3 genes, 2 MSp, 2 GFPp, (4 GFPc)	# Andriotis et al., 2010
"PEPDEPHOS-RXN",		# glycolysis	# 13 genes, 10 MSp, 2 GFPp

"GLU6PDEHYDROG-RXN",		# OPPP	# 5 genes, 5 MSp
"6PGLUCONOLACT-RXN",		# OPPP	# 3 genes ##########
"6PGLUCONDEHYDROG-RXN",		# OPPP	# 3 genes, 4 MSp, (1 MSm, 3 MSx, 1 GFPc)
"RIB5PISOM-RXN",		# PPP	# 3 genes, 8 MSp, (2 GFPc)	# Kruger 2003
"RIBULP3EPIM-RXN",		# PPP	# 3 genes, 7 MSp	# Kruger 2003

"FUMHYDR-RXN",		# TCA cycle	# 2 genes, 6 MSm, 1 GFPm, (1 GFPc)	# Sweetlove et al., 2010

"AMYLOMALT-RXN",	# Starch degradation	# 2 genes, 3 MSp, (1 GFPc)	# Lu and Sharkey, 2004
"RXN0-5182",		# Starch degradation	# no genes # maltotetraose	# Delvalle et al., 2005

"PHOSPHOGLUCMUT-RXN",	# Sucrose synthesis + degradation	# 4 genes, 10 MSp, (1 MSm, 1 GFPc)

"F16BDEPHOS-RXN",	# gluconeogenesis	# 3 genes, 10 MSp
"RXN-2141",		# amylase	# 4 genes, 2 MSp
"MALIC-NADP-RXN",	# malic enzyme	# 6 genes, 3 MSp, (4 MSm) # Wheeler et al., 2008
"MALATE-DEH-RXN",	# Redox	# 8 genes, 9 MSm, (14 MSp, 9 MSx)
"RXN0-5224",		# carbonic anhydrase	# 11 genes, 19 MSp, 2 GFPp, (11 MSm, 2 GFPc, 1 GFPm) # Fabre et al., 2007
"CHORISMATEMUT-RXN",	# shikimate pathway	# 1 gene ##########	# Rippert 2009
"HYDROXYPYRUVATE-REDUCTASE-RXN-(NADP)",	# 2 genes, 5 MSp, 1 GFPp, (4 MSx)	# Timm et al., 2011

"PRPPSYN-RXN",	# PRPP		# 5 genes, 1 GFPc, (2 MSp)	# Krath and Hove-Jensen, 1999
"GLUTKIN-RXN",			# Proline biosynthesis	# 2 genes, 1 MSp, 2 GFPp, (2 GFPc)	# Funck et al., 2010
"GLUTSEMIALDEHYDROG-RXN",	# Proline biosynthesis	# 2 genes, 1 MSp, 2 GFPp, (2 GFPc)	# Funck et al., 2010
"PROLINE-MULTI",	# Proline biosynthesis	# no genes ##########	# Verbruggen, 2008
"SPONTPRO-RXN",		# Proline biosynthesis + degradation	# no genes ##########	# Verbruggen, 2008
"PYRROLINECARBREDUCT-RXN-(NAD)",	# Proline biosynthesis	# 1 gene ##########	# Verbruggen, 2008
"PYRROLINECARBREDUCT-RXN-(NADP)",	# Proline biosynthesis	# 1 gene ##########	# Verbruggen, 2008

"SULFATE-ADENYLYLTRANS-RXN",	# S fix	# 4 genes, 8 MSp, 1 GFPp, (1 MSm)	# Rotte and Leustek, 2000
"ACSERLY-RXN",			# S fix + Cys biosynthesis	# 9 genes, 5 MSm, (17 MSp, 2 MSx)	# Wirtz et al., 2004
"SERINE-O-ACETTRAN-RXN",	# S fix + Cys biosynthesis	# 5 genes, 3 GFPc, (1 GFPp, 1 GFPm) ##########	# Noji et al., 1998

"HOMOCYSMETB12-RXN",	# Methionine biosynthesis	# 1 gene, 1 MSp, 1 GFPp	# Wirtz and Droux, 2005

"ALANINE-AMINOTRANSFERASE-RXN",	# Alanine	# 6 genes, 8 MSm, 1 GFPx, (3 MSp, 5 MSm, 1 GFPc)	# Miyashita et al., 2007
"ASPAMINOTRANS-RXN",		# Aspartate	# 7 genes, 3 MSx, 1 GFPx, (9 MSp, 3 MSm, 1 GFPp)	# Wadsworth, 1997
"GLUTAMINESYN-RXN",		# N fix + GLN synthesis	# 6 genes, 1 MSc, 1 GFPc, (12 MSp, 1 GFPp, 1 GFPm)	# Suzuki and Knaff, 2005

"INORGPYROPHOSPHAT-RXN",	# PPiase	# 9 genes, 10 MSp, (1 MSm)	# May et al., 2011
"ADENYL-KIN-RXN",		# adenylate kinase	# 8 genes, 8 MSp, 1 GFPp, (6 MSm)	# Zrenner et al., 2006
"UMPKI-RXN",			# uridine monophosphate kinase	# 4 genes, 1 GFPc, (1 MSp)	# Zrenner et al., 2006
"CMPKI-RXN",	# uridine monophosphate kinase	# 3 genes, 1 MSc, 1 GFPc	# Zrenner et al., 2006
"CDPKIN-RXN",	# nucleoside diphosphate kinase	# 4 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"UDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"GDPKIN-RXN",	# nucleoside diphosphate kinase	# 1 gene, 5 MSp, 1 GFPp	# Zrenner et al., 2006
"DUDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"DADPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"DGDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"DCDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006
"DTDPKIN-RXN",	# nucleoside diphosphate kinase	# 5 genes, 5 MSm, 1 GFPm, (7 MSp, 1 MSx, 1 GFPc, 1 GFPp, 1 GFPx)	# Zrenner et al., 2006

"ACONITATEDEHYDR-RXN",	# glyoxylate cycle	# 4 genes, 11 MSm, (7 MSp)	# Moeder et al., 2007
"ACONITATEHYDR-RXN",	# glyoxylate cycle	# 4 genes, 11 MSm, (7 MSp)	# Moeder et al., 2007

"GLUTATHIONE-SYN-RXN",		# glutathione biosynthesis	# 1 gene ##########	# Wirtz and Droux, 2005
"GLUTATHIONE-REDUCT-NADPH-RXN",	# GSH recycling + GSH-ascorbate cycle	# 2 genes, 2 MSm, 1 GFPm, (5 MSp, 3 MSx)	# Marty et al., 2009
"RXN-3521",	# GSH-ascorbate cycle	# 3 genes, 5 MSx, 1 GFPx, (4 MSp, 1 MSm)	# Narendra et al, 2006
"RXN-3522",	# GSH-ascorbate cycle	# 10 genes, 4 MSp, (4 MSx)	# Chew et al., 2003
"RXN-3523",	# GSH-ascorbate cycle	# no genes, non-enzymatic	# Chew et al., 2003
"1.8.5.1-RXN",	# GSH-ascorbate cycle	# 4 genes, 7 MSp, 1 GFPp, (1 MSm, 1 MSx, 1 GFPc, 1 GFPx)	# Chew et al., 2003
"L-ASCORBATE-PEROXIDASE-RXN",	# GSH-ascorbate cycle	# 2 genes, (1 MSp)	# Chew et al., 2003	# redundant

"SUPEROX-DISMUT-RXN",	# SOD	# 9 genes, (2 MSx, 21 MSp, 7 MSm)	# Alscher et al., 2002

"PYRUVATEORTHOPHOSPHATE-DIKINASE-RXN",	# PPDK	# 1 gene, 5 MSp, 1 GFPp	# Parsley and Hibberd, 2006
"THIOREDOXIN-REDUCT-NADPH-RXN",	# thioredoxin reductase	# 4 genes, 5 MSp, (1 MSx)	# Serrato et al., 2004
"ISOCITDEH-RXN",	# ICDH	# 3 genes, 4 MSx, 1 GFPx, (3 MSp, 1 MSm)	# Hodges et al., 2003
"RXN66-3",		# aldehyde dehydrogenase	# 1 gene, 4 MSm, (1 MSp)	# Kirch et al., 2004
#"ACETALD-DEHYDROG-RXN",	# aldehyde dehydrogenase	# no genes	# Kirch et al., 2004
"NAD-KIN-RXN",		# NADP biosynthesis	# 3 genes, 2 MSp, 2 GFP, (1 GFPc, 1 GFPx)	# Hashida et al., 2009

"GLURS-RXN",		# Chlorophyll biosynthesis + tRNA charging	# 2 genes, 3 MSp, 2 GFPp, (2 GFPm)	# Eckhardt et al., 2004

"ADENYLYLSULFKIN-RXN",	# PAPS biosynthesis	# 4 genes	# Mugford et al., 2009

"IPPISOM-RXN",		# isoprenoid biosynthesis	# 3 genes, 2 MSc, (5 MSp, 1 GFPp, 1 GFPm)	# Laule et al., 2003
"GPPSYN-RXN",		# isoprenoid biosynthesis	# 3 genes, (2 MSc)	# Laule et al., 2003
"FPPSYN-RXN",		# isoprenoid biosynthesis	# 6 genes, 2 MSc, (3 MSp, 2 GFPp)	# Laule et al., 2003

"BRANCHED-CHAINAMINOTRANSFERLEU-RXN",	# Leucine degradation	# 7 genes, 1 MSm, 1 GFPm, (5 MSp, 3 GFPp) 	# Schuster and Binder, 2005
"BRANCHED-CHAINAMINOTRANSFERVAL-RXN",	# Valine degradation	# 5 genes, 1 MSm, 1 GFPm, (5 MSp, 3 GFPp) 	# Schuster and Binder, 2005
"BRANCHED-CHAINAMINOTRANSFERILEU-RXN",	# Isoleucine degradation	# 5 genes, 1 MSm, 1 GFPm, (5 MSp, 3 GFPp) 	# Schuster and Binder, 2005

"NADH-KINASE-RXN",	# NADH kinase	# 2 genes, 1 GFPc, (1 GFPx)	# Berrin et al., 2005

"GLYC3PDEHYDROGBIOSYN-RXN",	# glycerol-3-phosphate dehydrogenase	# 4 genes, 1 MSp, 1 GFPp	# Wei et al., 2001

"FORMATETHFLIG-RXN",		# folate transformation # 5 genes, (5 MSp)	# Hanson and Roje, 2001
"METHENYLTHFCYCLOHYDRO-RXN",	# folate transformation # no genes	# Hanson and Roje, 2001
"GLYOHMETRANS-RXN",		# folate transformation	# 7 genes, 7 MSp, 1 GFPp, (4 MSm)	# Hanson and Roje, 2001

"ACETYL-COA-ACETYLTRANSFER-RXN",	# acetyl-CoA C-acetyltransferase	# 2 genes, 1 MSc, 2 GFPc, (2 MSx)

"ATP-CITRATE-PRO-S--LYASE-RXN",	# ATP:citrate lyase	# 6 genes, 1 MSp, (4 MSm)	# Rangasamy and Ratledge, 2000

"RXN-6903",	# succinic semialdehyde reductase isoforms	# no genes	# Shelp et al.., 2012

"RXN0-5330-(NAD)",		# Alternative NADPH dehydrogenase	# 36 genes, 132 MSm, 2 GFPm, (9 MSp)
"RXN0-5330-(NADP)",		# Alternative NADPH dehydrogenase	# 36 genes, 132 MSm, 2 GFPm, (9 MSp)

#################### Cytosol only (assume other reactions are into cytosol) ####################

"GLUTDECARBOX-RXN",	# GABA synthesis	# 3 genes	# Bouche and Fromm, 2004

"IMP-DEHYDROG-RXN",	# purine biosyntheis	# 2 genes	# Zrenner et al., 2006
"GMP-SYN-GLUT-RXN",	# purine biosyntheis	# 1 gene	# Zrenner et al., 2006

"1.5.1.8-RXN",		# lysine degradation	# 1 gene	# Zhu et al., 2000
"1.5.1.9-RXN",		# lysine degradation	# 1 gene, 1 MSc	# Zhu et al., 2000
]
