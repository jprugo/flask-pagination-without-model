# flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# python
import pytest
import json
import boto3
from json import loads

# mock aws
from moto import mock_s3, mock_secretsmanager

#
from handlers.routes import configure_routes
from utils import get_connection_data

# const
@pytest.fixture
def get_secret_name():
    return 'secreto'


@pytest.fixture
def get_bucket_name():
    return 'testeo'


@pytest.fixture
def get_file_path():
    return 'test.sql'


@pytest.fixture
def mock_app(
        mock_scm_resource  # mock the secrets manage
    ):
    app = Flask(__name__)

    client = app.test_client()

    conn_data = loads(get_connection_data("secreto"))

    app.config['SQLALCHEMY_DATABASE_URI'] =\
        "postgresql://{user}:{password}@{host}:{port}/{database}"\
        .format(*conn_data, **conn_data)

    db = SQLAlchemy(app)

    configure_routes(app, db)

    return app, client



# Mock boto clients
@pytest.fixture
def mock_s3_client():
    with mock_s3():
        yield boto3.client('s3')


@pytest.fixture
def mock_scm_client():
    with mock_secretsmanager():
        yield boto3.client('secretsmanager', region_name='us-east-1')


# Mock AWS Resources
@pytest.fixture
def mock_s3_resource(mock_s3_client, get_bucket_name, get_file_path):
    mock_s3_client.create_bucket(
        Bucket=get_bucket_name
    )

    mock_s3_client.put_object(
        Bucket=get_bucket_name,
        Key=get_file_path,
        Body=""" SELECT * FROM "tblPersona" WHERE to_char("fechacreacion", 'YYYY-MM-DD')= :creationDate ORDER BY "fechacreacion" desc;"""
    )


@pytest.fixture
def mock_scm_resource(mock_scm_client, get_secret_name):
    mock_scm_client.create_secret(
        Name=get_secret_name,
        SecretString=json.dumps({
            'database': "postgres",
            'user': "postgres",
            'password': "runscripts",
            'host': 'localhost',
            'port': "5432"
        }
        )
    )

