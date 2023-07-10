from flask import Blueprint, jsonify, request
from src.services.reports.index import get_all_denuncias, get_denuncia_by_id, delete_denuncia, update_denuncia

denuncias_bp = Blueprint("denuncias_bp", __name__, url_prefix="/denuncias")


@denuncias_bp.route("", methods=["GET"])
def get_all():
    denuncias = get_all_denuncias()
    return jsonify(denuncias)


@denuncias_bp.route("/<denuncia_id>", methods=["GET"])
def get_by_id(denuncia_id):
    denuncia = get_denuncia_by_id(denuncia_id)
    if denuncia:
        return jsonify(denuncia)
    else:
        return jsonify({"message": "Denúncia não encontrada"}), 404


@denuncias_bp.route("/<denuncia_id>", methods=["DELETE"])
def delete(denuncia_id):
    delete_denuncia(denuncia_id)
    return jsonify({"message": "Denúncia excluída com sucesso"})


@denuncias_bp.route("/<denuncia_id>", methods=["PUT"])
def update(denuncia_id):
    data = request.get_json()
    if "validada" in data:
        validada = data["validada"]
        update_denuncia(denuncia_id, validada)
        return jsonify({"message": "Denúncia atualizada com sucesso"})
    else:
        return jsonify({"message": "Dados inválidos"}), 400
