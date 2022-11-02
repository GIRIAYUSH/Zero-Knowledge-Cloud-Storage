from pkg.auth.service import Service
from pkg.auth.schema import AddUserSchema, SignInSchema
from db.db import get_database
import bson
import pytest 
from dotenv import load_dotenv

@pytest.fixture
def setup():
    load_dotenv()


def test_registeruser():
    u = AddUserSchema(name="Krishap",email="test@test.com",salt="rand",encrypted_master_password="encrypted",derived_key="derived")
    svc = Service(get_database())
    id = svc.RegisterUser(u)
    assert type(id) == bson.objectid.ObjectId

def test_signin():
    u = SignInSchema(email="test@test.com",derived_key="derived")
    svc = Service(get_database())
    user = svc.SignIn(u)
    assert user.encrypted_master_password == "encrypted"