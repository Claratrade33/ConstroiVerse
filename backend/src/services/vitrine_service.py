# backend/src/services/vitrine_service.py

class VitrineService:
    """
    Serviço simulado para a vitrine de profissionais.
    Em uma implementação real, este serviço faria a lógica de negócios
    para buscar dados de profissões, especialidades e faixas de preço.
    """
    
    def get_profissoes_por_categoria(self):
        """Retorna uma lista simulada de profissões."""
        return {
            "Construção Civil": [
                {"nome": "Pedreiro", "descricao": "Especialista em alvenaria e estruturas."},
                {"nome": "Eletricista", "descricao": "Instalação e manutenção elétrica."},
                {"nome": "Encanador", "descricao": "Instalação e reparo de sistemas hidráulicos."},
                {"nome": "Arquiteto", "descricao": "Projeto e planejamento de obras."},
                {"nome": "Engenheiro Civil", "descricao": "Gestão e execução de projetos de engenharia."}
            ],
            "Acabamento": [
                {"nome": "Pintor", "descricao": "Aplicação de tintas e revestimentos."},
                {"nome": "Gesseiro", "descricao": "Instalação de forros e divisórias de gesso."},
                {"nome": "Azulejista", "descricao": "Assentamento de pisos e revestimentos cerâmicos."}
            ]
        }

    def get_especialidades_profissao(self, profissao):
        """Retorna especialidades simuladas para uma profissão."""
        especialidades = {
            "Pedreiro": ["Alvenaria Estrutural", "Reboco", "Contrapiso"],
            "Eletricista": ["Baixa Tensão", "Instalações Residenciais", "Padrão de Entrada"],
            "Arquiteto": ["Design de Interiores", "Paisagismo", "Projetos 3D"]
        }
        return especialidades.get(profissao, ["Especialidade Padrão"])

    def get_faixa_preco_profissao(self, profissao):
        """Retorna faixa de preço simulada para uma profissão."""
        faixas = {
            "Pedreiro": {"min": 150.00, "max": 300.00, "unidade": "Diária"},
            "Eletricista": {"min": 200.00, "max": 400.00, "unidade": "Diária"},
            "Arquiteto": {"min": 50.00, "max": 150.00, "unidade": "m²"}
        }
        return faixas.get(profissao, {"min": 100.00, "max": 250.00, "unidade": "Diária"})
