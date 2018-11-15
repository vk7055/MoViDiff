# MoViDiff
Classification based on packet data agnostic feature of video flows, namely packet-size to identify the flows

This package contains several modules which manipulate QoS for different services.
This package does not contain any classifier or flow differentiator that can
differentiate between different types of app data. It rather uses a dummy
module for flow differentiation. Our dummy module for flow differentiation of Skype 
and You Tube uses the fact that Skype uses small packets which are in general smaller 
than 1000 bytes while You Tube uses bulky packets. The MTU in our network is 1500 bytes. 
Thus, most of the packets containing You Tube data are equal to 1500 bytes. So, our 
dummy module decides the packet to be of Skype if its size is below 1400 bytes otherwise 
the packet is of You Tube. It requires set_ratio.txt to have only two services. The last 
one should have a blank line before it.

Another svm.py dummy module could be imagined. This dummy svm.py module returns a number 
below the number of services randomly.

The file “set_ratio.txt” is used to assign ratio to various services being used. To assign 
ratio for a service, write the name of the service followed by a space and then followed 
by the ratio (must be an integer greater than or equal to -1) for the service. If the ratio 
assigned is -1, then there would be no scheduling and packets would be simply accepted. If 
the ratio assigned is 0, then there would be no scheduling and packets would be simply dropped. 
Otherwise the packet is enqueued in some queue. The ratio of a service specifies how many 
packets of that service can be dequeued back to back before turning to other service.

So, one line for every service with above mentioned specifications. The last service must be 
named as “Others” and must be separated by a blank line from rest of the services above it. This 
refers to all the ongoing services apart from the services mentioned above. Remember there should 
not be any extra spaces or lines anywhere in the file.

So, only svm.py and set_ratio.txt require editing.

If you have your own flow differentiator, you can test it by using it as svm.py. It should 
just accept a packet as an argument and return service type of the packet in correspondence
with set_ratio.txt file.

In order to run service differentiator, first you need to intercept packets using some iptables
rule such as
	iptables -I INPUT -j NFQUEUE --queue-num 5
Remember, the queue number must be 5.

Then, you need to run service_differentiater.py

This will successfully implement the required service differentiaition.
