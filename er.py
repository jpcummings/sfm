import math

# tuition from factbook and (webpage for year ending 2022 [https://www.siena.edu/offices/business-services/student-accounts/tuition-fees-room-board/])
# UG
# 2017
# 2018: 17728/35435 
# 2019: 18338/36675
# 2020: 19027.5/38055
# 2021: 19600/39200
# 2022: 19962.5/39925
#
# grad per credit hour - MSA
# 2018: 1181
# 2019: 1222.5
# 2020: 1268.5
# 2021: 1306
# 2022: 1330
#
# grad per credit hour - MBA
# 2018: -
# 2019: -
# 2020: 900
# 2021: 900
# 2022: 900


def getTuition(year, type):
	UGTuition = {
			2017:17305,	# 17305.5
			2018:17728,	# 17876.5
			2019:18338,	# 18487.5
			2020: 19027.5,	# 19177.5
			2021: 19600,	# 19748.5
			2022: 19962.5,	# 20336.5
			2023: 20561,	# 3% increase
			2024: 21178	# 3% increase
	}
	GradTuition = {
			2017: 17163,	# 17305.5
			2018: 17717,	# 17876.5
			2019: 18337,	# 18487.5
			2020: 19027,	# 19177.5
			2021: 19692,	# 19748.5
			2022: 20381,	# 20336.5
			2023: 21094,	# 20946.5
			2024: 21832	# 21597.0
	}
	MSATuition = {
			2018: 10629,	# 1181/cr
			2019: 10998,	# 1222/cr
			2020: 11416.5,	# 1268.5/cr (9 cr/sem for 3 sem?)
			2021: 11754,	# 1306/cr
			2022: 12106,	# (assume 3% increases)
			2023: 12470,	#
			2024: 13218	#
	}
	MBATuition = {
			2017: 0,	# 0
			2018: 0,	# 0
			2019: 0,	# 0
			2020: 10800,	# 900/cr  (12 cr/sem for 4 sem?)
			2021: 10800,	# 900/cr
			2022: 10800,	# (assume no increases)
			2023: 10800,	# 
			2024: 10800	# 
	}

	tuition = UGTuition
	if type == "grad" :
		tuition = MBATuition
	elif type == "MSA":
		tuition = MSATuition
	elif type == "MBA":
		tuition = MBATuition

	if type == "MBA":
		if year > 2022:
			return tuition[2022]  # assume no increase yearly after 2022
		else:
			return tuition[year]
	else:
		if year > 2022:
			return tuition[2022]*math.pow(1.025,(year-2022))  # assume 2.5% increase yearly after 2022
		else:
			return tuition[year]


#
# functions to return "fixed" revenues
#

def endowedScholarships(year):
	scholarship = {
		2018: 3153250,
		2019: 3153250,
		2020: 3153250,
		2021: 3153250,
		2022: 3153250,
	}
	if year > 2022:
		return scholarship[2022]  # assume no increase yearly after 2022
	else:
		return(scholarship[year])

def PTandSummer(year):
	ptandsummer = {
		2018: 2249697,
		2019: 2249697,
		2020: 2249697,
		2021: 2249697,
		2022: 2249697,
	}
	if year > 2022:
		return ptandsummer[2022]  # assume no increase yearly after 2022
	else:
		return(ptandsummer[year])

def PTNursing(year):
	ptnursing = {
		2018: 193725,
		2019: 193725,
		2020: 193725,
		2021: 193725,
		2022: 193725,
	}
	if year > 2022:
		return 0  # assume no PT nursing program after 2022
	else:
		return(ptnursing[year])


def StudyAbroadNet(year):
	studyabroadnet = {
		2018: 1000000,
		2019: 1000000,
		2020: 1000000,
		2021: 1000000,
		2022: 1000000,
	}
	if year > 2022:
		return studyabroadnet[2022]  # assume no increase yearly after 2022
	else:
		return(studyabroadnet[year])

def BundyAid(year):
	aid = {
		2021: 23000,
		2022: 20500,
	}
	if year > 2022:
		year = 2022
	return aid[year]

def ResearchGrants(year):
	grants = {
		2021: 759887,
		2022: 536326,
	}
	if year > 2022:
		year = 2022
	return grants[year]

def COVIDDiscretionary(year):
	aid = {
		2021: 3820189,
		2022: 3400000,
	}
	if year > 2022:
		ret = 0
	else:
		ret = aid[year]
	return ret

def AnnualFund(year):
	fund = {
		2021: 1725000,
		2022: 1760000,
	}
	if year > 2022:
		year = 2022
	return fund[year]

def GiftsGrantsDesignated(year):
	fund = {
		2021: 1854116,
		2022: 1712213,
	}
	if year > 2022:
		year = 2022
	return fund[year]

def GiftsGrantsOther(year):
	return 0

def InvestmentReturns(year):
	ret = {
		2021: 2408057,
		2022: 2229765,
	}
	if year > 2022:
		year = 2022
	return ret[year]

def EndowedGifts(year):
	ret = {
		2021: 4392234,
		2022: 4533300,
	}
	if year > 2022:
		year = 2022
	return ret[year]

def OtherResources(year):
	ret = {
		2021: 2038385,
		2022: 1707717,
	}
	if year > 2022:
		year = 2022
	return ret[year]

def AthleticRevenue(year):
	ret = {
		2021: 0,
		2022: 1185954,
	}
	if year > 2022:
		year = 2022
	return ret[year]

def SCRI(year):
	ret = {
		2021: 0,
		2022: 1050000,
	}
	if year > 2022:
		year = 2022
	return ret[year]

def ReleaseTempRestrictedAssets(year):
	ret = {
		2021: 950000,
		2022: 200000,
	}
	if year > 2022:
		year = 2022
	return ret[year]

def StaffAdminSalaries(year):
	ret = {
		2021: 23724100,
		2022: 26326046,
	}
	if year > 2022:
		return ret[2022]*math.pow(1.025,(year-2022))  # assume 2.5% increase yearly after 2022
	else:
		return ret[year]

def OtherSalaries(year):
	ret = {
		2021: 1047276,
		2022: 1047276,
	}
	if year > 2022:
		return ret[2022]*math.pow(1.025,(year-2022))  # assume 2.5% increase yearly after 2022
	else:
		return ret[year]

def DesignatedSalaries(year):
	ret = {
		2021: 609405,
		2022: 440563,
	}
	if year > 2022:
		return ret[2022]*math.pow(1.025,(year-2022))  # assume 2.5% increase yearly after 2022
	else:
		return ret[year]

def FYCCOVIDSalaries(year):
	sal = {
		2021: 0,
		2022: 461000,
	}
	if year > 2022:
		return 0
	else:
		return sal[year]

def GeneralCollegeOperations(year):
	ret = {
		2021: 13797943,
		2022: 14508067,
	}
	if year > 2022:
		return ret[2022]*math.pow(1.015,(year-2022))  # assume 1.5% increase yearly after 2022
	else:
		return ret[year]

def COVIDRelated(year):
	exp = {
		2021: 2104580,
		2022: 250000,
	}
	if year > 2022:
		return 0
	else:
		return exp[year]

def ProgramCostsDesignated(year):
	exp = {
		2021: 2876184,
		2022: 3141087,
	}
	if year > 2022:
		year = 2022
	return exp[year]

def ProgramFYCCOVID(year):
	exp =  {
		2021: 0,
		2022: 21500,
		2023: 21500,
		2024: 21500,
		2025: 21500,
	}
	if year > 2025:
		year = 0
	else:	
		return exp[year]

def GeneralOpsMaint(year):
# Nobel Hall online in 2025: $7*sq ft, assume 40k sq ft => 280000
# Wellness Center online in 2025: $7/sq.ft, assume 10k (too large?) => 70000
# Need to put wellness center in also
	exp = {
		2021: 1988899,
		2022: 2138899,
		2023: 2203066,
		2024: 2269158,
		2025: 2687233, # 2337233+280000+70000
		2026: 2767850,
		2027: 2850885,
	}
	if year > 2027:
		return exp[2027]*math.pow(1.03,(year-2027))  # assume 3% increase yearly after 2027 according to MJ Strunk
	else:
		return exp[year]

def Utilities(year):
	# electricity 
	exp = {
		2021: 1950000,
		2022: 1950000,
		2023: 2200000,
		2024: 2450000,
	}
	if year > 2024:
		return exp[2024]*math.pow(1.10,(year-2024))  # assume 10% increase yearly after 2024 (wow!) according to MJ Strunk
	else:
		return exp[year]

def DeferredMaint(year):
	exp = {
		2021: 500000,
		2022: 500000,
	}
	if year > 2022:
		year = 2022
	return exp[year]

def Food(year):
	ret = {
		2021: 6582271,
		2022: 8234610,
	}
	if year > 2022:
		return ret[2022]*math.pow(1.035,(year-2022))  # assume 3.5% increase yearly after 2022
	else:
		return ret[year]

def InterestExpense(year):
	exp = {
		2021: 862271,
		2022: 786159,
	}
	if year > 2022:
		year = 2022
	return exp[year]

def AssetRetirementObligation(year):
	exp = {
		2021: 125069,
		2022: 129973,
	}
	if year > 2022:
		year = 2022
	return exp[year]

def Depreciation(year):
	ret = {
		2021: 8089582,
		2022: 7891233,
	}
	if year > 2022:
		return ret[2022]*math.pow(1.05,(year-2022))  # assume 5% increase yearly after 2022
	else:
		return ret[year]

