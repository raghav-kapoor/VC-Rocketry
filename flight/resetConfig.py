def resetConf():
	# read a list of lines into data
	with open(path, 'r') as file:
		lines = file.readlines()

	# change values back to defaults

	lines[12] = "1\n"
	lines[15] = "0\n"
	lines[18] = "0\n"
	lines[21] = "1\n"
	lines[24] = "0\n"
	lines[27] = "-1.0\n"
	lines[30] = "39\n"
	lines[33] = "93\n"
	lines[36] = "3\n"
	lines[39] = "0.0\n"
	lines[42] = "2.0\n"
	lines[45] = "0.2\n"
	lines[48] = "1.0\n"
	lines[51] = "0.0\n"
	lines[54] = "0\n"
	lines[57] = "0\n"
	lines[61] = "1000\n"

	# and write everything back
	with open(path, 'w') as file:
		file.writelines(lines)

path = "masterconfig.txt" #replace with absolute path when known
resetConf()
