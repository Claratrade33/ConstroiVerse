# Arquitetura Completa do Construiverse

## Visão Geral

O **Construiverse** é uma plataforma integrada de gestão para a indústria da construção civil, combinando funcionalidades de marketplace, gestão de projetos, comunicação interna e inovação com IA. A plataforma une profissionais, clientes, fornecedores e corretores em um ecossistema digital completo.

## Estrutura do Projeto

```
construiverse-unified/
├── backend/
│   ├── src/
│   │   ├── main.py                 # Aplicação Flask principal
│   │   ├── config/
│   │   │   └── database.py         # Configuração MongoDB
│   │   ├── models/
│   │   │   ├── mongodb_models.py   # Modelos base (Usuário, Projeto, etc)
│   │   │   └── professional_models.py # Modelos avançados
│   │   └── routes/
│   │       ├── user.py             # Gerenciamento de usuários
│   │       ├── projetos.py         # Gerenciamento de projetos
│   │       ├── professionals.py    # Vitrine de profissionais
│   │       ├── financial.py        # Gestão financeira
│   │       ├── communication.py    # Chat e e-mail
│   │       ├── real_estate.py      # Módulo imobiliário
│   │       ├── orcamentos.py       # Orçamentos
│   │       ├── ia.py               # Integração com IA
│   │       ├── financeiro.py       # Financeiro
│   │       └── vitrine.py          # Vitrine de profissionais
│   ├── requirements.txt            # Dependências Python
│   └── database.py                 # Configuração do banco
├── frontend/                       # (A ser desenvolvido)
├── docs/
│   ├── ARCHITECTURE.md             # Documentação de arquitetura
│   ├── AWS_DEPLOYMENT.md           # Guia de deploy na AWS
│   └── ARCHITECTURE_COMPLETE.md    # Este arquivo
└── tests/
    ├── test_user_routes.py
    └── test_projetos_routes.py
```

## Modelos de Dados

### 1. Modelos Base (mongodb_models.py)

#### Usuario
- **_id**: ObjectId (PK)
- **nome**: string
- **email**: string (único)
- **senha_hash**: string
- **tipo_usuario**: "Cliente" | "Profissional" | "Loja" | "Corretor"
- **telefone**: string
- **endereco**: string
- **cidade**: string
- **estado**: string
- **data_criacao**: datetime
- **ativo**: boolean

#### Projeto
- **_id**: ObjectId (PK)
- **usuario_id**: ObjectId (FK - Usuario)
- **nome**: string
- **descricao**: string
- **localizacao**: string
- **data_inicio**: datetime
- **data_fim_prevista**: datetime
- **status**: "planejamento" | "em_andamento" | "concluido"
- **orcamento_total**: float
- **profissionais_envolvidos**: List[ObjectId]
- **materiais**: List[ObjectId]

#### Orcamento
- **_id**: ObjectId (PK)
- **projeto_id**: ObjectId (FK - Projeto)
- **usuario_solicitante**: ObjectId (FK - Usuario)
- **usuario_fornecedor**: ObjectId (FK - Usuario)
- **valor_total**: float
- **status**: "pendente" | "aceito" | "rejeitado"
- **data_criacao**: datetime
- **data_validade**: datetime
- **itens**: List[{material_id, quantidade, preco_unitario}]

### 2. Modelos Avançados (professional_models.py)

#### ProfessionalProfile
- **_id**: ObjectId (PK)
- **user_id**: ObjectId (FK - Usuario)
- **name**: string
- **email**: string
- **phone**: string
- **profession**: string (ex: "Pedreiro", "Eletricista")
- **location**: string
- **experience_years**: integer
- **profile_image_url**: string (opcional)
- **portfolio_images**: List[string]
- **average_rating**: float (0-5)
- **total_reviews**: integer
- **reviews**: List[{reviewer_id, rating, comment, date}]
- **is_available**: boolean
- **specialties**: List[string]
- **created_at**: datetime
- **updated_at**: datetime

#### FinancialRecord
- **_id**: ObjectId (PK)
- **user_id**: ObjectId (FK - Usuario)
- **project_id**: ObjectId (FK - Projeto, opcional)
- **type**: "income" | "expense"
- **category**: string (ex: "salary", "material", "equipment")
- **description**: string
- **amount**: float
- **currency**: string (default: "BRL")
- **date**: datetime
- **payment_method**: string (ex: "cash", "transfer", "credit_card")
- **status**: "pending" | "completed" | "cancelled"
- **invoice_number**: string (opcional)
- **notes**: string (opcional)
- **attachments**: List[string] (URLs)
- **created_at**: datetime
- **updated_at**: datetime

#### Message
- **_id**: ObjectId (PK)
- **sender_id**: ObjectId (FK - Usuario)
- **recipient_id**: ObjectId (FK - Usuario)
- **subject**: string (opcional, para e-mails)
- **content**: string
- **message_type**: "chat" | "email"
- **is_read**: boolean
- **read_at**: datetime (opcional)
- **attachments**: List[string] (URLs)
- **created_at**: datetime
- **updated_at**: datetime

#### RealEstateProperty
- **_id**: ObjectId (PK)
- **owner_id**: ObjectId (FK - Usuario)
- **title**: string
- **description**: string
- **property_type**: "house" | "apartment" | "commercial" | "land"
- **address**: string
- **city**: string
- **state**: string
- **zip_code**: string
- **area_sqm**: float
- **bedrooms**: integer
- **bathrooms**: integer
- **parking_spaces**: integer
- **price**: float
- **currency**: string (default: "BRL")
- **status**: "available" | "sold" | "rented"
- **images**: List[string] (URLs)
- **assigned_brokers**: List[ObjectId]
- **is_construction**: boolean
- **construction_status**: string (opcional)
- **estimated_completion**: datetime (opcional)
- **professionals_involved**: List[ObjectId]
- **created_at**: datetime
- **updated_at**: datetime

#### BrokerProfile
- **_id**: ObjectId (PK)
- **user_id**: ObjectId (FK - Usuario)
- **name**: string
- **email**: string
- **phone**: string
- **creci**: string (número do CRECI)
- **company**: string (opcional)
- **bio**: string (opcional)
- **profile_image_url**: string (opcional)
- **average_rating**: float
- **total_reviews**: integer
- **managed_properties**: List[ObjectId]
- **is_active**: boolean
- **created_at**: datetime
- **updated_at**: datetime

#### SmartStoreInteraction
- **_id**: ObjectId (PK)
- **property_id**: ObjectId (FK - RealEstateProperty)
- **visitor_name**: string
- **visitor_email**: string
- **visitor_phone**: string (opcional)
- **interaction_type**: "inquiry" | "visit" | "purchase_interest"
- **message**: string
- **ai_response**: string (opcional)
- **ai_sentiment**: "positive" | "neutral" | "negative" (opcional)
- **follow_up_status**: "pending" | "contacted" | "converted"
- **assigned_broker**: ObjectId (opcional)
- **created_at**: datetime
- **updated_at**: datetime

#### Task
- **_id**: ObjectId (PK)
- **project_id**: ObjectId (FK - Projeto)
- **title**: string
- **description**: string
- **category**: string (ex: "foundation", "ceramic", "painting")
- **assigned_professionals**: List[ObjectId]
- **status**: "pending" | "in_progress" | "completed" | "certified"
- **start_date**: datetime (opcional)
- **due_date**: datetime (opcional)
- **completion_date**: datetime (opcional)
- **professional_rating**: float (opcional)
- **project_manager_rating**: float (opcional)
- **project_owner_rating**: float (opcional)
- **notes**: string (opcional)
- **created_at**: datetime
- **updated_at**: datetime

## Rotas da API

### Autenticação e Usuários
```
POST   /api/auth/register          # Registrar novo usuário
POST   /api/auth/login             # Fazer login
POST   /api/auth/logout            # Fazer logout
GET    /api/users/{user_id}        # Obter perfil do usuário
PUT    /api/users/{user_id}        # Atualizar perfil
DELETE /api/users/{user_id}        # Deletar usuário
```

### Projetos
```
GET    /api/projetos               # Listar projetos
POST   /api/projetos               # Criar novo projeto
GET    /api/projetos/{project_id}  # Obter detalhes do projeto
PUT    /api/projetos/{project_id}  # Atualizar projeto
DELETE /api/projetos/{project_id}  # Deletar projeto
```

### Vitrine de Profissionais
```
GET    /api/professionals          # Listar profissionais (com filtros)
POST   /api/professionals          # Criar perfil de profissional
GET    /api/professionals/{id}     # Obter detalhes do profissional
PUT    /api/professionals/{id}     # Atualizar perfil
DELETE /api/professionals/{id}     # Deletar perfil
POST   /api/professionals/{id}/reviews        # Adicionar avaliação
GET    /api/professionals/{id}/reviews        # Obter avaliações
```

### Gestão Financeira
```
GET    /api/financial/records      # Listar registros financeiros
POST   /api/financial/records      # Criar novo registro
GET    /api/financial/records/{id} # Obter detalhes do registro
PUT    /api/financial/records/{id} # Atualizar registro
DELETE /api/financial/records/{id} # Deletar registro
GET    /api/financial/summary/{user_id}  # Obter resumo financeiro
```

### Comunicação Interna
```
GET    /api/communication/messages/{user_id}        # Listar mensagens
POST   /api/communication/messages                  # Enviar mensagem
GET    /api/communication/messages/{message_id}    # Obter mensagem
PUT    /api/communication/messages/{id}/read       # Marcar como lida
DELETE /api/communication/messages/{message_id}    # Deletar mensagem
GET    /api/communication/conversations/{user_id}  # Listar conversas
GET    /api/communication/conversations/{user_id}/{other_user_id}  # Obter conversa
```

### Módulo Imobiliário
```
GET    /api/real-estate/properties          # Listar propriedades
POST   /api/real-estate/properties          # Criar propriedade
GET    /api/real-estate/properties/{id}     # Obter detalhes
PUT    /api/real-estate/properties/{id}     # Atualizar propriedade
DELETE /api/real-estate/properties/{id}     # Deletar propriedade

GET    /api/real-estate/brokers             # Listar corretores
POST   /api/real-estate/brokers             # Criar perfil de corretor
GET    /api/real-estate/brokers/{id}        # Obter detalhes do corretor
PUT    /api/real-estate/brokers/{id}        # Atualizar corretor

POST   /api/real-estate/smartstore/interactions           # Registrar interação IA
GET    /api/real-estate/smartstore/interactions/{property_id}  # Obter interações
PUT    /api/real-estate/smartstore/interactions/{id}/assign-broker  # Atribuir corretor
```

## Funcionalidades Principais

### 1. Vitrine de Profissionais
- **Perfil de Profissional**: Exibição completa com foto, especialidades, experiência
- **Avaliações**: Sistema de 5 estrelas com comentários de clientes
- **Busca e Filtros**: Por profissão, localização, avaliação mínima
- **Convites para Obras**: Clientes podem convidar profissionais para projetos
- **Portfólio**: Galeria de projetos anteriores

### 2. Gestão Financeira
- **Registros de Entrada/Saída**: Controle completo de fluxo de caixa
- **Categorização**: Salários, materiais, equipamentos, serviços
- **Resumos Financeiros**: Totalizações por período
- **Integração com Projetos**: Associação de despesas a projetos específicos
- **Documentação**: Suporte a anexos (notas fiscais, comprovantes)

### 3. Comunicação Interna
- **Chat em Tempo Real**: Mensagens instantâneas entre usuários
- **E-mail Formal**: Sistema de e-mail para comunicações oficiais
- **Histórico**: Armazenamento de todas as mensagens
- **Leitura**: Indicador de mensagens lidas/não lidas
- **Anexos**: Suporte a documentos e imagens

### 4. Módulo Imobiliário
- **Publicação de Propriedades**: Casas, apartamentos, terrenos, comerciais
- **Gestão de Corretores**: Cadastro e avaliação de corretores
- **Obras em Andamento**: Publicação de obras com status de construção
- **SmartStore IA**: Interação automática com visitantes
- **Sugestões Inteligentes**: Recomendação de imóveis por localização

### 5. SmartStore IA (Inovação)
- **Interação Automática**: IA interage com visitantes de propriedades
- **Coleta de Contatos**: Captura informações de leads interessados
- **Análise de Sentimento**: Avalia interesse do visitante
- **Atribuição de Corretor**: Distribui leads para corretores
- **Follow-up Automático**: Rastreamento de conversão

### 6. Gestão de Projetos
- **Criação de Projetos**: Definição de escopo, datas, orçamento
- **Atribuição de Tarefas**: Distribuição de atividades para profissionais
- **Acompanhamento**: Status em tempo real de cada tarefa
- **Avaliações**: Feedback de qualidade após conclusão
- **Documentação**: Armazenamento de planos e especificações

## Fluxos de Negócio

### Fluxo 1: Contratação de Profissional
1. Cliente busca profissional na vitrine
2. Cliente visualiza perfil, avaliações e portfólio
3. Cliente envia convite para obra
4. Profissional aceita ou recusa
5. Projeto é criado com profissional atribuído
6. Tarefas são criadas e atribuídas
7. Profissional marca tarefas como concluídas
8. Responsável verifica e avalia
9. Avaliação é registrada no perfil

### Fluxo 2: Venda de Imóvel
1. Proprietário publica propriedade
2. SmartStore IA interage com visitantes
3. IA coleta contatos e analisa interesse
4. Leads são atribuídos a corretores
5. Corretor faz follow-up
6. Propriedade é marcada como vendida
7. Transação é registrada

### Fluxo 3: Gestão Financeira
1. Usuário registra entrada/saída
2. Sistema categoriza automaticamente
3. Resumo é atualizado em tempo real
4. Relatórios são gerados por período
5. Integração com projetos para análise de lucratividade

## Tecnologias Utilizadas

### Backend
- **Framework**: Flask (Python)
- **Banco de Dados**: MongoDB
- **ORM**: PyMongo
- **Validação**: Pydantic
- **API**: RESTful com JSON
- **Autenticação**: JWT (a implementar)
- **CORS**: Flask-CORS

### Frontend (A ser desenvolvido)
- **Framework**: React.js
- **Estilização**: Tailwind CSS
- **Gerenciamento de Estado**: Redux
- **Requisições HTTP**: Axios
- **Roteamento**: React Router

### DevOps
- **Cloud**: AWS (EC2, RDS, S3)
- **Containerização**: Docker
- **CI/CD**: GitHub Actions
- **Monitoramento**: CloudWatch

## Segurança

### Implementações
- **Hashing de Senhas**: bcrypt
- **Autenticação**: JWT
- **CORS**: Configurado para domínios específicos
- **Validação de Entrada**: Pydantic
- **Rate Limiting**: (A implementar)
- **Criptografia**: HTTPS/TLS

### Boas Práticas
- Variáveis de ambiente para secrets
- Separação de ambientes (dev, staging, prod)
- Logs de auditoria para operações críticas
- Backup automático do banco de dados

## Próximas Etapas

1. **Implementação de Autenticação**: JWT com refresh tokens
2. **Integração com IA**: OpenAI para SmartStore
3. **Frontend**: Desenvolvimento da interface React
4. **Testes**: Testes unitários e de integração
5. **Deploy**: Configuração na AWS
6. **Monitoramento**: Setup de logs e alertas
7. **Documentação**: API docs com Swagger

## Conclusão

O Construiverse é uma plataforma ambiciosa que integra múltiplas funcionalidades para transformar a indústria da construção civil. Com a arquitetura modular e escalável, o sistema pode crescer e evoluir conforme as necessidades do mercado.
