FROM python:3.12-slim

# 依存（テスト実行に必要）
RUN pip install --no-cache-dir pytest fastapi "httpx>=0.25" uvicorn

# ランナースクリプトをコピー（コピー時に実行権限を付与）
WORKDIR /runner
COPY --chmod=755 run.sh /runner/run.sh

# 非rootユーザで実行
RUN useradd -m runner
USER runner

ENTRYPOINT ["/runner/run.sh"]
