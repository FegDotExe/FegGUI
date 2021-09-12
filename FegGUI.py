import os
from math import floor


class GraphicalDict():
    """A dictionary which stores all the characters to be printed by Window.update()"""
    def __init__(self):
        self.dict={}
    def reset(self):
        self.dict={}
    def add_character(self,character,coordinates):
        if not str(coordinates[1]) in self.dict:
            self.dict[str(coordinates[1])]={}
        self.dict[str(coordinates[1])][str(coordinates[0])]=character
    def add_frame(self,frame_type,position,size):
        """Adds a frame of given size at given coordinates"""
        #Pretty useful for this: https://en.wikipedia.org/wiki/Box-drawing_character
        i_y=0
        while i_y<size[1]:
            i_x=0
            while i_x<=size[0]:
                addendum=" "
                if i_x==0 and i_y==0:
                    if frame_type in [1,3]:
                        addendum="┌"
                    elif frame_type==2:
                        addendum="┏"
                elif 0<i_x<size[0]-1 and i_y==0:
                    if frame_type==1:
                        addendum="─"
                    elif frame_type==2:
                        addendum="━"
                    elif frame_type==3:
                        addendum="┄"
                elif i_x==size[0]-1 and i_y==0:
                    if frame_type in [1,3]:
                        addendum="┐"
                    elif frame_type==2:
                        addendum="┓"
                elif (i_x==0 or i_x==size[0]-1) and 0<i_y<size[1]-1:
                    if frame_type==1:
                        addendum="│"
                    elif frame_type==2:
                        addendum="┃"
                    elif frame_type==3:
                        addendum="┆"
                if i_x==0 and i_y==size[1]-1:
                    if frame_type in [1,3]:
                        addendum="└"
                    elif frame_type==2:
                        addendum="┗"
                elif 0<i_x<size[0]-1 and i_y==size[1]-1:
                    if frame_type==1:
                        addendum="─"
                    elif frame_type==2:
                        addendum="━"
                    elif frame_type==3:
                        addendum="┄"
                elif i_x==size[0]-1 and i_y==size[1]-1:
                    if frame_type in [1,3]:
                        addendum="┘"
                    elif frame_type==2:
                        addendum="┛"
                if addendum!=" ":
                    self.add_character(addendum,(position[0]+i_x,position[1]+i_y))
                i_x+=1
            i_y+=1
    def to_string(self,size):
        """Transforms GraphicalDict.dict to a printable string"""
        outstring=""
        i_y=0
        while i_y<size[1]:
            if str(i_y) in self.dict:
                i_x=0
                while i_x<size[0]:
                    if str(i_x) in self.dict[str(i_y)]:
                        outstring+=self.dict[str(i_y)][str(i_x)]
                    else:
                        outstring+=" "
                    i_x+=1
            if i_y!=size[1]-1:
                outstring+="\n"
            i_y+=1
        return outstring

class Percent():
    """A class to represent size percentages"""
    def __init__(self,percent):
        self.percent = percent
    def get_percent(self,number):
        return (self.percent*number)/100
graphical_dict=GraphicalDict()

class Window():
    def __init__(self,size=(0,0),graphical_object=None,clear_terminal=True):
        """Creates a new Window class. If no width or height values are given, they are set to the current terminal size, which is returned by os.get_terminal_size()"""
        if size[0]!=0:
            width=size[0]
        else:
            width=os.get_terminal_size()[0]
        if size[1]!=0:
            height=size[1]
        else:
            height=os.get_terminal_size()[1]
        self.size=(width,height)
        self.clear_terminal=clear_terminal
        self.graphical_object=graphical_object
    def update(self):
        graphical_initiator=GraphicalContainer(orientation=self.graphical_object.orientation,content=[self.graphical_object])#This is done so that Window initializes its graphical object in the same way as the other objects are initialized
        
        graphical_initiator.pos=(0,0)
        graphical_initiator.cursor=(0,0)
        graphical_initiator.size=self.size
        graphical_dict.reset()
        graphical_initiator.initialize_content()
        
        outstring=""
        outstring=graphical_dict.to_string(self.size)
        if self.clear_terminal:
            os.system('cls' if os.name=='nt' else 'clear')
        print(outstring,end="")
    def get_input(self):
        pass#TODO: implement input logic

class GraphicalObject():
    """A simple graphical object which has some parameters, such as a position (example: (0,0) ) and a size (example: (10,10) )"""
    def __init__(self,size_value=Percent(100),framed=0):
        self.pos=(-1,-1)
        self.cursor=(-1,-1)
        self.size=(-1,-1)
        self.size_value=size_value#TODO: add a different way of measuring than percent
        self.framed=framed
        
    def __str__(self):
        output_dict={"pos":self.pos,"size":self.size}
        return str(output_dict)

class GraphicalContainer(GraphicalObject):
    """A Graphical Object made to hold things in itself; being the one which holds other objects, this class is the one which initializes its content"""
    def __init__(self,size_value=Percent(100),content=[],orientation="",framed=0,fix_percent=1,padding=(0,0,0,0)):
        """Padding goes clockwise starting from the left"""
        GraphicalObject.__init__(self,size_value,framed=framed)
        self.content=content
        self.orientation=orientation
        self.fix_percent=fix_percent
        self.padding=padding

    def initialize(self,target_object,value=0):
        """Initializes target_object, defining its mathematical values, such as pos and size"""
        target_object.pos=(self.cursor[0],self.cursor[1])#Set the position to the drawing cursor
        if self.orientation=="vertical":#TODO: should add a one line way to do this
            target_object.size=(self.size[0],value)#Sets the size depending on the percentage
            self.cursor=(self.cursor[0],self.cursor[1]+target_object.size[1])
        elif self.orientation=="horizontal":
            target_object.size=(value,self.size[1])#Sets the size depending on the percentage
            self.cursor=(self.cursor[0]+target_object.size[0],self.cursor[1])
        
        if target_object.framed!=0:
            graphical_dict.add_frame(target_object.framed,target_object.pos,target_object.size)
        
        if str(type(target_object).__bases__[0])=="<class 'FegGUI.FegGUI.GraphicalContainer'>":
            target_object.initialize_content()
    def initialize_content(self):
        """Initialize all of the GraphicalObject classes contained in the content variable given when creating the class. It should always be kept in mind that the elements are initialized starting from the values of the container in which they are"""
        self.cursor=self.pos #Sets the cursor back to the smallest coordinate for this object
        self.cursor=(self.cursor[0]+self.padding[0],self.cursor[1]+self.padding[1])
        self.size=(self.size[0]-(self.padding[0]+self.padding[2]),self.size[1]-(self.padding[1]+self.padding[3]))
        if self.orientation=="horizontal":
            ori=0
        elif self.orientation=="vertical":
            ori=1

        sizes=self.get_ideal_size(self.size[ori],[element.size_value for element in self.content])
        
        i=0
        for element in self.content:
            self.initialize(element,value=sizes[i])
            i+=1
    def get_ideal_size(self,total_size,size_values):
        """Input total size of an object and get the raccomended length based on the given percentages"""
        is_percent_list=[]
        output_size=[]
        for element in size_values:
            if str(type(element))=="<class 'FegGUI.FegGUI.Percent'>":
                is_percent_list.append(True)
                output_size.append(element)
            else:
                is_percent_list.append(False)
                output_size.append(element)
                total_size-=element
        i=0
        percent_list=[]
        if len(output_size)>0:
            for element in is_percent_list:
                if element:
                    output_size[i]=floor(output_size[i].get_percent(total_size))
                    percent_list.append(output_size[i])
                i+=1
            if ((total_size-sum(percent_list))*100)/total_size<=self.fix_percent:
                while sum(percent_list)<total_size:
                    if i>=len(output_size):
                        i=0
                    percent_list[i]+=1
                    i+=1
            i=0
            ii=0
            for element in is_percent_list:
                if element:
                    output_size[i]=percent_list[ii]
                    ii+=1
                i+=1
        return output_size

class Column(GraphicalContainer):
    def __init__(self,size_value=100,content=[],framed=0,fix_percent=1,padding=(0,0,0,0)):
        GraphicalContainer.__init__(self,size_value,content,orientation="vertical",framed=framed,fix_percent=fix_percent,padding=padding)
class Row(GraphicalContainer):
    def __init__(self,size_value=Percent(100),content=[],framed=0,fix_percent=1,padding=(0,0,0,0)):
        GraphicalContainer.__init__(self,size_value,content,orientation="horizontal",framed=framed,fix_percent=fix_percent,padding=padding)
class Rectangle(GraphicalObject):
    """A GraphicalObject which can't contain anything, but can be represented as a frame"""
    def __init__(self,size_value=Percent(100),framed=0):
        GraphicalObject.__init__(self,size_value,framed=framed)