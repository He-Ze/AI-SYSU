import time
chessboard = []
minlevel = 99999
CurDom = []
assigned =[]
rows = []
rowe = []
cols = []
cole = []
rowl = []
coll = []
path = []
blank = 0
def print_chessboard():
	for row in chessboard:
		print row

def ConfirmCandidate(board,row,col):
	candidate = []
	collimit = 0
	rowlimit = 0
	for i in range(9):
		candidate.append(i+1)
	colstart = col
	while(colstart>=0):
		if(len(board[row][colstart])>=2):
			break
		colstart -= 1

	colend = col
	while(colend<len(board[0])):
		if(len(board[row][colend])>=2):
			break
		colend += 1

	rowstart = row
	while(rowstart>=0):
		if(len(board[rowstart][col])>=2):
			break
		rowstart -= 1

	rowend = row
	while(rowend<len(board)):
		if(len(board[rowend][col])>=2):
			break
		rowend +=1
	sumc = 0
	sumr = 0
	rows[row][col] = rowstart
	rowe[row][col] = rowend
	cols[row][col] = colstart
	cole[row][col] = colend
#	print board[rowstart][col]
#	print board[row][colstart]
	if rowstart != -1:
		if board[rowstart][col] != '--':
			if board[rowstart][col][:2] != '--':
				rowlimit = int(board[rowstart][col][:2])
	if colstart !=-1:
		if board[row][colstart]!='--':
			if board[row][colstart][3:] != '--':
				collimit = int(board[row][colstart][3:])

#	print 'rowlimit' + str(rowlimit)
#	print 'collimit' + str(collimit)
	rowl[row][col] = rowlimit
	coll[row][col] = collimit
	

	for c in range(colstart+1,colend):
		if c != col:
			if board[row][c] != '':
				sumc += int(board[row][c])
				i = 0
				while i < len(candidate):
					if candidate[i] == int(board[row][c]):
						candidate[i] = 0
	for r in range(rowstart+1,rowend):
		if r != row:
			if board[r][col] != '':
				sumr +=  int(board[r][col])
				i = 0
				while i < len(candidate):
					if candidate[i] == int(board[r][col]):
						candidate[i] = 0
				
	i = 0
	while i < len(candidate):
		if candidate[i] + sumr > rowlimit:
			candidate[i] = 0
		if candidate[i] + sumc > collimit:
			candidate[i] = 0
		i += 1

	for can in candidate:
		if can != 0:
			CurDom[row][col].append(can)

	#for r in range(rowstart+1,rowend):

def Initialization(height,width):
	global blank,chessboard
	for i in range(height):
		chessboard.append([])
		CurDom.append([])
		assigned.append([])
		rows.append([])
		rowe.append([])
		cols.append([])
		cole.append([])
		rowl.append([])
		coll.append([])
		for j in range(width):
			chessboard[i].append('')
			assigned[i].append(0)
			CurDom[i].append([])
			rows[i].append(0)
			rowe[i].append(0)
			cols[i].append(0)
			cole[i].append(0)
			rowl[i].append(0)
			coll[i].append(0)
	choose = raw_input("Whether to use the default chessboard?(Y/N)")
	if choose == 'Y' or choose == 'y':
		if(height == 4 and width == 4):
			chessboard[0][0] = '--'
			chessboard[0][1] = '23|--'
			chessboard[0][2] = '21|--'
			chessboard[0][3] = '07|--'
			chessboard[1][0] = '--|20'
			chessboard[2][0] = '--|19'
			chessboard[3][0] = '--|12'

		elif height == 5 and width == 5:
			chessboard[0][0] = '--'
			chessboard[0][1] = '16|--'
			chessboard[0][2] = '07|--'
			chessboard[0][3] = '--'
			chessboard[0][4] = '--'
			chessboard[1][0] = '--|09'
			chessboard[1][3] = '24|--'
			chessboard[1][4] = '--'
			chessboard[2][0] = '--|20'
			chessboard[2][4] = '04|--'
			chessboard[3][0] = '--'
			chessboard[3][1] = '--|12'
			chessboard[4][0] = '--'
			chessboard[4][1] = '--'
			chessboard[4][2] = '--|10'

		elif height == 9 and width == 8:
			chessboard[0] = ['--','16|--','06|--','--','--','08|--','29|--','--']
			chessboard[1] = ['--|13','','','15|--','16|13','','','--']
			chessboard[2] = ['--|28','','','','','','','11|--']
			chessboard[3] = ['--','--','30|15','','','--|03','','']
			chessboard[4] = ['--','16|8','','','--','22|14','','']
			chessboard[5] = ['--|14','','','--','09|17','','','--']
			chessboard[6] = ['--|13','','','05|10','','','12|--','08|--']
			chessboard[7] = ['--','--|32','','','','','','']
			chessboard[8] = ['--','--|11','','','--','--|12','','']
		elif height ==  13 and width == 13:
			chessboard = [
			['--','16|--','07|--','--','16|--','17|--','--','--','10|--','16|--','--','--','--'],
			['--|09','','','--|10','','','03|--','--|09','','','--','--','--'],
			['--|10','','','16|12','','','','03|10','','','--','--','--'],
			['--','--|17','','','','--|06','','','','16|--','--','--','--'],
			['--','--','--|12','','','17|--','06|14','','','','06|--','--','--'],
			['--','--','03|--','06|13','','','','07|--','--|10','','','16|--','--'],
			['--','--|04','','','--|14','','','','16|--','--|10','','','--'],
			['--','--|03','','','16|--','--|12','','','','35|09','','','--'],
			['--','--','--|09','','','10|--','17|19','','','','16|--','--','--'],
			['--','--','--','--|21','','','','16|--','--|14','','','24|--','--'],
			['--','--','--','--','16|17','','','','04|24','','','','03|--'],
			['--','--','--','--|10','','','--|19','','','','--|11','',''],
			['--','--','--','--|11','','','--','--|07','','','--|08','','']
			]
		elif height == 15 and width == 15:
			chessboard = [
			['--','--','--','35|--','17|--','06|--','--','17|--','06|--','--','16|--','06|--','--','--','--'],
			['--','--','--|15','','','','--|12','','','28|09','','','--','--','--'],
			['--','--','04|18','','','','16|26','','','','','','04|--','--','--'],
			['--','--|09','','','--|10','','','04|04','','','03|04','','','39|--','--'],
			['--','--|12','','','16|--','--|12','','','17|05','','','--|09','','','03|--'],
			['--','04|--','22|12','','','24|--','--|19','','','','','--','16|05','',''],
			['--|10','','','--|17','','','41|--','--|10','','','23|--','--|18','','',''],
			['--|04','','','17|--','--|09','','','--','--|07','','','--|14','','','16|--'],
			['--','04|13','','','--|17','','','04|--','--|14','','','03|--','--|16','',''],
			['--|13','','','','--','17|05','','','16|--','--|09','','','16|15','',''],
			['--|03','','','16|--','--|25','','','','','03|--','--|06','','','16|--','--'],
			['--','--|11','','','24|15','','','07|11','','','06|--','--|10','','','--'],
			['--','--','--|16','','','04|09','','','16|03','','','16|11','','','--'],
			['--','--','--','--|27','','','','','','--|13','','','','--','--'],
			['--','--','--','--|12','','','--|10','','','--|14','','','','--','--']

			]
		else:
			print 'This height and width has not initial board'

	else:
		temp_chessboard = []
		for row in chessboard:

			t  = []
			for item in row:
				item = raw_input()
				t.append(item)
			temp_chessboard.append(t)
		chessboard = temp_chessboard
	print_chessboard()
	print "\n"
	for i in range(height):
		for j in range(width):
			#print i,j
			if len(chessboard[i][j])<2:
				blank += 1
			#	print i , j
				ConfirmCandidate(chessboard[:],i,j)
			else:
				assigned[i][j] = 1	

def delect_d(row,col,d):
	deleted_list = []
	for i in range(int(height)):
		deleted_list.append([])
		for j in range(int(width)):
			deleted_list[i].append([])
	sumr = 0
	sumc = 0
	for i in range(rows[row][col]+1,rowe[row][col]):
		if assigned[i][col] != 0:
			sumr += assigned[i][col]
		else:
			if d in CurDom[i][col]:
				if assigned[i][col] == False:
					CurDom[i][col].remove(d)
					deleted_list[i][col].append(d)
	for i in range(cols[row][col]+1,cole[row][col]):
		if assigned[row][i] !=0:
			sumc += assigned[row][i]
		else:
			if d in CurDom[row][i]:
				if assigned[row][i] == False:
					CurDom[row][i].remove(d)
					deleted_list[row][i].append(d)
	for i in range(rows[row][col]+1,rowe[row][col]):
		if assigned[i][col] == 0:
			tempc = CurDom[i][col]
			for cur in CurDom[i][col]:
				if sumr + cur > rowl[i][col]:
					deleted_list[i][col].append(cur)
					tempc.remove(cur)
			CurDom[i][col] = tempc
	for i in range(cols[row][col]+1,cole[row][col]):
		if assigned[row][i] == 0:
			tempc = CurDom[row][i]
			for cur in CurDom[row][i]:
				if sumc + cur > coll[row][i]:
					deleted_list[row][i].append(cur)
					tempc.remove(cur)
			CurDom[row][i] = tempc
	return deleted_list

def getVariable():
	min = 9
	row = len(chessboard)-1
	col = len(chessboard[0])-1
	i = 0
	while i < len(chessboard):
		j = 0
		while j< len(chessboard[0]):
			#print assigned[i][j],CurDom[i][j]
			if (assigned[i][j] == False and len(CurDom[i][j])<min):
				min = len(CurDom[i][j])
				row = i
				col = j
			j += 1
		i += 1
	return (row,col)

def GAC_Enforce():
	i =0
	while i<len(chessboard):
		j = 0
		while j <len(chessboard[0]):
			if assigned[i][j]==False and len(CurDom[i][j]) == 0:
				return False
			j+=1
		i+=1
	for i in range(len(rows)):
		for j in range (len(rows[i])):
			if rows != 0 and rowe != 0 and cols != 0 and cole != 0:
				flagr = True
				sumr = 0
				for r in range(rows[i][j]+1,rowe[i][j]):
					if assigned[r][j] == 0:
						flagr = False
					else:
						sumr += assigned[r][j]
				if flagr:
					if sumr	!= rowl[i][j]:
						return False

				flagc = True
				sumc = 0
				for c in range(cols[i][j]+1,cole[i][j]):
					if assigned[i][c] == 0:
						flagc = False
					else:
						sumc+= assigned[i][c]
				if flagc:
					if sumc	!= coll[i][j]:
						return False

	return True

def GAC(level):
	#print level
	global minlevel
	#if level < minlevel:
	#	minlevel = level
	#	print minlevel
	if level == 0:
		return True
	row,col = getVariable()
	c = len(CurDom[row][col])
	for i in range(c):
		CurDom[row][col].sort()
		#print CurDom[row][col]
		d = CurDom[row][col][i]
		assigned[row][col] = d
		temp_delete = delect_d(row,col,d) 
		path.append([row,col,d])
		#print 'path'
		#print path
		#if level == 50:
		#	print path
		if GAC_Enforce() == True:
			if GAC(level - 1):
				return True
		for i in range(int(height)):
			for j in range(int(width)):
				if temp_delete[i][j]!=[]:
					for d in temp_delete[i][j]:
						CurDom[i][j].append(d)
		#print row,col,assigned[row][col]
		assigned[row][col] = 0
		path.pop()
	#print 'out'
	return False

def slove():
	GAC(blank)
	for i in range(len(path)):
		chessboard[path[i][0]][path[i][1]] = path[i][2]
	print_chessboard()


height = raw_input('height of chessboard:')
width = raw_input('width of chessboard:')
Initialization(int(height),int(width))
time_start = time.time()
#print CurDom
slove()
time_end = time.time()
print 'cost_time:' + str(time_end - time_start)

#def GAC(level):

raw_input('print enter to close')