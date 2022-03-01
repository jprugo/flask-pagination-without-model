from flask import request, abort
from flask_paginate import Pagination
from utils import get_script_content


def configure_routes(app, db):

    class PersonaModel(db.Model):
        __tablename__ = 'tblPersona'

        idpersona = db.Column(db.Integer, primary_key=True)
        numerotelefono = db.Column(db.String())

        def __init__(self, numerotelefono):
            self.numerotelefono = numerotelefono

        def __repr__(self):
            return f"<Persona {self.name}>"

    @app.route('/persona-raw-paginated', methods=['GET'])
    def handle_personas():

        # Request parameters for query
        args = request.args
        creationDate = args.get('creationDate')

        # Requets parameters for pagination
        page = args.get('page', default=1, type=int)
        pageSize = args.get('pageSize', default=3)

        # get script content
        script = get_script_content('testeo', 'test.sql')

        print('script :', script)

        # Execute query
        records = db.session.execute(
            script,
            {
                'creationDate': creationDate
            }
        )

        # Cursor to convert CursorRow into Dict
        cursor = records.cursor

        results = [
            dict(zip([i[0] for i in cursor.description], row))
            for row in cursor
        ]

        total = len(results)

        if total == 0:
            return '', 204

        offset = ((page - 1) * pageSize)

        pagination = Pagination(
            page=page,
            per_page=pageSize,
            offset=offset,
            total=total,
            record_name='Personas'
        )

        if page > pagination.total_pages:
            return abort(404)

        return {
            'Info': {
                "pagination_next": f'http://localhost:5000/persona-raw-paginated?creationDate=2022-02-28&page={pagination.page+1}' if pagination.has_next else None,
                "pagination_prev": f'http://localhost:5000/persona-raw-paginated?creationDate=2022-02-28&page={pagination.page-1}' if pagination.has_prev else None,
                "pagination_page": pagination.page,
                "pagination_total_pages": pagination.total_pages,
                "pagination_total": pagination.total,
                "offset": offset
            },
            pagination.record_name: results[
                    offset: offset + pagination.per_page
            ]
        }

    @app.route('/persona/<int:id>', methods=['GET'])
    def handle_persona(id):

        persona = PersonaModel.query.get_or_404(id)

        response = {
            "id": persona.idpersona,
            "telefono": persona.numerotelefono,

        }
        return {"message": "success", "persona": response}
