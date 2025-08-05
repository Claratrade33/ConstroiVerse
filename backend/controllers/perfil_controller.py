"""Blueprint para rotas relacionadas aos painéis dos perfis de usuário."""

from flask import Blueprint

from backend.database import db


perfil_bp = Blueprint("perfil", __name__, url_prefix="/perfil")


@perfil_bp.get("/<email>")
def obter_painel(email: str):
    """Retorna a rota do painel correspondente ao perfil principal do usuário."""
    usuario = db.users.find_one({"email": email})
    if not usuario:
        return {"erro": "Usuário não encontrado"}, 404

    rotas = {
        "arquiteto": "/painel_arquiteto",
        "engenheiro": "/painel_engenheiro",
        "loja": "/painel_loja",
        "fabricante": "/painel_fabricante",
        "representante": "/painel_representante",
        "corretor": "/painel_corretor",
        "mestre": "/painel_mestre",
        "pedreiro": "/painel_pedreiro",
        "eletricista": "/painel_eletricista",
        "encanador": "/painel_encanador",
        "cliente": "/painel_cliente",
        "construtora": "/painel_construtora",
    }

    rota_painel = rotas.get(usuario.get("main_profile"))
    if not rota_painel:
        return {"erro": "Perfil não reconhecido"}, 400

    return {"painel": rota_painel}