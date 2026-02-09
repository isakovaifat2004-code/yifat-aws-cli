# AWS Platform Engineering CLI - Yifat's Project

This is a self-service CLI tool designed for developers to request and manage AWS resources within safe standards.

## 🛠 Prerequisites
* Python 3.x
* AWS CLI configured with valid credentials
* Dependencies installed (see below)

## 🚀 Installation
To install the required libraries, run:
```bash

pip install -r requirements.txt
## 🚀 Usage Examples

### EC2 Management
- List instances: `python yifat-main.py list-ec2`
- Stop an instance: `python yifat-main.py stop-ec2 <instance-id>`

### S3 Management
- Create a bucket: `python yifat-main.py create-s3 <bucket-name>`

### Route53 Management
- Create a zone: `python yifat-main.py create-zone <domain-name>`

## 🏷️ Tagging Convention
All resources created by this tool are automatically tagged with:
`CreatedBy: platform-cli`

## 🧹 Cleanup
To avoid AWS charges, please ensure you delete created S3 buckets and Route53 zones after testing.

## 📸 Demo Evidence
<img width="854" height="92" alt="image" src="https://github.com/user-attachments/assets/9f3ec952-4950-41c4-8ad7-fbfbac9a9147" />
