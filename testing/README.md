# Rit Formula Racing
## HIL Testing 

##About: 
This is a tool used by the RIT formula team


## How to run:
Run from GUI Controller
Enter a file name or test to be run
    
    parameters: gui/cmd comPort baud 

## File format:
File should be formatted as a list of tests. Each test should have a new line. 
Comments in the file can be made on a new line indicated by "//". There must be a space between
SET/CHK pin number and on/off

There is also a comment for a delay which should be in between each line(?)
this is indicated by //delay

Example:

    // FILE NAME AND INFO
    // will test XXXX
    SET 03 0 
    CHK 03 0
    SND 03 0000000000000000

## Test format:
     SND/SET/CHK + pin number + 16-digit hex num/0/1
    

