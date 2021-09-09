import os
from math import ceil, floor


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
        i_y=0
        while i_y<size[1]:
            i_x=0
            while i_x<=size[0]:
                addendum=" "
                if i_x==0 and i_y==0:
                    if frame_type==2:
                        addendum="┏"
                elif 0<i_x<size[0]-1 and i_y==0:
                    if frame_type==2:
                        addendum="━"
                elif i_x==size[0]-1 and i_y==0:
                    if frame_type==2:
                        addendum="┓"
                elif (i_x==0 or i_x==size[0]-1) and 0<i_y<size[1]-1:
                    if frame_type==2:
                        addendum="┃"
                if i_x==0 and i_y==size[1]-1:
                    if frame_type==2:
                        addendum="┗"
                elif 0<i_x<size[0]-1 and i_y==size[1]-1:
                    if frame_type==2:
                        addendum="━"
                elif i_x==size[0]-1 and i_y==size[1]-1:
                    if frame_type==2:
                        addendum="┛"
                if addendum!=" ":
                    self.add_character(addendum,(position[0]+i_x,position[1]+i_y))
                i_x+=1
            i_y+=1
    def to_string(self,size):
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
graphical_dict=GraphicalDict()

class Window():
    def __init__(self,width=0,height=0,graphical_object=None):
        """Creates a new Window class. If no width or height values are given, they are set to the current terminal size, which is returned by os.get_terminal_size()"""
        if width!=0:
            self.width=width
        else:
            self.width=os.get_terminal_size()[0]-2
        if height!=0:
            self.height=height
        else:
            self.height=os.get_terminal_size()[1]-2
        graphical_object.pos=(0,0)
        graphical_object.cursor=(0,0)
        graphical_object.size=(self.width,self.height)
        graphical_dict.reset()
        graphical_object.initialize_content()
    def update(self):
        #Pretty useful for this: https://en.wikipedia.org/wiki/Box-drawing_character
        outstring=""
        outstring=graphical_dict.to_string((self.width,self.height))
        print(outstring)
    def get_input(self):
        pass#TODO: implement input logic

class GraphicalObject():
    def __init__(self,percentage=0,content=[],orientation="",framed=0):
        self.percentage=percentage
        self.pos=(-1,-1)
        self.cursor=(-1,-1)
        self.size=(-1,-1)
        self.orientation=orientation
        self.framed=framed
        self.content=content
    def initialize_content(self):
        """Initialize all of the GraphicalObject classes contained in the content variable given when creating the class"""
        #Sets the cursor back to the smalles coordinate for this object
        self.cursor=self.pos
        for element in self.content:
            self.initialize(element)
    def initialize(self,target_object):
        """Initializes target_object, defining its mathematical values"""
        target_object.pos=(self.cursor[0],self.cursor[1])#Set the position to the drawing cursor
        if self.orientation=="vertical":
            target_object.size=(self.size[0],floor((self.size[1]*target_object.percentage)/100))#Sets the size depending on the percentage
            self.cursor=(self.cursor[0],self.cursor[1]+target_object.size[1])#TODO: add an option to not add anything, in order to make compenetrating graphical objects
        if target_object.framed!=0:
            graphical_dict.add_frame(target_object.framed,target_object.pos,target_object.size)
        if len(target_object.content)>0:
            target_object.initialize_content()
    def __str__(self):
        output_dict={"pos":self.pos,"size":self.size}
        return str(output_dict)

class Column(GraphicalObject):
    def __init__(self,percentage=100,content=[],framed=0):
        GraphicalObject.__init__(self,percentage,content,orientation="vertical",framed=framed)