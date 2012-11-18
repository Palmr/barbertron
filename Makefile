CXX := g++ -Wall -ggdb

INCLUDE := -Ilib/libpd/pure-data/src -Ilib/libpd/libpd_wrapper `pkg-config --cflags sndfile`
LIB := lib/libpd/libs/libpd.so `pkg-config --libs sndfile`


all: barberism.o
	${CXX} -o barberism ${LIB} barberism.o 

barberism.o: src/barberism.cpp
	${CXX} ${INCLUDE} -c src/barberism.cpp -o barberism.o

clean:
	rm barberism
	rm barberism.o
  
