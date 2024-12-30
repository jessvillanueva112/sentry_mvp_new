def test_basic():
    assert True

def test_import():
    try:
        from app import app
        assert True
    except ImportError as e:
        assert False, f"Failed to import app: {str(e)}"

def test_app_config(app):
    assert app.testing
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"