#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::ofstream myFile;
    std::string filename = "/path/to/sdcard/example.txt"; // Replace with your actual path

    myFile.open(filename, std::ios::out);

    if (myFile.is_open()) {
        myFile << "Writing to SD card example." << std::endl;
        myFile << "Another line of text." << std::endl;
        myFile.close();
        std::cout << "Data written to " << filename << " successfully." << std::endl;
    } else {
        std::cerr << "Error opening " << filename << std::endl;
        return 1;
    }
    return 0;
}