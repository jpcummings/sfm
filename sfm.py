#!/usr/bin/env python

import sys, getopt
import numpy as np
import pandas as pd
import copy
import trb



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

		self._tuition = trb.getTuition(self.year(), self.type())

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

	def type(self):
		return self._type

	def nstud(self):
		return self._numstudents

	def nresid(self):
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

	def semester(self):   
		return self._currentsemester%100  # returns 30 for fall semester, 40 for spring, (20 for summer)

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
		
		self._tuition = trb.getTuition(cyear,self._type)
		self._numstudents = self._retention[self.isemester()-1]*self._numstudents  # QQ: need to add in transfers
		self._room = 1.0275*self._room # QQ: how to model r&b increases?
		self._board = 1.0275*self._board # QQ: how to model r&b increases?
		# self._fees = fees # QQ: how to model fee increases?
		# self._aid = aid # QQ: is aid truly flat?
		# self._fracresidential = fracresidential  # QQ: does fraction of residents change?
		
		return self

# end of cohort definition


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
# summary function for lists of cohorts, by type
#

def totalTuition(cc,type):
	# loop over cohorts and add tuition and fees
	tot_tui = 0
#	print(type)
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_tui+= c.tuition()
	return tot_tui

def totalFees(cc,type):
	# loop over cohorts and add tuition and fees
	tot_fees = 0
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_fees+= c.fees()
	return tot_fees

def totalAid(cc,type):
	# loop over cohorts and add aid
	tot_stud_aid = 0
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_stud_aid+= c.financialaid()
	return tot_stud_aid

def totalRoom(cc,type):
	# loop over cohorts and add room and board
	tot_room = 0
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_room+= c.room()
	return tot_room

def totalBoard(cc,type):
	# loop over cohorts and add room and board
	tot_board = 0
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_board+= c.board()
	return tot_board

def totalNumStudents(cc,type):
	# loop over cohorts and add students
	tot_nstud = 0
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_nstud+= c.nstud()
	return tot_nstud

def totalNumResidents(cc,type):
	# loop over cohorts and add residents
	tot_nres = 0
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_nres+= c.nres()
	return tot_nres

def totalNetTuitionRev(cc,type="all"):
	year = cc
	yr = cc[0].year()

	if type == "ug":
		netUGTuitionRev = 0.00
		netUGTuitionRev += totalTuition(year,type)
		netUGTuitionRev -= totalAid(year,type)
		netUGTuitionRev -= trb.endowedScholarships(yr)
		netTuitionRev = netUGTuitionRev
	elif type == "MBA" or type == "MSA":
		netTuitionRev  = 0.0
		netTuitionRev += totalTuition(year,type)
		netTuitionRev -= totalAid(year,type)

	return netTuitionRev
	

def totalFacultyCost(cc,type="all"):
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

def printCohorts(cc):
	cc.sort(key= lambda x: (x._firstsemester, -x._currentsemester))
	for c in cc:
		c.printcohort()
                           
def printYearlyBudget(fall, spring):
	year = fall + spring
	yr = spring[0].year()
	print("")
	print("Budget summary %d-%d" % (yr-1, yr) )
	for type in ["ug", "MSA", "MBA"] :
		print("n %s fall/spr:\t %d/%d" % ( type, int(totalnumStudents(fall, type)), int(totalnumStudents(spring,type)) ) )

	netUGTuitionRev = 0.00
	print("Blended Tuition Full-time: %8.2f" % totalTuition(year,"ug"))
	netUGTuitionRev += totalTuition(year,"ug")
	print("Less:  Student Aid-Unrestricted Resources: %8.2f" % totalAid(year,"ug"))
	netUGTuitionRev -= totalAid(year,"ug")
	print("\tSupported by Endowed Scholarships: %8.2f" % endowedScholarships(yr))
	netUGTuitionRev -= endowedScholarships(yr)
	netStudentRev = netUGTuitionRev
	print("Net FT Undergraduate Tuition Revenue: %8.2f" % (netUGTuitionRev))

	print("Part-time and Summer: %8.2f" % trb.PTandSummer(yr))
	netStudentRev +=PTandSummer(yr)
	print("Part-time Nursing Program: %8.2f" % trb.PTNursing(yr))
	netStudentRev += PTNursing(yr)
	print("Foreign Study Abroad-Net: %8.2f" % trb.StudyAbroadNet(yr))
	netStudentRev += StudyAbroadNet(yr)
	print("MSA Program: %8.2f" % totalTuition(year,"MSA") )
	netStudentRev += totalTuition(year,"MSA") 
	print("MBA Program: %8.2f" % totalTuition(year,"MBA") )
	netStudentRev += totalTuition(year,"MBA") 
	print("\tMBA Program aid: %8.2f" % totalAid(year,"MSA") )
	netStudentRev -= totalAid(year,"MSA")

	print("Room: %8.2f" % totalRoom(year,"ug"))
	print("Board: %8.2f" % totalBoard(year,"ug"))
	print("Fees: %8.2f" % totalFees(year,"ug"))
	print("Net Student Revenue: %8.2f" % (netStudentRev+totalRoom(year,"ug")+totalBoard(year,"ug")+totalFees(year,"ug")) )


def printYear(dat, year, type="all"):
	foundyear = False
	for yr in dat:
		if yr[0].year() == year:
			foundyear = True
			print '%d ' % yr[0].year(),
	if not foundyear:
		sys.exit("cannot find year %d to output\n" % year)


def printType(dat, year, type="all"):
	foundyear = False
	for yr in dat:
		if yr[0].year() == year:
			foundyear = True
			print '%6.0f ' % totalNumStudents(yr,type),
			print '%6.0f ' % totalTuition(yr,type),
			print '%6.0f ' % totalAid(yr,type),
			print '%6.0f ' % totalRoom(yr,type),
			print '%6.0f ' % totalBoard(yr,type),
			print '%6.0f ' % totalFees(yr,type),
	if not foundyear:
		sys.exit("cannot find year %d to output\n" % year)

def printNetStudRev(dat,year):
	# print (tuition - aid  + room + board + fees) (ug and grad) + ptand summer + pt nursing + study abroad  - endowed scholarships
	foundyear = False
	for yr in dat:
		if yr[0].year() == year:
			foundyear = True
			tot = totalTuition(yr,"all")
			tot -= totalAid(yr,"all")
			tot += totalRoom(yr,"all")
			tot += totalBoard(yr,"all")
			tot += totalFees(yr,"all")
			tot += trb.PTandSummer(yr)
			tot += trb.PTNursing(yr)
			tot += trb.StudyAbroadNet(yr)
			tot -= trb.endowedScholarships(yr)
			print '%6.0f ' % tot,
			
def printFacultyCost(dat, year, type="all"):
	foundyear = False
	for yr in dat:
		if yr[0].year() == year:
			foundyear = True
			print '%6.0f ' % totalFacultyCost(yr,type),
	if not foundyear:
		sys.exit("cannot find year %d to output\n" % year)

def printAll(dat):
	years = []
	for yr in dat:
		if years.count(yr[0].year()) == 0:
			years.append(yr[0].year())
	for year in years:
		printYear(dat,year)
		printType(dat,year,"ug")
		printType(dat,year,"MSA")
		printType(dat,year,"MBA")
		printNetStudRev(dat,year)
		printFacultyCost(dat,year)
		print('')



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
	fall = readcohorts(df, simyear, facdfs)


	# collect the data
	springs = []
	falls = []
	yrs = []

#do the first year

	spring = []
	gen_spring(fall, spring,df, facdfs)
	year = fall + spring
	springs.append(spring)
	falls.append(fall)
	yrs.append(year)

	if print_cohorts == True :
		print("Year 1")
		printCohorts(fall)
		printCohorts(spring)
		printYearlyBudget(fall, spring)

		print("Faculty compensation (ug): %8.2f" % (totalFacultyCost(year,"ug")))
		print("Faculty compensation (MBA): %8.2f" % (totalFacultyCost(year,"MBA")))
		print("Faculty compensation (MSA): %8.2f" % (totalFacultyCost(year,"MSA")))
	

#
## do the next years
#

	for yr in range(5):
		nextfall = []
		nextspring = []
		nextfall = gen_nextfall(spring,df, facdfs)
		gen_spring(nextfall, nextspring,df, facdfs)
		nextyear = nextfall + nextspring
		if print_cohorts == True :
			print("Year %d" % (2+yr))
			printCohorts(nextfall)
			printCohorts(nextspring)
			printYearlyBudget(nextfall, nextspring)
			print("Faculty compensation (ug): %8.2f" % (totalFacultyCost(nextyear,"ug")))
			print("Faculty compensation (MBA): %8.2f" % (totalFacultyCost(nextyear,"MBA")))
			print("Faculty compensation (MSA): %8.2f" % (totalFacultyCost(nextyear,"MSA")))
#		fall = nextfall
		spring = nextspring
		yrs.append(nextyear)

	printAll(yrs)

if __name__ == "__main__":
	main(sys.argv[1:])

