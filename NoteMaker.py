#!/usr/bin/python3
import copy as cp,sys,os

class Node:
    def __init__(self,node_type,data):
        self.type=node_type
        self.data=data
        self.children=[]

references=dict()   #A dictionary of references created. For quickly looking up nodes

class Tree:
    def __init__(self):
        self.root=None
         
    def print_tree(self,node,indent):
        print(indent+node.type,node.data)
        for i in node.children:
            self.print_tree(i,indent+"\t")

    def insert_line_helper(self,node,data,level_ctr,cur_level,ref):
        if level_ctr==(cur_level+1):
            node.children.append(Node('L',data))
            retval=node.children[-1]
            if ref!=None:
                references[ref]=retval
            return cp.copy(retval)

        if len(node.children)==0:
            print('Syntax error: Level exceeded')
            return
 
        self.insert_line_helper(node.children[-1],data,level_ctr,cur_level+1,ref)
     
    def insert_header_helper(self,node,data,level_ctr,cur_level,ref):
        if level_ctr==(cur_level+1):
            node.children.append(Node('H',data))
            retval=node.children[len(node.children)-1]
            if ref!=None:
                references[ref]=retval
            return cp.copy(retval)

        if len(node.children)==0:
            print('Syntax error: Level exceeded')
            return
 
        self.insert_header_helper(node.children[-1],data,level_ctr,cur_level+1,ref)

    def insert_continuation_helper(self,node,data,level_ctr,cur_level):
        if level_ctr==(cur_level+1):
            node.children[-1].data=node.children[-1].data+' '+data
            return

        if len(node.children)==0:
            return

        self.insert_continuation_helper(node.children[-1],data,level_ctr,cur_level+1)


    
    def insert_header(self,data,level_ctr,ref):

        if self.root==None:
            self.root=Node('H',data)
            #print('Root added')
            return
        node=self.insert_header_helper(self.root,data,level_ctr,1,ref)
        return node

    def insert_line(self,data,level_ctr,ref):
        node=self.insert_line_helper(self.root,data,level_ctr,1,ref)
        return node

    def insert_continuation(self,data,level_ctr):
        self.insert_continuation_helper(self.root,data,level_ctr,1)

def make_tree(ifile):

    def is_header(line):
        if(line[0]==line[1] and line[-1]==line[-2] and line[0]=='{' and line[-1]=='}'):
            return True
    
    tree=Tree()
    prev_level_ctr=0

    for line in ifile.readlines():
        line=line.strip()

        if len(line)==0:
            #additional spaces provided
            #by the note taker for clarity
            continue

        if line[0]=='@':
            #reference to a previously defined reference
            ref,line=line.split()[0][1:],' '.join(line.split()[1:])
            references[ref].children.append(Node('L',line))
            prev_type_is_ref=True
            continue 

        level_ctr=0
        for i in line:
            if i=='>':
                level_ctr+=1
            else:
                break
        
        line=line[level_ctr:]

        ref=None
        ind=None
        try:
            ind=line.index('@')
            ref=line[(ind+1):]
            line=line[:ind].strip()
        except:
            pass

        if level_ctr==0:    #If it is a cont then it is not a new header or line
            level_ctr=prev_level_ctr
            #print('Continuation detected:',line)
            #print('prev_level_ctr =',prev_level_ctr)
            tree.insert_continuation(line,prev_level_ctr)  
        
        elif is_header(line):   
            
            line=line[2:-2]
            node=tree.insert_header(line,level_ctr,ref)

        else:   #It is a normal line
            node=tree.insert_line(line,level_ctr,ref)

        prev_level_ctr=level_ctr
        
    return tree

input_file=sys.argv[1]
#input_file='in'
#op_file='op'

#print('Input File:',input_file,'Output File:',op_file)

ifile=open(input_file,"r")
#print('Attempting to make tree')

#Convert the input file into a tree
tree=make_tree(ifile)

#print(references)
#for i in references:
#    print(references[i].data)
#print('Tree made')
#print('Basic view\n')
#tree.print_tree(tree.root,'')

#Now we have a tree representation of the entire document
#Now we can simply start off rendering the tree appropriately 
#We also have a list of references as requried by the user
tabwidth=8

print('Made with NoteMaker')

def render(node,indent,j_fact):
 
    #indent is the number of tabspaces (of size tabwidth) to be applied
    #as the current indent 

    def make_header_with_indent(line,indent):
        '''
        header=(' '*tabwidth)*indent+' +---'+'-'*len(line)+'---+\n'+\
               (' '*tabwidth)*indent+'||   '+line+'   ||\n'+\
               (' '*tabwidth)*indent+' +---'+'-'*len(line)+'---+'
        '''
        if indent==0:
            header=(' '*tabwidth)*indent+' +---'+'-'*len(line)+'---+\n'+\
                   (' '*tabwidth)*indent+'||   '+line+'   ||\n'+\
                   (' '*tabwidth)*indent+' +---'+'-'*len(line)+'---+'
            return header
            
        header=''
        for i in range(indent):
            header+=(' '*tabwidth)+'|'
        header+=' '*(tabwidth)+' +---'+'-'*len(line)+'---+\n'
        for i in range(indent):
            header+=(' '*tabwidth)+'|'
        header+='-'*(tabwidth-1)+'>'
        header+='||   '+line+'   ||\n'
        for i in range(indent):
            header+=(' '*tabwidth)+'|'
        header+=' '*(tabwidth)+' +---'+'-'*len(line)+'---+'
        return header

    i=0
    if node.type=='H':
        #print()
        for i in range(indent):
            print(' '*(tabwidth)+'|',end='')
        print()
        #print()
        for i in range(indent):
            print(' '*(tabwidth)+'|',end='')
        print()
        print(make_header_with_indent(node.data,indent))

    elif node.type=='L':
        #print()
        for i in range(indent):
            print((tabwidth)*' '+'|',end='')
        print()
        for i in range(indent):
            print(' '*(tabwidth)+'|',end='')
        print('-'*(tabwidth-1)+'> ',end='')
        is_first=True
        i=0
        while i<len(node.data):
            if is_first:
                print(node.data[i:i+j_fact])
                is_first=False
            else:
                for j in range(indent):
                    print(' '*tabwidth+'|',end='')
                print((tabwidth*' ')+' '+node.data[i:i+j_fact])
            i+=j_fact 

    for i in node.children:
        render(i,indent+1,j_fact)

justification_factor=50

render(tree.root,0,justification_factor)
print()
print()
ifile.close()


