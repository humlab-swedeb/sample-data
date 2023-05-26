"""Demonstrates how to compute and display trends data."""

import pandas as pd
from penelope.common.keyness import KeynessMetric
from penelope.corpus import VectorizedCorpus
from penelope.utility import PropertyValueMaskingOpts

from src.parlaclarin import codecs as md
from src.parlaclarin.trends_data import SweDebComputeOpts, SweDebTrendsData


def test_something():
    """Load corpus and metadata (codecs) and compute trends data."""

    folder: str = "./data/dataset-01/v0.6.0/dtm/lemma"
    tag: str = "lemma"

    corpus: VectorizedCorpus = VectorizedCorpus.load(folder=folder, tag=tag)

    metadata_filename: str = "../data/dataset-01/v0.6.0//riksprot_metadata.db"

    # Load codecs metadata
    codecs: md.PersonCodecs = md.PersonCodecs().load(source=metadata_filename)

    # Speakers metadata with encoded ids:
    persons: pd.DataFrame = codecs.persons_of_interest.head().copy()

    # Person metadata with decoded ids:
    print(codecs.decode(persons))

    # Person metadata with encoded and decoded ids:
    print(codecs.decode(persons, drop=False))

    # Specification of metadata properties (and actual data) avaliable for display, grouping and filtering
    # print(codecs.property_values_specs)

    # Create trends data object
    trends_data: SweDebTrendsData = SweDebTrendsData(
        corpus=corpus, person_codecs=codecs, n_top=100000
    )

    opts: SweDebComputeOpts = SweDebComputeOpts(
        fill_gaps=False,
        keyness=KeynessMetric.TF,
        normalize=False,
        pivot_keys_id_names=["party_id"],
        filter_opts=PropertyValueMaskingOpts(gender_id=2),
        smooth=False,
        temporal_key="year",
        top_count=100,
        unstack_tabular=False,
        words=["sverige", "jag"],
    )

    # Compute trends data
    trends_data.transform(opts)

    # Find indices of picked words stored in opts
    picked_indices = trends_data.find_word_indices(opts)

    # Extract a data frame with the picked words
    trends: pd.DataFrame = trends_data.extract(indices=picked_indices)

    # Display the trends data frame
    print(trends.head())

    # Decode any encoded ids in the trends data frame
    print(trends_data.person_codecs.decode(trends).head())

    # Find indices of picked words from corpus
    trends_data.transformed_corpus.find_matching_words_indices(
        word_or_regexp=["sverige", "jag"],
        n_max_count=100,
        descending=False,
    )
