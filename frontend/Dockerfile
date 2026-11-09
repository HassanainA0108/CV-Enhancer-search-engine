
FROM node:22-bookworm-slim

WORKDIR /app

# Install dependencies using the versions declared
# in package.json, not Windows node_modules.
COPY package.json ./

RUN npm install --include=optional

# Copy frontend source, excluding node_modules
# and the old lockfile through .dockerignore.
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
