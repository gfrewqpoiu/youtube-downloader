import ssl
import anyio
import anyio.exceptions
from loguru import logger

SERVER_CERT_CHAIN = 'FAKE_CERT_localhost_fullchain.pem'  # Change this with your server certificate's path.
PASSWORD = 'password1'.encode('utf-8')


async def serve(client: anyio.SocketStream):
    async with client:
        try:
            password = await client.receive_until(b'\n', 1024)
            if password != PASSWORD:
                logger.error("A client tried to connect but provided a wrong password.")
                await client.close()
            else:
                logger.debug("Recieved a valid connection from a client.")
                await client.send_all(b'Password accepted!\n')
                path = await client.receive_until(b'\n', 1024)
                await client.send_all(b'Set the path to: %s\n' % path)
                all_urls = await client.receive_until(b'\n', 8192)
                urls = str(all_urls, encoding='utf-8').split(';')
                for url in urls:
                    await client.send_all(f'Got the URL {url}'.encode('utf-8'))
        except anyio.exceptions.IncompleteRead:
            logger.warning("Connection was ended prematurely.")


async def main():
    logger.info("Starting up the Server.")
    # Create a context for the purpose of authenticating clients
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # Load the server certificate and private key
    context.load_cert_chain(certfile=SERVER_CERT_CHAIN)
    logger.debug("Loaded the server certificate.")
    async with anyio.create_task_group() as tg:
        async with await anyio.create_tcp_server(9123, ssl_context=context) as server:
            logger.info("Started the server on port 9123 (TCP).")
            async for client in server.accept_connections():
                await tg.spawn(serve, client)

if __name__ == '__main__':
    anyio.run(main, backend='trio')
