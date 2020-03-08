import collections.abc, types, inspect, functools

class UnknownOutputError(Exception):
    pass

#Styles

#Func styles
STANDARD_FUNC=0
JUST_INPUT_FUNC=1
JUST_OUTPUT_FUNC=2

#Object styles
STANDARD_OBJ=0
SPACIOUS_OBJ=1

#
default_settings={"output":None,"dict_separator":":","separator":" ","func_log":STANDARD_FUNC,"obj_log":STANDARD_OBJ}

class MainLogger:
    def __init__(self, **settings):
        self._called_from_log = False
        self.settings = default_settings
        for key in default_settings:
            if key in settings:
                self.settings[key]=settings.get(key,default_settings[key])
        pass
    
    def __output(self, text):
        if self.settings.get("output",None)==None:
            print(text)
        elif hasattr(self.settings.get("output",None), 'write'):
            self.settings["output"].write()
        else:
            raise UnknownOutputError("Unknown logging location")
        
    def log_list(self, obj):
        if self._called_from_log is False:
            if isinstance(obj,collections.abc.Iterable):
                if isinstance(obj, collections.abc.Mapping):
                    text=""
                    for i in obj:
                        text+=str(i)+self.settings.get("dict_separator",default_settings["dict_separator"])+str(obj.get(i,i))+self.settings.get("separator",default_settings["separator"])
                    self.__output(text)
                else:
                    text=""
                    for i in obj:
                        text+=str(i)+self.settings.get("separator"," ")
                    self.__output(text)
            else:
                raise TypeError("Object is not iterable")
        else:
            if isinstance(obj, collections.abc.Mapping):
                text=""
                for i in obj:
                    text+=str(i)+self.settings.get("dict_separator",default_settings["dict_separator"])+str(obj.get(i,i))+self.settings.get("separator",default_settings["separator"])
                self.__output(text)
            else:
                text=""
                for i in obj:
                    text+=str(i)+self.settings.get("separator"," ")
                self.__output(text)
        self._called_from_log=False


    def log_object(self, obj):
        DIR=dir(obj)
        params=[]
        
        log_type=self.settings.get("obj_log",STANDARD_OBJ)
        if inspect.isclass(obj):
            DIR.reverse()
            for i in DIR:
                if str(i)[0]== '_' and str(i)[1]=='_':
                    break
                params.append(i)
            if  log_type== STANDARD_OBJ:
                self. __output("class "+obj.__name__+':')
                for i in params:
                    self.__output(" -"+i+'='+repr(obj.__dict__.get(i,None)))

            elif log_type == SPACIOUS_OBJ:
                self. __output("class "+obj.__name__+':')
                for i in params:
                    self.__output("\n -"+i.replace("_"+obj.__class__.__name__,'')+' = '+repr(obj.__dict__.get(i,None)))
        else:
            DIR.reverse()
            for i in DIR:
                if str(i)[0]== '_' and str(i)[1]=='_':
                    break
                params.append(i)
   
            if  log_type== STANDARD_OBJ:
                self. __output("class "+obj.__class__.__name__+':')
                for i in params:
                    self.__output(" -"+i+'='+repr(obj.__getattribute__(i)))

            elif log_type == SPACIOUS_OBJ:
                self. __output("class "+obj.__class__.__name__+':')
                for i in params:
                    self.__output("\n -"+i.replace("_"+obj.__class__.__name__,'')+' = '+repr(obj.__getattribute__(i)))

    def log(self, obj):
        if isinstance(obj,collections.abc.Iterable):
            self._called_from_log=True
            self.__output(self.log_list(obj))
        else:
            self.log_object(obj)

    def debug_function(self,func):
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            kwargs.pop("name")         
            
            args_repr = [repr(a) for a in args]             
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  

            name=str(func.__name__)[func.__name__.find("function"):]
            signature = ", ".join(args_repr + kwargs_repr)   

            log_type=self.settings.get("func_log",STANDARD_FUNC)
            
            if log_type == STANDARD_FUNC:
                self.__output(f"Calling {name}({signature})")
                value = func(*args, **kwargs)
                self.__output(f"{name}({signature}) returned {value!r}")   

            elif log_type == JUST_INPUT_FUNC:
                self.__output(f"Calling {name}({signature})")
                value = func(*args, **kwargs)

            elif log_type == JUST_OUTPUT_FUNC:
                value = func(*args, **kwargs)
                self.__output(f"{name}({signature}) returned {value!r}")   
            
            return value            
        if isinstance(func,types.FunctionType):
            return wrapper_debug
    
    
    
