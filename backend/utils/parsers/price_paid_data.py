import os
import yaml
import pandas as pd
from tier_data.models import PricePaid


BASE_DIR = ("utils/parsers" if os.getenv('IN_DOCKER')
            else os.path.dirname(__file__))


with open(os.path.join(BASE_DIR, 'datalinks.yml'), 'r') as file:
    config = yaml.safe_load(file)


class PaidPriceUtil:
    def __init__(self) -> None:
        self.name = 'PRICE_PAID'
        self.uncleaned_csv = []
        self.clean_csv = []

        self.column_list = [

            'transaction_unique_identifier', 'price',
            'date_of_transfer', 'postcode', 'property_type',
            'age', 'tenure', 'paon', 'saon', 'street', 'locality',
            'town_or_city', 'district', 'county', 'price_paid_category',
            'monthly_record_status'
        ]
        self.column_list_monthly = [
            'transaction_unique_identifier', 'price',
            'date_of_transfer', 'postcode', 'property_type',
            'age', 'tenure', 'paon', 'saon', 'street', 'locality',
            'town_or_city', 'district', 'county', 'price_paid_category',
            'monthly_record_status'
        ]
        self.column_to_drop = [

            'transaction_unique_identifier',
            'age', 'tenure', 'paon', 'saon', 'street',
            'monthly_record_status'
        ]
        self.property_type_dict = {
            'D': 'Detached', 'S': 'Semi-Detached',
            'T': 'Terraced', 'F': 'Flats/Maisonettes',
            'O': 'Other'
        }
        self.age_dict = {
            'Y': 'newly built property',
            'N': 'established residential building'
        }
        self.tenure_dict = {
            'F': 'Freehold',
            'L': 'Leasehold'
        }
        self.price_paid_category_dict = {
            'A': 'Standard Price Paid entry',
            'B': 'Additional Price Paid entry'
        }
        self.monthly_record_status_dict = {
            'A': 'Addition',
            'C': 'Change',
            'D': 'Delete'
        }

    def set_unclean_csv(self, filepath):
        self.uncleaned_csv.append(filepath)

    def set_clean_csv(self, filepath):
        self.clean_csv.append(filepath)


def data_request(pp_helper: PaidPriceUtil) -> PaidPriceUtil:

    data_links = config[pp_helper.name]
    for data_link in data_links:
        paid_price_df = pd.read_csv(data_link)
        paid_price_df.columns = pp_helper.column_list

        paid_price_df.drop(pp_helper.column_to_drop,
                           axis=1,
                           inplace=True)

        file_name = str(data_link).split('/')[-1]

        paid_price_df.to_csv(os.path.join(BASE_DIR, file_name))

        pp_helper.set_unclean_csv(os.path.join(BASE_DIR, file_name))

    return pp_helper


def parse_row(row, data_list):
    paid_price = PricePaid(
                price=row['price'],
                date_of_transfer=pd.to_datetime(row["date_of_transfer"],
                                                errors="coerce"),
                postcode=row['postcode'],
                locality=row['locality'],
                town_or_city=row['town_or_city'],
                district=row['district'],
                county=row['county'],
                category=row['price_paid_category'],
            )
    data_list.append(paid_price)


def clean_files(pp_helper: PaidPriceUtil):
    unclean_CSVs = pp_helper.uncleaned_csv

    for unclean_csv in unclean_CSVs:
        unclean_df_chunk = pd.read_csv(unclean_csv,  chunksize=5000)

        chunk_index = 1
        for chunk in unclean_df_chunk:
            price_paid_df = pd.concat([chunk], ignore_index=True)

            data_list = []  # Reset for new chunk

            price_paid_df.apply(
                lambda row: parse_row(row, data_list),  # type: ignore
                axis=1
            )

            PricePaid.objects.bulk_create(data_list)
            print(f' Created DF chunk {chunk_index}')
            chunk_index += 1


paidprice_helper = PaidPriceUtil()
used_paidprice_helper = data_request(paidprice_helper)
data_load = clean_files(used_paidprice_helper)
