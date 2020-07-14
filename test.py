class Test:
    def __init__(self):
        print("This is the constructor")
    def private_method(a,b):
        print('First argument:',a,'Second argument:',b)
    def public_method(self,a,b):
        self.private_method(a,b)

t=Test()
t.public_method(1,2)