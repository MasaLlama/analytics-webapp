# Basic Analytics Web App using Streamlit

1. Build Docker Image
 docker build -t analyticswebapp:latest -f docker/Dockerfile 
2. check to see if image is present
   docker image ls
3. Create the container
   docker run -p 8501:8501 analyticswebapp:latest
