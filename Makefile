CXX := g++ -Wall -ggdb

INCLUDE := -Ilib/libpd/pure-data/src -Ilib/libpd/libpd_wrapper `pkg-config --cflags sndfile`
LIB := lib/libpd/libs/libpd.so  `pkg-config --libs sndfile`



all: barberism.o
	${CXX} -o barberism barberism.o ${LIB}

barberism.o: src/barberism.cpp
	${CXX} -o barberism.o ${INCLUDE} -c src/barberism.cpp

clean:
	rm -f barberism
	rm -f barberism.o
  
