import ssl
import anyio
import anyio.exceptions
import skript
from typing import Optional, List, Tuple
from loguru import logger
from functools import partial

SERVER_CERT_CHAIN = 'FAKE_CERT_localhost_fullchain.pem'  # Change this with your server certificate's path.
PASSWORD = 'password1'.encode('utf-8')  # An additional security check.
# You need to provide the same password in the client file.

# We can't pass these between the functions, because they only take a limited amount of arguments, and they return None,
# so we need to use globals.
path: Optional[str] = None
urls_to_dl: Optional[List[str]] = None
event = None


async def serve(client: anyio.SocketStream) -> Tuple[Optional[str], Optional[List[str]]]:
    global path, urls_to_dl
    async with client:
        try:
            password = await client.receive_until(b'\n', 1024)
            if password != PASSWORD:
                logger.error("A client tried to connect but provided a wrong password.")
                await client.close()
            else:
                logger.debug("Recieved a valid connection from a client.")
                await client.send_all(b'Password accepted!\n')
                path = str(await client.receive_until(b'\n', 1024), encoding='utf-8')
                await client.send_all(b'Set the path to: %s\n' % path.encode('utf-8'))
                all_urls = await client.receive_until(b'\n', 8192)
                urls_to_dl = str(all_urls, encoding='utf-8').split(';')
                for url in urls_to_dl:
                    await client.send_all(f'Got the URL {url}'.encode('utf-8'))
                await event.set()
                await client.close()
        except anyio.exceptions.IncompleteRead:
            logger.warning("Connection was ended prematurely.")
            path = None
            urls_to_dl = None
            await event.set()


async def download():
    global path, urls_to_dl
    await event.wait()
    logger.debug("Event fired.")
    logger.debug(f"Path: {path}")
    logger.debug(f"URLs: {urls_to_dl}")
    if path is None or urls_to_dl is None:
        return
    else:
        lpath = path
        links = urls_to_dl.copy()
        path = None
        urls_to_dl = None
        await anyio.run_in_thread(partial(skript.main, links=links, path=lpath))


async def main():
    global event
    event = anyio.create_event()
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
                await tg.spawn(download)

if __name__ == '__main__':
    anyio.run(main, backend='trio')
