FROM node:14

WORKDIR /frontend

COPY package.json package-lock.json /frontend/

RUN npm install

COPY . /frontend/

CMD ["npm", "start"]
