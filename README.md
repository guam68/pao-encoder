# pao-encoder


## Overview

The [PAO (Person-Action-Object)](https://artofmemory.com/wiki/Person-Action-Object_(PAO)_System) system is a technique used to memorize long numbers. It does this by dividing the numbers into small chunks and encoding them into images. These images are then usually stored in memory using a [memory palace](https://artofmemory.com/wiki/Memory_Palace). 

I had been looking for an excuse to make a command line interface for something and found this to be a nice opportunity. A while back I had created a shortened version of the PAO system using only people and objects. While I can quickly encode/decode numbers I use regularly, I find that the process is quite slow for other numbers. This program will be used to quickly encode numbers and can also be used as a testing program to keep unused numbers sharp. 

I realize that this somewhat goes against the spirit of using a system like PAO since I am essentially offloading brain work for the encoding step. I personally don't use the system to improve my cognitive abilities but rather as a means to quickly access important numbers without having to look them up. Encoding is by far the slowest process for me and I don't want to have to waste brain power on it. Basically, I'm lazy.


## Functionality

### Training Mode
Gives random word association chunks for the user to decode into the proper number. Output lets the user know if the guess was incorrect and the time it took to decode the number. Upon exit, will show the user decode accuracy, fastest decode time, slowest decode time, and average decode time.


### Options

**-n 1234**

The number to be encoded

**-m MODE**

The default mode is the standard pao if unset. Options are available for those who use a condensed or similar systems (Dominic, etc).

    options:  - training: Enters training mode
              - pa: Only encodes based on person/action
              - po: Only encodes based on person/object
              - ao: Only encodes based on action/object

ex. -m pa 134388
    -m training
    

**-f FILENAME.xlsx**

The program will automatically look for a file named pao.xlsx for its encoding. This will allow the user to encode from an alternate file.

**-r NUMBER VISUAL REPLACEMENT**

Allows the user to tweak the word associated with a number. The first argument is the number for which the word is to be replaced. The second is which visual associated with that number to be targeted. The last argument is the word that will replace the current association. 

    visual options (2nd arg):   p: person
                                a: action
                                o: object

ex.     -r 12 p "Abraham Lincoln"

**-h

Shows available options