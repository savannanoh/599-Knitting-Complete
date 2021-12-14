# Snake Designer
Code base for Savanna's final project for UW CSE 599: E-Textiles
Below I use the terms "bend" and "short rows" somewhat interchangeably.

## Requirement

In order to use the UI you will need to install tkinter. 
I think you can just run whatever you may usually use to install a package, followed by "tkinter"

## Important Files
The only files I've meaningfully added from the forked repo (599-Knitting-Complete) are test_tube.py and tube_ui.py. 
I may have made modifications to other files while experimenting, but I believe all the necessary updates are in these two files.

### test_tube.py
This file has methods for the non-user-facing parts of Snake Designer. 
If you want to generate KnitOut for a snake without using the UI, you can just run the code in this file.
If you choose to run from this file, the only two methods you should be calling directly are `test_multi_bend` and `Bend`'s constructor.

If you want to create a straight tube with no bends, you only need to call `test_multi_bend`.

If you want to create a tube with bends, you need to call Bend's constructor to create some bends to pass in to `test_multi_bend`.

#### Bend
`Bend` takes in a few parameters:
- `position`: an int representing the course number at which the bend should start
- `height`: the height of the short rows, which affects the severity of the bend
- `bend_dir`: an int representing where along the tube from 0 to the tube's circumference-1 the bend should begin

For example:
```
b1 = Bend(3, 4, 0)
```
Creates a Bend at the 3rd row of the tube that is 4 rows tall and that occurs at the 0th stitch in the round.

#### test_multi_bend
`test_multi_bend` takes in several parameters:
- `width`: the width of the tube, measured by the number of needles from a single bed. 
A width of n will produce a tube of circumference 2 * n.
- `end`: the number of rounds that should be added to the tube after the last set of short rows
- `bends`: a list of Bend objects to put on the tube
- `file`: the name of the file you want the KnitOut sent to. For example, setting `file="abc"` will output KnitOut to "abc.k". 
Giving the name of an existing file will cause an overwrite
- `carrier`: this is set to 3 by default. You can replace it with your chosen yarn carrier number

For example:
```
test_multi_bend(8, 4, [Bend(2, 1, 0), Bend(6, 2, 4)], "abc", 3)
```
Creates a tube of circumference 16, with two bends, one at the 2nd row that lasts for one row at the 0th stitch in the round, 
and the other at the 6th row that lasts for two rows and that starts at the 4th stitch in the round. 
The instructions will be output to a file called "abc.k" and carrier 3 will be used.

The KnitOut files from running this file will show up in the "tests" folder.

### tube_ui.py
This file has all the code for the Snake Designer interface. 
To run it, simply run this file.
You will see a very simple interface. 
The main part of the interface is a representation of the tube you are making.
You can adjust the tube's width and height using the sliders.
If you want to create just a straight tube, once you've adjusted the height and width to your liking you can enter a file name and then click "KNIT".
If you want to create some bends, simply click on the part of the tube you'd like the bend to go to.
An hourglass-like shape will appear showing you where your bend would go.
If you're happy with it, simply click "place", if you'd like to adjust the severity of the bend, you can do so with the slider.
If you change your mind, you can click "cancel".
Once you've started placing bends you can continue to adjust the width and height.
If you'd like to edit a bend you've placed, click on it and you can adjust its bendiness or remove it.
There is currently no way to move a bend, so if you want to move one you have to remove it and then create another where you'd want it to be.
When you're done placing the bends you want, you can enter a file name and then click "KNIT".

The KnitOut files from running this file will show up in the "ui" folder.
