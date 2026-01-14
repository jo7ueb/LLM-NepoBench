FROM node:20-slim

# /work側に package.json を要求しない MVP 構成（グローバル導入）
RUN npm i -g typescript@5.5.4 vitest@1.6.0

WORKDIR /runner
COPY --chmod=755 run.sh /runner/run.sh

RUN useradd -m runner
USER runner

ENTRYPOINT ["/runner/run.sh"]
