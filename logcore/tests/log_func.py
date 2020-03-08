import logcore.main as log

logger=log.MainLogger()

@logger.debug_function
def a(b,c,*args,**kwargs):
    print(b,c,args,kwargs)

a(1,2,3,4,5,name=a)
