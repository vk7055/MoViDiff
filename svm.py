"""

	This is a dummy svm module (Support Vector Machine)
	that differentiates between packets with size 
	less than 1450 bytes and packets larger than or
	equal to 1450 bytes. The MTU in our network is
	1500 bytes. We used it to differentiate between 
	Skype and You Tube packets using the fact that 
	Skype uses packets smaller than 1000 bytes whereas
	You Tube uses packets of 1500 bytes, i.e., size of
	our MTU. So, it would return 0 for a Skype packet
	and 1 for a You Tube packet. 

"""


from netfilterqueue import NetfilterQueue
import re
import random
from ratio_parse_file import get_number_of_services


def svm_decision(pkt):
	#return random.randrange(get_number_of_services())
	if int(re.search(r'\d+', str(pkt)).group()) < 1400:
		return 0
	else:
		return 1