from flask import Blueprint, jsonify, request, session, render_template
from src.services.avaluations.index import get_avaliacoes_by_ID
from src.services.students.index import get_user_by_id
from src.middlewares.index import check_admin, is_authenticated
from src.services.reports.index import create_denuncia, get_all_denuncias, get_denuncia_by_id, delete_denuncia, update_denuncia

reports_bp = Blueprint("reports_bp", __name__, url_prefix="/denuncias")

@reports_bp.route("", methods=["POST"])
@is_authenticated
def create_report():
    data = request.get_json(force=True)
    id_estudante = data.get("id_estudante")
    id_avaliacao = data.get("id_avaliacao")
    motivo = data.get("motivo")
    avaliada = data.get("avaliada", False)

    if id_estudante and id_avaliacao and motivo:
        report = create_denuncia(id_estudante, id_avaliacao, motivo, avaliada)
        return jsonify(report), 201
    else:
        return jsonify({"message": "Dados inválidos"}), 400


@reports_bp.route("/<int:report_id>", methods=["DELETE"])
@check_admin(True)
def delete_report(report_id):
    delete_denuncia(report_id)
    return jsonify({"message": "Relatório excluído com sucesso"})

@reports_bp.route("/<int:report_id>", methods=["PUT"])
@check_admin(True)
def update_report(report_id):
    data = request.get_json()
    id_estudante = data.get("id_estudante")
    id_avaliacao = data.get("id_avaliacao")
    motivo = data.get("motivo")
    avaliada = data.get("avaliada")

    if id_estudante or id_avaliacao or motivo or avaliada:
        update_denuncia(report_id, id_estudante=id_estudante, id_avaliacao=id_avaliacao, motivo=motivo, avaliada=avaliada)
        return jsonify({"message": "Relatório atualizado com sucesso"})
    else:
        return jsonify({"message": "Dados inválidos"}), 400

@reports_bp.route("", methods=["GET"])
@check_admin(True)
def get_all_reports():
    denuncias = get_all_denuncias()
    return denuncias

@reports_bp.route("/<int:report_id>", methods=["GET"])
@check_admin(True)
def get_report_by_id(report_id):
    report = get_denuncia_by_id(report_id)
    if report:
        return jsonify(report)
    else:
        return jsonify({"message": "Relatório não encontrado"}), 404

@reports_bp.route('/admin')
@check_admin(True)
def vdenuncias():
    user = get_user_by_id(session['user_id'])
    denuncias = get_all_denuncias()
    avaliacoes = []

    for denuncia in denuncias:
        avaliacao = get_avaliacoes_by_ID(denuncia['id_avaliacao'])
        avaliacoes.append(avaliacao)
        print(avaliacoes)
    return render_template('denuncias.html', user=user, avaliacoes=avaliacoes, denuncias=denuncias)
