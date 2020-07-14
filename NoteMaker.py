#!/usr/bin/python3
import sys,os

class Node:
    def __init__(self,node_type,data):
        self.type=node_type
        self.data=data
        self.children=[]

class Tree:
    def __init__(self):
        self.root=None
         
    def print_tree(self,node,indent):
        #print(indent+node.type,node.data)
        for i in node.children:
            self.print_tree(i,indent+"\t")

    def insert_line_helper(self,node,data,level_ctr,cur_level):
        if level_ctr==(cur_level+1):
            node.children.append(Node('L',data))
            return
        if len(node.children)==0:
            #print('Syntax error: Level exceeded')
            return
 
        self.insert_line_helper(node.children[-1],data,level_ctr,cur_level+1)
     
    def insert_header_helper(self,node,data,level_ctr,cur_level):
        if level_ctr==(cur_level+1):
            node.children.append(Node('H',data))
            return
        if len(node.children)==0:
            #print('Syntax error: Level exceeded')
            return
 
        self.insert_header_helper(node.children[-1],data,level_ctr,cur_level+1)

    def insert_continuation_helper(self,node,data,level_ctr,cur_level):
        if level_ctr==(cur_level+1):
            node.children[-1].data=node.children[-1].data+' '+data
            #print('****updated value:',node.children[-1].data)
            return

        if len(node.children)==0:
            #print('Syntax error: Level exceeded')
            #print('$$$$'+node.data+'s Children not found')
            return

        self.insert_continuation_helper(node.children[-1],data,level_ctr,cur_level+1)


    
    def insert_header(self,data,level_ctr):
        if self.root==None:
            self.root=Node('H',data)
            #print('Root added')
            return
        self.insert_header_helper(self.root,data,level_ctr,1)
        #print('header',data,'inserted')

    def insert_line(self,data,level_ctr):
        self.insert_line_helper(self.root,data,level_ctr,1)
        #print('line',data,'inserted')

    def insert_continuation(self,data,level_ctr):
        self.insert_continuation_helper(self.root,data,level_ctr,1)
        #print('continuation',data,'inserted')

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
        
        level_ctr=0
        for i in line:
            if i=='>':
                level_ctr+=1
            else:
                break
        
        line=line[level_ctr:]

        if level_ctr==0:    #If it is a cont then it is not a new header or line
            level_ctr=prev_level_ctr
            #print('Continuation detected:',line)
            #print('prev_level_ctr =',prev_level_ctr)
            tree.insert_continuation(line,prev_level_ctr)  
        
        elif is_header(line):   
            line=line[2:-2]
            tree.insert_header(line,level_ctr)
        
        else:   #It is a normal line
            tree.insert_line(line,level_ctr)
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

#print('Tree made')
#print('Basic view\n')
#tree.print_tree(tree.root,'')

#Now we have a tree representation of the entire document
#Now we can simply start off rendering the tree appropriately 

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
            header+=(' '*i*tabwidth)+'|'
        header+=' '*(tabwidth)+' +---'+'-'*len(line)+'---+\n'
        for i in range(indent):
            header+=(' '*i*tabwidth)+'|'
        header+='-'*(tabwidth-1)+'>'
        header+='||   '+line+'   ||\n'
        for i in range(indent):
            header+=(' '*i*tabwidth)+'|'
        header+=' '*(tabwidth)+' +---'+'-'*len(line)+'---+'
        return header

    i=0
    if node.type=='H':
        #print()
        for i in range(indent):
            print(' '*(tabwidth*i)+'|',end='')
        print()
        #print()
        for i in range(indent):
            print(' '*(tabwidth*i)+'|',end='')
        print()
        print(make_header_with_indent(node.data,indent))

    elif node.type=='L':
        #print()
        for i in range(indent):
            print(i*tabwidth*' '+'|',end='')
        print()
        for i in range(indent):
            print(' '*(tabwidth*i)+'|',end='')
        print('-'*(tabwidth-1)+'> ',end='')
        is_first=True
        i=0
        while i<len(node.data):
            if is_first:
                print(node.data[i:i+j_fact])
                is_first=False
            else:
                for j in range(indent):
                    print(' '*j*tabwidth+'|',end='')
                print((tabwidth*' ')+' '+node.data[i:i+j_fact])
            i+=j_fact 

    for i in node.children:
        render(i,indent+1,j_fact)

justification_factor=50

render(tree.root,0,justification_factor)

ifile.close()


