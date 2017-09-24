#!/usr/bin/python
#http://www.astro.ufl.edu/~warner/prog/python.html  - Python Basics if you want to learn some Python
#https://pypi.python.org/pypi/svgwrite/  - Library this script uses
#install Python27, download svgwrite, from svgwrite folder run "C:\Python27\python setup.py install"

# 2017.09.22 modified by eskolarateskolardotcom 
# added group feature for lined-up rects and lined up texts
# added group feature for all rects an all texts which are positioned near the page
# to use them in inkscape layers
# modified len(line)-1 to remove the last coloured cell
# from first row it makes a group at the bottom of page 

# This script starts by asking for a file, this name is saved as 'myfile'
# Input file is a 'myfile'.csv and is referred to as file
# Be careful what characters you use.  This is a comma deliminated file, so using a comma in your text will cause problems.  
# Also, some applications will change characters to non-standard characters you will get an error (" - " is often to a larger dash that is non standard)
# Output file is a 'myfile'.svg and is defined before the while loop
# The script is setup for 13 fields, to add more change the global fields variable and add another section to the writeField function with the colors you want.
# If the following words are in field 1 of a line it will change the structure of the output blocks to fit that heading "Left, Right, Top, Text, Extras"
# Text will not make a box, but make a new row of text for each field, each line will be a different section of text, this section must be after blocks
# Extras will look for a file in the folder /Images called value.png and add it to the svg, useful for things like ISP headers graphic, etc. (I'm not actually using this)
# File is read until field 1 is "EOF"

import os
import svgwrite
import time

################################################## GLOBAL VARIABLES ########################################

row=0 #row starts at the top
height=12 #height of a box
width=45 #width of a box
rowheight=15 #height of a row (leaving enough space between rows to move)
rowwidth=48 #width of a 'spot', basically width plus a few
fields=13 # number of fields 
documentWidth = rowwidth*fields +50 #maximum width the document should be
documentHeight = 2250 #this is  guess since we need to make the document before we know the file size, doesn't really matter anyway
direction = 'r' #which direction the tag is facing, staring out with labels on the right
offset=0 #this is where we start, for the left we will start on the right side of the page
previoustext = 0 #for text function, defines how much text we have already written so we know where to start
textheight=17 #how much we add each time we add a line of text
textstart=100 #where a block of text will start (y axis), this will be set in the code
myfile="ProMini" #file read in to be parsed
fontsize=10 #bkb
imagewidth=250
imageheight=250
indent = 1      # move text to the right
adjust = -2     # move text down (negative for up)


# "Theme"
#   Name,           Power,        GND,      Arduino Digital,  Arduino Analog,
#   Port,           Serial,       I2C/SPI,  PWM,              ADC,
#   Ext Interrupt,  PC Interrupt, Misc,     Misc2,            extra
# bkb added 2x blue
tcolor   = ['white', 'red',     'black',    '#FF0000',  '#000080', 
            'black',  'navy',   'yellow',   'black',    'purple', 
            'orange', 'orange', 'blue',     'blue',     'red']

# bkb added 2x 0.1 for blue
topacity = [ 0.3,     1,          0.9,        0.8,        1,     
             0.6 ,    0.8,        0.8,        0.3,      0.5,      
             0.8,     0.4,        0.3,        0.1,      0.1  ]

################################################# FUNCTIONS ###################################################

#Writes plain text from the text section
def writeText(i,value,row):
  
  text = dwg.add(dwg.text(str(value), insert=(0,textstart),font_size=12, font_family='Montserrat', fill='black'))
  #print ("Printing " + str(value) + " at " + str(textstart))
  global previoustext
  previoustext = previoustext + textheight  
  #end writeText

# Creates colored blocks and text for fields
def writeField(type, value, row, spot, direction, GrpName, GrpLineNameText, cellWidth):
    x = spot * rowwidth + offset
    y = row * rowheight

    color = tcolor[type]  # fill color of box
    crect = color         # color for rectangle around box
    ctext = 'black'       # default text color: black

    if color == 'white':  # white boxes get black outlines
        crect = 'black'

    if (color == 'black' or color == '#000080' or color == '#FF0000' or color == 'navy'):  # don't write black-on-black
        ctext = 'white'
   
    #if ( value!='' or value!=' '):
    myString = str(value)
    myString = myString.strip()
    # finding nasty empty strings
    #print ("myString: " + myString) 
    #print [ord(c) for c in myString]
    if myString:
        #print ("myString: " + myString) 
        # Box
        #dwg.add(dwg.rect(
        #shapes.add(dwg.rect(
            #(x, y), (width, height), 1, 1,
            #stroke = crect, opacity = topacity[type], fill = color
            #))
     
        GrpLineName.add(dwg.rect(
              (x, y), (cellWidth, height), 1, 1,
              stroke = crect, opacity = topacity[type], fill = color
            ))
         

        # Text
        #dwg.add(dwg.text(
            #str(value), insert = (x + indent, y + height + adjust),
            #font_size = fontsize, font_family='Montserrat', fill = ctext
            #))
        GrpLineNameText.add(dwg.text(
            str(value), insert = (x + indent, y + height + adjust),
            font_size = fontsize, font_family='Arial', font_weight='bold', fill = ctext
            ))


#adds images to end of document, currently not used as pngs don't work as well as I'd like and it is easier to just drag and drop the files I want into the final file.
def writeImages(i,value,row):
  global previoustext
  currentimage = "Images/" + value + ".png"
  if os.access(currentimage, os.R_OK):
    print "Adding " + currentimage
    image = dwg.add(dwg.image(href=("../" +  currentimage), insert=(i*imagewidth,textstart)))
  else:
    print "Could not find " + currentimage  
#end writeImages




#open file with read access
myfile = raw_input("Enter file name minus .csv extension (eg. ESP8266/Thing): ")
if os.access(myfile +".csv", os.R_OK):
  file = open(myfile +".csv","r")
  print "File opened"
else:
  print "File not found, please try again, there should be a comma deliminated csv file with the data in it.  See script for more details"
  time.sleep(10)
  os._exit(0)

#read in each line parse, and send each field to writeField  
rawline="not empty"
dwg = svgwrite.Drawing(filename=str(myfile+".svg"), profile='tiny', size=(documentWidth,documentHeight))
documentWidthPlus = documentWidth + 200
#https://stackoverflow.com/questions/23033796/shift-svg-objects-towards-origin
# these groups hold all shapes rows and text rows
grpAllshapes = svgwrite.container.Group(id='grpAllshapes', transform='translate('+str(documentWidthPlus)+',0)')
grpAllText = svgwrite.container.Group(id='grpAllText', transform='translate('+str(documentWidthPlus)+',0)')

while (rawline!=""):
  rawline  = file.readline()
  line = rawline.split(",") #Split into fields separated by ","
  row=row+1
  spot=0
  TheGrpName = "grpLine"+str(row)
  TheGrpNameText = "grpLineText"+str(row)
  GrpLineName = dwg.add(dwg.g(id=TheGrpName))
  GrpLineNameText = dwg.add(dwg.g(id=TheGrpNameText))
  cellWidth = width
  if(row ==1):      
    #cellWidth = width*2
    myline = line;
  #else:
    #cellWidth = width
       
  
  if (line[0] == "Left"):
    direction = "l"
    offset = documentWidth - rowwidth
    line[0] = ""
  if (line[0] == "Right"):
    direction = "r"
    offset = 0
    line[0] = ""
  if (line[0] == "Top"):
    direction = "r"
    offset = 0
    line[0] = ""
  if (line[0] == "Text"):
    offset = 0
    line[0] = ""
    direction = "text"
  if(line[0] == "Extras"):
    offset=0
    line[0]=""
    direction = "extras"
  if (line[0] == "EOF"): #if we are done
    dwg.save()
    break
  if (row>1): # don't build the header first row in csv file. I put it into footer
    for i in range(0, len(line)-1): #go through total number of fields      
        if(line[i]!="" and direction=='r'):        
          writeField(i,line[i],row, spot, direction, GrpLineName, GrpLineNameText, cellWidth) #call function to add that field to the svg file
          spot=spot+1 #move 'cursor' one spot to the right		
        if(line[i]!="" and direction=='l'):
          writeField(i,line[i],row, spot, direction, GrpLineName, GrpLineNameText, cellWidth) #call function to add that field to the svg file
          spot=spot-1 #move 'cursor' one spot to the left
      
        if (line[i]!="" and direction == "text"):
           textstart = row*rowheight+previoustext
           writeText(i,line[i],row)
            
        if (line[i]!="" and direction == "extras"):
          writeImages(i,line[i],row)
                      
    grpAllText.add(GrpLineNameText)
    grpAllshapes.add(GrpLineName)
    
dwg.add(grpAllshapes)
dwg.add(grpAllText)
#end of while

# footer
# this builds a map from the rowHeader
for i in range(0, len(myline)-1):
  row=row+1
  cellWidth = width*2
  direction = "l"
  offset = documentWidth + 200
  writeField(i,myline[i],row, spot, direction, GrpLineName, GrpLineNameText, cellWidth) #call function to add that field to the svg file
  
#end for  

print ("End of File, the output is located at " + myfile + ".svg")
dwg.save()
file.close()



