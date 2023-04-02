# QTI Enclave PoC 

Upon creation, the enclave will output a set of measurements: 
```
  "Measurements": {
    "HashAlgorithm": "Sha384 { ... }",
    "PCR0": "e2532880dd904f3ecb08b6e483ea1276b0b3289c4e807f675f2a0a71f54c7bc0beae15f92242a1a771e6faab235bb845",
    "PCR1": "bcdf05fefccaa8e55bf2c8d6dee9e79bbff31e34bf28a99aa19e6b29c37ee80b214a414b7607236edf26fcb78654e63f",
    "PCR2": "9a49a0ef0b0d23de9d700bd87f2c6da430f8b6f95cfdc4150b4adabb262b13552c1debf5728d6a99cb8f5cdcee405660"
    }
```
- PCR0 hash of the EIF 
- PCR1 A contiguous measurement of the kernel and boot ramfs data.
- PCR2 A contiguous, in-order measurement of the user applications, without the boot ramfs.

A client sends a request for a domain on the form of {hostname: binance.com, port: 443} to the secure enclave. The enclave itself has two components, a server and a http proxy. Communication between host and enclave goes through a vsock tunnel, so in order for the enclave server to send a http request, a local loopback is used against a vsock http proxy. This allows for the SSL connection to originate in the server, and is therefore sent encrypted through the proxy over the vsock-tunnel and to the destination via the host's NIC. 

On boot, the enclave process generate a RSA keypair. This is used in the enclave attestation document and to sign the message to the client. See attestation_doc.png. The attestation contains references to the AWS root certificate and hypervisor ID which can be further validated, but of more interest is the 'pcrs' and 'public key' parts. The 'pcrs'-field contains all locked PCRs at time of computation and can therefore verify that the given enclave image file and application are run (PCR0-2). 

The server component outputs the following: 

```
payload: 
    attestation_doc_b64: the b64 encoded CBOR (consise binary object representation) attestation
    content: The response itself (TLS transaction)
    public_key: also found in the attestation document
    signature_b64: a base64 encoded pkcs signature of the SHA256 hash of the content
```
 
The signature can then be verified with the given information. The enclave's public key is used in the attestation doc as well as outputted directly. So we can in essence take the message, know from the signature that the sender of the message has the private key used to sign the it, and that the public key belongs to the enclave, given that it's included in the attestation document, and that the attestation is created from the same enclave that runs the server, as PCRs 0-2 match those provided at boot. The attestation document is in COSE Sign1 format and signed by a certificate (the 'certificate' field of the doc) AWS Nitro Enclaves uses the ES384 algorithm to sign the attestation document itself. The certificate’s public key (x/y coordinate and curve) can then be used to verify the signature. Thus, we can prove to a reasonable degree that the price request to eg Binance's APIs originates from the enclave and is delivered to the end user without interference from us. 

As part of the attestation document we can also verify that the CA bundle and certificate matches the AWS root certificate 

https://tealfeed.com/use-aws-nitro-enclaves-attestation-document-bnpei