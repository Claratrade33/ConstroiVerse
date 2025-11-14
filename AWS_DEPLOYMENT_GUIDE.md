# Guia de Implantação do ConstroiVerse MVP na AWS (ECS/ECR)

Este guia detalha os passos necessários para implantar o backend do ConstroiVerse na Amazon Web Services (AWS) usando o Elastic Container Registry (ECR) e o Elastic Container Service (ECS).

## 1. Pré-requisitos

*   Conta AWS ativa.
*   AWS CLI configurada localmente.
*   Docker instalado localmente.
*   Código-fonte do ConstroiVerse (diretório `backend/`).

## 2. Configuração do Elastic Container Registry (ECR)

O ECR será usado para armazenar a imagem Docker do seu aplicativo.

1.  **Crie um Repositório ECR:**
    \`\`\`bash
    aws ecr create-repository --repository-name construiverse-mvp --region sua-regiao
    \`\`\`
    *Substitua \`sua-regiao\` pela região AWS desejada (ex: \`sa-east-1\` para São Paulo).*

2.  **Autentique o Docker:**
    \`\`\`bash
    aws ecr get-login-password --region sua-regiao | docker login --username AWS --password-stdin seu-aws-account-id.dkr.ecr.sua-regiao.amazonaws.com
    \`\`\`
    *Substitua \`seu-aws-account-id\` e \`sua-regiao\` pelos seus dados.*

## 3. Build e Push da Imagem Docker

1.  **Navegue até o Diretório do Backend:**
    \`\`\`bash
    cd /caminho/para/construiverse-unified/backend
    \`\`\`

2.  **Build da Imagem:**
    O `Dockerfile` já está configurado para instalar as dependências de SSL necessárias (`libssl-dev`, `build-essential`) e o `pymongo[srv]`.
    \`\`\`bash
    docker build -t construiverse-mvp .
    \`\`\`

3.  **Tag da Imagem:**
    \`\`\`bash
    docker tag construiverse-mvp:latest seu-aws-account-id.dkr.ecr.sua-regiao.amazonaws.com/construiverse-mvp:latest
    \`\`\`

4.  **Push para o ECR:**
    \`\`\`bash
    docker push seu-aws-account-id.dkr.ecr.sua-regiao.amazonaws.com/construiverse-mvp:latest
    \`\`\`

## 4. Configuração do Elastic Container Service (ECS)

O ECS será usado para orquestrar e executar o contêiner.

1.  **Crie um Cluster ECS:**
    Use o console AWS ou a CLI para criar um cluster ECS (tipo Fargate é recomendado para simplicidade).

2.  **Crie uma Definição de Tarefa (Task Definition):**
    *   **Família:** `construiverse-mvp-task`
    *   **Tipo de Lançamento:** Fargate
    *   **Contêiner:**
        *   **Nome:** `construiverse-mvp-container`
        *   **Imagem:** `seu-aws-account-id.dkr.ecr.sua-regiao.amazonaws.com/construiverse-mvp:latest`
        *   **Porta:** `5000` (mapeada para a porta 5000 do contêiner)
    *   **Variáveis de Ambiente:**
        *   `MONGO_URI`: Sua string de conexão real do MongoDB Atlas.
        *   `DB_NAME`: O nome do seu banco de dados.
        *   *Recomendação: Use o AWS Secrets Manager para gerenciar a \`MONGO_URI\` de forma segura.*

3.  **Crie um Serviço ECS:**
    *   **Cluster:** O cluster criado na etapa 1.
    *   **Tipo de Lançamento:** Fargate
    *   **Definição de Tarefa:** A definição de tarefa criada na etapa 2.
    *   **Balanceador de Carga (Load Balancer):** Configure um Application Load Balancer (ALB) para expor o serviço publicamente na porta 80/443, direcionando o tráfego para a porta 5000 do contêiner.

## 5. Configuração do MongoDB Atlas

1.  **Lista de Acesso IP:** Certifique-se de que o grupo de segurança da sua VPC/ECS tenha acesso à sua rede do MongoDB Atlas. A maneira mais fácil é adicionar `0.0.0.0/0` (acesso irrestrito) para testes iniciais, mas **recomenda-se restringir** ao IP de saída do seu ALB/VPC em produção.
2.  **String de Conexão:** Use a string de conexão `mongodb+srv://...` e certifique-se de que o usuário e a senha estejam corretos.

## 6. Teste Final

Após o deploy do serviço ECS, o ALB fornecerá um DNS público. Teste as rotas da API (ex: `http://seu-alb-dns/api/profissoes`) para confirmar que o serviço está ativo e se conectando ao MongoDB Atlas.

**Observação:** O código atual está usando lógica simulada. Para a implantação final, você deve **descomentar a lógica de banco de dados** em `src/database.py` e nas rotas, e garantir que as variáveis de ambiente (`MONGO_URI`, `DB_NAME`) estejam configuradas corretamente no ECS.
