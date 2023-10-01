
## Prerequisites

Before you begin, ensure you have the following software installed on your system:

-   Docker: [Install Docker](https://docs.docker.com/get-docker/)
-   Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)
-   Google Colab: [Get started](https://colab.research.google.com/)
-   Download trained BERT: [Link](https://drive.google.com/drive/folders/1zlUUJyxtWpgpTB9pEeEXJRmUS2zYC8iI?usp=sharing)

## Getting Started

1.  Clone this repository to your local machine:
    
    
    

	```shell  
	git clone https://github.com/isofinly/coconut
	```

    
-   Navigate to the root directory of the cloned repository:
	```shell  
	git clone coconut
	```
   
2.  Verify that you have the necessary Docker Compose file (usually named `docker-compose.yml`) in your project directory.
    

## Running the Services

To start the services defined in the `docker-compose.yml` file, run the following command from the root directory of your project:

```shell  
docker-compose up
```

This command will build the necessary Docker containers and start the services. By default, it will run in the foreground, and you will see the logs of each service in your terminal.

You should see output indicating that each service is running, and they will be accessible on the specified ports.

-   Next.js frontend: [http://localhost:3000](http://localhost:3000)
-   Node.js API: [http://localhost:3050](http://localhost:3050)
-   Python API: [http://localhost:3030](http://localhost:3030)
- Ai pyTorch API: [http://localhost:3033](http://localhost:3033)

To stop the services, press `Ctrl + C` in the terminal where they are running.

## Configuration Details

Here is a breakdown of the services and their configurations defined in the `docker-compose.yml` file:

### Nextjs web ui

-   Build context: `./frontend`
-   Container name: `nextjs-docker`
-   Exposed port: `3000`
-   Command to run: `bun run dev`

### Node-api
-	 Framework: `Express`
-   Build context: `./backend/node`
-   Container name: `node-api`
-   Exposed port: `3050`
-   Network: `backend` (bridge network)
-   Routes: 
	- `/extract_data`
	  - Allowed methods: `POST`
	  - Request body: ` json {"urls": [""]}`

### Python-api

-   Build context: `./backend/python`
-   Container name: `python-api`
-   Exposed port: `3030`
-   Network: `backend` (bridge network)
-   Routes: 
	- `/get_theme`
		- Allowed methods: `POST`
		-  Request body: ` {"url": ""} `
	- `/get_related_queries`
		- Allowed methods: `POST`
		- Request body: ` {"": ""} `
	- `/get_related_topics`
		- Allowed methods: `POST`
		- Request body: ` {"": ""} `
	- `/get_interest_over_time`
		- Allowed methods: `POST`
		- Request body: ` {"": ""} `
	- `/extract_metadata_batch`
		- Allowed methods: `POST`
		- Request body: ` {"": ""} `
	- `/extract_metadata`
		- Allowed methods: `POST`
		- Request body: ` {"": ""} `
	- `/extract_paragraphs`
		- Allowed methods: `POST`
		- Request body: ` {"": ""} `
	- `/get_site_pages`
		- Allowed methods: `POST`
		- Request body: ` {"": ""} `
	- `/extract_keywords`
		- Allowed methods: `POST`
		- Request body: ` {"": ""} `
	- `/get_domain`
		- Allowed methods: `POST`
		- Request body: ` {"": ""} `
### Python-ai-api
-   Build context: `./backend/ai`
-   Container name: `python-ai-api`
-   Exposed port: `3033`
-   Network: `backend` (bridge network)
-   Routes: 
	- `/`
		- Allowed methods: `POST`
		- Request body: `{"text":"<your_data>"}`
### Networks

-   `backend` network:
    -   Driver: `bridge`
