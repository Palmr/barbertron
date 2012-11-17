CXX := g++ -Wall -ggdb

INCLUDE := -Ilib/libpd/pure-data/src -Ilib/libpd/libpd_wrapper -O3
LIB := lib/libpd/libs/libpd.so

all: barberism.o
	${CXX} -o barberism ${LIB} barberism.o 

barberism.o: src/barberism.cpp
	${CXX} ${INCLUDE} -c src/barberism.cpp -o barberism.o

clean:
	rm barberism
	rm barberism.o
  
