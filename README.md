# Face Recognition as a Service on AWS PaaS

This repository contains the implementation of a cloud application providing face recognition as a service on videos streamed from clients, using AWS Lambda and other supporting AWS services.

## Project Overview

In this project, we developed a serverless cloud application using AWS Lambda and S3 to process video files and perform face recognition. The application is divided into two parts:
1. **Video Splitting Function**: Splits uploaded videos into frames and stores them in an S3 bucket.
2. **Face Recognition Function**: (To be implemented in Part 2) Processes frames to recognize faces and store results.

### Input Bucket
- Stores videos uploaded by clients.
- Naming convention: `id-input` (e.g., `12345678910-input`).
- Contains only `.mp4` video files.
- Triggers the `video-splitting` Lambda function upon new video upload.

### Video Splitting Function
- Lambda function named `video-splitting`.
- Triggered by new video uploads in the input bucket.
- Splits videos into Group-of-Pictures (GoP) using `ffmpeg`.
- Stores GoP in a corresponding folder in the `id-stage-1` bucket.

### Stage-1 Bucket
- Stores results of the `video-splitting` function.
- Naming convention: `id-stage-1`.
- Contains folders named after the input videos without extensions, each holding frame images.

## Files and Directory Structure
    Dockerfile.txt
    entry.sh
    handler.py
    requirements.txt
    README.md


### Dockerfile.txt
- Defines the Docker image for the Lambda function, including dependencies and `ffmpeg` installation.

### entry.sh
- Script to facilitate local testing of the Lambda function using AWS Lambda Runtime Interface Emulator.

### handler.py
- Lambda function code to handle video splitting and interaction with S3.

### requirements.txt
- Lists the Python dependencies required by the Lambda function.

## Setup and Deployment

### Prerequisites
- AWS account with necessary permissions.
- AWS CLI configured with appropriate credentials.

### Steps
1. **Create S3 Buckets**:
   - Input bucket: `id-input`
   - Stage-1 bucket: `id-stage-1`

2. **Deploy Lambda Function**:
   - Build Docker image:
     ```sh
     docker build -t video-splitting .
     ```
   - Create a Lambda function using the Docker image:
     ```sh
     aws lambda create-function --function-name video-splitting \
       --package-type Image \
       --code ImageUri=<your-docker-image-uri> \
       --role <your-lambda-role-arn>
     ```

3. **Configure S3 Trigger**:
   - Set up S3 event notification on the input bucket to trigger the `video-splitting` Lambda function on new object creation.

### Testing
- Use the provided workload generator to upload videos to the input bucket and verify that frames are correctly processed and stored in the stage-1 bucket.

## IAM Permissions for Grading
Create an IAM user with the following permissions and provide the access keys for grading:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:Get*",
        "s3:PutObject",
        "s3:List*",
        "lambda:GetFunction",
        "cloudwatch:GetMetricData"
      ],
      "Resource": "*"
    }
  ]
}
```
