# Sports API Deployment with AWS ECS, ALB, and API Gateway

This guide outlines the steps to deploy a Dockerized sports API using AWS Elastic Container Service (ECS) with Fargate, an Application Load Balancer (ALB), and expose it via API Gateway.

---

## Prerequisites
- AWS CLI installed and configured.
- Docker installed and running.
- Sports Data API Key (`SPORTS_API_KEY`).

---

## Step 1: Create an ECR Repository
Create an ECR repository to store the Docker image.
```bash
aws ecr create-repository --repository-name sports-api --region us-east-1
```

---

## Step 2: Authenticate, Build, and Push the Docker Image

1. Authenticate Docker with ECR:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
   ```

2. Build the Docker image:
   ```bash
   docker build --platform linux/amd64 -t sports-api .
   ```

3. Tag the Docker image:
   ```bash
   docker tag sports-api:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:sports-api-latest
   ```

4. Push the image to ECR:
   ```bash
   docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:sports-api-latest
   ```

---

## Step 3: Set Up an ECS Cluster with Fargate

### Create an ECS Cluster
1. Navigate to **ECS Console → Clusters → Create Cluster**.
2. Name the cluster: `sports-api-cluster`.
3. Choose **Fargate** as the infrastructure.
4. Create the cluster.

### Create a Task Definition
1. Go to **Task Definitions → Create New Task Definition**.
2. Name the task definition: `sports-api-task`.
3. Select **Fargate** as the infrastructure.
4. Add container details:
   - Name: `sports-api-container`
   - Image URI: `<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:sports-api-latest`
   - Container Port: `8080`
   - Protocol: `TCP`
5. Add an environment variable:
   - Key: `SPORTS_API_KEY`
   - Value: `<YOUR_SPORTSDATA.IO_API_KEY>`
6. Save the task definition.

### Run the Service with ALB
1. Navigate to **Clusters → Select Cluster → Service → Create**.
2. Configure the service:
   - Capacity Provider: **Fargate**
   - Deployment Configuration: `sports-api-task`
   - Service Name: `sports-api-service`
   - Desired Tasks: `2`
3. Networking:
   - Create a new security group:
     - Type: **All TCP**
     - Source: **Anywhere**
   - Use **Application Load Balancer (ALB)**:
     - Name: `sports-api-alb`
     - Health Check Path: `/sports`
4. Deploy the service.

---

## Step 4: Test the ALB
1. Retrieve the DNS name of the ALB, e.g.,  
   `sports-api-alb-<AWS_ACCOUNT_ID>.us-east-1.elb.amazonaws.com`.
2. Verify the API is accessible by visiting:  
   `http://sports-api-alb-<AWS_ACCOUNT_ID>.us-east-1.amazonaws.com/sports`.

---

## Step 5: Configure API Gateway

### Create a REST API
1. Navigate to **API Gateway Console → Create API → REST API**.
2. Name the API: `Sports API Gateway`.

### Set Up Integration
1. Create a resource: `/sports`.
2. Create a GET method.
3. Choose **HTTP Proxy** as the integration type.
4. Enter the DNS name of the ALB that includes `/sports`, e.g.,  
   `http://sports-api-alb-<AWS_ACCOUNT_ID>.us-east-1.elb.amazonaws.com/sports`.

### Deploy the API
1. Deploy the API to a stage, e.g., `prod`.
2. Note the endpoint URL.

---

## Step 6: Test the System
1. Use `curl` or a browser to test the API:
   ```bash
   curl https://<api-gateway-id>.execute-api.us-east-1.amazonaws.com/prod/sports
   ```

Verify the response to confirm the setup is working as expected.
