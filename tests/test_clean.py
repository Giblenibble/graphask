from graphask.ingest.clean import clean_text


def test_rejoins_hyphenated_words():
    assert clean_text("incredi-\nble potential") == "incredible potential"


def test_normalizes_ligatures():
    assert clean_text("find a fit") == "find a fit"


def test_joins_broken_words():
    assert clean_text("one line\nsecond line") == "one line second line"
