import base64
import json
import pprint
import cbor2
import cose
from Crypto.Signature import pkcs1_15                                                                                  
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

received_data= {
    "attestation_doc_b64": "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", 
    "content": "{\"version\": \"TLSv1.2\", \"peerCert\": {\"subject\": [[[\"countryName\", \"KY\"]], [[\"localityName\", \"West Bay\"]], [[\"organizationName\", \"Binance Holdings Limited\"]], [[\"commonName\", \"*.binance.com\"]]], \"issuer\": [[[\"countryName\", \"US\"]], [[\"organizationName\", \"DigiCert Inc\"]], [[\"organizationalUnitName\", \"www.digicert.com\"]], [[\"commonName\", \"GeoTrust RSA CA 2018\"]]], \"version\": 3, \"serialNumber\": \"03FA7FC3267C91A32334719E99AC6014\", \"notBefore\": \"Feb  9 00:00:00 2023 GMT\", \"notAfter\": \"Feb 16 23:59:59 2024 GMT\", \"subjectAltName\": [[\"DNS\", \"*.binance.com\"], [\"DNS\", \"binance.com\"]], \"OCSP\": [\"http://status.geotrust.com\"], \"caIssuers\": [\"http://cacerts.geotrust.com/GeoTrustRSACA2018.crt\"], \"crlDistributionPoints\": [\"http://cdp.geotrust.com/GeoTrustRSACA2018.crl\"]}}", 
    "public_key": "b'0\\x82\\x01\"0\\r\\x06\\t*\\x86H\\x86\\xf7\\r\\x01\\x01\\x01\\x05\\x00\\x03\\x82\\x01\\x0f\\x000\\x82\\x01\\n\\x02\\x82\\x01\\x01\\x00\\x9b\\xc4.n\\xe7\\x8ak\\x94\\x94/\\xb7\\x0c\\x8f\\xa1\\x02\\xd8\\xbd\\x9c\\xb7\\xea\\x022J\\xa5(\\xa65\\xec\\x11\\xd7\\x10e\\'\\x07{4U\\xc9cl2\\xa2\\x81k\\x07\\xfb$\\xa6\\x03\\xf8\\xdc.\\xf6-C\\xc5\\x9e\\x85\\xc4\\xae(\\xff\\x9f/\\x0c4!\\x89I\\xbb4\\xed\\x08\\xbba\\xfd\\xf3=\\xb7\\r\\xfa\\xbb\\xb3C\\xcb\\\\\\xd6h&\\x8d\\x99D?\\x03\\xacw\\xf0\\xbc*b\\x92x\\xef;\\xd5\\x97>\\xb3k\\xdd\\xc8Q\\xa8;[\\xb2/\\x958\\xcb\\x8a\\xba\\xf7\\xb9\\xbd\\x062\\x81@\\xda$+6c\\xc4z\\x17JchCz@\\xac\\xfa\\xece[\\x12\\x1d\\xab\\xac\\xfb\\x01\\xbeM}\\xc7bPj\\xe7Bl\\x84t\\x9e\\xce\\rF\\x92\\xfa(\\x95W\\xe3\\xbc5\\xd5;z\\x18,\\tC\\x06\\x07\\x03\\xc1\\\\\\xc0\\x80\\x1a\\xe0\\x18\\x85\\xc0V>\\xa5\\xa0\\r^\\xc7\\x88A\\xb6\\xbf\\xf2\\xc8\\x90c\\x9a\\x91Y\\xeej1P\\xe3\\xb7\\xa8\\xc3q\\xcf\\xae\\x06\\xc4*\\xea\\xc9\\xd4\\xf6\\x98Q\\x02]\\xc1\\r\\xf2\\xe5p\\xf8\\x12\\xa1y\\xf7\\x1c\\x1e\\x19\\xc3\\xa8X1.\\x13\\x02\\x03\\x01\\x00\\x01'", 
    "signature_b64": "G1PJMr5m3fdJKLLI0fs3lhV9ekkowWx5HgcQnqs6u35+ZlfQtb2Zk9+wN2qEDTJWwKCwy503EpDCNEEb2+Lb6Hx0R/bGIH8T5W8rI4y8nGGVdcbtveNn9Y9uhYA7mz1YJwYX1o4UAolWD77fJ8c3vfLx/T99C0FTjOw2RUrrobYYiRjKDdcKVeFtJMukppJwSax9jM/7HuV6tVubex6iXphAGjmOD3OllKRWiggAQhOvGVm447ojw6b+1RxHuDKtAHE3poOxlHgdI4vLG/GAXt9wb7k5hPJpNsAGJnBLFoBWy6NYJc3nqg/C9IsyZ+Q0uwQEDnKr4P12I+g8jvrMSw=="
    }
def validate_signature(public_key, signature, msg):
    verifier = pkcs1_15.new(RSA.importKey(public_key))

    h_v = SHA256.new() 
    try:
        h_v.update(msg)
        verifier.verify(h_v,signature)
        return True
    except ValueError: 
        print("invalid signature")
        return False

content_serialized = json.loads(received_data["content"])

print(content_serialized)

# Decode CBOR attestation document
data = cbor2.loads(base64.b64decode(received_data['attestation_doc_b64']))# Load and decode document payload
doc = data[2]
doc_obj = cbor2.loads(doc)

print(pprint.pprint(doc_obj))

# Get signing certificate from attestation document
cert = crypto.load_certificate(
    crypto.FILETYPE_ASN1,
    doc_obj['certificate']
)# Get the key parameters from the cert public key
cert_public_numbers = cert.get_pubkey()\
    .to_cryptography_key().public_numbers()
x = long_to_bytes(cert_public_numbers.x)
y = long_to_bytes(cert_public_numbers.y)# Create the EC2 key from public key parameters
key = EC2(
    alg = CoseAlgorithms.ES384,
    x   = x,
    y   = y,
    crv = CoseEllipticCurves.P_384
)


'''
# Create an X509Store object for the CA bundles
store = crypto.X509Store()# Create the CA cert object from PEM string,
# and store into X509Store
_cert = crypto.load_certificate(crypto.FILETYPE_PEM, root_cert_pem)
store.add_cert(_cert)# Get the CA bundle from attestation document
# and store into X509Store
# Except the first certificate, which is the root certificate
for _cert_binary in doc_obj['cabundle'][1:]:
    _cert = crypto.load_certificate(
        crypto.FILETYPE_ASN1,
        _cert_binary
    )
    store.add_cert(_cert)# Get the X509Store context
store_ctx = crypto.X509StoreContext(store, cert)# Validate the certificate
# If the cert is invalid, it will raise exception
store_ctx.verify_certificate()
'''