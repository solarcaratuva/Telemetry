#include <boost/beast/core.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <iostream>
#include <string>

using tcp = boost::asio::ip::tcp; // from <boost/asio/ip/tcp.hpp>
namespace websocket = boost::beast::websocket; // from <boost/beast/websocket.hpp>

int main()
{
    try
    {
        // Set up the I/O context, the endpoint, and the acceptor
        boost::asio::io_context ioc;
        tcp::endpoint endpoint(boost::asio::ip::make_address("127.0.0.1"), 12345);
        tcp::acceptor acceptor(ioc, endpoint);

        // Wait for a connection
        tcp::socket socket(ioc);
        acceptor.accept(socket);

        // Make the socket into a WebSocket stream
        websocket::stream<tcp::socket> ws(std::move(socket));
        ws.accept();

        while(true) {
            // Read a message
            boost::beast::multi_buffer buffer;
            ws.read(buffer);

            // Echo the message back
            ws.text(ws.got_text());
            ws.write(buffer.data());
        }
    }
    catch (std::exception const& e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
