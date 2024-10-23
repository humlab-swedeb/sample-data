import pandas as pd
import pytest


@pytest.mark.skip(reason="Only used for development & debugging")
def test_speech_index():

    di: pd.DataFrame = pd.read_feather('data/1867-2020/v1.1.0/speech-index.feather')

    assert di is not None
    assert len(di) > 0

    si: pd.DataFrame = pd.read_csv('data/1867-2020/v1.1.0/dtm/lemma/lemma_document_index.csv.gz', sep=';', index=0)

    assert si is not None
    assert len(si) > 0
