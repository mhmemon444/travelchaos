# SPECIFY A BASE IMAGE  
FROM node:14-alpine

WORKDIR /usr/app

# INSTALL DEPENDENCIES
COPY ./package.json ./
RUN npm install
COPY ./ ./

# DEFAULT COMMAND
CMD ["npm", "start"]