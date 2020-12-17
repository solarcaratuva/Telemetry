#!/bin/sh

touch ttyS10
touch ttyS11


chmod 666 ttyS10
chmod 666 ttyS11


#raw means passing of input output almost unfiltered
#pty generates pseudo terminal to let this happen
#-u indicates unidirectional transfer (one is to write into and the other is to read out of)
socat -u -u pty,raw,echo=0,link=ttyS10 pty,raw,echo=0,link=ttyS11 &
