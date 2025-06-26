FROM node:20.19

WORKDIR /app

COPY package*.json ./

RUN npm i

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]