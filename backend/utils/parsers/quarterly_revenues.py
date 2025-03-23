import os
import pandas as pd
import yaml
from tier_data.models import QuarterlyRevenue

# BASE_DIR = os.path.dirname(__file__)
BASE_DIR = "utils/parsers"

with open(os.path.join(BASE_DIR, 'datalinks.yml')) as file:
    config = yaml.safe_load(file)


class QuarterlyRevenuesUtil:
    def __init__(self) -> None:
        self.name = 'LOCAL_GOVERNMENT_FINANCES'
        self.subname = 'QUARTERLY_REVENUES'
        self.uncleaned_csv = []
        self.clean_csv = []
        self.column_list = [
            'E-code', 'ONS Code', 'Local authority', 'Region', 'Class',
            'Public order and Safety Total ', 'Economic Affairs Total ',
            'Housing and Community Amenities Total ', 'Health Total ',
            'Education Total', 'Social Protection Total ',
            'Net Current Expenditure (including Education Non-Pay Element)',
            'Total Service Expenditure (including Education Non-Pay Element)',
            'Housing Revenue Account Income Total',
            'Housing Revenue Account Expenditure Total',
            'sheet_name'
        ]

    def set_unclean_csv(self, filepath):
        self.uncleaned_csv.append(filepath)

    def set_clean_csv(self, filepath):
        self.clean_csv.append(filepath)


def data_request(quarter_revenue_helper: QuarterlyRevenuesUtil):
    data_link = (config[quarter_revenue_helper.name]
                 [quarter_revenue_helper.subname])

    get_sheet_name = pd.read_excel(data_link,
                                   engine='odf',
                                   sheet_name=None,
                                   nrows=1).keys()
    # Quarterly Revenue Update (QRU) returns, Q3 2023-24
    wanted_sheet_name = [
        sheetname for sheetname in list(get_sheet_name)
        if (sheetname.startswith('QRU_LA_Data_Q'))]

    pd_list = []
    for s_name in wanted_sheet_name:
        quarterly_revenue_df = pd.read_excel(
            data_link, engine='odf', skiprows=6,
            sheet_name=s_name
        )

        quarterly_revenue_df['sheet_name'] = s_name
        columns = quarter_revenue_helper.column_list
        quarterly_revenue_df = quarterly_revenue_df[columns]
        quarterly_revenue_df = quarterly_revenue_df[
            quarterly_revenue_df[columns[0]].notnull()
        ]
        pd_list.append(quarterly_revenue_df)

    final_df = pd.concat(pd_list, ignore_index=True)
    final_df.columns = quarter_revenue_helper.column_list

    file_name = str(data_link).split('/')[-1].split('.')[0]

    final_df.to_csv(os.path.join(BASE_DIR, f"{file_name}.csv"))

    quarter_revenue_helper.set_unclean_csv(
        os.path.join(BASE_DIR, f"{file_name}.csv")
    )

    return quarter_revenue_helper


def parse_row(row, data_list):
    def update_invalid(val):
        try:
            val = float(val)
            return val
        except Exception as err:
            print(err)
            return 0.0

    quarterly_revenue = QuarterlyRevenue(
        e_code=row['E-code'],
        ons_code=row['ONS Code'],
        local_authority=row['Local authority'],
        region=row['Region'],
        class_of_authority=row['Class'],
        public_order_and_safety_total=update_invalid(
            row['Public order and Safety Total ']

        ),
        economic_affairs_total=update_invalid(row['Economic Affairs Total ']),
        housing_and_community_amenities_total=update_invalid(row[
            'Housing and Community Amenities Total '
        ]),
        health_total=update_invalid(row['Health Total ']),
        education_total=update_invalid(row['Education Total']),
        social_protection_total=update_invalid(row[
            'Social Protection Total '
        ]),
        net_current_expenditure_including_education_non_pay_element=update_invalid(row[
            'Net Current Expenditure (including Education Non-Pay Element)'
        ]),
        total_service_expenditure_including_education_non_pay_element=update_invalid(row[
            'Total Service Expenditure (including Education Non-Pay Element)'
        ]),
        housing_revenue_account_income_total=update_invalid(row[
            'Housing Revenue Account Income Total'
        ]),
        housing_revenue_account_expenditure_total=update_invalid(row[
            'Housing Revenue Account Expenditure Total'
        ]),
        sheet_name=row['sheet_name'],
    )
    data_list.append(quarterly_revenue)


def clean_files(quarter_revenue_helper: QuarterlyRevenuesUtil):
    unclean_CSVs = quarter_revenue_helper.uncleaned_csv

    for unclean_csv in unclean_CSVs:
        unclean_df_chunk = pd.read_csv(unclean_csv, chunksize=5000)

        chunk_index = 1
        for chunk in unclean_df_chunk:
            quarterly_revenue_df = pd.concat([chunk], ignore_index=True)

            data_list = []  # Reset for new chunk
            quarterly_revenue_df.apply(
                lambda row: parse_row(row, data_list),  # type: ignore
                axis=1
            )

            QuarterlyRevenue.objects.bulk_create(data_list)
            print(f' Created DF chunk {chunk_index}')
            chunk_index += 1


quarter_revenue_helper = QuarterlyRevenuesUtil()
used_quarter_revenue_helper = data_request(quarter_revenue_helper)
clean_files(used_quarter_revenue_helper)
