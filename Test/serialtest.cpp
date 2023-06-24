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
    std::string port = get_available_port();
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
        std::cout << (int) c << "\n";
        if((int) c == 249) {
            char msg[24];
            for(int i=0; i<24; ++i) {
                boost::asio::read(serial, boost::asio::buffer(msg + i, 1));
            }
            int message_id = msg[0]*0x0100+msg[1];
            if(message_id == 1046) { // Detected message with ID 1046
                printf("msg: id: %d data: ", message_id);
                // assuming message_data is uint8_t[]
                uint16_t low_cell_voltage = ((uint16_t) (msg[2] << 8)) | (uint16_t) msg[3]; // Extract 16-bit signal starting at byte index 3
                uint8_t low_cell_voltage_id = msg[4]; // Extract 8-bit signal at byte index 5
                uint16_t high_cell_voltage = (msg[5] << 8) | msg[6]; // Extract 16-bit signal starting at byte index 6
                uint8_t high_cell_voltage_id = msg[7]; // Extract 8-bit signal at byte index 8
                printf("Low Cell Voltage: %.4f V, ID: %d, High Cell Voltage: %.4f V, ID: %d\n",
                       low_cell_voltage*0.0001, low_cell_voltage_id, high_cell_voltage*0.0001, high_cell_voltage_id);
                for(int i=2; i<8; ++i) {
                    for(int j=0; j<8; ++j) {
                        std::cout << ((msg[i] >> j) & 1);
                    }
                    std::cout << " ";
                }
                std::cout << "\n";
            }
        }
    }

    return 0;
}
