# py_label_printer
> Easy way to print labels/stickers via reportlab to pdf in Python

Canvas is used to draw elements. The library takes care of dimensions, positioning, duplication and cutting marks.

### Please Note:
All units are in millimeters! 

### Usage 
```python
L = LabelPage(size=(X, Y), cnt=(X, Y), space=(X, Y), LeftBottom=(X, Y), pagesize=A4, filename="output.pdf")
```

| Paramter | Description | Datatype | Default |
| :---:     | :--- | :---: | :---: |
| ```size=(X, Y)``` | defines the size of the label | tuple(float, float) | - |
| ```cnt=(X, Y)```  | defines the number of labels in both directions | tuple(float, float) | -
| ```space=(X, Y)```  | defines the spacing between two labels in both directions | tuple(float, float) | ```(0, 0)``` |
| ```LeftBottom=(X, Y)```  | defines the distance between the lower left corner of the sheet and the lower left corner of the lower left label. if not specified all labels are centered| tuple(float, float) | ```None``` or ```[None, None]``` |
| ```pagesize=(X, Y)```  | defines the size of she sheet| tuple(float, float) | DIN A4 |
| ```filename="output.pdf```  | defines the path and the filename of the output. Practical use is: ```filename=__file__[:-2]+"pdf"``` | string | ```"Label_Lib.pdf"``` |

### Get the canvas object
You need the canvas object for drwaing. You can find the command set in the reportlab docs.
```python
c = L.get_canvas_object()
```

### Iteration through the labels
You can simple go through the labels with a for loop:
```python
for i in L.iter_label():
    c.drawString(10, 20, "Your Text")
```
If no parameter set in ```iter_label()``` it will fill exactly one sheet. The counter ```i``` returns the number of the label, starts with 0. The number is calculated from cnt(X * Y).

#### Iteration with data
Give ```iter_label(data)``` a list of data to iterate through the data:
```python
data = [{"color": "red", "name":"Hans"}, {"color": "green", "name":"Klaus"}, {"color": "blue", "name":"Fritz"}]
for i in L.iter_label(data):
    c.drawString(10, 20, i["color"])
    c.drawString(20, 20, i["name"])
```
There are exactly so many labels drawn, how many entries the list has. If there are more than fit on one page, a new page is started automatically.

### Finishing
To finish and save use:
```
L.save()
```
After saving you can show the pdf file with your default viewer:
```
L.show()
```
Or print it with your default viewer and default printer automaticly:
```
L.print()
```

### Frame
With this function, you can easily check the accuracy of fit when you first print on a sheet of paper. Place this with one side of the sticker on top of the other and hold it against the light.
```python
L.setFrame(thickness = 0.5, spacing=0.0, round=False)
```
| Paramter | Description | Datatype | Default |
| :---:     | :--- | :---: | :---: |
| ```thickness=0.5``` | defines the thickness | float | ```0.5``` |
| ```spacing=0.0``` | defines the spacing relativ to the label | float | ```0.0``` |
| ```round=False``` | defines the rounding of the corner | float | ```False``` |

### Cutting Marks
Cutting marks are for automated cutting machines. You can choice between inner and outer cutting marks.
##### Outer Cutting Marks
Outer cutting marks are on the four corners of all labels on a page.
```python
L.setMarksOuter(thickness = 0.5, spacing=5.0)
```
| Paramter | Description | Datatype | Default |
| :---:     | :--- | :---: | :---: |
| ```thickness=0.5``` | defines the thickness | float | ```0.5``` |
| ```spacing=0.0``` | defines the spacing relativ to the label | float | ```5.0``` |

##### Inner Cuttin Marks
Inner cutting marks are at every corner of each label.
If the labels are close together, this method is not recommended.
```python
L.setMarksInner(thickness = 0.5, spacing=5.0)
```
| Paramter | Description | Datatype | Default |
| :---:     | :--- | :---: | :---: |
| ```thickness=0.5``` | defines the thickness | float | ```0.5``` |
| ```spacing=0.0``` | defines the spacing relativ to the label | float | ```5.0``` |

### Datamatix
Because the Datamatix code in Reportlab does not work properly, an alternative (via pyStrich) is available here.
```
L.draw_datamatrix(data, x, x, size, anchor='C')
```
| Paramter | Description | Datatype | Default |
| :---:     | :--- | :---: | :---: |
| ```data``` | defines the data of the barcode | string | - |
| ```x``` | x position of the Barcode | float | - |
| ```y``` | y position of the Barcode | float | - |
| ```size``` | size of the Barcode | float | - |
| ```anchor``` | anchor for placing in canvas ('C'=center, 'N'=north, 'SW'=south-west...)| string | ```'C'``` |