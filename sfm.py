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
	def __init__(self, name, type, nstud, startsem, currsem, tuition, room,board, sfees, aid, f_res,ret):
		self._name = name
		self._type = type	# ug, grad, MSA, MBA (currently)
		self._numStudents = int(nstud)
		self._startSemester = int(startsem)
		self._currentSemester = int(currsem)
		self._tuition = tuition
		self._room = room
		self._board = board
		self._sfees = sfees
		self._aid = aid
		self._f_res = f_res 
		self._retention = ret
		self._tuition = getTuition(self.year(), self.type())

#	def __repr__(self):
#		print("%s, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f %6.2f" % (self._name,self._numStudents,self._startSemester,self._currentSemester,self._tuition,self._room, self._board, self._sfees, self._aid, self._f_res))
#		s = ""
#		return s

	def print_c(self):
		print("%d %s, %s, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f %6.2f %6.2f" % (self.isemester(), self._name,self._type,self._numStudents,self._startSemester,self._currentSemester,self._tuition,self._room,self._board, self._sfees, self._aid, self._f_res))
		# print('isemester: '+str(c.isemester()))

	def get_prefix(self):
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
		return self._numStudents

	def numberResidential(self):
		return self._f_res*self._numStudents

	def tuition(self):
		return self._numStudents*(self._tuition)

	def fees(self):
		return self._numStudents*(self._sfees)

	def financial_aid(self):
		return self._numStudents*self._aid

	def revenue(self):
		return self.tuition()+self.fees()+self.room()+self.board()

	def room(self):
		room = self._numStudents*(self._room)*self._f_res
		return room

	def board(self):
		board = self._numStudents*(self._board)*self._f_res
		return board

	def isemester(self):
		syear = self._startSemester/100
		ssem = self._startSemester%100
		cyear = self._currentSemester/100
		csem = self._currentSemester%100
		return (csem-ssem)/10 + 2*(cyear-syear)

	def iyear(self):
		syear = self._startSemester/100
		cyear = self._currentSemester/100
		return (cyear-syear)

	def year(self):
		return self._currentSemester/100

	# bump this group of students by a semester
	def age(self):
		cyear = self._currentSemester/100
		csem = self._currentSemester%100
		if csem == 30:
			#add 10 to semester
			csem += 10
#			print(cyear*100+csem)
			self._currentSemester = cyear*100+csem
		elif csem == 40:
			#add 1 to year and set csem to 30
			cyear += 1
			csem = 30
#			print(cyear*100+csem)
			self._currentSemester = cyear*100+csem
		else:
			print('bad semester in .age()')

		#update values
		
		self._tuition = getTuition(cyear,self._type)
		self._numStudents = self._retention[self.isemester()-1]*self._numStudents  # QQ: need to add in transfers
		self._room = 1.0275*self._room # QQ: how to model r&b increases?
		self._board = 1.0275*self._board # QQ: how to model r&b increases?
		# self._sfees = sfees # QQ: how to model fee increases?
		# self._aid = aid # QQ: is aid truly flat?
		# self._f_res = f_res  # QQ: does fraction of residents change?
		
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

def read_cohorts(d, semester):
	cc = []		
	for i, r in d.iterrows():
		if (d['stype'][i] != 'comment') and (d['semester'][i] == semester) :
			ret =[d['r2'][i],d['r3'][i],d['r4'][i],d['r5'][i],d['r6'][i],d['r7'][i],d['r8'][i],d['r9'][i],d['r10'][i],d['r11'][i],d['r12'][i]]
			cc.append(Cohort(d['name'][i], d['type'][i], d['nstud'][i], d['startsem'][i], d['semester'][i], d['tuition'][i], d['room'][i], d['board'][i], d['fees'][i], d['aid'][i], d['f_res'][i], ret ))
	return cc


def add_cohorts(cc,d,semester):
	# we should add a test here to make sure we are starting in the fall
	# loop over data frame and find cohorts starting in *semester*
	for i, r in d.iterrows():
		if d['startsem'][i] == semester :
			ret =[d['r2'][i],d['r3'][i],d['r4'][i],d['r5'][i],d['r6'][i],d['r7'][i],d['r8'][i],d['r9'][i],d['r10'][i],d['r11'][i],d['r12'][i]]
			cc.append(Cohort(d['name'][i], d['type'][i], d['nstud'][i], d['startsem'][i], d['semester'][i], d['tuition'][i], d['room'][i], d['board'][i], d['fees'][i], d['aid'][i], d['f_res'][i], ret ))
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
	print(type)
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
			tot_stud_aid+= c.financial_aid()
	return tot_stud_aid

def totalRoom(cc,type):
	# loop over cohorts and add room and board
	tot_room = 0
	for c in cc:
		if c.type() == type:
			tot_room+= c.room()
	return tot_room

def totalBoard(cc,type):
	# loop over cohorts and add room and board
	tot_board = 0
	for c in cc:
		if c.type() == type:
			tot_board+= c.board()
	return tot_board

def totalNumStudents(cc,type):
	# loop over cohorts and add students
	tot_nstud = 0
	for c in cc:
		if c.type() == type:
			tot_nstud+= c.nstud()
	return tot_nstud

def totalNumResidents(cc,type):
	# loop over cohorts and add residents
	tot_nres = 0
	for c in cc:
		if c.type() == type:
			tot_nres+= c.nres()
	return tot_nres

#
#def drate(cc):
#	return tot_aid(cc)/tot_tui(cc)

def print_cohorts(cc):
	cc.sort(key= lambda x: (x._startSemester, -x._currentSemester))
	for c in cc:
		c.print_c()
		
#def print_budget(cc):
#	print('tuition:\t% 11.2f' % (tot_tui(cc)))
#	print('stud. aid:\t% 11.2f' % (tot_aid(cc)))
#	print('net trev.:\t% 11.2f'% (tot_net_trev(cc)))
#	print('fees:   \t% 11.2f'% (tot_fees(cc)))
#	print('randb:  \t% 11.2f' % (tot_randb(cc)))
#	print('net rev.:\t% 11.2f' % (tot_net_rev(cc)))
#
#
#def print_4yr_report(f1,s1,f2,s2,f3,s3,f4,s4,sep):
#	y1 = s1+f1
#	y2 = s2+f2
#	y3 = s3+f3
#	y4 = s4+f4
#	print('f nstud:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_nstud(f1),sep,tot_nstud(f2),sep,tot_nstud(f3),sep,tot_nstud(f4) ))
#	print('s nstud:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_nstud(s1),sep,tot_nstud(s2),sep,tot_nstud(s3),sep,tot_nstud(s4) ))
#	print('tuition:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_tui(y1),sep,tot_tui(y2),sep,tot_tui(y3),sep,tot_tui(y4) ))
#	print('stud. aid:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_aid(y1),sep,tot_aid(y2),sep,tot_aid(y3),sep,tot_aid(y4) ))
#	print('net trev.:%s%12.2f%s%12.2f%s%12.2f%s%12.2f'% (sep,tot_net_trev(y1),sep,tot_net_trev(y2),sep,tot_net_trev(y3),sep,tot_net_trev(y4) ))
#	print('f ngmsa:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_msa_nstud(f1),sep,tot_msa_nstud(f2),sep,tot_msa_nstud(f3),sep,tot_msa_nstud(f4) ))
#	print('s ngmsa:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_msa_nstud(s1),sep,tot_msa_nstud(s2),sep,tot_msa_nstud(s3),sep,tot_msa_nstud(s4) ))
#	print('msa tui.:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_msa_tui(y1),sep,tot_msa_tui(y2),sep,tot_msa_tui(y3),sep,tot_msa_tui(y4) ))
#	print('msa aid:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_msa_aid(y1),sep,tot_msa_aid(y2),sep,tot_msa_aid(y3),sep,tot_msa_aid(y4) ))
#	print('f ngmba:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_mba_nstud(f1),sep,tot_mba_nstud(f2),sep,tot_mba_nstud(f3),sep,tot_mba_nstud(f4) ))
#	print('s ngmba:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_mba_nstud(s1),sep,tot_mba_nstud(s2),sep,tot_mba_nstud(s3),sep,tot_mba_nstud(s4) ))
#	print('mba tui.:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_mba_tui(y1),sep,tot_mba_tui(y2),sep,tot_mba_tui(y3),sep,tot_mba_tui(y4) ))
#	print('mba aid:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_mba_aid(y1),sep,tot_mba_aid(y2),sep,tot_mba_aid(y3),sep,tot_mba_aid(y4) ))
#	print('f ngrad:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_gr_nstud(f1),sep,tot_gr_nstud(f2),sep,tot_gr_nstud(f3),sep,tot_gr_nstud(f4) ))
#	print('s ngrad:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_gr_nstud(s1),sep,tot_gr_nstud(s2),sep,tot_gr_nstud(s3),sep,tot_gr_nstud(s4) ))
#	print('gr tui.:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_gr_tui(y1),sep,tot_gr_tui(y2),sep,tot_gr_tui(y3),sep,tot_gr_tui(y4) ))
#	print('gr aid: %s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_gr_aid(y1),sep,tot_gr_aid(y2),sep,tot_gr_aid(y3),sep,tot_gr_aid(y4) ))
#	print('fees:   %s%12.2f%s%12.2f%s%12.2f%s%12.2f'% (sep,tot_fees(y1),sep,tot_fees(y2),sep,tot_fees(y3),sep,tot_fees(y4) ))
#	print('f nres: %s%12d%s%12d%s%12d%s%12d' % (sep,tot_nres(f1),sep,tot_nres(f2),sep,tot_nres(f3),sep,tot_nres(f4) ))
#	print('s nres: %s%12d%s%12d%s%12d%s%12d' % (sep,tot_nres(s1),sep,tot_nres(s2),sep,tot_nres(s3),sep,tot_nres(s4) ))
#	print('randb:  %s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_randb(y1),sep,tot_randb(y2),sep,tot_randb(y3),sep,tot_randb(y4) ))
#	print('net rev.:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_net_rev(y1),sep,tot_net_rev(y2),sep,tot_net_rev(y3),sep,tot_net_rev(y4) ))
#	print('dis. rate:%s%12.3f%s%12.3f%s%12.3f%s%12.3f' % (sep,drate(y1),sep, drate(y2),sep,drate(y3),sep,drate(y4) ) ) 
#
#
#printcohorts = False
#
#def print_report(f,s,y):
#	global printcohorts
#	print('\n')
#	if printcohorts == True :
#		print_cohorts(f)
#		print_cohorts(s)
#	print('f nstud:\t% 4d' % (tot_nstud(f)))
#	print('s nstud:\t% 4d' % (tot_nstud(s)))
#	print_budget(y)
#	print('dis. rate:\t'+str(tot_aid(y)/tot_tui(y)))

def gen_spring(fall, spring,df):
	for c in fall:
		if c.isemester() <= 10 : # dont advance 12th semester (isemester == 11)
			cc = copy.deepcopy(c)
			cc.age()
			spring.append(cc)
			csem = cc._currentSemester
	add_cohorts(spring,df,csem)
		
	
def gen_nextfall(spring, df):
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
	add_cohorts(nextfall,df,csemester)
#	reset_tuition(nextfall)
	return(nextfall)	

                                
                            
def print_yearly_budget(fall, spring):
	year = fall + spring
	yr = spring[0].year()
	print_cohorts(year)
	print("")
	print("Budget summary %d-%d" % (yr-1, yr) )
	print("n ug fall:\t %d" % int(totalNumStudents(fall,"ug")))
	print("n ug spr.:\t %d" % int(totalNumStudents(spring,"ug")))

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

	print("Room: %8.2f" % totalRoom(year,"ug"))
	print("Board: %8.2f" % totalBoard(year,"ug"))
	print("Fees: %8.2f" % totalFees(year,"ug"))
	print("Net Student Revenue: %8.2f" % (netStudentRev+totalRoom(year,"ug")+totalBoard(year,"ug")+totalFees(year,"ug")) )


printcohorts = False



def main(argv):
	global printcohorts
	inputfile = 'current.xlsx'
	outputfile = ''
	excel_flag = False
	sep = "\t"


	try:
		opts, args = getopt.getopt(argv,"hxcF:i:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'simbud.py -h -x -c -F <osep> -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'simbud.py -h -x -c -F <osep> -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-x"):
			excel_flag = True
		elif opt in ("-c"):
			print('setting printcohorts')
			printcohorts = True
			print(printcohorts)
		elif opt in ("-F"):
			sep = arg
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	simyear = int(args[0])

	if excel_flag:
		df = pd.read_excel(inputfile)
	else:
		df = pd.read_csv(inputfile,skipinitialspace=True)
	fall1 = read_cohorts(df, simyear)
#	print_cohorts(fall1)
#	print(totalTuition(fall1))
#	print(totalRoom(fall1))
#	print(totalBoard(fall1))
#	print(totalFees(fall1))
#	print(totalAid(fall1))
#	print(totalTuition(fall1)+totalRoom(fall1)+totalBoard(fall1)+totalFees(fall1)-totalAid(fall1))


#do the first year

	spring1 = []
	gen_spring(fall1, spring1,df)
	year1 = fall1 + spring1
	if printcohorts == True :
		print("Year 1")
		print_cohorts(fall1)
		print_cohorts(spring1)
	print_yearly_budget(fall1, spring1)

#
## do the next year
#
#	fall2 = []
#	spring2 = []
#	fall2 = gen_nextfall(spring1,df)
#	gen_spring(fall2, spring2,df)
#	year2 = fall2 + spring2
#	if printcohorts == True :
#		print("Year 2")
#		print_cohorts(fall2)
#		print_cohorts(spring2)
#	print_yearly_budget(fall2, spring2)

#
## do the next next year
#
#	fall3 = []
#	spring3 = []
#	fall3 = gen_nextfall(spring2,df)
#	gen_spring(fall3, spring3,df)
#	year3 = fall3 + spring3
#	if printcohorts == True :
#		print("Year 3")
#		print_cohorts(fall3)
#		print_cohorts(spring3)
#
## do the next next year
#
#	fall4 = []
#	spring4 = []
#	fall4 = gen_nextfall(spring3,df)
#	gen_spring(fall4, spring4,df)
#	year4 = fall4 + spring4
#	if printcohorts == True :
#		print("Year 4")
#		print_cohorts(fall4)
#		print_cohorts(spring4)
#
#	print_4yr_report(fall1,spring1,fall2,spring2,fall3,spring3,fall4,spring4,sep)
#
#

if __name__ == "__main__":
	main(sys.argv[1:])

