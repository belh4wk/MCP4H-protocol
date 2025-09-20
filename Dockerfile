
# Simple Node + TS runtime for MCP echo server
FROM node:20-alpine

WORKDIR /app

# Install deps
COPY examples/package.json ./examples/package.json
RUN cd examples && npm install

# Copy source
COPY examples/ ./examples/

# Default command
WORKDIR /app/examples
CMD ["npx", "ts-node", "echo-server.ts"]
