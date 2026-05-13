FROM golang:1.25-alpine AS builder

ENV CGO_ENABLED 0

ENV GOOS linux

RUN apk add --no-cache git

WORKDIR /build

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build -ldflags="-s -w" -o /app/server .

FROM alpine

WORKDIR /app

RUN apk add --no-cache ca-certificates

COPY --from=builder /app/server /app/server

CMD [ "./server" ]