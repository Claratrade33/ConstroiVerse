# Documentação de Deploy para AWS

Esta documentação detalha os passos necessários para realizar o deploy da aplicação ConstroiVerse na Amazon Web Services (AWS).

## 1. Pré-requisitos

Antes de iniciar o processo de deploy, certifique-se de ter os seguintes pré-requisitos:

*   Conta AWS ativa com permissões administrativas.
*   AWS CLI configurado localmente.
*   Docker e Docker Compose instalados (para deploy containerizado).
*   Git instalado.
*   Repositório do projeto clonado localmente.

## 2. Estratégia de Deploy

Considerando a arquitetura da aplicação (backend Flask, frontend e MongoDB Atlas), a estratégia de deploy recomendada para a AWS envolve:

*   **Backend (API Flask):** Utilização do AWS Elastic Beanstalk ou AWS Fargate para deploy de containers Docker.
*   **Frontend (Cliente Web):** Hospedagem de arquivos estáticos no AWS S3 com distribuição via AWS CloudFront.
*   **Banco de Dados:** MongoDB Atlas (já configurado e gerenciado externamente).

## 3. Deploy do Backend (Flask API)

### Opção A: AWS Elastic Beanstalk (Recomendado para simplicidade)

1.  **Crie um ambiente Elastic Beanstalk:**
    *   Vá para o console do Elastic Beanstalk.
    *   Crie uma nova aplicação e um novo ambiente.
    *   Escolha a plataforma `Python` e o tipo de ambiente `Web server environment`.
    *   Faça upload do seu código-fonte (o diretório `backend` do seu projeto).
    *   Configure as variáveis de ambiente necessárias (ex: `MONGO_URI`, `JWT_SECRET_KEY`).

2.  **Configuração do Docker (se aplicável):**
    *   Se o backend estiver containerizado, inclua um `Dockerfile` e `requirements.txt` no diretório raiz do backend.
    *   O Elastic Beanstalk pode construir e executar o container automaticamente.

### Opção B: AWS Fargate (Para maior controle e escalabilidade)

1.  **Crie um repositório ECR (Elastic Container Registry):**
    *   Faça o build da imagem Docker do seu backend.
    *   Faça o push da imagem para o ECR.

2.  **Crie um Cluster ECS (Elastic Container Service):**
    *   Defina uma `Task Definition` para o seu container, especificando a imagem do ECR, portas, variáveis de ambiente, etc.
    *   Crie um `Service` no ECS para executar e manter o número desejado de tarefas (instâncias do seu container).
    *   Configure um `Load Balancer` (ALB) para distribuir o tráfego para as tarefas do ECS.

## 4. Deploy do Frontend (Cliente Web)

1.  **Crie um bucket S3:**
    *   Crie um novo bucket S3.
    *   Configure-o para hospedagem de site estático.
    *   Faça upload dos arquivos estáticos do seu frontend (HTML, CSS, JS, imagens) para o bucket.

2.  **Configure o CloudFront (Opcional, mas recomendado para performance e segurança):**
    *   Crie uma distribuição CloudFront apontando para o seu bucket S3 como origem.
    *   Configure um certificado SSL/TLS (AWS Certificate Manager) para HTTPS.

## 5. Variáveis de Ambiente

Certifique-se de que todas as variáveis de ambiente necessárias para o backend (como `MONGO_URI`, `JWT_SECRET_KEY`, etc.) estejam configuradas corretamente no ambiente de deploy (Elastic Beanstalk ou ECS Task Definition).

## 6. Monitoramento e Logs

*   Utilize o AWS CloudWatch para monitorar a saúde da aplicação e coletar logs.
*   Configure alarmes para eventos importantes (erros, alta utilização de CPU, etc.).

## 7. Atualizações e Manutenção

*   Para atualizar o backend, faça o deploy de uma nova versão do código (Elastic Beanstalk) ou de uma nova imagem Docker (Fargate).
*   Para atualizar o frontend, faça o upload dos novos arquivos para o S3 e invalide o cache do CloudFront (se estiver usando).

---

**Autor:** Manus AI
**Data:** 12 de Outubro de 2025
