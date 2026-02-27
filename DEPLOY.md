
## STEP 1 - REBUILD YOUR DOCKER IMAGE
**Clone the repo if you are on a new machine or just navigate to the folder**  
```
cd C:\Users\henry\flask-cicd-api
venv\Scripts\activate
docker build -t flask-cicd-api .
```

## STEP 2 - RECREATE AWS INFRASTRUCTURE
**Authenticate to ECR, create the repository again, and push:**  
```
aws ecr create-repository --repository-name flask-cicd-api --region us-east-1

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 903236527067.dkr.ecr.us-east-1.amazonaws.com

docker tag flask-cicd-api:latest 903236527067.dkr.ecr.us-east-1.amazonaws.com/flask-cicd-api:latest

docker push 903236527067.dkr.ecr.us-east-1.amazonaws.com/flask-cicd-api:latest
```
**Then deploy to App Runner:**  
```
aws apprunner create-service --service-name flask-cicd-api --source-configuration "{\"ImageRepository\":{\"ImageIdentifier\":\"903236527067.dkr.ecr.us-east-1.amazonaws.com/flask-cicd-api:latest\",\"ImageConfiguration\":{\"Port\":\"5000\"},\"ImageRepositoryType\":\"ECR\"},\"AutoDeploymentsEnabled\":false,\"AuthenticationConfiguration\":{\"AccessRoleArn\":\"arn:aws:iam::903236527067:role/AppRunnerECRRole\"}}" --instance-configuration "{\"Cpu\":\"1 vCPU\",\"Memory\":\"2 GB\"}" --region us-east-1
```
**Note:** The IAM role AppRunnerECRRole still exists in your AWS account. You do not need to recreate it.

## STEP 3 - RECREATE AZURE INFRASTRUCTURE
```
az login

az group create --name flask-cicd-rg --location eastus

az acr create --resource-group flask-cicd-rg --name flaskcicdregistry --sku Basic --admin-enabled true

az acr login --name flaskcicdregistry

docker tag flask-cicd-api:latest flaskcicdregistry.azurecr.io/flask-cicd-api:latest

docker push flaskcicdregistry.azurecr.io/flask-cicd-api:latest

az containerapp env create --name flask-cicd-env --resource-group flask-cicd-rg --location eastus

az containerapp create --name flask-cicd-app --resource-group flask-cicd-rg --environment flask-cicd-env --image flaskcicdregistry.azurecr.io/flask-cicd-api:latest --target-port 5000 --ingress external --registry-server flaskcicdregistry.azurecr.io --query "properties.configuration.ingress.fqdn" --output json
```

## STEP 4 - VERIFY BOTH ARE LIVE

Hit the health endpoint on both URLs that get returned and confirm you see the healthy response.
