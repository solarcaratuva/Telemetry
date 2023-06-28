# Set the compiler
CC = g++

# Set the build target
TARGET = writetest

# Set any compile flags
CFLAGS = -Wall -std=c++11

# Set any required libraries
LDFLAGS = -lrt -lpthread

all: $(TARGET)

$(TARGET): main.cpp
	$(CC) $(CFLAGS) -o $(TARGET) main.cpp $(LDFLAGS)

clean:
	rm $(TARGET)
