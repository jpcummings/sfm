import math

# tuition from factbook and (wepage for year ending 2022 [https://www.siena.edu/offices/business-services/student-accounts/tuition-fees-room-board/])
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
		tuition = GradTuition
	elif type == "MSA":
		tuition = MSATuition
	elif type == "MBA":
		tuition = MSATuition

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

