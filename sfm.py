#!/usr/bin/env python

import sys, getopt
import numpy as np
import pandas as pd
import copy


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



class Cohort:
	def __init__(self, name, type, nstud, startsem, currsem, tuition, room, board, fees, aid, fracresidential, retention, facultydf):
		self._debug = False
		self._name = name
		self._type = type	# ug, grad, MSA, MBA (currently)
		self._numstudents = int(nstud)
		self._firstsemester = int(startsem)
		self._currentsemester = int(currsem)
#		self._tuition = tuition
		self._room = room
		self._board = board
		self._fees = fees
		self._aid = aid
		self._fracresidential = fracresidential 
		self._retention = retention

		self._tuition = getTuition(self.year(), self.type())

		self._meansecsize = 22  # set section size to 21 for now
		self._facultyfte = facultydf.values[0]
		self._facultymix = facultydf.values[1]
		self._facultysalary = facultydf.values[2]

#	def __repr__(self):
#		print("%s, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f %6.2f" % (self._name,self._numstudents,self._firstsemester,self._currentsemester,self._tuition,self._room, self._board, self._fees, self._aid, self._fracresidential))
#		s = ""
#		return s

	def printcohort(self):
		print("%d %s, %s, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f %6.2f %6.2f" % (self.isemester(), self._name,self._type,self._numstudents,self._firstsemester,self._currentsemester,self._tuition,self._room,self._board, self._fees, self._aid, self._fracresidential))
		# print('isemester: '+str(c.isemester()))

	def getprefix(self):
		# assumes for of name if prefix_semester
		return self._name.partition('_')[0]

	def type(self):
		return self._type

	def isgrad(self):
		if self._type == "grad":
			return True
		else:
			return False

	def nstud(self):
		return self._numstudents

	def numberresidential(self):
		return self._fracresidential*self._numstudents

	def tuition(self):
		return self._numstudents*(self._tuition)

	def fees(self):
		return self._numstudents*(self._fees)

	def financialaid(self):
		return self._numstudents*self._aid

	def revenue(self):
		return self.tuition()+self.fees()+self.room()+self.board()

	def room(self):
		room = self._numstudents*(self._room)*self._fracresidential
		return room

	def board(self):
		board = self._numstudents*(self._board)*self._fracresidential
		return board

	def isemester(self):
		fyear = self._firstsemester/100
		fsem = self._firstsemester%100
		cyear = self._currentsemester/100
		csem = self._currentsemester%100
		return (csem-fsem)/10 + 2*(cyear-fyear)

	def iyear(self):
		fyear = self._firstsemester/100
		cyear = self._currentsemester/100
		return (cyear-fyear)

	def year(self):
		return self._currentsemester/100

	def setfaculty(self, facultydf):
		# faculty df read from excel file, each colum represents a faculty "cohort": 
		# first row: fraction of FTE for this type of faculty
		# second row: fraction of total faculty of this type
		# third row: salary of this type of faculty

		self._facultymix = facultydf.values[1]
		self._facultyfte = facultydf.values[0]
		self._facultysalary = facultydf.values[2]

	def setmeansectionsize(self, size):
		self._meansecsize = size

	def facultycost(self):
		sections_per_student = 10.0
		sections_per_fte = 8.0
		f = self._facultymix
		c = 1.4*self._facultysalary/2.0  # assume benefits 0.4*salary and 1/2 year
		f_fte = self._facultyfte
		N_s = self._numstudents
		Nbar = self._meansecsize
		if self._debug:
			print "sections_per_student: ", sections_per_student
			print "sections_per_fte: ", sections_per_fte
			print "N_s: ", N_s
			print "Nbar: ", Nbar
			print "(sections_per_student/sections_per_fte)*N_s/Nbar: ", (sections_per_student/sections_per_fte)*N_s/Nbar
			print "f: ",f
			print "f_fte ", f_fte
			print "c: ", c
			print "(f*c/f_fte): ", (f*c/f_fte)
		C = (f*c/f_fte)*(sections_per_student/sections_per_fte)*N_s/Nbar
		return np.sum(C)


	# bump this group of students by a semester
	def age(self):
		cyear = self._currentsemester/100
		csem = self._currentsemester%100
		if csem == 30:
			#add 10 to semester
			csem += 10
#			print(cyear*100+csem)
			self._currentsemester = cyear*100+csem
		elif csem == 40:
			#add 1 to year and set csem to 30
			cyear += 1
			csem = 30
#			print(cyear*100+csem)
			self._currentsemester = cyear*100+csem
		else:
			print('bad semester in .age()')

		#update values
		
		self._tuition = getTuition(cyear,self._type)
		self._numstudents = self._retention[self.isemester()-1]*self._numstudents  # QQ: need to add in transfers
		self._room = 1.0275*self._room # QQ: how to model r&b increases?
		self._board = 1.0275*self._board # QQ: how to model r&b increases?
		# self._fees = fees # QQ: how to model fee increases?
		# self._aid = aid # QQ: is aid truly flat?
		# self._fracresidential = fracresidential  # QQ: does fraction of residents change?
		
		return self

# end of cohort definition

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
			2022: 10800,	# 
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
	return tuition[year]


def readcohorts(d, semester, facdfs):
	cc = []		
	for i, r in d.iterrows():
		if (d['stype'][i] == 'cohort') and (d['semester'][i] == semester) :
			retention =[d['r2'][i],d['r3'][i],d['r4'][i],d['r5'][i],d['r6'][i],d['r7'][i],d['r8'][i],d['r9'][i],d['r10'][i],d['r11'][i],d['r12'][i]]
			cc.append(Cohort(d['name'][i], d['type'][i], d['nstud'][i], d['startsem'][i], d['semester'][i], d['tuition'][i], d['room'][i], d['board'][i], d['fees'][i], d['aid'][i], d['fracresidential'][i], retention, facdfs[d['type'][i]] ))
			
	return cc


def addcohorts(cc,d,semester, facdfs):
	# we should add a test here to make sure we are starting in the fall
	# loop over data frame and find cohorts starting in *semester*
	for i, r in d.iterrows():
		if (d['stype'][i] == 'cohort') and (d['semester'][i] == semester) :
			retention =[d['r2'][i],d['r3'][i],d['r4'][i],d['r5'][i],d['r6'][i],d['r7'][i],d['r8'][i],d['r9'][i],d['r10'][i],d['r11'][i],d['r12'][i]]
			cc.append(Cohort(d['name'][i], d['type'][i], d['nstud'][i], d['startsem'][i], d['semester'][i], d['tuition'][i], d['room'][i], d['board'][i], d['fees'][i], d['aid'][i], d['fracresidential'][i], retention, facdfs[d['type'][i]] ) )
	return cc

def reset_tuition(cc):
	for c in cc:
		c.set_tuition()


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
		2023: 3153250,
		2024: 3153250,
		2025: 3153250,
	}
	return(scholarship[year])

def PTandSummer(year):
	ptandsummer = {
		2018: 2249697,
		2019: 2249697,
		2020: 2249697,
		2021: 2249697,
		2022: 2249697,
		2023: 2249697,
		2024: 2249697,
		2025: 2249697,
	}
	return(ptandsummer[year])

def PTNursing(year):
	ptnursing = {
		2018: 193725,
		2019: 193725,
		2020: 193725,
		2021: 193725,
		2022: 193725,
		2023: 0,
		2024: 0,
		2025: 0,
	}
	return(ptnursing[year])

def StudyAbroadNet(year):
	studyabroadnet = {
		2018: 1000000,
		2019: 1000000,
		2020: 1000000,
		2021: 1000000,
		2022: 1000000,
		2023: 1000000,
		2024: 1000000,
		2025: 1000000,
	}
	return(studyabroadnet[year])

#
# summary function for lists of cohorts, by type
#
def totalTuition(cc,type):
	# loop over cohorts and add tuition and fees
	tot_tui = 0
#	print(type)
	for c in cc:
		if c.type() == type:
			tot_tui+= c.tuition()
	return tot_tui

def totalFees(cc,type):
	# loop over cohorts and add tuition and fees
	tot_fees = 0
	for c in cc:
		if c.type() == type:
			tot_fees+= c.fees()
	return tot_fees

def totalAid(cc,type):
	# loop over cohorts and add aid
	tot_stud_aid = 0
	for c in cc:
		if c.type() == type:
			tot_stud_aid+= c.financialaid()
	return tot_stud_aid

def totalroom(cc,type):
	# loop over cohorts and add room and board
	tot_room = 0
	for c in cc:
		if c.type() == type:
			tot_room+= c.room()
	return tot_room

def totalboard(cc,type):
	# loop over cohorts and add room and board
	tot_board = 0
	for c in cc:
		if c.type() == type:
			tot_board+= c.board()
	return tot_board

def totalnumstudents(cc,type):
	# loop over cohorts and add students
	tot_nstud = 0
	for c in cc:
		if c.type() == type:
			tot_nstud+= c.nstud()
	return tot_nstud

def totalnumresidents(cc,type):
	# loop over cohorts and add residents
	tot_nres = 0
	for c in cc:
		if c.type() == type:
			tot_nres+= c.nres()
	return tot_nres

def totalfacultycost(cc,type="all"):
	# loop over cohorts and add facultycost
	tot_faccost = 0
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_faccost+= c.facultycost()
	return tot_faccost

def setfacdfs(cc, facdfs):
	for c in cc:
		c.setfaculty(facdfs[c.type()])
		c.setmeansectionsize(21)

def gen_spring(fall, spring,df,facdfs):
	for c in fall:
		if c.isemester() <= 10 : # dont advance 12th semester (isemester == 11)
			cc = copy.deepcopy(c)
			cc.age()
			spring.append(cc)
			csem = cc._currentsemester
	addcohorts(spring,df,csem, facdfs)
		
	
def gen_nextfall(spring, df, facdfs):
	# find the current year
	nextfall = []
	oyear = spring[0].year()
	deltayear = 1
	for c in spring:
		if c.isemester() <= 10 : # dont advance 12th semester (isemester == 11)
			cc = copy.deepcopy(c)
			cc.age()
			nextfall.append(cc)
	# add next freshman class - ex 202130
	csemester = (oyear + deltayear)*100 + 30
	addcohorts(nextfall,df,csemester, facdfs)
#	reset_tuition(nextfall)
	return(nextfall)	

                                


# display functions

def printcohorts(cc):
	cc.sort(key= lambda x: (x._firstsemester, -x._currentsemester))
	for c in cc:
		c.printcohort()
                           
def printyearlybudget(fall, spring):
	year = fall + spring
	yr = spring[0].year()
	print("")
	print("Budget summary %d-%d" % (yr-1, yr) )
	for type in ["ug", "MSA", "MBA"] :
		print("n %s fall/spr:\t %d/%d" % ( type, int(totalnumstudents(fall, type)), int(totalnumstudents(spring,type)) ) )

	netUGTuitionRev = 0.00
	print("Blended Tuition Full-time: %8.2f" % totalTuition(year,"ug"))
	netUGTuitionRev += totalTuition(year,"ug")
	print("Less:  Student Aid-Unrestricted Resources: %8.2f" % totalAid(year,"ug"))
	netUGTuitionRev -= totalAid(year,"ug")
	print("\tSupported by Endowed Scholarships: %8.2f" % endowedScholarships(yr))
	netUGTuitionRev -= endowedScholarships(yr)
	netStudentRev = netUGTuitionRev
	print("Net FT Undergraduate Tuition Revenue: %8.2f" % (netUGTuitionRev))

	print("Part-time and Summer: %8.2f" % PTandSummer(yr))
	netStudentRev +=PTandSummer(yr)
	print("Part-time Nursing Program: %8.2f" % PTNursing(yr))
	netStudentRev += PTNursing(yr)
	print("Foreign Study Abroad-Net: %8.2f" % StudyAbroadNet(yr))
	netStudentRev += StudyAbroadNet(yr)
	print("MSA Program: %8.2f" % totalTuition(year,"MSA") )
	netStudentRev += totalTuition(year,"MSA") 
	print("MBA Program: %8.2f" % totalTuition(year,"MBA") )
	netStudentRev += totalTuition(year,"MBA") 
	print("\tMBA Program aid: %8.2f" % totalAid(year,"MSA") )
	netStudentRev -= totalAid(year,"MSA")

	print("Room: %8.2f" % totalroom(year,"ug"))
	print("Board: %8.2f" % totalboard(year,"ug"))
	print("Fees: %8.2f" % totalFees(year,"ug"))
	print("Net Student Revenue: %8.2f" % (netStudentRev+totalroom(year,"ug")+totalboard(year,"ug")+totalFees(year,"ug")) )



# expense functions 

def get_f(d):
	b = d.values[1]
	return b

def get_f_fte(d):
	b = d.values[0]
	return b

def get_c(d):
	c = get_salary(d) + get_benefits(d)
	return c

def get_salary(d):
	s = d.values[2]
	return s

def get_benefits(d):
	b = d.values[2]*0.40 
	return b

def cost(f,c,f_fte,N_s,Nbar, debug=False):
	sections_per_student = 10.0
	sections_per_fte = 8.0
	if debug:
		print "sections_per_student: ", sections_per_student
		print "sections_per_fte: ", sections_per_fte
		print "N_s: ", N_s
		print "Nbar: ", Nbar
		print "(sections_per_student/sections_per_fte)*N_s/Nbar: ", (sections_per_student/sections_per_fte)*N_s/Nbar
		print "f: ",f
		print "f_fte ", f_fte
		print "c: ", c
		print "(f*c/f_fte): ", (f*c/f_fte)
	C = (f*c/f_fte)*(sections_per_student/sections_per_fte)*N_s/Nbar
	return np.sum(C)

# end expense functions



print_cohorts = False

def main(argv):
	debug = False
	global print_cohorts
	inputfile = 'input/testinput.csv'
	facinputfile = 'input/fac_dat_Schools_true_rel.xlsx'
	outputfile = ''
	excel_flag = False
	sep = "\t"
	simyear = 202130


	try:
		opts, args = getopt.getopt(argv,"hxcF:i:o:y:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'sfm.py -h -x -c -F <osep> -i <inputfile> -o <outputfile> -y <YYYYSS>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'sfm.py -h -x -c -F <osep> -i <inputfile> -o <outputfile> -y <YYYYSS>'
			sys.exit()
		elif opt in ("-x"):
			excel_flag = True
		elif opt in ("-c"):
			print_cohorts = True
		elif opt in ("-F"):
			sep = arg
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-y"):
			simyear = int(arg)

# read faculty data for expenses
	facultydf = pd.read_excel(facinputfile)

	f_fte = get_f_fte(facultydf)
	f = get_f(facultydf)
	c = get_c(facultydf)

	facdfs = {}
	facdfs["ug"] = facultydf
	facdfs["MBA"] = facultydf
	facdfs["MSA"] = facultydf

# read the student cohorts
	if excel_flag:
		df = pd.read_excel(inputfile)
	else:
		df = pd.read_csv(inputfile,skipinitialspace=True)
	fall1 = readcohorts(df, simyear, facdfs)




#do the first year

	spring1 = []
	gen_spring(fall1, spring1,df, facdfs)
	year1 = fall1 + spring1
	if print_cohorts == True :
		print("Year 1")
		printcohorts(fall1)
		printcohorts(spring1)
	printyearlybudget(fall1, spring1)

	nSpring = int(totalnumstudents(spring1,"ug"))
	nFall = int(totalnumstudents(fall1,"ug"))
	Nbar = 21
	N_s = nFall if (nFall>nSpring) else nSpring
	N_s = (nFall+nSpring)/2.0
	facultyCompensation = cost(f,c,f_fte,N_s,Nbar,debug)
	print("Faculty compensation (ug): %8.2f" % (totalfacultycost(year1,"ug")))
	print("Faculty compensation (MBA): %8.2f" % (totalfacultycost(year1,"MBA")))
	print("Faculty compensation (MSA): %8.2f" % (totalfacultycost(year1,"MSA")))
	

#
## do the next years
#

	for yr in range(3):
		fall2 = []
		spring2 = []
		fall2 = gen_nextfall(spring1,df, facdfs)
		gen_spring(fall2, spring2,df, facdfs)
		year2 = fall2 + spring2
		if print_cohorts == True :
			print("Year %d" % (2+yr))
			printcohorts(fall2)
			printcohorts(spring2)
		printyearlybudget(fall2, spring2)
		print("Faculty compensation (ug): %8.2f" % (totalfacultycost(year2,"ug")))
		print("Faculty compensation (MBA): %8.2f" % (totalfacultycost(year2,"MBA")))
		print("Faculty compensation (MSA): %8.2f" % (totalfacultycost(year2,"MSA")))
		fall1 = fall2
		spring1 = spring2



if __name__ == "__main__":
	main(sys.argv[1:])

