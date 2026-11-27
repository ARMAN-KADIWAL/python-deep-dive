import os,sys
def badFunction(x,y):
    result=x+y
    if result>10:
        return result*2
    else:
        return result
class badClass:
    def __init__(self,name):
        self.name=name
    def getName(self):
        return self.name
def main():
    obj=badClass('test')
    print('Name:',obj.getName())
    print('Result:',badFunction(5,7))
if __name__=='__main__':
    main()
