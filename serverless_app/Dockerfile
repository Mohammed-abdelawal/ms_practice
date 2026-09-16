# Local serverless sandbox. osls (the open-source Serverless Framework) plus
# serverless-offline emulate API Gateway + Lambda, so functions answer plain
# HTTP with no AWS account. One image carries both runtimes because this
# service mixes a Node function and a Python one.
FROM node:22-bookworm-slim

# serverless-offline runs Python handlers by spawning python3 per invocation.
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 \
 && rm -rf /var/lib/apt/lists/*

# The handlers are mounted from your machine by docker-compose.yml. Without
# this, each Python call writes __pycache__/ back into that source folder.
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY package.json .npmrc ./
RUN npm install --no-audit --no-fund

COPY serverless.yml ./
COPY functions/ ./functions/

EXPOSE 4000

CMD ["npm", "run", "offline"]
