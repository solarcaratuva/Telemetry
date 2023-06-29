#include <boost/asio.hpp>
#include <iostream>
#include <fstream>

#define BAUD_RATE 19200 // Replace with your baud rate

std::string get_available_port() {
    std::ifstream check_port;

    check_port.open("/dev/ttyUSB0");
    if(check_port) {
        return "/dev/ttyUSB0";
    }

    check_port.close();
    check_port.open("/dev/ttyUSB1");
    if(check_port) {
        return "/dev/ttyUSB1";
    }

    return "";
}

int main() {
    std::string port = "/dev/canUART";
    if(port.empty()) {
        std::cerr << "No available port found" << std::endl;
        return 1;
    }

    boost::asio::io_service io;
    boost::asio::serial_port serial(io, port);
    serial.set_option(boost::asio::serial_port_base::baud_rate(BAUD_RATE));

    char c;
    while (true) {
        boost::asio::read(serial, boost::asio::buffer(&c,1));
//        std::cout << (int) c << "\n";
        if((int) c == 249) {
            char msg[24];
            for(int i=0; i<24; ++i) {
                boost::asio::read(serial, boost::asio::buffer(msg + i, 1));
            }
            int message_id = msg[0]*0x0100+msg[1];
            if(message_id == 1030) { // Detected message with ID 1046
                printf("battery message msg: id: %d data: ", message_id);
                for(int i=0; i<24; ++i) {
                    printf("%c", msg[i]);
                }
                printf("\n");
            }
        }
    }

    return 0;
}
