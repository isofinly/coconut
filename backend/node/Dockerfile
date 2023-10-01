FROM node:latest

WORKDIR /app/

COPY /package*.json ./

RUN npm install

RUN apt-get update 

RUN apt-get install -y libnss3
RUN apt-get install -y libnspr4         
RUN apt-get install -y libatk1.0-0        
RUN apt-get install -y libatk-bridge2.0-0     
RUN apt-get install -y libcups2         
RUN apt-get install -y libdrm2          
RUN apt-get install -y libdbus-1-3      
RUN apt-get install -y libxkbcommon0      
RUN apt-get install -y libatspi2.0-0     
RUN apt-get install -y libxcomposite1     
RUN apt-get install -y libxdamage1        
RUN apt-get install -y libxfixes3         
RUN apt-get install -y libxrandr2         
RUN apt-get install -y libgbm1      
RUN apt-get install -y libasound2

RUN npx playwright install

COPY . .

EXPOSE 3050

CMD [ "node", "index.js" ]
