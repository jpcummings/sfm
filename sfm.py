#!/usr/bin/env python3

import sys, getopt
import math
import numpy as np
import pandas as pd
import copy
import xlwt
import er



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
		self._oldres = -1 
		self._retention = retention

		self._tuition = er.getTuition(self.year(), self.type())

		self._meansecsize = 21  # set section size to 21 for now
		self._sections_per_student = 10.0  # set sections per student to 10.0 
		self._sections_per_fte = 8.0  # set sections per FTE to 8.0                                 
		self._facultyfte = facultydf.values[0]
		self._facultymix = facultydf.values[1]
		self._facultysalary = facultydf.values[2]

		self._sectionsneeded = int(nstud) / self._meansecsize * self._sections_per_student / 2 # Assume sections_per_student is for the full year

		# base salaries from 2020.  Assume 2.5% raises
		if self._type == 'grad':
			self._facultymix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.333, 0.333, 0.333, 0, 0, 0, 0, 0, 0]
#			print(self._facultymix)
#			print(self._facultysalary)
#			print(self._facultymix*self._facultysalary)
		year = self.year()
		if year > 2020:
			self._facultysalary *= math.pow(1.025,year-2020)




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
		fyear = int(self._firstsemester/100) 
		fsem = self._firstsemester%100
		cyear = int(self._currentsemester/100) 
		csem = self._currentsemester%100
		return int( (csem-fsem)/10 + 2*(cyear-fyear) ) 

	def iyear(self):
		fyear = int(self._firstsemester/100) 
		cyear = int(self._currentsemester/100) 
		return (cyear-fyear)

	def year(self):
		return int(self._currentsemester/100) 

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

	def sectionsneeded(self):
		self._sectionsneeded = float(self._numstudents) / self._meansecsize * self._sections_per_student / 2 # Assume sections_per_student is for the year
		return self._sectionsneeded 

	def facultysalary(self):
		sections_per_student = self._sections_per_student
		sections_per_fte = self._sections_per_fte
		f = self._facultymix
		c = self._facultysalary/2.0  # assume 1/2 year
		f_fte = self._facultyfte
		N_s = self._numstudents
		Nbar = self._meansecsize
		if self._debug:
			print ("sections_per_student: ", sections_per_student)
			print ("sections_per_fte: ", sections_per_fte)
			print ("N_s: ", N_s)
			print ("Nbar: ", Nbar)
			print ("(sections_per_student/sections_per_fte)*N_s/Nbar: ", (sections_per_student/sections_per_fte)*N_s/Nbar)
			print ("f: ",f)
			print ("f_fte ", f_fte)
			print ("c: ", c)
			print ("(f*c/f_fte): ", (f*c/f_fte))
		C = (f*c/f_fte)*(sections_per_student/sections_per_fte)*N_s/Nbar
		return np.sum(C)

	def facultycost(self):
		sections_per_student = self._sections_per_student
		sections_per_fte = self._sections_per_fte
		f = self._facultymix
		c = 1.4*self._facultysalary/2.0  # assume benefits 0.4*salary and 1/2 year
		f_fte = self._facultyfte
		N_s = self._numstudents
		Nbar = self._meansecsize
		if self._debug:
			print ("sections_per_student: ", sections_per_student)
			print ("sections_per_fte: ", sections_per_fte)
			print ("N_s: ", N_s)
			print ("Nbar: ", Nbar)
			print ("(sections_per_student/sections_per_fte)*N_s/Nbar: ", (sections_per_student/sections_per_fte)*N_s/Nbar)
			print ("f: ",f)
			print ("f_fte ", f_fte)
			print ("c: ", c)
			print ("(f*c/f_fte): ", (f*c/f_fte))
		C = (f*c/f_fte)*(sections_per_student/sections_per_fte)*N_s/Nbar
		return np.sum(C)


	# bump this group of students by a semester
	def age(self):
		cyear = int(self._currentsemester/100) 
		csem = self._currentsemester%100
		if csem == 30:
			#add 10 to semester
			csem += 10
			self._currentsemester = cyear*100+csem
		elif csem == 40:
			#add 1 to year and set csem to 30
			cyear += 1
			csem = 30
#			print(cyear*100+csem)
#			print("bumping room from {} to {}".format(self._room, 1.03*self._room))
			self._currentsemester = cyear*100+csem
			# update room and board - 2.5% increase
			self._room = 1.025*self._room # QQ: how to model r&b increases?
			self._board = 1.025*self._board # QQ: how to model r&b increases?
			self._facultysalary *= 1.025 # JPC - give faculty raises!
		else:
			print('bad semester in .age()')

		#update values
		
		self._tuition = er.getTuition(cyear,self._type)
		self._numstudents = self._retention[self.isemester()-1]*self._numstudents  # QQ: need to add in transfers
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

def cleanCohorts(cc):
	removeEmptyCohorts(cc)
#	correctResidentFrac(cc)

def removeEmptyCohorts(cc):
	for c in cc:
		if c.nstud() == 0:
			cc.remove(c)

def correctResidentFrac(sem,nresidmax):
	'''Correct resident fractions of all cohorst in a semester to avoid going over capacity'''
	# assume sem is an entire semester.
	# nresidmax = 2454   
	tot_nres = 0
	correction = 1

	if sem[0].year() == 2021:
		nresidmax = 2146   # Use 2146, projected actual in 2021

	for c in sem:
		if c._oldres >= 0:
			c._fracresidential = c._oldres
			c._oldres = -1
		tot_nres+= c.nresid()

	if (tot_nres > nresidmax):
		correction = nresidmax/tot_nres
		for c in sem:
			# print("correcting res fraction by %f" % correction)
			c._oldres = c._fracresidential 
			c._fracresidential = correction*c._fracresidential 

	return correction
	


def reset_tuition(cc):
	for c in cc:
		c.set_tuition()


#
# summary function for lists of cohorts, by type
#

def totalSections(cc,type):
	# loop over cohorts and add required sections
	tot_sec = 0
#	print(type)
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_sec+= c.sectionsneeded()
	return tot_sec


def totalTuition(cc,type):
	# loop over cohorts and add tuition and fees
	tot_tui = 0
#	print(type)
	for c in cc:
		if (type == 'all' or c.type() == type):
			if c._name.startswith('TE'): # tuition exchange students pay no tuition
				print ("found TE cohort")
			else:
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
			if c._name.startswith('TE'): # tuition exchange students pay no tuition, so they get no aid!
				print ("found TE cohort")
			else:
			#	print(c._name, c._currentsemester, c.financialaid())
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

def totalNumResidents(cc,type,nresidmax):
	# loop over cohorts and add residents
	tot_nres = 0
	correctResidentFrac(cc, nresidmax)
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_nres+= c.nresid()
	return tot_nres 


def totalNumResidentsOLD(cc,type):
	nresidmax = 9999 # 2454
	# loop over cohorts and add residents
	tot_nres = 0
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_nres+= c.nresid()
	return tot_nres if tot_nres < nresidmax else nresidmax 

def totalNetTuitionRev(cc,type="all"):
	year = cc
	yr = cc[0].year()

	if type == "ug":
		netUGTuitionRev = 0.00
		netUGTuitionRev += totalTuition(year,type)
		netUGTuitionRev -= totalAid(year,type)
		netUGTuitionRev -= er.endowedScholarships(yr)
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

def totalFacultySalary(cc,type="all"):
	# loop over cohorts and add facultycost
	tot_faccost = 0
	for c in cc:
		if (type == 'all' or c.type() == type):
			tot_faccost+= c.facultysalary()
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
		print("n %s fall/spr:\t %d/%d" % ( type, int(totalNumStudents(fall, type)), int(totalNumStudents(spring,type)) ) )

	netUGTuitionRev = 0.00
	print("Blended Tuition Full-time: %8.2f" % totalTuition(year,"ug"))
	netUGTuitionRev += totalTuition(year,"ug")
	print("Less:  Student Aid-Unrestricted Resources: %8.2f" % totalAid(year,"ug"))
	netUGTuitionRev -= totalAid(year,"ug")
	print("\tSupported by Endowed Scholarships: %8.2f" % er.endowedScholarships(yr))
	netUGTuitionRev -= er.endowedScholarships(yr)
	netStudentRev = netUGTuitionRev
	print("Net FT Undergraduate Tuition Revenue: %8.2f" % (netUGTuitionRev))

	print("Part-time and Summer: %8.2f" % er.PTandSummer(yr))
	netStudentRev += er.PTandSummer(yr)
	print("Part-time Nursing Program: %8.2f" % er.PTNursing(yr))
	netStudentRev += er.PTNursing(yr)
	print("Foreign Study Abroad-Net: %8.2f" % er.StudyAbroadNet(yr))
	netStudentRev += er.StudyAbroadNet(yr)
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


def printYear(dat, year, hdr=False):
	if hdr:
		print ('year',)
		return
	foundyear = False
	for yr in dat:
		if yr[0].year() == year:
			foundyear = True
			print ('%d ' % yr[0].year(),)
	if not foundyear:
		sys.exit("cannot find year %d to output\n" % year)


def printType(dat, year, type="all",hdr=False):
	if hdr:
		print ('nstud%s' % type,)
		print ('tuition%s' % type,)
		print ('aid%s' % type,)
		print ('room%s' % type,)
		print ('board%s' % type,)
		print ('fees%s' % type,)
		print ('netrev%s' % type,)
		print ('faccomp%s' % type,)
		return
	foundyear = False
	for yr in dat:
		if yr[0].year() == year:
			foundyear = True
			print ('%6.0f ' % totalNumStudents(yr,type),)
			print ('%6.0f ' % totalTuition(yr,type),)
			print ('%6.0f ' % totalAid(yr,type),)
			print ('%6.0f ' % totalRoom(yr,type),)
			print ('%6.0f ' % totalBoard(yr,type),)
			print ('%6.0f ' % totalFees(yr,type),)
			print ('%6.0f ' % (totalTuition(yr,type)-totalAid(yr,type)+totalRoom(yr,type)+totalBoard(yr,type)+totalFees(yr,type)),)
			print ('%6.0f ' % totalFacultyCost(yr,type),)
	if not foundyear:
		sys.exit("cannot find year %d to output\n" % year)

def printNetStudRev(dat,year,hdr=False):
	if hdr:
		print ('netstudrevenue',)
		return
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
			tot += er.PTandSummer(yr)
			tot += er.PTNursing(yr)
			tot += er.StudyAbroadNet(yr)
			tot -= er.endowedScholarships(yr)
			print ('%6.0f ' % tot,)
			
def printFacultyCost(dat, year, type="all",hdr=False):
	if hdr:
		print ('faccomp%s' % type,)
		return
	foundyear = False
	for yr in dat:
		if yr[0].year() == year:
			foundyear = True
			print ('%6.0f ' % totalFacultyCost(yr,type),)
	if not foundyear:
		sys.exit("cannot find year %d to output\n" % year)

def printAll(dat, hdr=False):
	year = 0  # dummy arg to print header
	if hdr:
		printYear(dat,year,hdr)
		printType(dat,year,"ug",hdr)
		printType(dat,year,"MSA",hdr)
		printType(dat,year,"MBA",hdr)
		printNetStudRev(dat,year,hdr)
		printFacultyCost(dat,year,"all",hdr)
		print('')
		return
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
		printFacultyCost(dat,year,"all")
		print('')
		

# output to excel
row = 0

def writeExcelNext(sheet, label, value, style, col = 1):
	global row 
	row+=1
	sheet.write(row, 0, label)
	sheet.write(row, col, value, style )

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
for i in range(10):
	sheet1.col(i).width = 17*256
sheet1.col(0).width = 60*256
currency = xlwt.XFStyle()
currency.num_format_str = '$#,##0'
integer = xlwt.XFStyle()
integer.num_format_str = '0'

def openExcel():
	global book
	global sheet1
	global currency
	global integer
	sheet1.col(0).width = 60*256
	sheet1.col(1).width = 17*256
	currency = xlwt.XFStyle()
	currency.num_format_str = '$#,##0.00'
	integer = xlwt.XFStyle()
	integer.num_format_str = '0'


def closeExcel(oname):
	global book
	book.save(oname)

	
def writeHeaderExcel(title, sp=False):
	global book
	global sheet1
	global currency
	global integer

	bold = xlwt.XFStyle()
	# font
	font = xlwt.Font()
	font.bold = True
	bold.font = font

	sheet1.write(0, 0, title, style = bold)

	row = 1
	row+=1;sheet1.write(row, 0, "Fall Full Time Undergraduate Paying Enrollment")
	row+=1;sheet1.write(row, 0, "Spring Full Time Undergraduate Paying Enrollment")
	row+=1;sheet1.write(row, 0, "Average Full Time Undergraduate Paying Enrollment")
	row+=1;sheet1.write(row, 0, "FT Tuition & Mandatory Fees - Undergraduate Students")
	row+=1;sheet1.write(row, 0, "Average MSA student Enrollment")
	row+=1;sheet1.write(row, 0, "Average MBA student Enrollment")
	row+=1;sheet1.write(row, 0, "Average Grad student Enrollment")
	row+=1;sheet1.write(row, 0, "Average Master Programs Credit Hours")
	row+=1;sheet1.write(row, 0, "Total Enrollment")
	row+=1;sheet1.write(row, 0, "Resident Students Demand")
	row+=1;sheet1.write(row, 0, "Resident Students Actual")
	row+=1;sheet1.write(row, 0, "Board Participants")
	row+=1;sheet1.write(row, 0, "Average Part Time Credit Hours")
	row+=1
	row+=1;sheet1.write(row, 0, "Operating Revenues")
	row+=1;sheet1.write(row, 0, "Tuition")
	row+=1;sheet1.write(row, 0, "Blended Tuition Full-time")
	row+=1;sheet1.write(row, 0, "Less:  Student Aid-Unrestricted Resources")
	row+=1;sheet1.write(row, 0, "                                 Supported by Endowed Scholarships")
	row+=1;sheet1.write(row, 0, "                            Net FT Undergraduate Tuition Revenue", style = bold)
	row+=1; sheet1.write(row, 0, "  Part-time & Summer")
	row+=1; sheet1.write(row, 0, "  Part-time Nursing Program")
	row+=1; sheet1.write(row, 0, "  Masters in Accounting Program")	
	row+=1; sheet1.write(row, 0, "  MBA Program")
	row+=1; sheet1.write(row, 0, "       Masters Program Financial Aid")
	row+=1; sheet1.write(row, 0, "  Grad Program tuition")
	row+=1; sheet1.write(row, 0, "  Foreign Study Abroad-Net")
	row+=1; sheet1.write(row, 0, "      Total Tuition", style = bold)
	row+=1; sheet1.write(row, 0, "Fees")
	row+=1; sheet1.write(row, 0, "Room")
	row+=1; sheet1.write(row, 0, "Board")
	row+=1; sheet1.write(row, 0, "Net Student Revenue", style = bold)
	row+=1
	row+=1; sheet1.write(row, 0, "Government Grants")
	row+=1; sheet1.write(row, 0, "  N.Y.S. Bundy Aid")
	row+=1; sheet1.write(row, 0, "  Sponsored Research & Other Government Grants")
	row+=1; sheet1.write(row, 0, "  COVID - Discretionary")
	row+=1; sheet1.write(row, 0, "Private Gifts & Grants")
	row+=1; sheet1.write(row, 0, "  Annual Fund")
	row+=1; sheet1.write(row, 0, "  Gifts & Grants Designated for Specific Purposes")
	row+=1; sheet1.write(row, 0, "  Other (e.g. unanticipated Bequests)")
	row+=1; sheet1.write(row, 0, "Investment Returns-Unrestricted Resources")
	row+=1; sheet1.write(row, 0, "                                  Supported by Endowed Gifts")
	row+=1; sheet1.write(row, 0, "Other Resources")
	row+=1; sheet1.write(row, 0, "Athletic Revenue")
	row+=1; sheet1.write(row, 0, "Siena College Research Institute")
	row+=1; sheet1.write(row, 0, "Net Release of Temporarily Restricted Net Assets")
	row+=1; sheet1.write(row, 0, "  Total Operating Revenues", style = bold)
	
	row+=1
	row+=1; sheet1.write(row, 0, "Operating Expenditures")
	row+=1; sheet1.write(row, 0, "Compensation")
	row+=1; sheet1.write(row, 0, "  Salaries- Full Time & Part Time Faculty")
	row+=1; sheet1.write(row, 0, "  Salaries- Staff & Administration")
	row+=1; sheet1.write(row, 0, "  Salaries- Other")
	row+=1; sheet1.write(row, 0, "  Salaries - Designated")
	row+=1; sheet1.write(row, 0, "  Salaries - First Year Class/COVID Effects")
	row+=1; sheet1.write(row, 0, "  Fringes - Faculty")
	row+=1; sheet1.write(row, 0, "  Fringes - Staff and Admin")
	row+=1; sheet1.write(row, 0, "  Fringes - Designated")
	row+=1; sheet1.write(row, 0, "      Total Compensation", style = bold)
	
	row+=1
	row+=1; sheet1.write(row, 0, "  General College Operations")
	row+=1; sheet1.write(row, 0, "  COVID Related")
	row+=1; sheet1.write(row, 0, "   Program Costs- Designated")
	row+=1; sheet1.write(row, 0, "  Program- First Year Class/COVID Effects")
	if sp:
		row+=1; sheet1.write(row, 0, "Strategic Plan Investments")
	row+=1; sheet1.write(row, 0, "      Total Administrative & Program Costs", style = bold)
	row+=1; sheet1.write(row, 0, "Operation of Physical Plant")
	row+=1; sheet1.write(row, 0, "General Operation & Maintenance of Plant")
	row+=1; sheet1.write(row, 0, "Utilities")
	row+=1; sheet1.write(row, 0, "Deferred/Critical Maintenance")
	row+=1; sheet1.write(row, 0, "Food")
	row+=1; sheet1.write(row, 0, "Interest Expense")
	row+=1; sheet1.write(row, 0, "Asset Retirement Obligation")
	row+=1; sheet1.write(row, 0, "Depreciation")
	row+=1; sheet1.write(row, 0, "Total Operating Expenses", style = bold)
	row+=1; 
	row+=1; sheet1.write(row, 0, "Contingency/Targeted Surplus(Deficit)", style = bold)

def writeYearExcel(fall, spring, col = 1, sp=False):
	global book
	global sheet1
	global currency
	global integer

	yr = fall + spring

	year = yr[0].year()
	sheet1.write(0, col,"%d-%d" % (year-1, year) )

	row = 1
	row+=1; sheet1.write(row, col, totalNumStudents(fall,"ug"), integer )
	row+=1; sheet1.write(row, col, totalNumStudents(spring,"ug"), integer )
	row+=1; sheet1.write(row, col, totalNumStudents(yr,"ug")/2, integer )
	row+=1; sheet1.write(row, col, er.getTuition(year, "ug")*2, currency)
	row+=1; sheet1.write(row, col, (totalNumStudents(yr,"MSA"))/2, integer )
	row+=1; sheet1.write(row, col, (totalNumStudents(yr,"MBA"))/2, integer )
	row+=1; sheet1.write(row, col, (totalNumStudents(yr,"grad"))/2, integer )
	row+=1
	row+=1; sheet1.write(row, col, (totalNumStudents(yr,"ug")+totalNumStudents(yr,"MSA")+totalNumStudents(yr,"MBA")+totalNumStudents(yr,"grad"))/2, integer )
	row+=1; sheet1.write(row, col, (totalNumResidents(fall,"ug",9999)+totalNumResidents(spring,"ug",9999))/2, integer )
	row+=1; sheet1.write(row, col, (totalNumResidents(fall,"ug",2454)+totalNumResidents(spring,"ug",2454))/2, integer )

	row+=5
	row+=1; sheet1.write(row, col, totalTuition(yr,"ug"), currency); iTuition = i2e(row,col)
	row+=1; sheet1.write(row, col, totalAid(yr,"ug"), currency); iAid = i2e(row,col)	
	row+=1; sheet1.write(row, col, er.endowedScholarships(year), currency); iEndowedScholarships = i2e(row,col) 
	row+=1; sheet1.write(row, col, xlwt.Formula('{}-{}-{}'.format(iTuition,iAid,iEndowedScholarships)), currency ); iTotUGTuition = i2e(row,col)
	
	row+=1; sheet1.write(row, col, er.PTandSummer(year), currency ); iPTandSumm = i2e(row,col)
	row+=1; sheet1.write(row, col, er.PTNursing(year), currency ); iPTNurs = i2e(row,col)
	row+=1; sheet1.write(row, col, totalTuition(yr,"MSA"), currency); iMSA = i2e(row,col)
	row+=1; sheet1.write(row, col, totalTuition(yr,"MBA"), currency); iMBA = i2e(row,col)
	row+=1; sheet1.write(row, col, totalAid(yr,"MBA"), currency); iMBAAid = i2e(row,col)
	row+=1; sheet1.write(row, col, totalTuition(yr,"grad"), currency); iGrad = i2e(row,col)
	row+=1; sheet1.write(row, col, er.StudyAbroadNet(year), currency); iAbroad = i2e(row,col)
	row+=1; sheet1.write(row, col, xlwt.Formula('{}+{}+{}+{}+{}-{}+{}+{}'.format(iTotUGTuition,iPTandSumm,iPTNurs,iMSA,iMBA,iMBAAid,iGrad,iAbroad)), currency); iTotTuition = i2e(row,col)
	row+=1; sheet1.write(row, col, totalFees(yr,"all"), currency); iFees = i2e(row,col)
	row+=1; sheet1.write(row, col, totalRoom(yr,"all"), currency); iRoom = i2e(row,col)
	row+=1; sheet1.write(row, col, totalBoard(yr,"all"), currency); iBoard = i2e(row,col)
	row+=1; sheet1.write(row, col, xlwt.Formula('{}+{}+{}+{}'.format(iTotTuition,iFees,iRoom,iBoard)), currency); iNetStudRev = i2e(row,col)
	row+=1
	row+=1; #sheet1.write(row, 0, "Government Grants")
	row+=1; sheet1.write(row, col, er.BundyAid(year), currency)
	row+=1; sheet1.write(row, col, er.ResearchGrants(year), currency)
	row+=1; sheet1.write(row, col, er.COVIDDiscretionary(year), currency)
	row+=1; #sheet1.write(row, 0, "Private Gifts & Grants")
	row+=1; sheet1.write(row, col, er.AnnualFund(year), currency)
	row+=1; sheet1.write(row, col, er.GiftsGrantsDesignated(year), currency)
	row+=1; sheet1.write(row, col, er.GiftsGrantsOther(year), currency)
	row+=1; sheet1.write(row, col, er.InvestmentReturns(year), currency)
	row+=1; sheet1.write(row, col, er.EndowedGifts(year), currency)
	row+=1; sheet1.write(row, col, er.OtherResources(year), currency)
	row+=1; sheet1.write(row, col, er.AthleticRevenue(year), currency)
	row+=1; sheet1.write(row, col, er.SCRI(year), currency)
	row+=1; sheet1.write(row, col, er.ReleaseTempRestrictedAssets(year), currency); iNetRestrAssets = i2e(row,col)
	row+=1; sheet1.write(row, col, xlwt.Formula('SUM({}:{})'.format(iNetStudRev,iNetRestrAssets)), currency ); iTotOpRev = i2e(row,col)
	
	row+=1
	row+=1; #sheet1.write(row, 0, "Operating Expenditures")
	row+=1; #sheet1.write(row, 0, "Compensation")
	row+=1; sheet1.write(row, col, totalFacultySalary(yr,"all"), currency); iFacSal = i2e(row,col)
	row+=1; sheet1.write(row, col, er.StaffAdminSalaries(year,sp), currency)
	row+=1; sheet1.write(row, col, er.OtherSalaries(year), currency)
	row+=1; sheet1.write(row, col, er.DesignatedSalaries(year), currency)
	row+=1; sheet1.write(row, col, er.FYCCOVIDSalaries(year), currency)
	row+=1; sheet1.write(row, col, 0.4*totalFacultySalary(yr,"all"), currency)
	row+=1; sheet1.write(row, col, 0.4*er.StaffAdminSalaries(year), currency)
	row+=1; iDesigFringe = i2e(row,col); # sheet1.write(row, col, 0.4*er.DesignatedSalaries(year), currency)
	row+=1; sheet1.write(row, col, xlwt.Formula('SUM({}:{})'.format(iFacSal,iDesigFringe)), currency ); iTotComp = i2e(row,col)
	
	row+=1
	row+=1; sheet1.write(row, col, er.GeneralCollegeOperations(year), currency); iGenOps = i2e(row,col)
	row+=1; sheet1.write(row, col, er.COVIDRelated(year), currency)
	row+=1; sheet1.write(row, col, er.ProgramCostsDesignated(year), currency)
	row+=1; sheet1.write(row, col, er.ProgramFYCCOVID(year), currency); iEndAdmProg = i2e(row,col)
	if sp:
		row+=1; sheet1.write(row, col, er.StrategicPlanInvest(year), currency); iEndAdmProg = i2e(row,col)
	row+=1; sheet1.write(row, col, xlwt.Formula('SUM({}:{})'.format(iGenOps,iEndAdmProg)), currency ); iTotAdmin  = i2e(row,col)
	row+=1; # sheet1.write(row, 0, "Operation of Physical Plant")
	row+=1; sheet1.write(row, col, er.GeneralOpsMaint(year), currency); iGenOpsMaint = i2e(row,col)
	row+=1; sheet1.write(row, col, er.Utilities(year), currency)
	row+=1; sheet1.write(row, col, er.DeferredMaint(year), currency)
	row+=1; sheet1.write(row, col, er.Food(year), currency)
	row+=1; sheet1.write(row, col, er.InterestExpense(year), currency)
	row+=1; sheet1.write(row, col, er.AssetRetirementObligation(year), currency)
	row+=1; sheet1.write(row, col, er.Depreciation(year), currency); iDepreciation = i2e(row,col)
	row+=1; sheet1.write(row, col, xlwt.Formula("{}+{}+SUM({}:{})".format(iTotComp,iTotAdmin,iGenOpsMaint,iDepreciation)), currency ); iTotOpExp = i2e(row,col)
	row+=1;
	row+=1; sheet1.write(row, col, xlwt.Formula("{}-{}".format(iTotOpRev,iTotOpExp)), currency )

def i2e(i, j):
	if j<26:
		col = chr(ord('@')+j+1)
	else:
		sys.exit("bad col in index2excel()")
	row = i + 1
	return ('{}{}'.format(col, row))



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
	sections_per_student = c._sections_per_student 
	sections_per_fte = c._sections_per_fte 
	if debug:
		print ("sections_per_student: ", sections_per_student)
		print ("sections_per_fte: ", sections_per_fte)
		print ("N_s: ", N_s)
		print ("Nbar: ", Nbar)
		print ("(sections_per_student/sections_per_fte)*N_s/Nbar: ", (sections_per_student/sections_per_fte)*N_s/Nbar)
		print ("f: ",f)
		print ("f_fte ", f_fte)
		print ("c: ", c)
		print ("(f*c/f_fte): ", (f*c/f_fte))
	C = (f*c/f_fte)*(sections_per_student/sections_per_fte)*N_s/Nbar
	return np.sum(C)

# end expense functions



print_cohorts = False

def main(argv):
	debug = False
	global print_cohorts
	BASENAME = 'Untitled'
	inputfile = 'input/Model000.csv'
	outputfile = 'output/Model000.xls'
	facinputfile = 'input/fac_dat_Schools_true_rel.xlsx'
	excel_flag = False
	sep = "\t"
	simyear = 202230   # startyear for simulation
	stratplan = False  # include Strategic Plan investments


	try:
		opts, args = getopt.getopt(argv,"hxscF:i:o:y:b:",["ifile=","ofile="])
	except getopt.GetoptError:
		print ('sfm.py -h -x -c -F <osep> -i <inputfile> -o <outputfile> -y <YYYYSS> -b <basename>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('sfm.py -h -x -c -F <osep> -i <inputfile> -o <outputfile> -y <YYYYSS> -b <basename>')
			sys.exit()
		elif opt in ("-x"):
			excel_flag = True
		elif opt in ("-s"):
			stratplan = True
		elif opt in ("-c"):
			print_cohorts = True
		elif opt in ("-F"):
			sep = arg
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-y"):
			simyear = int(arg)   # startyear for simulation
		elif opt in ("-b"):
			basename = arg
			inputfile = 'input/{}-in.csv'.format(basename)
			outputfile = 'output/{}-out.xls'.format(basename)

# read faculty data for expenses
	facultydf = pd.read_excel(facinputfile)
	# facultydf = facultydf.iloc[:,1:] # GLB first column contains description, not numbers; was failing when calculating benefits
	# Georges fix seems to have broken the ther calcs... all the vectors were missing the first element(!?)  fractions, salaries, ftes, etc

	f_fte = get_f_fte(facultydf)
	f = get_f(facultydf)
	c = get_c(facultydf)

	facdfs = {}
	facdfs["ug"] = facultydf
	facdfs["TE"] = facultydf
	facdfs["MBA"] = facultydf
	facdfs["MSA"] = facultydf
	facdfs["grad"] = facultydf

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
	cleanCohorts(fall)
	cleanCohorts(spring)
	springs.append(spring)
	falls.append(fall)
	yrs.append(year)
	writeHeaderExcel(basename,stratplan)
	writeYearExcel(fall,spring,1,stratplan)

	# test print of sections needed
	# print("Total sections needed for Fall: {0:8.2f}".format(totalSections(fall,'all')))
	# print("Total sections needed for Spring: {0:8.2f}".format(totalSections(spring,'all')))
	# print("")

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
		cleanCohorts(nextfall)
		cleanCohorts(nextspring)
		# test print of sections needed
		# print("Total sections needed for Fall: {0:8.2f}".format(totalSections(nextfall,'all')))
		# print("Total sections needed for Spring: {0:8.2f}".format(totalSections(nextspring,'all')))
		# print("")
		writeYearExcel(nextfall,nextspring,yr+2,stratplan)
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

#	printAll(yrs,hdr=True)
#	printAll(yrs)
	closeExcel(outputfile)
	print("done")

if __name__ == "__main__":
	main(sys.argv[1:])

