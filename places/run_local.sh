go get github.com/gorilla/mux
go get github.com/satori/go.uuid
go get github.com/aws/aws-sdk-go
go get github.com/jmespath/go-jmespath
go get github.com/go-ini/ini

mkdir out 2> /dev/null
cd src
go build -o ../out/places-service
cd ../out
./places-server