from src.models.member import Member

def test_member_creation():
    m = Member("John", "001", "john@email.com")
    assert m.get_name() == "John"