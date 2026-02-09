AWS Platform Engineering CLI - Yifat's Project

This is a self-service CLI tool designed for developers to request and manage AWS resources within safe standards.

🛠 Prerequisites

Python 3.x

AWS CLI configured with valid credentials

🚀 Installation

To install the required libraries, run:

pip install -r requirements.txt


🚀 Usage Examples

EC2 Management

List instances: python yifat-main.py list-ec2

Create instance: python yifat-main.py create-ec2 --type t3.micro

S3 Management

Create a bucket: python yifat-main.py create-s3 <bucket-name>

Route53 Management

Create a zone: python yifat-main.py create-zone <domain-name>

🏷️ Tagging Convention

All resources created by this tool are automatically tagged with:
CreatedBy: platform-cli

🧹 Cleanup

To avoid AWS charges, please ensure you delete created S3 buckets and Route53 zones after testing.

📸 Demo Evidence
<img width="864" height="118" alt="image" src="https://github.com/user-attachments/assets/3fec008e-b728-46aa-9815-65c9db71207b" />

<img width="609" height="216" alt="image" src="https://github.com/user-attachments/assets/164a3e1c-a147-4b62-b0e1-6ef75a0ccd24" />



