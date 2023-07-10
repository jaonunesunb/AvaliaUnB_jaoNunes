from flask import Blueprint, jsonify, request
from src.middlewares.index import authenticate_token, check_admin
from src.services.reports.index import get_all_denuncias, get_denuncia_by_id, delete_denuncia, update_denuncia

denuncias_bp = Blueprint("denuncias_bp", __name__, url_prefix="/denuncias")


@denuncias_bp.route("", methods=["GET"])
@check_admin
def get_all():
    denuncias = get_all_denuncias()
    return jsonify(denuncias)


@denuncias_bp.route("/<denuncia_id>", methods=["GET"])
@check_admin
def get_by_id(denuncia_id):
    denuncia = get_denuncia_by_id(denuncia_id)
    if denuncia:
        return jsonify(denuncia)
    else:
        return jsonify({"message": "Denúncia não encontrada"}), 404


@denuncias_bp.route("/<denuncia_id>", methods=["DELETE"])
@check_admin
def delete(denuncia_id):
    delete_denuncia(denuncia_id)
    return jsonify({"message": "Denúncia excluída com sucesso"})


@denuncias_bp.route("/<denuncia_id>", methods=["PUT"])
@check_admin
def update(denuncia_id):
    data = request.get_json()
    if "validada" in data:
        validada = data["validada"]
        update_denuncia(denuncia_id, validada)
        return jsonify({"message": "Denúncia atualizada com sucesso"})
    else:
        return jsonify({"message": "Dados inválidos"}), 400
