def get_integer_at_last_position(line):
	"""
		This method accepts a string or a series of strings
		separated by spaces as an argument. line has an 
		integer as its last string.
	"""
	words = line.split(' ')
	last_word_position = len(words) - 1
	last_word = words[last_word_position].strip('\n')
	return int(last_word)

def get_ratio_list_of_services():
	"""
		This method parses the file set_ratio.txt and 
		computes list service that contains ratio of
		every service according to their occurence
		in file set_ratio.txt.
	"""
	service = []

	fo = open("set_ratio.txt", "r")

	lin = fo.readline()
	while(lin != ""):
		if len(lin) == 1:
			break
		service.append(get_integer_at_last_position(lin))
		lin = fo.readline()

	lin = fo.readline()
	if lin != "":
		service.append(get_integer_at_last_position(lin))

	fo.close()
	return service

def get_number_of_services():
	"""
		This method parses the file set_ratio.txt and 
		computes the number of services listed in the
		in file set_ratio.txt.
	"""
	number_of_services = 0

	fo = open("set_ratio.txt", "r")
	lin = fo.readline()
	while(lin != ""):
		if len(lin) == 1:
			break
		number_of_services += 1
		lin = fo.readline()

	lin = fo.readline()
	if lin != "":
		number_of_services += 1

	fo.close()
	return number_of_services