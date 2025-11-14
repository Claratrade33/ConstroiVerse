import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

from backend.routes.user import user_bp
from backend.routes.projetos import projetos_bp
# from backend.routes.orcamentos import orcamentos_bp
# from backend.routes.ia import ia_bp
# from backend.routes.financeiro import financeiro_bp
# from backend.routes.vitrine import vitrine_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'construiverse#2025$SECRET'

# Habilitar CORS para permitir requisições do frontend
CORS(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(projetos_bp, url_prefix='/api')
app.register_blueprint(orcamentos_bp, url_prefix='/api')
app.register_blueprint(ia_bp, url_prefix='/api')
app.register_blueprint(financeiro_bp, url_prefix='/api')
app.register_blueprint(vitrine_bp, url_prefix='/api')

# Configuração do banco de dados


# Criar tabelas e dados de exemplo
from src.config.database import mongodb, get_db, get_collection
from src.models.mongodb_models import Usuario, PerfilProfissional, PerfilVitrine, Loja, Material, Projeto, Orcamento, Transacao, AvaliacaoProfissional, ConviteObra, Imovel, COLLECTIONS

# Inicializar MongoDB
with app.app_context():
    try:
        mongodb.connect()
        db = get_db()
        
        # Criar coleções se não existirem e inserir dados de exemplo
        for collection_name, Model in COLLECTIONS.items():
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
                print(f"Coleção [32m'{collection_name}'[0m criada.")
            else:
                print(f"Coleção [33m'{collection_name}'[0m já existe.")
        
        # Inserir dados de exemplo se as coleções estiverem vazias
        if db.usuarios.count_documents({}) == 0:
            print("Inserindo dados de exemplo...")
            
            # Cliente
            cliente = Usuario(
                nome='João Silva',
                email='joao@email.com',
                senha_hash='hash_senha',
                tipo_usuario='Cliente'
            )
            db.usuarios.insert_one(cliente.to_dict())
            
            # Profissional (Arquiteto)
            usuario_arquiteto = Usuario(
                nome='Maria Arquiteta',
                email='maria@arquitetura.com',
                senha_hash='hash_senha',
                tipo_usuario='Profissional'
            )
            db.usuarios.insert_one(usuario_arquiteto.to_dict())
            
            perfil_arquiteto = PerfilProfissional(
                usuario_id=usuario_arquiteto.id,
                profissao='Arquiteto',
                crea_cau='CAU123456',
                especialidades='Projetos residenciais e comerciais'
            )
            db.perfis_profissionais.insert_one(perfil_arquiteto.to_dict())
            
            vitrine_arquiteto = PerfilVitrine(
                usuario_id=usuario_arquiteto.id,
                titulo_profissional='Arquiteto',
                descricao_resumida='Arquiteta especializada em projetos residenciais e comerciais',
                descricao_completa='Arquiteta com mais de 8 anos de experiência em projetos residenciais e comerciais. Especialista em sustentabilidade e design moderno.',
                cidade='São Paulo',
                estado='SP',
                telefone='(11) 99999-1234',
                email_contato='maria@arquitetura.com',
                anos_experiencia=8,
                projetos_concluidos=45,
                especialidades=['Projetos Residenciais', 'Projetos Comerciais', 'Sustentabilidade', 'Design Moderno'],
                preco_por_dia=450.00,
                preco_por_m2=35.00,
                nota_media=4.8,
                total_avaliacoes=12
            )
            db.perfis_vitrine.insert_one(vitrine_arquiteto.to_dict())
            
            profissionais_exemplo = [
                {
                    'nome': 'Carlos Pedreiro',
                    'email': 'carlos@pedreiro.com',
                    'titulo': 'Pedreiro / Oficial de Obras',
                    'descricao': 'Pedreiro experiente em alvenaria estrutural e de vedação',
                    'cidade': 'São Paulo',
                    'estado': 'SP',
                    'experiencia': 15,
                    'projetos': 120,
                    'preco_dia': 180.00,
                    'preco_m2': 25.00,
                    'nota': 4.6,
                    'avaliacoes': 28
                },
                {
                    'nome': 'Ana Pintora',
                    'email': 'ana@pintura.com',
                    'titulo': 'Pintor',
                    'descricao': 'Pintora especializada em acabamentos residenciais e comerciais',
                    'cidade': 'Rio de Janeiro',
                    'estado': 'RJ',
                    'experiencia': 6,
                    'projetos': 85,
                    'preco_dia': 150.00,
                    'preco_m2': 12.00,
                    'nota': 4.9,
                    'avaliacoes': 35
                },
                {
                    'nome': 'Roberto Eletricista',
                    'email': 'roberto@eletrica.com',
                    'titulo': 'Eletricista',
                    'descricao': 'Eletricista especializado em instalações residenciais e comerciais',
                    'cidade': 'Belo Horizonte',
                    'estado': 'MG',
                    'experiencia': 12,
                    'projetos': 95,
                    'preco_dia': 220.00,
                    'preco_m2': 35.00,
                    'nota': 4.7,
                    'avaliacoes': 22
                },
                {
                    'nome': 'Fernanda Engenheira',
                    'email': 'fernanda@engenharia.com',
                    'titulo': 'Engenheiro Civil',
                    'descricao': 'Engenheira Civil especializada em estruturas e fundações',
                    'cidade': 'São Paulo',
                    'estado': 'SP',
                    'experiencia': 10,
                    'projetos': 38,
                    'preco_dia': 650.00,
                    'preco_m2': 45.00,
                    'nota': 4.9,
                    'avaliacoes': 15
                },
                {
                    'nome': 'José Mestre',
                    'email': 'jose@mestre.com',
                    'titulo': 'Mestre de Obras',
                    'descricao': 'Mestre de obras com experiência em coordenação de equipes',
                    'cidade': 'Brasília',
                    'estado': 'DF',
                    'experiencia': 20,
                    'projetos': 78,
                    'preco_dia': 320.00,
                    'preco_m2': 18.00,
                    'nota': 4.5,
                    'avaliacoes': 31
                }
            ]
            
            for prof_data in profissionais_exemplo:
                usuario_prof = Usuario(
                    nome=prof_data['nome'],
                    email=prof_data['email'],
                    senha_hash='hash_senha',
                    tipo_usuario='Profissional'
                )
                db.usuarios.insert_one(usuario_prof.to_dict())
                
                vitrine_prof = PerfilVitrine(
                    usuario_id=usuario_prof.id,
                    titulo_profissional=prof_data['titulo'],
                    descricao_resumida=prof_data['descricao'],
                    cidade=prof_data['cidade'],
                    estado=prof_data['estado'],
                    telefone=f"({prof_data['estado'][:2]}) 99999-{prof_data['nome'][:4]}",
                    email_contato=prof_data['email'],
                    anos_experiencia=prof_data['experiencia'],
                    projetos_concluidos=prof_data['projetos'],
                    preco_por_dia=prof_data['preco_dia'],
                    preco_por_m2=prof_data['preco_m2'],
                    nota_media=prof_data['nota'],
                    total_avaliacoes=prof_data['avaliacoes']
                )
                db.perfis_vitrine.insert_one(vitrine_prof.to_dict())
            
            lojas_exemplo = [
                {
                    'nome': 'Construção Total',
                    'email': 'contato@construcaototal.com',
                    'fantasia': 'Construção Total',
                    'razao': 'Construção Total Ltda',
                    'cnpj': '12.345.678/0001-90',
                    'endereco': 'Rua das Construções, 123 - São Paulo/SP',
                    'telefone': '(11) 1234-5678'
                },
                {
                    'nome': 'Material Prime',
                    'email': 'vendas@materialprime.com',
                    'fantasia': 'Material Prime',
                    'razao': 'Material Prime S.A.',
                    'cnpj': '98.765.432/0001-10',
                    'endereco': 'Av. dos Materiais, 456 - Rio de Janeiro/RJ',
                    'telefone': '(21) 9876-5432'
                },
                {
                    'nome': 'Mega Construção',
                    'email': 'atendimento@megaconstrucao.com',
                    'fantasia': 'Mega Construção',
                    'razao': 'Mega Construção Materiais Ltda',
                    'cnpj': '11.222.333/0001-44',
                    'endereco': 'Rua do Comércio, 789 - Belo Horizonte/MG',
                    'telefone': '(31) 1111-2222'
                }
            ]
            
            for loja_data in lojas_exemplo:
                usuario_loja = Usuario(
                    nome=loja_data['nome'],
                    email=loja_data['email'],
                    senha_hash='hash_senha',
                    tipo_usuario='Loja'
                )
                db.usuarios.insert_one(usuario_loja.to_dict())
                
                loja = Loja(
                    usuario_id=usuario_loja.id,
                    nome_fantasia=loja_data['fantasia'],
                    razao_social=loja_data['razao'],
                    cnpj=loja_data['cnpj'],
                    endereco=loja_data['endereco'],
                    telefone=loja_data['telefone']
                )
                db.lojas.insert_one(loja.to_dict())
            
            materiais_basicos = [
                {'nome': 'Cimento Portland CP II-E-32', 'unidade': 'kg', 'categoria': 'Cimento'},
                {'nome': 'Tijolo Cerâmico 6 furos', 'unidade': 'un', 'categoria': 'Alvenaria'},
                {'nome': 'Areia Média Lavada', 'unidade': 'm³', 'categoria': 'Agregado'},
                {'nome': 'Brita 1 (9,5 a 19mm)', 'unidade': 'm³', 'categoria': 'Agregado'},
                {'nome': 'Ferro CA-50 10mm', 'unidade': 'kg', 'categoria': 'Estrutura'},
                {'nome': 'Ferro CA-50 12mm', 'unidade': 'kg', 'categoria': 'Estrutura'},
                {'nome': 'Tinta Acrílica Branca', 'unidade': 'l', 'categoria': 'Tinta'},
                {'nome': 'Fio Elétrico 2,5mm²', 'unidade': 'm', 'categoria': 'Elétrico'},
                {'nome': 'Tubo PVC 100mm', 'unidade': 'm', 'categoria': 'Hidráulico'},
                {'nome': 'Cerâmica 45x45cm', 'unidade': 'm²', 'categoria': 'Revestimento'}
            ]
            
            for mat in materiais_basicos:
                material = Material(
                    nome=mat['nome'],
                    unidade_medida=mat['unidade'],
                    categoria=mat['categoria']
                )
                db.materiais.insert_one(material.to_dict())
            
            print("Dados de exemplo criados com sucesso!")
        else:
            print("Dados de exemplo já existem. Pulando inserção.")
            
    except Exception as e:
        print(f"Erro na inicialização do MongoDB ou inserção de dados de exemplo: {e}")



@app.route("/api/status", methods=["GET"])
def status():
    """Endpoint para verificar se a API está funcionando"""
    return {
        'status': 'ConstroiVerse API está funcionando!',
        'version': '2.0.0',
        'endpoints': [
            '/api/projetos',
            '/api/orcamentos',
            '/api/ia',
            '/api/users',
            '/api/financeiro',
            '/api/vitrine'
        ]
    }

@app.route("/api/profissoes", methods=["GET"])
def get_profissoes():
    """Endpoint para obter lista de profissões da construção civil"""
    from src.services.vitrine_service import VitrineService
    service = VitrineService()
    return jsonify(service.get_profissoes_por_categoria()), 200

@app.route("/api/especialidades/<profissao>", methods=["GET"])
def get_especialidades(profissao):
    """Endpoint para obter especialidades de uma profissão"""
    from src.services.vitrine_service import VitrineService
    service = VitrineService()
    especialidades = service.get_especialidades_profissao(profissao)
    return jsonify({'especialidades': especialidades}), 200

@app.route("/api/faixa-preco/<profissao>", methods=["GET"])
def get_faixa_preco(profissao):
    """Endpoint para obter faixa de preço de uma profissão"""
    from src.services.vitrine_service import VitrineService
    service = VitrineService()
    faixa = service.get_faixa_preco_profissao(profissao)
    return jsonify(faixa), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
