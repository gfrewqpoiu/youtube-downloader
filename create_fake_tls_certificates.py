"""
IMPORTANT NOTICE: This file creates a fake certificate for use of the client and server to allow the connection
to be encrypted.
If you can use a real certificate for your hostname, please do so. This is just to provide some
security rather than having to use unencrypted connections when you can't get a real cert.
(For example when you have a server without a hostname.)"""

import trustme
from pathlib import Path
from loguru import logger


def get_ca() -> trustme.CA:
    if not Path('CA_CERT.pem').exists():
        authority = trustme.CA(organization_name="youtube-dl-Downloader")
        logger.info("Saving CA Certificate to file CA_CERT.pem, you can use it to configure trust of server certificate.")
        authority.cert_pem.write_to_path("CA_CERT.pem")
        logger.info("Saving CA Private Key to CA_PRIV_KEY.pem")
        authority.private_key_pem.write_to_path("CA_PRIV_KEY.pem")
        return authority
    else:
        with open('CA_CERT.pem', 'rb') as cert, open('CA_PRIV_KEY.pem', 'rb') as key:
            logger.info("Loading Certificate Authority from the given files.")
            cert_bytes = cert.read()
            key_bytes = key.read()
        authority = trustme.CA().from_pem(cert_bytes=cert_bytes, private_key_bytes=key_bytes)
        return authority


def issue_certificate(authority: trustme.CA, host: str) -> trustme.LeafCert:
    cert = ca.issue_cert(f"{host}")
    logger.info(f"Saving Certificate to file FAKE_CERT_{host}_fullchain.pem")
    cert.private_key_and_cert_chain_pem.write_to_path(f"FAKE_CERT_{host}_fullchain.pem")
    return cert


if __name__ == '__main__':
    ca = get_ca()
    print("For what IP address should the server certificate be issued?")
    host = input("Please enter the address here: ")
    server_cert = issue_certificate(ca, host)
    print("Please enter a certificate 'Username' for the client")
    client_name = input('Enter it here: ')
    client_cert = issue_certificate(ca, client_name)
    logger.success("Created the CA, Server Certificate, and Client Certificate.")
    logger.success(f"Now download the files CA_CERT.pem and FAKE_CERT_{client_name}_fullchain.pem for your client.")
