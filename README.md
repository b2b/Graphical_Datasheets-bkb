# Graphical Datasheets for MCUs from csv file

Python script used to help generate the graphical datasheets.


# Step 1
download and install svgwrite
https://bitbucket.org/mozman/svgwrite/downloads/
```
cd [downloaded Directory]/svgwrite-1.1.9
python setup.py install
```

# Step 2
download and extract bkb_tagscript.py
https://github.com/b2b/Graphical_Datasheets-bkb/archive/master.zip

```
cd [downloaded Directory]/Graphical_Datasheets-master
python bkb_tagscript.py
```
**Enter file name minus .csv extension (eg. ESP8266/Thing):**
```
Datasheets/ATMEL2560/ATMEL2560-16AU
```
*End of File, the output is located at Datasheets/ATMEL2560/ATMEL2560-16AU.svg*

[![Video](http://img.youtube.com/vi/skr3AqV6k20/0.jpg)](http://www.youtube.com/watch?v=skr3AqV6k20)

# RAW Result and final example

| svg img generated by the script| Modified in Inkscape | 
| ------------- |:-------------:| 
| <img src="https://github.com/b2b/Graphical_Datasheets-bkb/blob/master/Datasheets/ATMEL2560/ATMEL2560-16AU.svg" width="240px">     |<img class=myimage src="https://github.com/b2b/Graphical_Datasheets-bkb/blob/master/Datasheets/ATMEL2560/ATMEL2560-16AU_ok.svg" width="240px"> | 
# csv file usage
| Name|  | 
| ------------- |:-------------:| 
| Row 1| name of the PIN types This will be the **Legend** | 
| Left| this row is emty (everything below this will be on the left side of the board| 
| Right| this row is emty (everything below this will be on the left side of the board| 
| Text| this row is emty (everything below this will texts below the rows|
| Extras| this row is emty (everything below this will **linked** as image from **Images** folder| 
| EOF| this is the last row. This row is emty (End of file) |


2017.09.23 this is the modified version of Sparkfun Graphical Datasheets
- added groups of shapes
- added groups of text
- added group of row Header

[svgwrite doc](http://svgwrite.readthedocs.io/en/master/overview.html)


This repo includes the Python script used to help generate the graphical datasheets.  It also includes the final .svg, and .pdf files as well as the .csv files use.  The .csv files were used as a starting point and some text did change between the file and the final version.  There is also a User Submitted folder for external contributions.

For more information on the graphical datasheets check sparkfun blog post on them.
https://www.sparkfun.com/news/1947

(how to install svgwrite http://www.schoolcoders.com/projects-inkscape-intro-2)
