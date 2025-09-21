# Simple Dockerfile to run MCP Echo Server
FROM node:20-alpine

# Create app directory
WORKDIR /usr/src/app

# Copy package.json and install deps
COPY examples/package.json ./
RUN npm install

# Copy echo server
COPY examples/echo-server.ts ./

# Install ts-node + typescript globally for runtime
RUN npm install -g ts-node typescript

EXPOSE 8080

CMD ["ts-node", "echo-server.ts"]
