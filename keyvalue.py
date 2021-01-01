import os
import json
import threading
import time

class ValueCapacityExceededException(Exception):
    #User Defined Exception Class
    def __init__(self,message):
        self.message=message

class KeyAlreadyExistsException(Exception):
    #User Defined Exception Class
    def __init__(self,message):
        self.message=message

class KeySizeExceededException(Exception):
    #User Defined Exception Class
    def __init__(self,message):
        self.message=message

class KeyDoesNotExistsException(Exception):
    #User Defined Exception Class
    def __init__(self,message):
        self.message=message

class FileAlreadyOpenedException(Exception):
     #User Defined Exception Class
    def __init__(self,message):
        self.message=message
       

class FileStorageExceededException(Exception):
     #User Defined Exception Class
    def __init__(self,message):
        self.message=message



#Class for crd operations
class crd:    
    Opened_Files=[]
    def __init__(self,path=os.path.join(os.getcwd(),"file.json")):
        #Creating or opening the existing JSON file
        self.path=path
        if path not in crd.Opened_Files:
            self.f=open(self.path,'a+')
            crd.Opened_Files.append(path)
            self.mutex=threading.Lock()

        else: 
            raise FileAlreadyOpenedException("Requested File is being used by another process")  


    def check(self,key):
        #Cheks for ttl value and updates the File

        self.f.seek(0)
        dfile=json.load(self.f)
        di=json.loads(dfile["ttl"])
        try:
            limit=(di[key])
            now=time.time()
            if(now<limit):
                pass
            else:
                dfile.pop(key)
                di.pop(key)
                dfile["ttl"]=json.dumps(di)
                self.f.truncate(0)
                json.dump(dfile,self.f,indent=4)
                self.f.flush()
        except:
            pass        
               


    def create(self,key,value,ttl=None):
        #Inserting new key value pairs
        flag=0 
        #for chechking if its entered
        self.mutex.acquire()
        length=(len(value.encode('utf-8')))
        keyAlreadyExists="This key {}  already Exists".format(key)
        if os.stat(self.path).st_size<=1000000000:
            if(len(key)<=32):
                if(length<=16000):
                    if os.stat(self.path).st_size==0:
                        #Creating a new entry in JSON file
                        s='{"'+key+'":"'+(value)+'","ttl":"{}"}'
                        flag=1
                        dfile=json.loads(s)            
                    else:   
                        #updaing new entries in the JSON file
                        self.f.seek(0) 
                        dfile=json.load(self.f)
                        try:
                            dfile["ttl"]
                        except:
                            dfile["ttl"]=json.dumps({})
                            self.f.truncate(0)    
                            json.dump(dfile,self.f,indent=4)
                            self.f.flush()
                            self.mutex.release()

                        if key in dfile.keys():
                            self.mutex.release()
                            raise KeyAlreadyExistsException(keyAlreadyExists)
                        else:    
                            dfile[key]=value
                            flag=1
                    if ttl and flag:
                        a=dfile["ttl"]
                        di=json.loads(a)
                        t=time.time()
                        di[key]=t+ttl
                        dfile["ttl"]=json.dumps(di)
                    self.f.truncate(0)    
                    json.dump(dfile,self.f,indent=4)
                    self.f.flush()
                    self.mutex.release()
                else:
                    self.mutex.release()
                    raise ValueCapacityExceededException("Value capacity exceeded 16Kb")    
            else:
                self.mutex.release()
                raise KeySizetExceededException("Key exceeded the 32 Characters,Couldn't create a entry")    
        else:
            raise FileStorageExceededException("The storage file Exceeded 1Gb")



    def read(self,key):            
        #Returning the suitable key and value pair
        self.mutex.acquire()
        self.check(key)
        self.f.seek(0)
        keynotExists="The given key {} does not exists".format(key)
        try:
            self.j=json.loads(self.f.read())
            val=self.j[key]
            self.mutex.release()
            return val
        except:
            self.mutex.release()
            raise KeyDoesNotExistsException(keynotExists)
        self.mutex.release()    



    def delete(self,key):
        #Deleting the suitable key and value pair
        self.mutex.acquire()
        self.f.seek(0)
        keynotExists="The given key {} does not exists".format(key)
        try:
            self.j=json.loads(self.f.read())
            self.j.pop(key)
            d=json.loads(self.j["ttl"])
    
            try:
                d.pop(key)
                self.j["ttl"]=json.dumps(d)
            except:
                pass
            self.f.truncate(0)    
            json.dump(self.j,self.f,indent=4)
            self.f.flush()
        except:
            self.mutex.release()
            raise KeyDoesNotExistsException(keynotExists)
        self.mutex.release()



