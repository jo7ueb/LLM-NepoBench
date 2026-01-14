FROM node:20-slim

# /work側に package.json を要求しない MVP 構成（グローバル導入）
RUN npm i -g typescript@5.5.4 vitest@1.6.0 @vitest/coverage-v8

# runnerユーザーを作成
RUN useradd -m runner

WORKDIR /runner
COPY --chmod=755 run.sh /runner/run.sh
COPY package.json /runner/package.json
COPY vitest.config.ts /runner/vitest.config.ts

# /work と /tmp/.vite, /tmp/.vitest に書き込み権限を設定
RUN mkdir -p /work /tmp/.vite /tmp/.vitest && \
    chown -R runner:runner /work /tmp/.vite /tmp/.vitest

USER runner

ENTRYPOINT ["/runner/run.sh"]
