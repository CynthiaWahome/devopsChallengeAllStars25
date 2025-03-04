# DevOps Challenge All-Stars 2025

A collection of 6 DevOps projects demonstrating various cloud-native technologies, infrastructure as code, containerization, and serverless architectures.

![DevOps Challenge](/docs/images/devops-challenge-banner.jpg)

## Project Overview

This repository contains six distinct projects that demonstrate different DevOps skills and cloud technologies:

1. **Weather Dashboard App** - A Python application that fetches weather data and stores it in AWS S3.
2. **Sports Alert System** - A serverless notification system for sports updates.
3. **Sports Data Lake** - AWS-based data lake for sports analytics.
4. **Sports API Management** - Containerized Flask API with AWS ECS deployment.
5. **Sports Game Highlights** - Media processing pipeline for sports highlights using FFmpeg.
6. **Sports Alerts Terraform** - IaC implementation of a sports alert system using Terraform.

## Contents

- [Prerequisites](#prerequisites)
- [Projects](#projects)
  - [Weather Dashboard App](#weather-dashboard-app)
  - [Sports Alert System](#sports-alert-system)
  - [Sports Data Lake](#sports-data-lake)
  - [Sports API Management](#sports-api-management)
  - [Sports Game Highlights](#sports-game-highlights)
  - [Sports Alerts Terraform](#sports-alerts-terraform)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [License](#license)

## Prerequisites

- Python 3.8 or higher
- AWS CLI configured with appropriate permissions
- Docker installed and running
- Terraform CLI (v1.10.5 or higher)
- FFmpeg (for the Sports Game Highlights project)
- Various API keys (details in each project's README)

## Projects

### Weather Dashboard App

A Python application that fetches real-time weather data for specified cities using the OpenWeather API and stores the data in AWS S3.

**Key Features:**
- Fetches real-time weather data for multiple cities
- Stores weather data in AWS S3
- Implements error handling and retries

[Go to Weather Dashboard App →](./01weatherDashboardApp)

### Sports Alert System

A serverless notification system that sends real-time sports event updates to subscribers.

**Key Features:**
- Fetches sports data from external APIs
- Formats game information based on status
- Sends notifications via AWS SNS

[Go to Sports Alert System →](./02sports-alert-system)

### Sports Data Lake

An AWS-based data lake that collects, processes, and analyzes sports data.

**Key Features:**
- Creates S3 buckets for data storage
- Sets up AWS Glue databases and tables
- Configures Athena for SQL-based queries

[Go to Sports Data Lake →](./03sports-data-lake)

### Sports API Management

A containerized Flask API for sports data with AWS ECS deployment.

**Key Features:**
- REST API built with Flask
- Docker containerization
- AWS ECS deployment with Application Load Balancer
- API Gateway integration

[Go to Sports API Management →](./04sports-api-management)

### Sports Game Highlights

A media processing pipeline for sports video highlights using FFmpeg.

**Key Features:**
- Fetches sports highlights from RapidAPI
- Processes videos with FFmpeg
- Stores processed videos in S3
- Docker containerization

[Go to Sports Game Highlights →](./05sports-game-highlights)

### Sports Alerts Terraform

Infrastructure as Code implementation of a sports alert system using Terraform.

**Key Features:**
- AWS Lambda for serverless processing
- AWS SNS for notifications
- EventBridge for scheduling
- Parameter Store for secure API key storage
- Comprehensive IAM policies

[Go to Sports Alerts Terraform →](./06sports-alerts-terraform)

## Technologies Used

- **Cloud Services**: AWS (S3, Lambda, SNS, ECS, Glue, Athena)
- **Containerization**: Docker
- **Infrastructure as Code**: Terraform
- **Programming Languages**: Python, JSON, HCL
- **CI/CD**: GitHub Actions
- **Media Processing**: FFmpeg
- **Web Frameworks**: Flask
- **API Management**: API Gateway
- **Security**: IAM, Parameter Store

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/CynthiaWahome/devopsChallengeAllStars25.git
   cd devopsChallenge25

## Acknowledgments

This challenge was created as part of the DevOps Challenge All-Stars 2025 organized by:

- [Ifeanyi Onyeabor](https://github.com/ifeanyiro9) - Challenge Creator & Mentor
- [Alicia Ahl](https://github.com/alahl1) - Challenge Creator & Mentor
- [Shae Cloud](https://github.com/ShaeInTheCloud) - Challenge Creator & Mentor

Special thanks to the entire DevOps Challenge team for their mentorship and guidance throughout this learning journey. 
Their expertise and well-structured challenge projects provided an excellent opportunity to develop practical DevOps skills with real-world applications.
