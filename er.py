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
	# all tuitions are per semester
	UGTuition = {
			2017:17305,	# 17305.5
			2018:17728,	# 17876.5
			2019:18338,	# 18487.5
			2020: 19027.5,	# 19177.5
			2021: 19600,	# 19748.5
			2022: 19962.5,	# 20336.5
			2023: 20472.5,	# 2.6% increase	
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
	CertificateTuition = {
			2017: 0,	# 0
			2018: 0,	# 0
			2019: 0,	# 0
			2020: 5400,	# 900/cr  (6 cr/sem for 2 sem?)
			2021: 5400,	# 900/cr
			2022: 5400,	# (assume no increases)
			2023: 5400,	# 
			2024: 5400	# 
	}

	tuition = UGTuition
	if type == "grad" :
		tuition = MBATuition
	elif type == "MSA":
		tuition = MSATuition
	elif type == "MBA":
		tuition = MBATuition
	elif type == "cert":
		tuition = CertificateTuition

	if type == "TE": # we get no tuition revenue from tuition exchange students
		return 0

	if type == "MBA":
		if year > 2022:
			return tuition[2022]  # assume no increase yearly after 2022
		else:
			return tuition[year]
	else:
		if year > 2023:
			return tuition[2023]*math.pow(1.03,(year-2023))  # assume 3% increase yearly after 2023
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
		2023: 3483500,
		2024: 3791009,
	}
	if year > 2024:
		return scholarship[2024]  # assume no increase yearly after 2022
	else:
		return(scholarship[year])

def PTandSummer(year):
	ptandsummer = {
		2018: 2249697,
		2019: 2249697,
		2020: 2249697,
		2021: 2249697,
		2022: 2249697,
		2023: 3419873,    # change to 2022-23 projected -Feb 2023 val
	}
	if year > 2023:
		return ptandsummer[2023]  # assume no increase yearly after 2022
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
		2021: 230000,
		2022: 205000,
		2023: 225000,
		2024: 223000,
	}
	if year > 2024:
		year = 2024
	return aid[year]

def ResearchGrants(year):
	grants = {
		2021: 759887,
		2022: 536326,
		2023: 763829,
		2024: 809342,
	}
	if year > 2024:
		year = 2024
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
		2022: 1625000, # adopted budget: 1760000, use projected (Apr 2022)
		2023: 1625000, # adopted budget: 1760000, use projected (Apr 2022)
		2024: 1825000, # use MJs # from Jason R. email 20230522
	}
	if year > 2024:
		year = 2024
	return fund[year]

def GiftsGrantsDesignated(year):
	fund = {
		2021: 1854116,
		2022: 1712213,
		2023: 1940575,
		2024: 1985477,
	}
	if year > 2024:
		year = 2024
	return fund[year]

def GiftsGrantsOther(year):
	return 0

def InvestmentReturns(year):
	# numbers from MJ Strunk email 4/20/2022
	ret = {
		2021: 2408057,
		2022: 2229765,
		2023: 2378168,
		2024: 2563343, # use MJs # from Jason R. email 20230522
		2025: 2858366,
		2026: 2938306,
		2027: 3013365,
	}
	if year > 2027:
		year = 2027
	return ret[year]

def EndowedGifts(year):
	# numbers from MJ Strunk email 4/20/2022
	ret = {
		2021: 4392234,
		2022: 4533300,
		2023: 5175471,
		2024: 5552809, # use MJs # from Jason R. email 20230522
		2025: 6283970,
		2026: 6466648,
		2027: 6632935,
	}
	if year > 2027:
		year = 2027
	return ret[year]

def OtherResources(year):
	ret = {
		2021: 2038385,
		2022: 1707717,
		2023: 1777212,
		2024: 2003147,
	}
	if year > 2024:
		year = 2024
	return ret[year]

def AthleticRevenue(year):
	ret = {
		2021: 0,
		2022: 1068954,  # adopted budget:1185954, use projected (Apr 2022)
		2023: 1876180,  # proposed budget
		2024: 1708163,  # proposed budget
	}
	if year > 2024:
		year = 2024
	return ret[year]

def SCRI(year):
	ret = {
		2021: 0,
		2022: 1050000,
		2023: 521667,
		2024: 1520000,  # use MJs # from Jason R. email 20230522
	}
	if year > 2024:
		year = 2024
	return ret[year]

def ReleaseTempRestrictedAssets(year):
	ret = {
		2021: 950000,
		2022: 200000,
		2023: 735000,
		2024: 742500,  # use MJs # from Jason R. email 20230522
	}
	if year > 2024:
		year = 2024
	return ret[year]


def StaffAdminSalaries(year, sp=False):
	ret = {
		2021: 23724100,
		2022: 26326046,
#		2023: 26789752,  # budget number
		2023: 27112946,  # feb 23 projection number
		2024: 28158478,  # use MJs # from Jason R. email 20230522 ($28508478 decreased by sp increase $350000, added in below)
	}
##	if year > 2023 and year < 2025:
##		ret[year] =  ret[2023]*math.pow(1.02,(year-2023))  # assume 2% increase yearly after 2022
##	elif year > 2024:
##		ret[year] = ret[2023]*math.pow(1.02,2)*math.pow(1.03,(year-2024))  # assume 2 years @ 2%, 3% increase yearly after 2024
#	if year > 2024:
#		ret[year] = ret[2024]*math.pow(1.02,1)*math.pow(1.03,(year-2025))  # assume 1 years @ 2%, 3% increase yearly after 2025
#
#	if sp and (year > 2023 and year < 2028):
#		ret[year] += 350000*(year-2023)  # readjust staff/adm salaries to reach 0.95*mid; $350/yr for 4 years => $1.4M

	if sp:
		if (year > 2023 and year < 2028):
			ret[year] = ret[2024]+350000*(year-2023)  # readjust staff/adm salaries to reach 0.95*mid; $350/yr for 4 years => $1.4M
		elif year >= 2027:
			ret[year] = (ret[2024]+1400000)*math.pow(1.03,(year-2027))
	else:
		if year > 2024:
			ret[year] = ret[2024]*math.pow(1.02,1)*math.pow(1.03,(year-2025))  # assume 1 years @ 2%, 3% increase yearly after 2025
		

	return ret[year]

def OtherSalaries(year):
	ret = {
		2021: 1047276,
		2022: 1047276,
		2023: 1073876,
	}
	if year > 2023 and year < 2025:
		return ret[2023]*math.pow(1.02,(year-2023))  # assume 2% increase yearly after 2023
	elif year > 2024:
		return ret[2023]*math.pow(1.02,2)*math.pow(1.03,(year-2024))  # assume 3% increase yearly after 2024
	else:
		return ret[year]

def DesignatedSalaries(year):
	ret = {
		2021: 609405,
		2022: 440563,
		2023: 515455,
		2024: 639977,
	}
#	if year > 2023 and year < 2025:
#		return ret[2023]*math.pow(1.02,(year-2023))  # assume 2% increase yearly after 2023
#	elif year > 2024:
#		return ret[2023]*math.pow(1.02,2)*math.pow(1.03,(year-2024))  # assume 3% increase yearly after 2024
	if year > 2024:
		return ret[2024]*math.pow(1.02,(year-2024))  # assume 2% increase yearly after 2023
	else:
		return ret[year]

def FYCCOVIDSalaries(year):
	sal = {
		2021: 0,
		2022: 461000,
		2023: 102960,
	}
	if year > 2023:
		return 0
	else:
		return sal[year]

def GeneralCollegeOperations(year):
	ret = {
		2021: 13797943,
		2022: 14511218, # adopted budget: 14508067, use projected (Apr 2022)
#		2023: 15023166, # proposed budget
		2023: 15070104, # projected feb 2023
		2024: 14849754, # use MJs budget # from Jason R. email 20230522
	}
	if year > 2024:
		return ret[2024]*math.pow(1.015,(year-2024))  # assume 1.5% increase yearly after 2022
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
		2023: 3721919,
		2024: 3845642, # use MJs budget # from Jason R. email 20230522
	}
	if year > 2024:
		year = 2024
	return exp[year]

def ProgramFYCCOVID(year):
	exp =  {
		2021: 0,
		2022: 21500,
		2023: 21500,
		2024: 21500,
		2025: 21500,
	}
	if year > 2022:  # i thought this continued 'til 2025 when the big class left(?) 
		year = 0
	else:	
		return exp[year]

def StrategicPlanInvest(year):
	exp =  {
		2021: 0,
		2022: 0,
		2023: 0,
		2024: 250000,
		2025: 500000,
		2026: 750000,
		2027: 1000000,
		2028: 1250000,
		2029: 1500000,
	}
	return exp[year]
	

def GeneralOpsMaint(year):
# numbers from MJ Strunk email 4/20/2022
# Nobel Hall online in 2025: $7*sq ft, assume 40k sq ft => 280000
# Wellness Center online in 2025: $7/sq.ft, assume 10k (too large?) => 70000
	exp = {
		2021: 1988899,
		2022: 2138899,
		2023: 2202976, # MJ initallygave 2203066, is from 2202976 from proposed budget
#		2024: 2269158, 
		2024: 2182492, # use MJs budget # from Jason R. email 20230522
		2025: 2687233, # 2337233+280000+70000
		2026: 2767850,
		2027: 2850885,
	}
	if year > 2027:
		return exp[2027]*math.pow(1.03,(year-2027))  # assume 3% increase yearly after 2027 according to MJ Strunk
	else:
		return exp[year]

def Utilities(year):
	# how much is electricity,  oil, gas(?)
	# numbers from MJ Strunk email 4/20/2022
	exp = {
		2021: 1950000,
		2022: 1950000,
#		2023: 2250000, # +300000 or 15%
		2023: 2200000, # +300000 or 15% - changed from 2250000 to 2200000 to match MJs #'s 20230508
#		2024: 2400000, # +150000 or 6%
		2024: 2200000, # use MJs budget # from Jason R. email 20230522
		2025: 2500000, # +100000 or 4%
	}
	if year > 2024:
		return exp[2025]*math.pow(1.10,(year-2025))  # assume 10% increase yearly after 2025 (wow!) according to MJ Strunk
	else:
		return exp[year]

def DeferredMaint(year):
	exp = {
		2021: 500000,
		2022: 500000,
		2023: 500000,
		2024: 450000, # use MJs budget # from Jason R. email 20230522
	}
	if year > 2024:
		year = 2024
	return exp[year]

def Food(year):
	# numbers from MJ Strunk email 4/20/2022
	ret = {
		2021: 6582271,
		2022: 8954319, # use projected (4/21/2022), the budget number was 8234610,
#		2023: 9361625,
#		2023: 8961558, # proposed budget number
		2023: 8935537, # projected feb 2023 number
		2024: 9424235, # use MJs budget # from Jason R. email 20230522
	}
	if year > 2024:
		return ret[2024]*math.pow(1.035,(year-2024))  # assume 4.5% increase yearly after 2023
	else:
		return ret[year]

def InterestExpense(year):
	exp = {
		2021: 862271,
		2022: 786159,
		2023: 707338,
		2024: 626401, # use MJs budget # from Jason R. email 20230522
	}
	if year > 2024:
		year = 2024
	return exp[year]

def AssetRetirementObligation(year):
	exp = {
		2021: 125069,
		2022: 129973,
		2023: 95073, # projection feb 2023
		2024: 139490, # use MJs budget # from Jason R. email 20230522
	}
	if year > 2024:
		year = 2024
	return exp[year]

def Depreciation(year):
	# numbers from MJ Strunk email 4/20/2022
	ret = {
		2021: 8089582,
		2022: 7891233,
		2023: 8460459,
#		2024: 8831738,
		2024: 8571537, # use MJs budget # from Jason R. email 20230522
		2025: 10904758,
		2026: 12760341,
		2027: 12056872,
	}
	if year > 2027:
		year = 2024
	return ret[year]

