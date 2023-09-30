FROM node:latest

WORKDIR /app

COPY package*.json ./

RUN npx playwright install

RUN npm install

COPY . .

EXPOSE 3050

CMD [ "node", "index.js" ]
