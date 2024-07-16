FROM winamd64/golang:1.21-nanoserver as build

WORKDIR /go/src/github.com/mccutchen/go-httpbin

COPY . .

RUN mkdir dist
RUN go build -ldflags="-s" -o dist/go-httpbin.exe ./cmd/go-httpbin

FROM mcr.microsoft.com/windows/nanoserver:ltsc2019

COPY --from=build /go/src/github.com/mccutchen/go-httpbin/dist /app

WORKDIR /app

EXPOSE 8080
CMD ["/app/go-httpbin.exe"]
