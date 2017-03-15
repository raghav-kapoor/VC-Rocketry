def resetConf():
    # read a list of lines into data
	  with open(path, 'r') as file:
        lines = file.readlines()

	  # change values back to defaults

		lines[12] = "1\n"

	elif parameter == "apogeeReached":
		lines[15] = value

	elif parameter == "flightMode":
		lines[18] = value

	elif parameter == "SQUIBDELAY":
		lines[21] = value

	elif parameter == "delayStart":
		lines[24] = value

	elif parameter == "QNH":
		lines[27] = value

	elif parameter == "FRAMESIZE":
		lines[30] = value

	elif parameter == "DECSIZE":
		lines[33] = value

	elif parameter == "roundOff":
		lines[36] = value

	elif parameter == "k1":
		lines[39] = value

	elif parameter == "k2":
		lines[42] = value

	elif parameter == "k3":
		lines[45] = value

	elif parameter == "k4":
		lines[48] = value

	elif parameter == "k5":
		lines[51] = value

	elif parameter == "passedCutoff":
		lines[54] = value

	elif parameter == "squibDeployed":
                lines[57] = value

	# and write everything back
	with open(path, 'w') as file:
		file.writelines(lines)
