#include <boost/asio.hpp>
#include <iostream>

#define SERIAL_PORT "/dev/serial0" // Replace with your serial port
#define BAUD_RATE 9600 // Replace with your baud rate

int main() {
    boost::asio::io_service io;
    boost::asio::serial_port serial(io, SERIAL_PORT);

    serial.set_option(boost::asio::serial_port_base::baud_rate(BAUD_RATE));

    char c;
    while (true) {
        boost::asio::read(serial, boost::asio::buffer(&c,1));
        std::cout << c;
    }

    return 0;
}
