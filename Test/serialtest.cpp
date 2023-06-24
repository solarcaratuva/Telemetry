#include <iostream>
#include <wiringPi.h>
#include <wiringSerial.h>

int main ()
{
    if (wiringPiSetup () == -1) {
        std::cerr << "Unable to setup wiringPi" << std::endl;
        return 1;
    }

    int serial_port;
    if ((serial_port = serialOpen ("/dev/ttyUSB0", 9600)) < 0 && (serial_port = serialOpen ("/dev/ttyUSB1", 9600)) < 0) { //change to the correct port and baud rate
        std::cerr << "Unable to open serial device" << std::endl;
        return 1;
    }

    while (true) {
        if (serialDataAvail (serial_port)) {
            char incomingByte = serialGetchar (serial_port);
            std::cout << incomingByte;
            fflush(stdout);
        }
    }

    return 0;
}
