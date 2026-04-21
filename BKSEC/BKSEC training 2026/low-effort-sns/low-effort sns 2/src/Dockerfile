# Build stage
FROM golang:1.24 AS build
WORKDIR /app

ENV GOPROXY=https://goproxy.io,direct

COPY go.* ./
RUN go mod download

COPY . .
RUN go build -o binary .

# Runtime stage
FROM gcr.io/distroless/base
WORKDIR /app

COPY --from=build /app/binary /app/binary

ENTRYPOINT ["/app/binary"]
