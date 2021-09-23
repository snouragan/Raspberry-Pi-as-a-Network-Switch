# library to convert the bytes sent from arduino 
# to information about the relay state
# 1 - relay on 
# 0 - relay off

class Relay:
    
    def __init__(self, number):
        self.number = number
    def getNumber(self):
        return self.number

def TEST_1():
    relay = Relay(0)
    print(relay.getNumber())

def TEST_2():
    relays = []
    for _ in range(8):
        relays.append( Relay(_))
    for relay in relays:
        print(relay.getNumber(), sep=' ', end = '\n')

if __name__ == '__main__':
    #TEST_1()
    #TEST_2()    
    #TEST_3()
    
