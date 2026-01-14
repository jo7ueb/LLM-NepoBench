FROM golang:1.22-alpine

WORKDIR /runner
COPY --chmod=755 run.sh /runner/run.sh

RUN adduser -D runner
USER runner

ENTRYPOINT ["/runner/run.sh"]
