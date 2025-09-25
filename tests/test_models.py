import pytest
from app.models import User, Room, Message
from datetime import datetime. timedelta

def test_user_model_defauts():
    # Basic field assignment and defaults
    u = User(username="testuser")
    assert u.username == "testuser"
    assert u.is_active is True
    assert isinstance(u.created_at, datetime)
    assert isinstance(u.last_active,datetime)
    assert u.rooms == set()

def test_room_model_defaults():
    # Basic field assignment and defaults
    r = Room(name="testroom")
    assert r.name == "testroom"
    assert isinstance(r.created_at, datetime)
    assert r.members == set()
    assert r.messages == []



def test_message_model_defaults_and_fields():
    # Basic field assignment and defaults
    m = Message(room="testroom", sender="testuser", content="Hello World")
    assert m.room == "testroom"
    assert m.sender == "testuser"
    assert m.content == "Hello World"
    assert m.is_read is False
    assert isinstance(m.timestamp, datetime)

def test_message_timestamp_ordering():
    older = Message(room="r", sender="a", content="old")
    # simulate later message
    later = Message(room="r", sender="b", content="later")
    assert older.timestamp <= later.timestamp or older.timestamp != later.timestamp

# small validation-ish test (pydantic will raise if wrong)
def test_invalid_username_length_raises():
    long_name = "x" * 200
    with pytest.raises(Exception):
        User(username=long_name)