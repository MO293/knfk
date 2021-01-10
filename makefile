CXX = g++
CXXFLAGS = -Wall
LFLAGS =

OBJS = main.o

all: program

program: $(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@
	
clean:
	rm -f *.o program
	
.PHONY: all clean
