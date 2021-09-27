# FegGUI
It's just a stupid GUI lib I made for python after being tired of not understanding anything about complex real gui libraries in Py and c#

Mind that the documentation here is reaaaaaally incomplete, even though I'm working on completing it

## How it works
### Simple explanation
You just create a Window class and give it a graphical object of your choice. The window will handle the initialization of the given object, setting its values depending on the specified properties.
For more info about graphical objects, look at the section I wrote about them down here!
In order to print the window, just use the `Window.update()` method.

Here's an example:
```Python
this_window=FegGUI.Window(size=(20,10),graphical_object=FegGUI.Row(content=[
    FegGUI.Rectangle(size_value=FegGUI.Percent(100),framed=2)
]))
this_window.update()
```
And here's the output:
```
┏━━━━━━━━━━━━━━━━━━┓
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┗━━━━━━━━━━━━━━━━━━┛
```
### More complex and useful explanation
When you specify a `graphical_object` for a `FegGUI.Window` class, a class of the same type is create, whose only content is a deepcopy of the `graphical_object`.

This is done because `FegGUI.GraphicalObject` classes need to be initialized by the `FegGUI.GraphicalContainer` which contains them, giving them the fundamental properties such as size and position.

This is how initialization works (the mentioned object is the inner object): Variables are set → The object is initialized graphically through the function `FegGUI.GraphicalObject.graphical_initialization` → If the object is a GraphicalContainer, it initializes its content through the function `FegGUI.GraphicalContainer.initialize_content`

# Graphical objects
Graphical objects are objects used to draw things on the screen. They can be either visible or not, depending on what you whish to do with them.
They can either be empty graphical objects (which inherit `FegGUI.GraphicalObject`) or graphical containers  (which inherit `FegGUI.GraphicalContainer`, which again inherits `FegGUI.GraphicalObject`).

Graphical objects fundamentally have a `pos` variable, which expresses their position on the terminal, starting from the top left (Yeah that's not really an hortodox approach to xy coordinates but I did it like this so yeah you can just accept what I did) and a `size` variable, which expresses how big the object is for the two axis.

The values just mentioned up here are automatically set by graphical containers when they are initialized. If a Graphical object is meant to occupy 100% of a container, then when the container initializes said object it sets the object's `size` value to its own size, and same can be said for the `pos` variable.
In the example down here, the frame we see comes from the Rectangle which occupied 100% of the Row.
```Python
this_window=FegGUI.Window(size=(20,10),graphical_object=FegGUI.Row(content=[
    FegGUI.Rectangle(size_value=FegGUI.Percent(100),framed=2)
]))
this_window.update()
```
Output:
```
┏━━━━━━━━━━━━━━━━━━┓
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┗━━━━━━━━━━━━━━━━━━┛
```
## Graphical containers
These are objects which can contain other objects; 
The current graphical containers are `FegGUI.Row`, which displays objects horizontally and `FegGUI.Column`, which displays objects vertically

Here's a list of their properties:
 - [GraphicalContainer.content](https://github.com/FegDotExe/FegGUI#graphicalcontainercontent)
 - [GraphicalContainer.padding](https://github.com/FegDotExe/FegGUI#graphicalcontainerpadding)
### GraphicalContainer.content
The `content` variable is the most important in a graphical container: it's a list of all the graphical objects a container contains.

Here's an example:
```Python
this_window=FegGUI.Window(size=(20,10),graphical_object=FegGUI.Row(content=[
    FegGUI.Rectangle(size_value=FegGUI.Percent(50),framed=2),
    FegGUI.Rectangle(size_value=FegGUI.Percent(50),framed=2)
]))
this_window.update()
```
And here's the output:
```
┏━━━━━━━━┓┏━━━━━━━━┓
┃        ┃┃        ┃
┃        ┃┃        ┃
┃        ┃┃        ┃
┃        ┃┃        ┃
┃        ┃┃        ┃
┃        ┃┃        ┃
┃        ┃┃        ┃
┃        ┃┃        ┃
┗━━━━━━━━┛┗━━━━━━━━┛
```
### GraphicalContainer.padding
In order to specify how much space should be left around the contained objects, you can use the `padding` property, which starts from the left and goes clockwise.

Here's an example:
```Python
this_window=FegGUI.Window(size=(20,10),graphical_object=FegGUI.Row(padding=(2,1,2,1),framed=1,content=[
    FegGUI.Rectangle(size_value=FegGUI.Percent(50),framed=2),
    FegGUI.Rectangle(size_value=FegGUI.Percent(50),framed=2)
]))
this_window.update()
```
And here's the output:
```
┌──────────────────┐
│ ┏━━━━━━┓┏━━━━━━┓ │
│ ┃      ┃┃      ┃ │
│ ┃      ┃┃      ┃ │
│ ┃      ┃┃      ┃ │
│ ┃      ┃┃      ┃ │
│ ┃      ┃┃      ┃ │
│ ┃      ┃┃      ┃ │
│ ┗━━━━━━┛┗━━━━━━┛ │
└──────────────────┘
```