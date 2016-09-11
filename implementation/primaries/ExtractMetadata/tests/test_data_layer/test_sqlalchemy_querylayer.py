class TestSuiteQuerylayer(object):
    def test_insert_piece(self, qlayer):
        data = [{"name": "hello", "filename": "file.xml"}]
        self.result_against_dict(data, qlayer, table="pieces")

    def test_insert_instrument(self, qlayer):
        data = [{"name": "clarinet", "diatonic": 0, "chromatic": -1}]
        self.result_against_dict(data, qlayer, table="instruments")

    def test_insert_tempo(self, qlayer):
        data = [{"beat": "quaver", "minute": 100}]
        self.result_against_dict(data, qlayer, table="tempos")

    def test_insert_time(self, qlayer):
        data = [{"beat": 4, "beat_type": 4}]
        self.result_against_dict(data, qlayer, table="time_signatures")

    def test_insert_clef(self, qlayer):
        data = [{"name": "treble", "line": 2, "sign": "G"}]
        self.result_against_dict(data, qlayer, table="clefs")

    def test_insert_key(self, qlayer):
        data = [{"name": "C major", "fifths": 0, "mode": "major"}]
        self.result_against_dict(data, qlayer, table="keys")

    def test_update_piece(self, qlayer):
        data = [{"name": "hello", "archived": False}]
        self.result_against_dict(data, qlayer)
        update_set = data
        update_set[0]["archived"] = True
        results = list(qlayer.get())
        qlayer.update(results[0][0], update_set[0])
        data = qlayer.get()
        val = list(data)
        assert val[0]["archived"] == True

    def result_against_dict(self, data, qlayer, table="pieces"):
        for entry in data:
            qlayer.add(entry, table=table)
            results = qlayer.get(table=table)
            listed_res = list(results)
            assert len(listed_res) == len(data)

            for result in listed_res:
                for key in entry:
                    assert key in result
                    assert result[key] == entry[key]

