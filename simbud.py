#!/usr/bin/env python

import sys, getopt
import numpy as np
import pandas as pd
import copy

class Cohort:
	def __init__(self, name, nstud, startsem, currsem, tuition, randb, sfees, aid, f_res,ret,grad):
		self._name = name
		self._nstud = int(nstud)
		self._startsem = int(startsem)
		self._currsem = int(currsem)
		self._randb = randb
		self._sfees = sfees
		self._aid = aid
		self._f_res = f_res 
		self._retention = ret
		self._grad = int(grad)
		self._tui_yr = {  # check that these are not off by 1 - year is END of academic year
			# need a way to set the increases in the future years
			2017:17163,	# 17305.5
			2018:17717,	# 17876.5
			2019:18337,	# 18487.5
			2020: 19027,	# 19177.5
			2021: 19692,	# 19748.5
			2022: 20381,	# 20336.5
			2023: 21094,	# 20946.5
			2024: 21832	# 21597.0
		}
		self._gr_tui_yr = {  # check that these are not off by 1 - year is END of academic year
			2017:17160,  	
			2018:17715,  
			2019:18337.5, 
			2020:19027.5,  
			2021:19692,
			2022:20381,
			2023:21094,
			2024:21832
#			2017:16137,  #16068,	
#			2018:14938,  #15147,
#			2019:16975,  #15191,
#			2020:13526,  #17869,
#			2021:17869,
#			2022:17869,
#			2023:17869,
#			2024:17869
		}
		self.set_tuition()


	def __repr__(self):
		print("%s, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f %6.2f" % (self._name,self._nstud,self._startsem,self._currsem,self._tuition,self._randb, self._sfees, self._aid, self._f_res))
#		s = "%s:\n\tnstud: %s\n\tstartsem: %s\n\tcurrsem: %s\n\ttuition: %s\n\trandb: %s\n\tfees: %s\n\taid: %s\n\tf_res: %s\n" % (self._name,self._nstud,self._startsem,self._currsem,self._tuition,self._randb, self._sfees, self._aid, self._f_res)
		s = ""
		return s

	def print_c(self):
		print("%d %s, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f %6.2f" % (self.isemester(), self._name,self._nstud,self._startsem,self._currsem,self._tuition,self._randb, self._sfees, self._aid, self._f_res))
		# print('isemester: '+str(c.isemester()))


	def set_tuition(self):
		if self._grad == 1:
			self._tuition = self._gr_tui_yr[self.year()]
		else:
			self._tuition = self._tui_yr[self.year()]

	def add_transfers(self,ntrans):
		self._nstud+=ntrans

	def get_prefix(self):
		# assumes for of name if prefix_semester
		return self._name.partition('_')[0]

	def isgrad(self):
		if self._grad == 1:
			return True
		else:
			return False

	def nstud(self):
		return self._nstud

	def nres(self):
		return self._f_res*self._nstud

	def tui(self):
		return self._nstud*(self._tuition)

	def fees(self):
		return self._nstud*(self._sfees)

	def financial_aid(self):
		return self._nstud*self._aid

	def tui_fees(self):
		return self.tui()+self.fees()

	def rev(self):
		return self.tui_fees()+self.randb()

	def randb(self):
		rb = self._nstud*(self._randb)*self._f_res
#		print('c.randb(): '+str(self._nstud)+'*'+str(self._randb)+'*'+str(self._f_res)+'='+str(rb))
		return rb

	def isemester(self):
		syear = self._startsem/100
		ssem = self._startsem%100
		cyear = self._currsem/100
		csem = self._currsem%100
		return (csem-ssem)/10 + 2*(cyear-syear)

	def iyear(self):
		syear = self._startsem/100
		cyear = self._currsem/100
		return (cyear-syear)

	def year(self):
		return self._currsem/100

	def age(self):
		cyear = self._currsem/100
		csem = self._currsem%100
		if csem == 30:
			#add 10 to semester
			csem += 10
#			print(cyear*100+csem)
			self._currsem = cyear*100+csem
		elif csem == 40:
			#add 1 to year and set csem to 30
			cyear += 1
			csem = 30
#			print(cyear*100+csem)
			self._currsem = cyear*100+csem
		else:
			print('bad semester in .age()')

		#update values
		
		self._nstud = self._retention[self.isemester()-1]*self._nstud  # QQ: need to add in transfers
		self._randb = 1.0275*self._randb # QQ: how to model r&b increases?
		# self._sfees = sfees # QQ: how to model fee increases?
		# self._aid = aid # QQ: is aid truly flat?
		# self._f_res = f_res  # QQ: does fraction of residents change?
		
		return self




def read_cohorts(d, semester):
	cc = []		
	for i, r in d.iterrows():
		if (d['stype'][i] != 'comment') and (d['semester'][i] == semester) :
			ret =[d['r2'][i],d['r3'][i],d['r4'][i],d['r5'][i],d['r6'][i],d['r7'][i],d['r8'][i],d['r9'][i],d['r10'][i],d['r11'][i],d['r12'][i]]
			cc.append(Cohort(d['name'][i],d['nstud'][i],d['startsem'][i],d['semester'][i],d['tuition'][i],d['randb'][i],d['fees'][i],d['aid'][i],d['f_res'][i], ret, d['grad'][i]  ))
	return cc


def add_cohorts(cc,d,semester):
	# we should add a test here to make sure we are starting in the fall
	# loop over data frame and find cohorts starting in *semester*
	for i, r in d.iterrows():
		if d['startsem'][i] == semester :
			ret =[d['r2'][i],d['r3'][i],d['r4'][i],d['r5'][i],d['r6'][i],d['r7'][i],d['r8'][i],d['r9'][i],d['r10'][i],d['r11'][i],d['r12'][i]]
			cc.append(Cohort(d['name'][i],d['nstud'][i],d['startsem'][i],d['semester'][i],d['tuition'][i],d['randb'][i],d['fees'][i],d['aid'][i],d['f_res'][i], ret, d['grad'][i]  ))
	return cc

def reset_tuition(cc):
	for c in cc:
		c.set_tuition()

#
# summary function for undergrads 
#
def tot_tui(cc):
	# loop over cohorts and add tuition and fees
	tot_tui = 0
	for c in cc:
		if c.isgrad() == False:
			tot_tui+= c.tui()
	return tot_tui

def tot_fees(cc):
	# loop over cohorts and add tuition and fees
	tot_fees = 0
	for c in cc:
		tot_fees+= c.fees()
	return tot_fees

def tot_tui_fees(cc):
	# loop over cohorts and add tuition and fees
	tot_tui_fees = 0
	for c in cc:
		tot_tui_fees+= c.tui_fees()
	return tot_tui_fees

def tot_rev(cc):
	# loop over cohorts and add revenues
	tot_stud_rev = 0
	for c in cc:
		tot_stud_rev+= c.rev()
	return tot_stud_rev

def tot_aid(cc):
	# loop over cohorts and add aid
	tot_stud_aid = 0
	for c in cc:
		if c.isgrad() == False:
			tot_stud_aid+= c.financial_aid()
	return tot_stud_aid

def tot_net_trev(cc):
	return tot_tui(cc)-tot_aid(cc)

def tot_net_rev(cc):
	return tot_tui(cc)+tot_g_tui(cc)-tot_aid(cc)-tot_g_aid(cc)+tot_fees(cc)+tot_randb(cc) 

def tot_randb(cc):
	# loop over cohorts and add room and board
	tot_randb = 0
	for c in cc:
		tot_randb+= c.randb()
	return tot_randb

def tot_nstud(cc):
	# loop over cohorts and add students
	tot_nstud = 0
	for c in cc:
		if c.isgrad() == False:
			tot_nstud+= c.nstud()
	return tot_nstud

def tot_nres(cc):
	# loop over cohorts and add residents
	tot_nres = 0
	for c in cc:
		if c.isgrad() == False:
			tot_nres+= c.nres()
	return tot_nres

#
# summary function for grads 
#

def tot_g_tui(cc):
	# loop over cohorts and add tuition and fees
	tot_tui = 0
	for c in cc:
		if c.isgrad() == True:
			tot_tui+= c.tui()
	return tot_tui


def tot_g_aid(cc):
	# loop over cohorts and add aid
	tot_stud_aid = 0
	for c in cc:
		if c.isgrad() == True:
			tot_stud_aid+= c.financial_aid()
	return tot_stud_aid


def tot_g_nstud(cc):
	# loop over cohorts and number of students
	tot_nstud = 0
	for c in cc:
		if c.isgrad() == True:
			tot_nstud+= c.nstud()
	return tot_nstud

# msa only
	
def tot_msa_tui(cc):
	# loop over cohorts and add tuition and fees
	tot_tui = 0
	for c in cc:
		if c.isgrad() == True and c.get_prefix() == 'msa':
			tot_tui+= c.tui()
	return tot_tui


def tot_msa_aid(cc):
	# loop over cohorts and add aid
	tot_stud_aid = 0
	for c in cc:
		if c.isgrad() == True and c.get_prefix() == 'msa':
			tot_stud_aid+= c.financial_aid()
	return tot_stud_aid

def tot_msa_nstud(cc):
	# loop over cohorts and add aid
	tot_nstud = 0
	for c in cc:
		if c.isgrad() == True and c.get_prefix() == 'msa':
			tot_nstud+= c.nstud()
	return tot_nstud

#mba only
def tot_mba_tui(cc):
	# loop over cohorts and add tuition and fees
	tot_tui = 0
	for c in cc:
		if c.isgrad() == True and c.get_prefix() == 'mba':
			tot_tui+= c.tui()
	return tot_tui


def tot_mba_aid(cc):
	# loop over cohorts and add aid
	tot_stud_aid = 0
	for c in cc:
		if c.isgrad() == True and c.get_prefix() == 'mba':
			tot_stud_aid+= c.financial_aid()
	return tot_stud_aid


def tot_mba_nstud(cc):
	# loop over cohorts and add aid
	tot_nstud = 0
	for c in cc:
		if c.isgrad() == True and c.get_prefix() == 'mba':
			tot_nstud+= c.nstud()
	return tot_nstud

#
# summary function for grads other than mba or msa
#

def tot_gr_tui(cc):
	# loop over cohorts and add tuition and fees
	tot_tui = 0
	for c in cc:
		if c.isgrad() == True and c.get_prefix() == 'gr':
#			print("c tuition: "+str(c._tuition))
#			print("c nstud: "+str(c._nstud))
#			print("tui(): "+str(c.tui()))
			tot_tui+= c.tui()
	return tot_tui


def tot_gr_aid(cc):
	# loop over cohorts and add aid
	tot_stud_aid = 0
	for c in cc:
		if c.isgrad() == True and c.get_prefix() == 'gr':
			tot_stud_aid+= c.financial_aid()
	return tot_stud_aid


def tot_gr_nstud(cc):
	# loop over cohorts and add aid
	tot_nstud = 0
	for c in cc:
		if c.isgrad() == True and c.get_prefix() == 'gr':
			tot_nstud+= c.nstud()
	return tot_nstud



def drate(cc):
	return tot_aid(cc)/tot_tui(cc)

def print_cohorts(cc):
	cc.sort(key= lambda x: (x._startsem, -x._currsem))
	for c in cc:
		c.print_c()
		
def print_budget(cc):
	print('tuition:\t% 11.2f' % (tot_tui(cc)))
	print('stud. aid:\t% 11.2f' % (tot_aid(cc)))
	print('net trev.:\t% 11.2f'% (tot_net_trev(cc)))
	print('fees:   \t% 11.2f'% (tot_fees(cc)))
	print('randb:  \t% 11.2f' % (tot_randb(cc)))
	print('net rev.:\t% 11.2f' % (tot_net_rev(cc)))


def print_4yr_report(f1,s1,f2,s2,f3,s3,f4,s4,sep):
	y1 = s1+f1
	y2 = s2+f2
	y3 = s3+f3
	y4 = s4+f4
	print('f nstud:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_nstud(f1),sep,tot_nstud(f2),sep,tot_nstud(f3),sep,tot_nstud(f4) ))
	print('s nstud:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_nstud(s1),sep,tot_nstud(s2),sep,tot_nstud(s3),sep,tot_nstud(s4) ))
	print('tuition:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_tui(y1),sep,tot_tui(y2),sep,tot_tui(y3),sep,tot_tui(y4) ))
	print('stud. aid:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_aid(y1),sep,tot_aid(y2),sep,tot_aid(y3),sep,tot_aid(y4) ))
	print('net trev.:%s%12.2f%s%12.2f%s%12.2f%s%12.2f'% (sep,tot_net_trev(y1),sep,tot_net_trev(y2),sep,tot_net_trev(y3),sep,tot_net_trev(y4) ))
	print('f ngmsa:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_msa_nstud(f1),sep,tot_msa_nstud(f2),sep,tot_msa_nstud(f3),sep,tot_msa_nstud(f4) ))
	print('s ngmsa:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_msa_nstud(s1),sep,tot_msa_nstud(s2),sep,tot_msa_nstud(s3),sep,tot_msa_nstud(s4) ))
	print('msa tui.:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_msa_tui(y1),sep,tot_msa_tui(y2),sep,tot_msa_tui(y3),sep,tot_msa_tui(y4) ))
	print('msa aid:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_msa_aid(y1),sep,tot_msa_aid(y2),sep,tot_msa_aid(y3),sep,tot_msa_aid(y4) ))
	print('f ngmba:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_mba_nstud(f1),sep,tot_mba_nstud(f2),sep,tot_mba_nstud(f3),sep,tot_mba_nstud(f4) ))
	print('s ngmba:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_mba_nstud(s1),sep,tot_mba_nstud(s2),sep,tot_mba_nstud(s3),sep,tot_mba_nstud(s4) ))
	print('mba tui.:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_mba_tui(y1),sep,tot_mba_tui(y2),sep,tot_mba_tui(y3),sep,tot_mba_tui(y4) ))
	print('mba aid:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_mba_aid(y1),sep,tot_mba_aid(y2),sep,tot_mba_aid(y3),sep,tot_mba_aid(y4) ))
	print('f ngrad:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_gr_nstud(f1),sep,tot_gr_nstud(f2),sep,tot_gr_nstud(f3),sep,tot_gr_nstud(f4) ))
	print('s ngrad:%s%12d%s%12d%s%12d%s%12d' % (sep,tot_gr_nstud(s1),sep,tot_gr_nstud(s2),sep,tot_gr_nstud(s3),sep,tot_gr_nstud(s4) ))
	print('gr tui.:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_gr_tui(y1),sep,tot_gr_tui(y2),sep,tot_gr_tui(y3),sep,tot_gr_tui(y4) ))
	print('gr aid: %s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_gr_aid(y1),sep,tot_gr_aid(y2),sep,tot_gr_aid(y3),sep,tot_gr_aid(y4) ))
	print('fees:   %s%12.2f%s%12.2f%s%12.2f%s%12.2f'% (sep,tot_fees(y1),sep,tot_fees(y2),sep,tot_fees(y3),sep,tot_fees(y4) ))
	print('f nres: %s%12d%s%12d%s%12d%s%12d' % (sep,tot_nres(f1),sep,tot_nres(f2),sep,tot_nres(f3),sep,tot_nres(f4) ))
	print('s nres: %s%12d%s%12d%s%12d%s%12d' % (sep,tot_nres(s1),sep,tot_nres(s2),sep,tot_nres(s3),sep,tot_nres(s4) ))
	print('randb:  %s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_randb(y1),sep,tot_randb(y2),sep,tot_randb(y3),sep,tot_randb(y4) ))
	print('net rev.:%s%12.2f%s%12.2f%s%12.2f%s%12.2f' % (sep,tot_net_rev(y1),sep,tot_net_rev(y2),sep,tot_net_rev(y3),sep,tot_net_rev(y4) ))
	print('dis. rate:%s%12.3f%s%12.3f%s%12.3f%s%12.3f' % (sep,drate(y1),sep, drate(y2),sep,drate(y3),sep,drate(y4) ) ) 


printcohorts = False

def print_report(f,s,y):
	global printcohorts
	print('\n')
	if printcohorts == True :
		print_cohorts(f)
		print_cohorts(s)
	print('f nstud:\t% 4d' % (tot_nstud(f)))
	print('s nstud:\t% 4d' % (tot_nstud(s)))
	print_budget(y)
	print('dis. rate:\t'+str(tot_aid(y)/tot_tui(y)))

def gen_spring(fall, spring,df):
	for c in fall:
		if c.isemester() <= 10 : # dont advance 12th semester (isemester == 11)
			cc = copy.deepcopy(c)
			cc.age()
			spring.append(cc)
			csem = cc._currsem
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
	reset_tuition(nextfall)
	return(nextfall)	




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


#do the first year

	spring1 = []
	gen_spring(fall1, spring1,df)
	year1 = fall1 + spring1
	if printcohorts == True :
		print("Year 1")
		print_cohorts(fall1)
		print_cohorts(spring1)


# do the next year

	fall2 = []
	spring2 = []
	fall2 = gen_nextfall(spring1,df)
	gen_spring(fall2, spring2,df)
	year2 = fall2 + spring2
	if printcohorts == True :
		print("Year 2")
		print_cohorts(fall2)
		print_cohorts(spring2)


# do the next next year

	fall3 = []
	spring3 = []
	fall3 = gen_nextfall(spring2,df)
	gen_spring(fall3, spring3,df)
	year3 = fall3 + spring3
	if printcohorts == True :
		print("Year 3")
		print_cohorts(fall3)
		print_cohorts(spring3)

# do the next next year

	fall4 = []
	spring4 = []
	fall4 = gen_nextfall(spring3,df)
	gen_spring(fall4, spring4,df)
	year4 = fall4 + spring4
	if printcohorts == True :
		print("Year 4")
		print_cohorts(fall4)
		print_cohorts(spring4)

	print_4yr_report(fall1,spring1,fall2,spring2,fall3,spring3,fall4,spring4,sep)



if __name__ == "__main__":
	main(sys.argv[1:])

