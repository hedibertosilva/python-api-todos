from app.helpers.json import JSON


def test_json_load():
    """ Testing JSON helper. """
    data =  JSON.read_file("tests/data/json_sample.json")
    assert data == dict(test=1)

def test_json_load_bad_format():
    """ Testing JSON helper. """
    data =  JSON.read_file("tests/data/json_bad_format_sample.json")
    assert data == "File is not in JSON format."
