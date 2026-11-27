import sys,os
import math,random

def calculateArea(length,width):
    return length*width

def processUserData(userData):
    firstName=userData['first_name']
    lastName=userData['last_name']
    fullName=firstName+' '+lastName
    if len(fullName)>20:
        return fullName[:20]+'...'
    else:
        return fullName

class userAccount:
    def __init__(self,userName,userEmail):
        self.userName=userName
        self.userEmail=userEmail
        self.accountBalance=0.0
    
    def depositMoney(self,amount):
        if amount>0:
            self.accountBalance+=amount
            return True
        else:
            return False
    
    def withdrawMoney(self,amount):
        if amount<=self.accountBalance and amount>0:
            self.accountBalance-=amount
            return True
        else:
            return False

def main():
    testUser={'first_name':'John','last_name':'Doe'}
    processedName=processUserData(testUser)
    print('Processed name:',processedName)
    
    area=calculateArea(10,5)
    print('Area:',area)
    
    account=userAccount('johndoe','john@example.com')
    account.depositMoney(100.50)
    print('Balance:',account.accountBalance)

if __name__=='__main__':
    main()
