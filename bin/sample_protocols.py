"""
This script creates a sample of protocol titles from the protocols.csv.gz file.
It samples n titles per year for a given range of years and saves the sampled titles to a text file.

DEPRECATED! Use Bash script ./bin/sample-protocols.sh instead!
"""

# type: ignore

from os.path import dirname

import pandas as pd


def create_sample_n_titles(years: list[int], n_samples_per_year, filename: str) -> None:
    """Create a sample of protocol titles from the protocols.csv.gz file.

    Args:
        years (list[int]): List of years to sample from.
        n_samples_per_year (int): Number of samples per year.
        filename (str): Path to the protocols.csv.gz file.
    """

    di: pd.DataFrame = pd.read_csv(filename, sep="\t")
    di = di[di.year.isin(years)][["document_name", "year"]]

    def sample_n_titles(df: pd.DataFrame, n: int):
        return df.sample(n=n, replace=True) if len(df) < n else df.sample(n=n)

    sample_protocols = (
        di.groupby("year")
        .apply(sample_n_titles, n=n_samples_per_year)
        .reset_index(drop=True)
    )

    (sample_protocols.document_name + ".xml").to_csv(
        f"{dirname(__file__)}/protocols.txt", index=False
    )


def main():
    """Main function to create a sample of protocol titles."""
    years: list[int] = list(range(1970, 1980))
    n_samples_per_year: int = 3
    filename: str = "./metadata/v1.2.2/protocols.csv.gz"

    create_sample_n_titles(years, n_samples_per_year, filename)


if __name__ == "__main__":

    main()
