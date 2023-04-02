# Labs enclave PoC 

This is a temporary project for pulling scripts and files into the data PoC enclaves. this project will be deleted and a new one ordered and setup in compliance with policy when PoC hypothesis test is concluded

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
                                     