from os.path import dirname

import pandas as pd


def create_sample_n_titles(
    year_range: tuple[int,int] = range(1960, 2021),
    n_samples_per_year: int = 3,
    filename: str = "/data/riksdagen_corpus_data/metadata/v0.10.0/protocols.csv.gz"
) -> None:
    
    di: pd.DataFrame = pd.read_csv(filename, sep='\t')
    di = di[di.year.isin(year_range)][["document_name", "year"]]

    # c: Corpus = load_corpus(".env_1960")

    # di: pd.DataFrame = c.document_index[c.document_index.year.isin(year_range)][["document_name"]]
    # di = di[["document_name"]].assign(
    #     protocol_name=di.document_name.str.split("_").str[0],
    #     year=di.document_name.str.split("-").str[1].str[:4].astype(int),
    # )[["protocol_name", "year"]].drop_duplicates()

    def sample_n_titles(df: pd.DataFrame, n: int):
        return df.sample(n=n, replace=True) if len(df) < n else df.sample(n=n)

    sample_protocols = di.groupby('year').apply(sample_n_titles, n=n_samples_per_year).reset_index(drop=True)

    (sample_protocols.document_name + '.xml').to_csv(f"{dirname(__file__)}/protocols.txt", index=False)

if __name__ == "__main__":

    year_range: tuple[int,int] = range(1970, 1980)
    n_samples_per_year: int = 1
    filename: str = "/data/riksdagen_corpus_data/metadata/v0.10.0/protocols.csv.gz"

    create_sample_n_titles(year_range, n_samples_per_year, filename)
