# Puppeteer Stealth Scraper

This project is a web scraper built using Puppeteer with the Stealth Plugin. It provides an API route (`/extract-data`) that allows you to extract data from a specified URL.

## Installation
### Without docker
1. Clone the repository:
    `git clone`

2. Install the dependencies:
`npm i`
3. Run the server `node index.js`
### With docker
1. ```docker build -t <Image Name> .```

2. ```docker run -p 3000:3000 -d your-api-image-name```


## Usage

To start the server, run the following command:

Once the server is running, you can make a POST request to the `/extract-data` endpoint with the following payload:

```json
{
  "url": "https://example.com"
}
```

## Allowed methods:

POST /extract-data
