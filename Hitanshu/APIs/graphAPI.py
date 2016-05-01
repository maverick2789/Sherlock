# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 20:37:52 2016
Title : Graph API
@author: Proactive Panda
"""

#Imports
import pyorient as pdb
import ast
import wordNetAPI

"""
JUST PASTE THIS FILE NEXT TO YOUR SCRIPT (SAME FOLDER).. THAT'S ALL, CALL ANY
FUCNTION AS YOU WANT!! 

IF UNABLE TO CONNECT CALL ME, SERVER MIGHT NOT BE RUNNING!! :P :P 
"""
#Server Configurations
server_address = '192.168.54.237'
server_port = 2424
server_login = 'root'
server_password = 'hitanshu'

#Database Configuration
db_name = 'Testing_v2'
db_login = 'admin'       #'reader','writer'
db_password = 'admin'    #'reader','writer'


"""
This function setups the connection between this script and GraphDB
NOTE: MAKE SURE AT THE END OF YOUR SNIPPET YOU ADD THE FOLLOWING LINE
            client.db_close()
Its for closing the DB Instance.
"""
def open_db():
    client = pdb.OrientDB(server_address, server_port)
    session_id = client.connect( server_login,server_password)
    print 'Connect with Server, Session Id:',session_id
    
    if client.db_exists(db_name, pdb.STORAGE_TYPE_PLOCAL):
        client.db_open(db_name, db_login, db_password)
        print 'Database ready!'
        return client
    else:
        client.db_close()
        print 'Database not available!'





"""
Function for Inserting a new node

Input Parameters:
    client : (Returned from calling open_db() function)
    thing: (String) Name of the New Node. 
    list_attributes: 2D list of Attribute-Value Pair
    e.g. list_attributes = [['Type','Wizard'],['House','Ravenclaw'],['Pet','Pheonix']]
    
Output:
Nothing

Note: Make sure that that the node doesn't already exists.(Use thing_count())
"""
def insert_node(client,thing,list_attributes):
    stmt = ""
    for i in range(len(list_attributes)):
        #list_attributes[i][1] = list_attributes[i][1]+'.'+fetch_class(list_attributes[i][0])
        stmt = stmt + " , " + list_attributes[i][0] + " = '" + list_attributes[i][1] + "' "
    client.command("CREATE VERTEX Thing SET Name = '"+thing+"'" +stmt)
    print thing+' inserted successfully!'





"""
Function for Updating a new node

Input Parameters:
    client : (Returned from calling open_db() function)
    thing: (String) Name of the New Node. 
    list_attributes: 2D list of Attribute-Value Pair
    e.g. list_attributes = [['Type','Wizard'],['House','Ravenclaw'],['Pet','Pheonix']]
    
Output:
Nothing

"""
def update_node(client,thing,list_attributes):
    #Query : UPDATE Thing SET Type = 'Auror',... WHERE Name = 'James Potter'
    stmt = ""
    for i in range(len(list_attributes)):
        list_attributes[i][1] = list_attributes[i][1]+'.'+fetch_class(list_attributes[i][0])
        stmt = stmt + list_attributes[i][0] + " = '" + list_attributes[i][1] + "'," 
    stmt = str(stmt[:-1])
    client.command("UPDATE Thing SET "+stmt+" WHERE Name = '" + thing +"'")
    print thing+' updated successfully!'






"""
Function for inserting a new Edge called Relation

Input Parameters:
    client : (Returned from calling open_db() function)
    thing1: (String) The Name of the Node from the Relation Originates.
    thing2: (String) Name of the New Node where Relation Points. 
    relatedby: (String) The relation they share
    edge_properties: 2D list of Attribute-Value Pair
    e.g. 
        thing1 = 'Harry Potter'
        thing2 = 'Ginny Potter'
        relatedby = 'Wife'
        edge_properties = [['time','<the marriage date>']]
    
Output:
Nothing

Note: No need to check if it exists or not, just insert a new if new information has arrived.
"""

def insert_edge(client,thing1,thing2,relatedby,edge_properties):
    stmt = ", "
    for i in range(len(edge_properties)):
        edge_properties[i][1] = edge_properties[i][1]+'.'+fetch_class(edge_properties[i][0])
        stmt = stmt + edge_properties[i][0] + " = '" + edge_properties[i][1] + "'," 
    stmt = str(stmt[:-1])
    client.command("CREATE EDGE Relation FROM (SELECT FROM Thing WHERE Name = '"+thing1+"') to (SELECT FROM Thing WHERE Name = '"+thing2+"') SET Name = '"+relatedby+"' "+stmt)
    print relatedby+' realtion created!'







"""
Function for Updating an Edge called Relation

Input Parameters:
    client : (Returned from calling open_db() function)
    thing1: (String) The Name of the Node from the Relation Originates.
    thing2: (String) Name of the New Node where Relation Points. 
    relatedby: (String) The relation they share
    edge_properties: 2D list of Attribute-Value Pair
    e.g. 
        thing1 = 'Harry Potter'
        thing2 = 'Ginny Potter'
        relatedby = 'Wife'
        edge_properties = [['time','<the marriage date>']]
    
Output:
Nothing

Note: This is just incase we need to add some more properties of an Edge.
Prefer creating a new if there is a time gap. i.e. another instance occuring after 3-4 paragraph
"""
def update_edge(client,thing1,thing2,relatedby,edge_properties):
    stmt = " "
    #UPDATE Relation SET time ='31st July 1980' WHERE Name = 'father' AND in = (SELECT FROM Thing WHERE Name = 'Harry Potter') AND out = (SELECT FROM Thing WHERE Name = 'James Potter')
    for i in range(len(edge_properties)):
        edge_properties[i][1] = edge_properties[i][1]+'.'+fetch_class(edge_properties[i][0])
        stmt = stmt + edge_properties[i][0] + " = '" + edge_properties[i][1] + "'," 
    stmt = str(stmt[:-1])
    client.command("UPDATE Relation SET "+stmt+" WHERE Name = '"+relatedby+"' "+ "AND out = (SELECT FROM Thing WHERE Name = '"+thing1+"')  AND out = (SELECT FROM Thing WHERE Name = '"+thing2+"')")
    print relatedby+' realtion updated!'







"""
Function for couting instance of a particular Thing
May also be used to check whether the Thing exists or not.

Input Parameters:
    client : (Returned from calling open_db() function)
    thing: (String) The Name of the Node
    
Output:
(Int) Count of Instances of that Node

Note: Technically speaking it shouldn't be above 1... :P Else we have gone wrong somewhere...
"""
def thing_count(client,thing):
    output = client.command("SELECT COUNT(*) FROM Thing WHERE Name = '"+thing+"'")
    response = str(output[0])
    count = int(response[11:response.index('L')])
    return count







"""
Function to get all the properties of a particular Thing

Input Parameters:
    client : (Returned from calling open_db() function)
    thing: (String) The Name of the Node 

Output: All the attributes of the Thing
[List of Dictionary]
Each Dictionary represents one Instance.
And each entry in the dictonary consists of following:
> Name of the Thing
> All the Attributes Value pair of the Thing
> All the In-Edges and All the Out-Edges

Ouput Example: 
[{'out_Relation': ['Friends'], 'Type': 'Student', 'Name': 'Harry Potter', 'in_Relation': ['Mother', 'Friends', 'father']}]


Note: Only one entry as it contains only one instance.
"""
def fetch_thing(client,thing):
    output = client.command("SELECT in_Relation.Name,out_Relation.Name,* FROM Thing WHERE Name LIKE '%"+thing+"%'")
    response = []
    for i in range(len(output)):
        abc = str(output[i])
        alpha = abc[abc.index(':{')+1:abc.index('},')+1]
        obj = ast.literal_eval(alpha.decode()) 
        response.append(obj)
    return response

def fetch_thing_list(client,thing):
    response = []    
    for entity in thing:
         output = fetch_thing(client,entity)
         for data in output:         
             response.append(data)
    reorder = sorted(response, key = response.count, reverse=True)
    response = []
    for i in reorder:
        if i not in response:
            response.append(i)
    return response




"""
Function to get all the properties of a type of Relation

Input Parameters:
    client : (Returned from calling open_db() function)
    relatedby: (String) The relation from which the nodes are related.

Output: List of all the instances of that relation 
[List of Dictionary]
Each Dictionary represents one Instance.
And each entry in the dictonary consists of following:
> Name of the relation
> All the Attributes Value pair of the relations (like time)
> Both the Nodes from which the relation is connected.{in and out}

"""
def fetch_relation(client,relatedby):
    output = client.command("SELECT in.Name,out.Name,* FROM Relation WHERE Name LIKE '%"+relatedby+"%'")
    response = []
    for i in range(len(output)):
        abc = str(output[i])
        alpha = abc[abc.index(':{')+1:abc.index('},')+1]
        obj = ast.literal_eval(alpha) 
        response.append(obj)
    return response
 
def fetch_relation_list(client,relatedby):
    response = []    
    for entity in relatedby:
         output = fetch_relation(client,entity)
         for data in output:         
             response.append(data)
    reorder = sorted(response, key = response.count, reverse=True)
    response = []
    for i in reorder:
        if i not in response:
            response.append(i)
    return response
 
 
 
 
 
 
 
"""
Function to find relation(s) between two things... It look both the way,
i.e. 
    thing1 ---r--> thing2 
    thing2 ---r--> thing1

Input Parameters:
    client : (Returned from calling open_db() function)
    thing1: (String) Name of the Thing
    thing2: (String) Name of the things

Output: List of all the instances of that relation 
[List of Dictionary]
Each Dictionary represents one Instance.
And each entry in the dictonary consists of following:
> Name of the relation
> All the Attributes Value pair of the relations (like time)
> Both the Nodes from which the relation is connected.{in and out}

example: 
for find_relation(client,'Harry Potter','James Potter') : 
[{'out': 'James Potter', 'Name': 'father', 'in': 'Harry Potter'}]
"""
def find_relation(client,thing1,thing2):
    output = client.command("SELECT in.Name,out.Name,* FROM Relation WHERE in.Name LIKE '%"+thing1+"%' AND out.Name LIKE '%"+thing2+"%'")
    response = []
    for i in range(len(output)):
        abc = str(output[i])
        alpha = abc[abc.index(':{')+1:abc.index('},')+1]
        obj = ast.literal_eval(alpha) 
        response.append(obj)
    output = client.command("SELECT in.Name,out.Name,* FROM Relation WHERE in.Name LIKE '%"+thing2+"%' AND out.Name LIKE '%"+thing1+"%'")
    for i in range(len(output)):
        abc = str(output[i])
        alpha = abc[abc.index(':{')+1:abc.index('},')+1]
        obj = ast.literal_eval(alpha) 
        response.append(obj)
    return response

def find_relation_list(client,thing1,thing2):
    response = []    
    for entity1 in thing1:
        for entity2 in thing2:
            output = find_relation(client,entity1,entity2)
            for data in output:         
                response.append(data)
    reorder = sorted(response, key = response.count, reverse=True)
    response = []
    for i in reorder:
        if i not in response:
            response.append(i)
    return response










"""
Function to find thing(s) which are related with thing1 with a realtion r,
Again it look both the ways....
i.e. 
    thing1 ---outR--> thing 
    thing1 <--inR--- thing

Input Parameters:
    client : (Returned from calling open_db() function)
    thing1: (String) Name of the Thing
    relation: (String) Name of the relation

Output: List of all the instances of that relation 
[List of Dictionary]
Each Dictionary represents one Instance.
And each entry in the dictonary consists of following:
> Name of the thing
> All the Attributes Value pair of the relations (like time)

example: 
for find_thing(client,'Harry Potter','father'): 
[{'out_Relation': ['father'], 'Type': 'Auror', 'Name': 'James Potter'}]
"""
def find_thing(client,thing1,relation):
    output = client.command("SELECT in_Relation.Name,out_Relation.Name,* FROM Thing WHERE out_Relation IN (SELECT FROM Relation WHERE in.Name LIKE '%"+thing1+"%' AND Name LIKE '%"+relation+"%')")
    response = []
    for i in range(len(output)):
        abc = str(output[i])
        alpha = abc[abc.index(':{')+1:abc.index('},')+1]
        obj = ast.literal_eval(alpha) 
        response.append(obj)
    output = client.command("SELECT in_Relation.Name,out_Relation.Name,* FROM Thing WHERE in_Relation IN (SELECT FROM Relation WHERE out.Name LIKE '%"+thing1+"%' AND Name LIKE '%"+relation+"%')")
    for i in range(len(output)):    
        abc = str(output[i])
        alpha = abc[abc.index(':{')+1:abc.index('},')+1]
        obj = ast.literal_eval(alpha) 
        response.append(obj)
    return response

def find_thing_list(client,thing1,relation):
    response = []    
    for entity1 in thing1:
        for entity2 in relation:
            output = find_thing(client,entity1,entity2)
            for data in output:         
                response.append(data)
    reorder = sorted(response, key = response.count, reverse=True)
    response = []
    for i in reorder:
        if i not in response:
            response.append(i)
    return response



#SAMPLE CODE FOR REFERENCE
"""
list_attributes = [['Type','Wizard'],['House','Ravenclaw'],['Pet','Pheonix']]

import graphAPI

client = open_db()
print 'Connected'

#insert_node(client,'Lily Potter',properties)
#insert_edge(client,'Lily Potter','Harry Potter','Mother',properties)
#update_edge(client,'James Potter','Harry Potter','father',properties)
#print thing_count(client,'Donald Trump')
#obj = fetch_thing(client,'Harry Potter')
#obj = fetch_relation(client,'Mother')
#obj = find_relation(client,'Harry Potter','James Potter')
#obj = find_thing(client,'Harry Potter','father')

obj = find_thing(client,'Harry Potter','father')
print obj
print obj[0].keys()
print obj[0][obj[0].keys()[1]]


client.db_close()
"""

client = open_db()
print 'Connected'
thing = ['watts','steam','engine']
output = fetch_thing_list(client,thing)
client.db_close()