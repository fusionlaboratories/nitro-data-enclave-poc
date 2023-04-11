# Labs enclave PoC 
AWS Nitro-based PoC for tls non-repuditation

build: 
```
docker build ./Enclave/Dockerfile -t kataak/dataenclave:latest & docker push  kataak/dataenclave:latest
./Enclave/build.sh

vsock-proxy --config vsock-proxy.yaml 8000 binance.com 443 &
```

binance.com is hardcoded per time for local loopback

Req: 
````
curl --header "Content-Type: application/json" \
                                     --request POST \
                                     --data '{"hostname":"binance.com","port":443}' \
                                     http://10.56.32.98:5000/host
                                     