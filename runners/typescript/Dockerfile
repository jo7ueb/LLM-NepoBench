FROM node:20-slim

# /work側に package.json を要求しない MVP 構成（グローバル導入）
RUN npm i -g typescript@5.5.4 vitest@1.6.0 @vitest/coverage-v8

WORKDIR /runner
COPY --chmod=755 run.sh /runner/run.sh
COPY package.json /runner/package.json

# rootのまま実行（/workへの書き込み権限のため）
ENTRYPOINT ["/runner/run.sh"]
