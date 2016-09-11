class TestSuiteQuerylayer(object):
    def test_insert_piece(self, querylayer):
        data = {"name": "hello", "filename": "file.xml"}
        querylayer.add_piece(data)
        pieces = querylayer.get_pieces()
        listed = list(pieces)
        assert len(listed) == 1
        assert listed[0]["name"] == data["name"]
