import os
from datetime import datetime

from flask import Flask, request, send_file
from flask_restful import Api, Resource
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs import DB_CONNECTION, UPLOAD_PATH, ALLOWED_EXTENSIONS

app = Flask(__name__)
api = Api(app)
Base = declarative_base()
engine = create_engine(DB_CONNECTION)
Session = sessionmaker(bind=engine)


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    filename = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)
    extension = Column(String)

    def __repr__(self):
        return f"<File {self.filename}>"


Base.metadata.create_all(engine)


class FileResource(Resource):
    def get(self, id):
        session = Session()
        file_record = session.query(File).filter_by(id=id).first()

        if file_record is None:
            session.close()
            return {"error": "File not found"}, 404

        path = f"{UPLOAD_PATH}/{file_record.filename}"
        session.close()

        return send_file(path, as_attachment=True)

    def delete(self, id):
        session = Session()
        file_record = session.query(File).filter_by(id=id).first()

        if file_record is None:
            session.close()
            return {"error": "File not found"}, 404

        file_path = os.path.join(file_record.path, file_record.filename)
        os.remove(file_path)

        session.delete(file_record)
        session.commit()
        session.close()

        return {}, 200


class FileListResource(Resource):
    def post(self):
        file = request.files["file"]
        extension = os.path.splitext(file.filename)[1][1:]

        if extension not in ALLOWED_EXTENSIONS:
            return {"error": "Invalid file extension"}, 400

        filename = f"{datetime.now().isoformat()}.{extension}".replace(" ", "")

        if not os.path.exists(UPLOAD_PATH):
            os.makedirs(UPLOAD_PATH)

        file.save(os.path.join(UPLOAD_PATH, filename))
        file_record = File(path=UPLOAD_PATH, filename=filename, extension=extension)
        session = Session()
        session.add(file_record)
        session.commit()

        response = {"filename": f"{filename}", "id": file_record.id}
        session.close()

        return response, 200

    def get(self):
        session = Session()
        file_records = session.query(File).all()
        session.close()

        files = [
            {
                "id": file_record.id,
                "filename": file_record.filename,
                "path": file_record.path,
                "extension": file_record.extension,
                "upload_time": file_record.upload_time.isoformat(),
            }
            for file_record in file_records
        ]

        return files, 200


class FileMetaDataResource(Resource):
    def get(self, id):
        session = Session()
        file_record = session.query(File).filter_by(id=id).first()

        if file_record is None:
            session.close()
            return {"error": "File not found"}, 404

        metadata = {
            "id": file_record.id,
            "filename": file_record.filename,
            "path": file_record.path,
            "extension": file_record.extension,
            "upload_time": file_record.upload_time.isoformat(),
        }
        session.close()

        return metadata, 200


api.add_resource(FileListResource, "/file")
api.add_resource(FileResource, "/file/<int:id>")
api.add_resource(FileMetaDataResource, "/file/<int:id>/metadata")


if __name__ == "__main__":
    app.run(debug=False)
