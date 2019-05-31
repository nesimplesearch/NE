import numpy as np
import os
from utils import matrix as M
from itertools import combinations
from utils import lp
import time
import signal

s1 = 0
s2 = 0

def readsol(filename):
	with open(filename) as f:
		# read row and column
		l = f.readline()
		l = l.split(' ')
		row = int(l[0])
		col = int(l[1])
		#print("row =", row, "col =", col)
		# solve matrix data
		lines = f.readlines()
		A = np.zeros((row*2, col), dtype=float)
		A_row = 0
		for line in lines:
			_list = line.strip('\n').split(' ')
			A[A_row:] = _list[0:col]
			A_row += 1
		#print(A)
		#build matrix
		game = M.Matrix(row, col, A)
		#print("readsol finished")
		return game


def solve(x1, x2, G):
	r = [i for i in range(G.row)]
	c = [j for j in range(G.col)]
	# print("x1=",x1, x2)
	for x in combinations(r, x1):
		S1 = np.array(x, dtype = int)
		A2 = G.dominate_col(S1, c)
		#print(x, S1)
		#print(S1, A2)
		if G.rdom(S1, A2):
			for y in combinations(A2, x2):
				S2 = np.array(y, dtype = int)
				if G.rdom(S1, S2):					
					if lp.solveLP(G.A, G.B, S1, S2, G.row, G.col):
						global s1
						global s2
						s1 = len(S1)
						s2 = len(S2)
						#print("solution = ", S1, S2)
						return True
	return False

def handler(signum, frame):
	raise Exception("timeout")

def solveTD(t, d):
	if (d+t)%2 == 0:
		x1 = int((d+t)/2)
		x2 = d-x1
		if x1 > 0 and x2 > 0:
			if x1 <= gameMatrix.row and x2 <= gameMatrix.col:
				if solve(x1, x2, gameMatrix):
					return True
					
			if x1 != x2 and x2 <= gameMatrix.row and x1 <= gameMatrix.col:
				if solve(x2, x1, gameMatrix):
					return True
	return False

def rand_per(n, m):
	return np.random.rand(n,m)
	I = np.eye(n)
	p = np.random.permutation(np.arange(n))
	return I[p]

def pure(gameMatrix):
	col_max = np.max(gameMatrix.A, axis = 0)
	row_max = np.max(gameMatrix.B, axis = 1)
	#print(col_max)
	#print(row_max)
	for i in range(	gameMatrix.row ):
		for j in range (gameMatrix.col)  :
			if gameMatrix.A[i][j] == col_max[j] and gameMatrix.B[i][j] == row_max[i]:
				print("best pure:", i,  " ", j)
				global s1
				global s2
				s1 = 1
				s2 = 1
				return True
	return False
	
def Game(gameMatrix):
	eps = 1e-3
	#gameMatrix.A = gameMatrix.A + rand_per(gameMatrix.row, gameMatrix.col) * eps
	#gameMatrix.B = gameMatrix.B + rand_per(gameMatrix.row, gameMatrix.col) * eps
	#print(gameMatrix.A)
	if pure(gameMatrix):
		return "pure"
	#if solveTD(0, gameMatrix.row+gameMatrix.col):
		#return True
	# check for pure
	
	for t in range(gameMatrix.row+1):
		for d in range(3, 2*gameMatrix.row+1):
		# |x1-x2|=t, x1+x2=d, assume x1 > x2 and swap
			if solveTD(t,d):
				return True
			continue
			if (d+t)%2 == 0:
				x1 = int((d+t)/2)
				x2 = d-x1
				if x1 > 0 and x2 > 0:
					if x1 <= gameMatrix.row and x2 <= gameMatrix.col:
						if solve(x1, x2, gameMatrix):
							return True
							
					if x1 != x2 and x2 <= gameMatrix.row and x1 <= gameMatrix.col:
						if solve(x2, x1, gameMatrix):
							return True
	return False
# Main	
filedir = './gamut_game/'
filelist = os.listdir(filedir)
print(filelist)

cnt = 0
tot = 0
cnt_pure = 0
file = open("outdata.csv","w")
for name in filelist:
	tot = tot + 1
	gameMatrix = readsol(filedir+name)
	print(name)
	try:
		#signal.signal(signal.SIGALRM, handler)
		#signal.alarm(60)
		start_time = time.time()
		flag = Game(gameMatrix)
		end_time = time.time()
		if flag == False:
			print("why not found!?!")
		if  flag == "pure":
			cnt_pure = cnt_pure+1
		cnt = cnt + 1
		print(str(cnt) + "/ " + str(tot))
		print(str(cnt_pure) + "/ " + str(tot))
		print("exec time: ", end_time-start_time,  "s")
		file.write('{},{},{},{},{},{}\n'.format(name, flag, end_time-start_time, flag=="pure", s1, s2))
		print(name, flag, end_time-start_time, flag=="pure", s1, s2)
	except :
		file.write('{},{},{},{},{},{}\n'.format(name, 0, 100, -1, 20, 20))
		print("time out")
	finally:
		signal.alarm(0)
		
file.close()
print(str(cnt) + "/ " + str(tot))
print(cnt/tot)
print("\n")
