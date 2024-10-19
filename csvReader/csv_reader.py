import requests
from bs4 import BeautifulSoup as bs
import datetime
import polars as pl
import pandas as pd
import re

class CSVReader():
    def read_csv_data(self, filename: str) -> pl.DataFrame:
        # read the column names from the file
        with open(filename, 'r') as file:
            for _ in range(5):
                file.readline()
            column_names = file.readline().strip().split(';')

        # read the data into a polars dataframe
        df = pl.read_csv(filename, skip_rows=5, separator=';', skip_rows_after_header=2, encoding="ISO-8859-1", ignore_errors=True) #errors cause no actual issues

        return df


    def replace_unicode_chars(self, df: pl.DataFrame, col_name: str) -> pl.Series:
        # Get the column to be iterated
        col = df[col_name]
        regex = re.compile(r"\\u(\d+)\?")
        # Iterate through each row in the column
        for i, val in enumerate(col):
            # Check if the value contains a unicode character
            match = regex.search(val)
            if match:
                # Extract the unicode character code from the string
                hex_code = val.split("\\u")[1].split("?")[0]
                # Convert the hex code to an integer and then to its corresponding unicode character
                char = chr(int(hex_code))

                # Replace the original value with the new value containing the unicode character
                col[i] = val.replace(match.group(), char)

        return col


    def strip_strings(self, x: str) -> str:
        if isinstance(x, str):
            return x.strip()
        else:
            return x


    def rtf_data_processing(self, df: pl.DataFrame) -> pl.DataFrame:
        df = df.with_columns([
            pl.when(pl.col('Year(s) Weapon of Order').str.contains(r'\(.*\)'))
            .then(pl.lit("Yes"))
            .otherwise(pl.lit("No"))
            .alias("is estimated year order")
        ])

        df = df.with_columns([
            pl.col('Year(s) Weapon of Order').str.replace_all(r"[()]", "").alias('Year(s) Weapon of Order').cast(pl.Int64)
        ])

        return df


    def joined_table(self, df_rtf, csv_df):
        processed_dF = self.rtf_data_processing(df_rtf)
        # remove possible spaces for the designations
        csv_df = csv_df.with_columns(csv_df['Designation'].str.strip_chars())

        processed_dF = processed_dF.with_columns(self.replace_unicode_chars(df_rtf, "No. Designation"))
        processed_dF = processed_dF.with_columns(self.replace_unicode_chars(df_rtf, "No. Comments"))

        joined_dF = csv_df.join(processed_dF,
                            left_on=['Seller', 'Buyer',
                                        'Designation', 'Order date',
                                        ],
                            right_on=["Supplier", "Recipient",
                                        "No. Designation", 'Year(s) Weapon of Order',
                                        ],
                            how="left")
        joined_dF = joined_dF.select(
            ['Deal ID', 'Seller', 'Buyer', 'Designation', 'Description', 'Armament category', 'Order date',
            'Order date is estimate', 'Numbers delivered', 'Numbers delivered is estimate', 'Delivery year',
            'Delivery year is estimate', 'Status', 'SIPRI estimate', 'TIV deal unit', 'TIV delivery values',
            'Local production', 'No. Comments'])

        return joined_dF


def main():
    reader = CSVReader()
    print(reader.read_csv_data("DealsAndTIVs-2023-03-11-16_22_41 (1).txt").columns
          )

if __name__ == '__main__':
    main()