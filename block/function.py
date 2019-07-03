from block.models import blocks



def t_count():
	file1 = open("finalcount.txt","r")
	x = file1.readline(2)
	y = int(x)
	y = y+1
	file1.close()
	file2 = open("finalcount.txt","w")
	file2.write(str(y))
	return y