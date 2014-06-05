radiation.so: radiation.o
	gcc -w -shared -o radiation.so radiation.o -lc
 
radiation.o: radiation.c
	gcc -w -fPIC -g -c -Wall radiation.c