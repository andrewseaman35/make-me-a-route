FROM google/golang

COPY . /go
ENV GOPATH /go

RUN go get github.com/gorilla/mux
RUN go get github.com/satori/go.uuid
RUN go get github.com/aws/aws-sdk-go
RUN go get github.com/jmespath/go-jmespath
RUN go get github.com/go-ini/ini

WORKDIR /go
RUN go build -o application

EXPOSE 3000
ENTRYPOINT /go/application