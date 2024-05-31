<a id="top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="https://github.com/Pramit726/RasoiGuru/assets/149934842/1e6708e9-86b7-4fc9-a87f-b1355bd20e31" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">RasoiGuru</h3>

  <p align="center">
    Ultimate culinary companion offering expert cooking guidance and ingredient tips seamlessly 
    <br />
    <a href="https://github.com/Pramit726/RasoiGuru/assets/149934842/c453ac60-e91e-4990-929b-2f5b6f83767d">View Demo</a>
    ·
    <a href="https://github.com/Pramit726/RasoiGuru/blob/main/.github/ISSUE_TEMPLATE/bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Pramit726/RasoiGuru/blob/main/.github/ISSUE_TEMPLATE/feature-request---.md">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Demo](#project-demo)
3. [Architecture](#architecture)
4. [Required API Keys](#required-api-keys)
5. [Project Setup](#project-setup)
6. [Deployment on AWS](#deployment-on-aws)
7. [Dependencies](#dependencies)
8. [Author](#author)

<!-- PROJECT OVERVIEW -->
## Project Overview

<div align="justify"> 
RasoiGuru is your ultimate cooking assistant chatbot, designed to offer detailed cooking instructions, ingredient substitutions, and personalized culinary tips to elevate your kitchen skills.
</div>
</br>

<div align="justify"> 
It uses Retrieval-Augmented Generation (RAG) from multiple data sources like professional cookbook PDFs and Wikipedia. This combination ensures that the chatbot provides accurate and comprehensive culinary information.
</div>
</br>

<div align="justify"> 
The application is converted to an API using FastAPI, allowing seamless integration and access to RasoiGuru's capabilities through a user-friendly interface. It has robust logging and exception handling mechanisms to ensure smooth operation and error detection. Additionally, a setup module is implemented to streamline the installation process and manage dependencies effectively.
</div>
</br>
<div align="justify"> 
Deployed on Amazon Web Services (AWS), RasoiGuru offers easy access and utilization for users. AWS also ensures scalability, allowing the application to handle varying user loads seamlessly.
</div>

## Architecture

<img src="https://github.com/Pramit726/RasoiGuru/assets/149934842/1c070d8f-73f1-4ee5-9a27-bca1c70db104" alt="architecture" width="840" height="663">

<!-- PROJECT DEMO -->
## API information


- **API Recording**


https://github.com/Pramit726/RasoiGuru/assets/149934842/c453ac60-e91e-4990-929b-2f5b6f83767d

<br/>

- **API Information**

<img src="https://github.com/Pramit726/RasoiGuru/assets/149934842/97061fc0-3bb0-4731-93cc-12018e984991" alt="API-info" width="1000" height="500">

``/``: Check service status

``/chat``: Initiate a conversation with RasoiGuru chatbot. Accepts a POST request with a JSON payload containing the user's query. Returns a response with the chatbot's answer. Requires a session_id cookie for session management.



<!-- REQUIRED API KEYS -->
## Required API Keys

This project requires the following API keys:

- **LangChain API key:** Required for LangSmith tracking.
- **Pinecone API key:** Required for storing vectors in Vector database.
- **Cohere API key:** Required for vector Embedding.
- **Groq API key:** Required for accessing the LLM.

LangSmith facilitates usage tracking and provides valuable insights into user behavior through seamless integration. The screenshot below illustrates a sample view of RasoiGuru usage data within the LangSmith platform.

![App Screenshot](https://github.com/Pramit726/RasoiGuru/assets/149934842/e42ef8e3-13fb-4bd7-85ef-2e716f80b9cb)
<br/>
<br/>

Ensure that you obtain these API keys before running the project.

<!-- PROJECT SETUP -->
## Project Setup

**Clone this GitHub repository**

```bash
(base)$: git clone https://github.com/Pramit726/RasoiGuru.git
```

**Go to the project directory**

```bash
(base)$: cd RasoiGuru
```

**Configure environment**

- Create the conda environment

```bash
(base)$: conda  create -p venv python==3.10 -y
```

- Activate the environment

```bash
(base)$: conda activate venv
```
- Install the required dependencies

```bash
(venv)$: pip install -r requirements.txt
```
**Run it**

```bash
(venv)$: python uvicorn main:app --host 0.0.0.0 --port 8000
```

 It will start the FastAPI application, making it accessible at ``http://localhost:8000``

<!-- DEPLOYMENT ON AWS-->
## Deployment on AWS

**Step 1**

First login to the AWS: https://aws.amazon.com/console/

**Step 2**

Search about EC2 in the services section.

**Step 3**

Configure the Ubuntu machine.

**Step 4**

Launch the instance.

**Step 5**

Do the port mapping to this port: 8000

**Step 6**

Run the following commands.

```bash
sudo apt update
```

```bash
sudo apt-get update
```
```bash
sudo apt upgrade -y
```
```bash
sudo apt install git curl unzip tar make sudo vim wget -y
```
```bash
git clone https://github.com/Pramit726/RasoiGuru.git
```

```bash
cd RasoiGuru
```

```bash
sudo apt install python3-pip
```

```bash
sudo apt install python3-venv
```

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip3 install -r requirements.txt
```

**If you want to add the API keys**

- Create .env file in the AWS server using  touch .env

- Next write vi .env

- Press i 

- Copy API keys and paste it

- Press : , then wq! and hit enter

**Step 7**
```bash
#Temporary running
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

```bash
#Permanent running
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```
<!-- DEPENDENCIES -->
## Dependencies
- fastapi
- langchain
- langchain-community
- langchain_cohere
- langchain_core
- langchain_groq
- langchain_pinecone
- pinecone-client
- pypdf
- python-dotenv
- wikipedia


<!-- AUTHOR -->
## Author
**Pramit De**
- <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Github-Dark.svg" alt="GitHub" width="20"/> [Pramit726](https://github.com/Pramit726)
- <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Gmail-Dark.svg" alt="Email" width="20"/> pramitde726@gmail.com / pramit.de.cse.2021@tint.edu.in
- Department of CSE, Techno International New Town, West Bengal, India

© 2024 RasoiGuru by Pramit De

<p align="right">
    <a href="#top">Back to Top</a>
</p>


















