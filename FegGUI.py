import os
from math import floor
import datetime
from textwrap import wrap

class SizeValueError(Exception):
    def __init__(self,container):
        super().__init__("The container "+str(container)+" had contents which exceeded its size.")

class GraphicalDict():
    """A dictionary which stores all the characters to be printed by Window.update()"""
    def __init__(self):
        self.dict={}
        self.init_list=[]
        self.cache={}
    def reset(self):
        self.dict={}
    def clear(self,position,size,outer_size):
        i_y=0
        while i_y<size[1]:
            i_x=0
            while i_x<size[0]:
                self.remove_character((i_x+position[0], i_y+position[1]),outer_size)
                i_x+=1
            i_y+=1
    def add_character(self,character,coordinates,outer_size):
        if coordinates[0]<=outer_size[0] and coordinates[1]<=outer_size[1]:
            if not str(coordinates[1]) in self.dict:
                self.dict[str(coordinates[1])]={}
            self.dict[str(coordinates[1])][str(coordinates[0])]=character
    def remove_character(self,coordinates,outer_size):
        if coordinates[0]<=outer_size[0] and coordinates[1]<=outer_size[1]:
            if str(coordinates[1]) in self.cache:
                del self.cache[str(coordinates[1])]
            if str(coordinates[1]) in self.dict:
                if str(coordinates[0]) in self.dict[str(coordinates[1])]:
                    del self.dict[str(coordinates[1])][str(coordinates[0])]
    def add_frame(self,frame_type,position,size,outer_size):
        """Adds a frame of given size at given coordinates; outer_size is the size value of the outer object"""
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
                    self.add_character(addendum,(position[0]+i_x,position[1]+i_y),outer_size)
                i_x+=1
            i_y+=1
    def add_text(self,position,size,text,outer_size,cursor=(0,0)):#FIXME: fix problem with relative texts and percentages
        i=0
        i_y=cursor[1]
        while i_y<size[1]:
            i_x=cursor[0]
            while i_x<size[0]:
                if i<len(text):
                    self.add_character(text[i],(i_x+position[0],i_y+position[1]),outer_size)
                i+=1
                i_x+=1
            i_y+=1
    def to_string(self,size):
        """Transforms GraphicalDict.dict to a printable string"""
        outstring=""
        i_y=0
        while i_y<size[1]:
            if str(i_y) not in self.cache:
                self.cache[str(i_y)]=""
                if str(i_y) in self.dict:
                    i_x=0
                    while i_x<size[0]:
                        if str(i_x) in self.dict[str(i_y)]:
                            outstring+=self.dict[str(i_y)][str(i_x)]
                            self.cache[str(i_y)]+=self.dict[str(i_y)][str(i_x)]
                        else:
                            outstring+=" "
                            self.cache[str(i_y)]+=" "
                        i_x+=1
                if i_y!=size[1]-1:
                    outstring+="\n"
                    self.cache[str(i_y)]+="\n"
            else:
                outstring+=self.cache[str(i_y)]
            i_y+=1
        return outstring

class Percent():
    """A class to represent size percentages"""
    def __init__(self,percent):
        self.percent = percent
    def get_percent(self,number):
        return (self.percent*number)/100
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return str(self.percent)+"%"
graphical_dict=GraphicalDict()

class Window():
    def __init__(self,size=(0,0),graphical_object=None,clear_terminal=True,print_milliseconds=False):
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
        self.print_milliseconds=print_milliseconds
        self.end_character="" if clear_terminal==True else "\n"
        self.graphical_object=graphical_object

        #This part initializes the outer initializator
        self.graphical_initiator=GraphicalContainer(orientation=self.graphical_object.orientation,content=[self.graphical_object])#This is done so that Window initializes its graphical object in the same way as the other objects are initialized
        
        self.graphical_initiator.pos=(0,0)
        self.graphical_initiator.cursor=(0,0)
        self.graphical_initiator.size=self.size
        graphical_dict.reset()

        graphical_dict.init_list.append(self.graphical_initiator)
    def update(self):
        if self.print_milliseconds:
            start_time=datetime.datetime.now()
        for graphical_initiator in graphical_dict.init_list:
            graphical_initiator.initialize_content()
        graphical_dict.init_list=[]
        
        outstring=""
        outstring=graphical_dict.to_string(self.size)
        if self.clear_terminal:
            os.system('cls' if os.name=='nt' else 'clear')
        print(outstring,end=self.end_character)
        if self.print_milliseconds:
            end_time=datetime.datetime.now()
            print((end_time-start_time).microseconds)
    def get_input(self):
        pass#TODO: implement input logic

class GraphicalObject():
    """A simple graphical object which has some parameters, such as a position (example: (0,0) ) and a size (example: (10,10) )"""
    def __init__(self,size_value=Percent(100),framed=0,clear=True):
        self._outer_object=None#This variable should be used to indicate which GraphicalContainer contains this object; when the variable is created but not initialized, this is set to None
        self.pos=(-1,-1)
        self.cursor=(-1,-1)
        self.size=(-1,-1)
        self._size_value=0#The first time the value is set, it uses the internal variable in order to not call the setters, which are meant for post-initialized use
        self.size_value=size_value
        self.framed=framed
        self.init_times=0#How many times this object has been initialized
        self.clear=clear
    
    def graphical_initialization(self):
        """Inserts the correct data in the graphical dictionaries"""
        if self.clear:
            graphical_dict.clear(self.pos,self.size,self._outer_object.size)
        if self.framed!=0:
            graphical_dict.add_frame(self.framed,self.pos,self.size,self._outer_object.size)

    @property
    def size_value(self):
        return self._size_value
    @size_value.setter
    def size_value(self,value):
        if self._outer_object!=None:
            if self._outer_object not in graphical_dict.init_list:
                graphical_dict.init_list.append(self._outer_object)#Appends the outer class to the init class so that it is reinitialized when modified
        self._size_value=value
        
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        output_dict={"pos":self.pos,"size":self.size,"size_value":self.size_value,"type":str(type(self))}
        if str(type(self).__bases__[0])=="<class 'FegGUI.FegGUI.GraphicalContainer'>":
            output_dict["content"]=self.content
        return str(output_dict)

class GraphicalContainer(GraphicalObject):
    """A Graphical Object made to hold things in itself; being the one which holds other objects, this class is the one which initializes its content"""
    def __init__(self,size_value=Percent(100),content=[],orientation="",framed=0,fix_percent=1,padding=(0,0,0,0),clear=True):
        """Padding goes clockwise starting from the left"""
        GraphicalObject.__init__(self,size_value,framed=framed)
        self.clear=clear
        self.content=content
        self.orientation=orientation
        self.fix_percent=fix_percent
        self.padding=padding

    def initialize(self,target_object,value=0,only_maths=False):
        """Initializes target_object, defining its mathematical values, such as pos and size. If only_maths is set to Ture, only values will be calculated"""
        target_object.pos=(self.cursor[0],self.cursor[1])#Set the position to the drawing cursor
        if self.orientation=="vertical":#TODO: should add a one line way to do this
            target_object.size=(self.size[0],value)#Sets the size depending on the percentage
            if not only_maths:
                self.cursor=(self.cursor[0],self.cursor[1]+target_object.size[1])
        elif self.orientation=="horizontal":
            target_object.size=(value,self.size[1])#Sets the size depending on the percentage
            if not only_maths:
                self.cursor=(self.cursor[0]+target_object.size[0],self.cursor[1])
        
        target_object._outer_object=self

        if not only_maths:
            target_object.graphical_initialization()
        
            if str(type(target_object).__bases__[0])=="<class 'FegGUI.FegGUI.GraphicalContainer'>":
                target_object.pre_initialize_content()
                target_object.initialize_content()

    def pre_initialize_content(self):
        """An empty function made in case any child class needs to do things before initializing its content"""
        pass
    def initialize_content(self):
        """Initialize all of the GraphicalObject classes contained in the content variable given when creating the class. It should always be kept in mind that the elements are initialized starting from the values of the container in which they are"""
        self.cursor=self.pos #Sets the cursor back to the smallest coordinate for this object
        self.cursor=(self.cursor[0]+self.padding[0],self.cursor[1]+self.padding[1])
        if self.init_times==0:#Makes sure padding is only applied the first time
            self.size=(self.size[0]-(self.padding[0]+self.padding[2]),self.size[1]-(self.padding[1]+self.padding[3]))
        else:
            self.size=self.size
        if self.orientation=="horizontal":
            ori=0
        elif self.orientation=="vertical":
            ori=1

        for element in self.content:
            if str(type(element))=="<class 'FegGUI.FegGUI.TextBox'>":
                self.initialize(element,value=self.size[ori],only_maths=True)
                """print(self.size)
                element.size=(self.size[0],element.size[1])"""

        sizes=self.get_ideal_size(self.size[ori],[element.size_value for element in self.content])
        self.init_times+=1

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
            if total_size>0:
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
        """if sum(output_size)>total_size:
            raise SizeValueError(self)#TODO: there is a better way. Should add limits to objects"""
        return output_size

class Column(GraphicalContainer):
    def __init__(self,size_value=Percent(100),content=[],framed=0,fix_percent=1,padding=(0,0,0,0)):
        GraphicalContainer.__init__(self,size_value,content,orientation="vertical",framed=framed,fix_percent=fix_percent,padding=padding)
class Row(GraphicalContainer):
    def __init__(self,size_value=Percent(100),content=[],framed=0,fix_percent=1,padding=(0,0,0,0)):
        GraphicalContainer.__init__(self,size_value,content,orientation="horizontal",framed=framed,fix_percent=fix_percent,padding=padding)
class Rectangle(GraphicalObject):
    """A GraphicalObject which can't contain anything, but can be represented as a frame"""
    def __init__(self,size_value=Percent(100),framed=0):
        GraphicalObject.__init__(self,size_value,framed=framed)

class TextBox(GraphicalContainer):
    """A GraphicalObject which contains text"""
    def __init__(self,size_value=Percent(100),framed=0,clear=False,text="Text",wrap=True):
        """If the size_value is set to 'rel' and the orientation of the outer object is vertical, the size_value will return a value equal to the total lenght of the lines of this object"""
        GraphicalContainer.__init__(self,size_value,framed=framed,clear=clear,orientation="vertical")#TODO: add clear to other inits
        self.text=text
        self.wrap=wrap

    @property
    def size_value(self):
        output_value=self._size_value
        if self._outer_object.orientation=="vertical" and output_value=="rel":
            output_value=len(self.text_to_lines())#TODO: should add a limit if percentage or normal size was previously set
        else:
            pass
        return output_value
    @size_value.setter
    def size_value(self,value):
        self._size_value=value

    def pre_initialize_content(self):
        lines=self.text_to_lines()
        self.content=[]
        for line in lines:
            self.content.append(Text(clear=self.clear,text=line))
    
    def text_to_lines(self):
        if self.wrap:
            lines=wrap(self.text,self.size[0])
        else:
            lines=[self.text[i:i+self.size[0]] for i in range(0,len(self.text),self.size[0])]
        return lines
    
class Text(GraphicalObject):
    """The text contained in a TextBox"""
    def __init__(self,size_value=1,clear=True,text="Text"):
        GraphicalObject.__init__(self,size_value,clear=clear)
        self.text=text
    def graphical_initialization(self):
        graphical_dict.add_text(self.pos,self.size,self.text,self._outer_object.size)