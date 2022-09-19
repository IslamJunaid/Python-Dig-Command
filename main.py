import dns.message
import dns.query
import dns.name
import time
from datetime import datetime

def mydig(domain, ip):
    x=dns.message.make_query(domain,dns.rdatatype.A)
    response=dns.query.udp(x,ip, timeout=3) #makes the query with the inputted domain name
    if not response.answer:         #checks if there's an ip answer
        if response.additional:        #if no IP checks additional to grab first server to query
            for data in response.additional:
                if data.rdtype == dns.rdatatype.A:
                    root = data[0].to_text().split()[-1]    #Changes root to first additional
                    return mydig(domain, root)
        else:
            name = response.authority[0].to_text().split()[-1]              #If no additional it queries the authority
            newip = mydig(name,'198.41.0.4').answer[0].to_text().split()[-1]
            return mydig(domain, newip)
    elif 'CNAME' in response.answer[0].to_text():               #query the CNAME
        return mydig(response.answer[0].to_text().split()[-1], '198.41.0.4')
    return response

domain = input("Enter Website: ") # gets user input
try:      #if it doesn't work returns error
    timein = time.time() #query timer
    answer = mydig(domain,'198.41.0.4')
    timeout = time.time()
    qtime = (timeout-timein) *1000 #converts seconds to ms
except:
    print("error")
    quit()
 #Prints answer
print("Question Section: ")
print(domain + "\tIN A")
print("Answer Section: ")
print(answer.answer[0].to_text())
print("Query Time " + str(qtime)+"ms")
print("When: " + str(datetime.now()))

