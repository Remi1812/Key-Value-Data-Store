# Key-Value-Data-Store
 It's a key-value data store library. It uses a json file to store the key-value pairs. Additional to storage support, create API also supports the TTL value in seconds. Which specifies the life of the key-value pair. 
<br>
The semantics of deleting expired keys is made efficient by checking the expiration only if that key is read or deleted. This is to avoid consuming CPUs for checking a long list of keys.
<br>
CRD operations are thread safe. Locks are done to execute critical paths. 
The critical paths are made as less possible for efficiency.
# Project documentation
<b><h3>Library import</h3></b>

```
from keyvalue import * #imports crd class and exception handlers
from keyvalue import crd #imports only crd class
import keyvalue as k #imports all contents
```
Clone the contents of this repo and place the files in the project folder. Import using any of the following cmd
<hr>
<b><h3>Object instantiation</h3></b>

```
Obj = crd(filepath)
```
During object instantiation filepath could be provided or by default it creates 'file.json' in cwd. Note: No two objects on a runtime could use the same file path. If used, raises an exception (Exception no : 5).
<br>
<hr>

<b><h3>Methods</h3></b>
<b>Create</b><br>
  ```
  Obj.create(key,value,ttl)
  ```
  Parameter : key (String) , value (String) , TTL [seconds] (int optional) <br>
  Function description : Create a new key-value pair in the object’s file path<br>
  Exceptions thrown<sup>*</sup> : 1,2,3,6<br>
  <br>
<b>Read</b><br>
  ```
  Value = Obj.read(key)
  ```
  Parameters : key (String)<br>
  Return : value (String)<br>
  Function description : Read the value for the given key in the object’s file path and returns the value in string<br>
  Exception thrown : 4<br>
  <br>

<b>Delete</b><br>
  ```
  Obj.delete(key)
  ```
Parameters : key (String)<br>
Function description : Delete the given key in object’s file path<br>
Exception thrown : 4<br>
 
  <br>

<sup>*</sup><i>Exceptions thrown are mentioned by number, details description is provided in the Exception section.</i>

<hr>
<b><h3>Exceptions</h3></b>
<b>ValueCapacityExceededException</b><sup>1</sup><br>
&nbsp;This exception is raised when a key's value size goes beyond 16KB.<br><br>
<b>KeyAlreadyExistsException</b><sup>2</sup><br>
&nbsp;This exception is raised when create is issued for the key that already exist<br><br>
<b>KeySizeExceededException</b><sup>3</sup><br>
&nbsp;This exception is raised when “key” issued to create has more than 32 characters<br><br>
<b>KeyDoesNotExistsException</b><sup>4</sup><br>
&nbsp;This exception is raised when read or delete is issued to the key that doesn't exist.<br><br>
<b>FileAlreadyOpenedException</b><sup>5</sup><br>
&nbsp;This exception is raised when the File is already opened by another crd obj.<br><br>
<b>FileStorageExceededException</b><sup>6</sup><br>
&nbsp;This exception is raised when the size of the File exceeds 1GB <br><br>
<b>Exception handling semantics</b>

```
try:
 #Statement(s)
except ExceptionToBeHandled:
 #Handle Statment(s)
except ...
```
