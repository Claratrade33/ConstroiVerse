# Guia Completo de Deploy na AWS

## Visão Geral

Este guia fornece instruções passo a passo para fazer o deploy do Construiverse na AWS, utilizando os melhores serviços disponíveis para escalabilidade, segurança e performance.

## Arquitetura na AWS

```
┌─────────────────────────────────────────────────────────────┐
│                        Route 53 (DNS)                        │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    CloudFront (CDN)                          │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                  Application Load Balancer                   │
└────────────────────────────┬────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼──────┐    ┌────────▼────────┐   ┌──────▼──────┐
│   ECS Task   │    │   ECS Task      │   │  ECS Task   │
│   (Backend)  │    │   (Backend)     │   │  (Backend)  │
└──────────────┘    └─────────────────┘   └─────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    MongoDB Atlas                             │
│              (Banco de dados gerenciado)                     │
└─────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼──────┐    ┌────────▼────────┐   ┌──────▼──────┐
│   S3 Bucket  │    │  CloudWatch     │   │   Secrets   │
│  (Arquivos)  │    │   (Logs)        │   │  Manager    │
└──────────────┘    └─────────────────┘   └─────────────┘
```

## Pré-requisitos

- Conta AWS ativa
- AWS CLI instalado e configurado
- Docker instalado localmente
- Git configurado
- Conhecimento básico de AWS

## Passo 1: Preparar a Aplicação

### 1.1 Criar arquivo .dockerignore

```
__pycache__
*.pyc
.env
.git
.gitignore
.pytest_cache
tests/
docs/
```

### 1.2 Criar arquivo .env para produção

```env
MONGODB_URI=mongodb+srv://fragmentosdaalma33_db_user:<password>@cluster0.dxbozq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
FLASK_ENV=production
SECRET_KEY=<gerar_chave_segura>
JWT_SECRET_KEY=<gerar_chave_segura>
AWS_REGION=sa-east-1
```

### 1.3 Testar Docker localmente

```bash
docker build -t construiverse:latest .
docker run -p 5000:5000 construiverse:latest
```

## Passo 2: Configurar ECR (Elastic Container Registry)

### 2.1 Criar repositório ECR

```bash
aws ecr create-repository \
  --repository-name construiverse \
  --region sa-east-1
```

### 2.2 Fazer login no ECR

```bash
aws ecr get-login-password --region sa-east-1 | \
  docker login --username AWS --password-stdin \
  <ACCOUNT_ID>.dkr.ecr.sa-east-1.amazonaws.com
```

### 2.3 Fazer push da imagem

```bash
docker tag construiverse:latest \
  <ACCOUNT_ID>.dkr.ecr.sa-east-1.amazonaws.com/construiverse:latest

docker push \
  <ACCOUNT_ID>.dkr.ecr.sa-east-1.amazonaws.com/construiverse:latest
```

## Passo 3: Configurar ECS (Elastic Container Service)

### 3.1 Criar cluster ECS

```bash
aws ecs create-cluster \
  --cluster-name construiverse-cluster \
  --region sa-east-1
```

### 3.2 Criar task definition

Criar arquivo `ecs-task-definition.json`:

```json
{
  "family": "construiverse-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "construiverse",
      "image": "<ACCOUNT_ID>.dkr.ecr.sa-east-1.amazonaws.com/construiverse:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "MONGODB_URI",
          "valueFrom": "arn:aws:secretsmanager:sa-east-1:<ACCOUNT_ID>:secret:construiverse/mongodb-uri"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/construiverse",
          "awslogs-region": "sa-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "executionRoleArn": "arn:aws:iam::<ACCOUNT_ID>:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::<ACCOUNT_ID>:role/ecsTaskRole"
}
```

Registrar task definition:

```bash
aws ecs register-task-definition \
  --cli-input-json file://ecs-task-definition.json \
  --region sa-east-1
```

### 3.3 Criar serviço ECS

```bash
aws ecs create-service \
  --cluster construiverse-cluster \
  --service-name construiverse-service \
  --task-definition construiverse-task:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:sa-east-1:<ACCOUNT_ID>:targetgroup/construiverse/xxx,containerName=construiverse,containerPort=5000 \
  --region sa-east-1
```

## Passo 4: Configurar Load Balancer

### 4.1 Criar Application Load Balancer

```bash
aws elbv2 create-load-balancer \
  --name construiverse-alb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx \
  --scheme internet-facing \
  --type application \
  --region sa-east-1
```

### 4.2 Criar target group

```bash
aws elbv2 create-target-group \
  --name construiverse-tg \
  --protocol HTTP \
  --port 5000 \
  --vpc-id vpc-xxx \
  --target-type ip \
  --region sa-east-1
```

### 4.3 Criar listener

```bash
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:sa-east-1:<ACCOUNT_ID>:loadbalancer/app/construiverse-alb/xxx \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:sa-east-1:<ACCOUNT_ID>:targetgroup/construiverse-tg/xxx \
  --region sa-east-1
```

## Passo 5: Configurar Secrets Manager

### 5.1 Armazenar secrets

```bash
aws secretsmanager create-secret \
  --name construiverse/mongodb-uri \
  --secret-string "mongodb+srv://..." \
  --region sa-east-1

aws secretsmanager create-secret \
  --name construiverse/jwt-secret \
  --secret-string "<JWT_SECRET_KEY>" \
  --region sa-east-1
```

## Passo 6: Configurar CloudWatch

### 6.1 Criar log group

```bash
aws logs create-log-group \
  --log-group-name /ecs/construiverse \
  --region sa-east-1
```

### 6.2 Criar alarmes

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name construiverse-cpu-high \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --region sa-east-1
```

## Passo 7: Configurar Route 53

### 7.1 Criar hosted zone

```bash
aws route53 create-hosted-zone \
  --name construiverse.com \
  --caller-reference $(date +%s)
```

### 7.2 Criar registros DNS

```bash
aws route53 change-resource-record-sets \
  --hosted-zone-id <ZONE_ID> \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "api.construiverse.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "<ALB_ZONE_ID>",
          "DNSName": "construiverse-alb-xxx.sa-east-1.elb.amazonaws.com",
          "EvaluateTargetHealth": false
        }
      }
    }]
  }'
```

## Passo 8: Configurar CI/CD com GitHub Actions

O arquivo `.github/workflows/deploy.yml` já está configurado para:

1. Executar testes automaticamente
2. Fazer build da imagem Docker
3. Fazer push para ECR
4. Fazer deploy para ECS

### 8.1 Adicionar secrets no GitHub

Vá para Settings > Secrets and variables > Actions e adicione:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_ACCOUNT_ID`

## Passo 9: Monitoramento e Manutenção

### 9.1 Verificar logs

```bash
aws logs tail /ecs/construiverse --follow
```

### 9.2 Escalar serviço

```bash
aws ecs update-service \
  --cluster construiverse-cluster \
  --service construiverse-service \
  --desired-count 3 \
  --region sa-east-1
```

### 9.3 Fazer rollback

```bash
aws ecs update-service \
  --cluster construiverse-cluster \
  --service construiverse-service \
  --task-definition construiverse-task:1 \
  --region sa-east-1
```

## Checklist de Deploy

- [ ] Configurar ECR
- [ ] Fazer push da imagem Docker
- [ ] Criar cluster ECS
- [ ] Registrar task definition
- [ ] Criar serviço ECS
- [ ] Configurar Load Balancer
- [ ] Armazenar secrets no Secrets Manager
- [ ] Configurar CloudWatch
- [ ] Configurar Route 53
- [ ] Testar endpoints da API
- [ ] Configurar CI/CD
- [ ] Monitorar logs e métricas
- [ ] Configurar backups do MongoDB

## Estimativa de Custos

| Serviço | Estimativa Mensal |
|---------|-------------------|
| ECS Fargate | $50-100 |
| Load Balancer | $20 |
| MongoDB Atlas | $57 (M10) |
| CloudWatch | $10-20 |
| Route 53 | $0.50 |
| **Total** | **~$140-190** |

## Troubleshooting

### Erro: "Task failed to start"
- Verificar logs no CloudWatch
- Validar task definition
- Verificar security groups

### Erro: "Connection refused"
- Verificar se MongoDB Atlas está acessível
- Verificar variáveis de ambiente
- Verificar security groups

### Erro: "Out of memory"
- Aumentar memória na task definition
- Otimizar código da aplicação
- Implementar caching

## Recursos Adicionais

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [AWS Fargate Documentation](https://docs.aws.amazon.com/fargate/)
- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/)

## Suporte

Para dúvidas sobre o deploy, consulte:
1. A documentação da AWS
2. Os logs do CloudWatch
3. A comunidade do projeto

## Conclusão

Seguindo este guia, você terá o Construiverse rodando em produção na AWS com alta disponibilidade, escalabilidade e segurança.
