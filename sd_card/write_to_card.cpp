#include <iostream>
#include <fstream>
#include <string>
#include <ctime>      // for time()
#include <cstdlib>    // for rand(), srand()
#include <utility>    // for std::pair

// Generate a random (message_id, value) pair.
std::pair<int,int> generate_data() {
    // For demonstration, message ID goes from 0..8
    int random_message_id = rand() % 3;

    int random_value;
    // If you want the range to depend on the message ID, you could do so:
    switch (random_message_id) {
        case 0: 
            random_value = rand() % 10;       // values 0..9
            break;
        case 1: 
            random_value = rand() % 20 + 10;  // values 10..29
            break;
        case 2:
            random_value = rand() % 30 + 30;  // values 30..59
            break;
        default:
            random_value = rand() % 100;      // values 0..99
            break;
    }

    return std::make_pair(random_message_id, random_value);
}

int main() {
    // Seed the random number generator. Without this, you'll get the same
    // random sequence each time you run the program.
    srand(static_cast<unsigned>(time(nullptr)));

    std::string filename = "sample.txt";
    std::ofstream myFile(filename, std::ios::out);

    if (!myFile.is_open()) {
        std::cerr << "Error opening " << filename << std::endl;
        return 1;
    }

    // Let's write 10 random pairs for demonstration.
    for (int i = 0; i < 10; ++i) {
        auto [message_id, value] = generate_data(); 
        myFile << "Message ID: " << message_id 
               << ", Value: " << value << "\n";
    }

    myFile.close();
    std::cout << "Data written to " << filename << " successfully." << std::endl;
    return 0;
}
