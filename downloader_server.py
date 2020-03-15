import ssl
import anyio

SERVER_CERT_CHAIN = 'FAKE_CERT_fullchain.pem'  # Change this with your server certificate's path.


async def serve(client: anyio.SocketStream):
    async with client:
        path = await client.receive_until(b'\n', 1024)
        await client.send_all(b'Set the path to: %s\n' % path)
        all_urls = await client.receive_until(b'\n', 8192)
        urls = str(all_urls, encoding='utf-8').split(';')
        for url in urls:
            await client.send_all(f'Got the URL {url}'.encode('utf-8'))


async def main():
    # Create a context for the purpose of authenticating clients
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # Load the server certificate and private key
    context.load_cert_chain(certfile=SERVER_CERT_CHAIN)

    async with anyio.create_task_group() as tg:
        async with await anyio.create_tcp_server(9123, ssl_context=context) as server:
            async for client in server.accept_connections():
                await tg.spawn(serve, client)

anyio.run(main, 'trio')
