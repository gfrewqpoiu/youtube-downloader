import ssl
import anyio
import os
from loguru import logger
from typing import List, Optional, Union

CA_FILE = 'CA_CERT.pem'
CLIENT_CERT_FILE = 'FAKE_CERT_localhost-gfrewqpoiu_fullchain.pem'  # Replace with your cert file.
PASSWORD = 'password1'.encode('utf-8')


async def main(urls: List[str], path: Union[str, os.PathLike]):
    # These two steps are only required for certificates that are not trusted by the
    # installed CA certificates on your machine, so you can skip this part if you use
    # Let's Encrypt or a commercial certificate vendor.

    client_context = ssl.create_default_context(cafile=CA_FILE)
    client_context.load_cert_chain(certfile=CLIENT_CERT_FILE)

    async with await anyio.connect_tcp('localhost', 9123, ssl_context=client_context, autostart_tls=True) as client:
        await client.send_all(b'%s\n' % PASSWORD)
        response = await client.receive_until(b'\n', 1024)
        logger.debug(response)

if __name__ == '__main__':
    anyio.run(main, backend='trio')
