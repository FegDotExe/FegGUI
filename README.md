# FegGUI
It's just a stupid GUI lib I made for python after being tired of not understanding anything about complex real gui libraries in Py and c#

## How it works
You just create a Window class and give it a graphical object of your choice. The window will handle the initialization of the given object, setting its values depending on the specified properties.
In order to print the window, just use the `Window.update()` method
Here's an example:
```Python
this_window=FegGUI.Window(graphical_object=FegGUI.Rectangle(percentage=100,framed=2))
this_window.update()
```

# Graphical objects
## Graphical containers
These are objects which can contain other objects; 
The current graphical containers are `FegGUI.Row`, which displays items horizontally and `FegGUI.Column`, which displays items vertically
### Content
The `content` variable is the most important in a graphical container: it's a list of all the graphical objects a container contains.
Here's an example:
```Python
this_window=FegGUI.Window(graphical_object=FegGUI.Row(percentage=100,content=[
    FegGUI.Rectangle(percentage=50,framed=2),
    FegGUI.Rectangle(percentage=50,framed=2)
]))
this_window.update()
```
### Padding
In order to specify how much space should be left around the object, you can use the `padding` property, which starts from the left and goes clockwise.
Here's an example:
```Python
this_window=FegGUI.Window(graphical_object=FegGUI.Row(percentage=100,padding=(2,1,2,1),content=[
    FegGUI.Rectangle(percentage=50,framed=2),
    FegGUI.Rectangle(percentage=50,framed=2)
]))
this_window.update()
```