# NODE image used to build the application
FROM node:11-alpine as builder
WORKDIR /home

RUN apk add yarn
RUN apk add --no-cache git

COPY public/ app/public
COPY src/ app/src
COPY package.json yarn.lock app/
COPY .env.development app/

WORKDIR /home/app
RUN yarn

CMD ["yarn", "start"]