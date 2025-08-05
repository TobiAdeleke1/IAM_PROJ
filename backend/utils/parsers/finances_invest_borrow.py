import os
import pandas as pd
import yaml
from tier_data.models import FinanceBorrowing, FinanceInvestment

# BASE_DIR = os.path.dirname(__file__)
BASE_DIR = "utils/parsers"

with open(os.path.join(BASE_DIR, 'datalinks.yml')) as file:
    config = yaml.safe_load(file)


class FinancesUtil:
    def __init__(self) -> None:
        self.name = 'LOCAL_GOVERNMENT_FINANCES'
        self.subname = 'INVESTMENT_BORROWING'
        self.sheetnames = [{'LA_Investments': []}, {'LA_Borrowing': []}]
        self.sheet_columns = {
            'LA_Investments': [
                'num', 
                'lgf_code', 'local_authority_name', 'deposits:_banks',
                'deposits:_building_societies', 'treasury_bills',
                'certificates_of_deposit:_banks',
                'certificates_of_deposit:_building_societies',
                'british_government_(gilt-edge)_securities',
                'other_financial_intermediaries', 'public_corporations',
                'debt_management_account_deposit_facility_[note_2]',
                'money_market_funds', 'externally_managed_funds',
                'other_investments', 'loans_local_government', 'country',
                'class_of_authority', 'ons_code', 'notes', 'sheet_name'
                ],

            'LA_Borrowing': [
                'num', 
                'lgf_code', 'local_authority_name',
                'loans_short_term_banks_in_uk',
                'loans_short_term_building_societies',
                'loans_short_term_other_financial_intermediaries',
                'loans_short_term_public_corporations',
                'loans_short_term_private_nonfinancial_corporations',
                'loans_short_term_central_government',
                'loans_short_term_households_sector',
                'loans_short_term_other_sources',
                'securities_negotiable_bonds_&_commercial_paper',
                'securities_other_stock_issues',
                'loans_longerterm_pwlb[note_2]_[note_5]',
                'loans_longerterm_banks_in_uk',
                'loans_longerterm_building_societies',
                'loans_longerterm_other_financial_intermediaries',
                'loans_longerterm_public_corporations',
                'loans_longerterm_private_nonfinancial_corporations',
                'loans_longerterm_central_government',
                'loans_longerterm_households_sector',
                'loans_longerterm_other_sources',
                'short_term_loans_local_authorities',
                'longer_term_loans_local_authorities',
                'country',
                'class_of_authority',
                'ons_code', 'notes', 'sheet_name'

                ]
            }
        self.uncleaned_csv = []
        self.clean_csv = []

    def set_unclean_csv(self, filepath):
        self.uncleaned_csv.append(filepath)

    def set_clean_csv(self, filepath):
        self.clean_csv.append(filepath)


def data_request(gov_finance_helper: FinancesUtil):
    data_link = config[gov_finance_helper.name][gov_finance_helper.subname]

    get_sheet_name = pd.read_excel(data_link,
                                   engine='odf',
                                   sheet_name=None,
                                   nrows=1).keys()

    def excel_request(newfile_name, file_sheet_list, column_list):
        pd_list = []
        for s_name in file_sheet_list:
            gov_finance_df = pd.read_excel(
                data_link, engine='odf', skiprows=7, sheet_name=s_name,
                header=None
            )
            print("Loading sheet ...", s_name)
            # Remove variable column
            if 'Notes' not in gov_finance_df.columns:
                gov_finance_df['Notes'] = ''

            gov_finance_df['sheet_name'] = s_name
            pd_list.append(gov_finance_df)

        final_df = pd.concat(pd_list, ignore_index=True)
        final_df.columns = column_list

        final_df.to_csv(
            os.path.join(BASE_DIR, f"{newfile_name}.csv")
        )

        gov_finance_helper.set_unclean_csv(
           [newfile_name, os.path.join(BASE_DIR, f"{newfile_name}.csv")]
        )

    for invest_or_borrow in gov_finance_helper.sheetnames:
        invest_or_borrow_key = list(invest_or_borrow.keys())[0]

        invest_or_borrow[invest_or_borrow_key] = [
            sheetname for sheetname in list(get_sheet_name)
            if sheetname.startswith(invest_or_borrow_key)
            and '_Q' in sheetname and 'Table' not in sheetname
        ]

        excel_request(
            invest_or_borrow_key,
            invest_or_borrow[invest_or_borrow_key],
            gov_finance_helper.sheet_columns[invest_or_borrow_key]
        )

        try:
            excel_request(
                invest_or_borrow_key,
                invest_or_borrow[invest_or_borrow_key],
                gov_finance_helper.sheet_columns[invest_or_borrow_key]
            )
        except Exception as err:
            print(err)

    return gov_finance_helper

def update_invalid(val):
    try:
        val = float(val)
        return val
    except Exception as err:
        
        print(err)
        return 0.0


def parse_row_invest(row, data_list):
    finance_investment = FinanceInvestment(
        local_government_finance_code=row['lgf_code'],
        local_authority_name=row['local_authority_name'],
        bank_deposits_thousands=update_invalid(row['deposits:_banks']),
        building_societies_deposits_thousands=update_invalid(row[
            'deposits:_building_societies'
        ]),
        treasury_bills_thousands=update_invalid(row['treasury_bills']),
        banks_cert_of_deposit_thousands=update_invalid(row['certificates_of_deposit:_banks']),
        building_societies_cert_of_deposit_thousands=update_invalid(row[
            'certificates_of_deposit:_building_societies'
        ]),
        british_government_securities_thousands=update_invalid(row[
            'british_government_(gilt-edge)_securities'
        ]),
        other_financial_intermediaries_thousands=update_invalid(row[
            'other_financial_intermediaries'
        ]),
        public_corporations_thousands=update_invalid(row['public_corporations']),
        debt_management_account_deposit_facility_thousands=update_invalid(row[
            'debt_management_account_deposit_facility_[note_2]'
        ]),
        money_market_funds_thousands=update_invalid(row['money_market_funds']),
        externally_managed_funds_thousands=update_invalid(row['externally_managed_funds']),
        other_investments_thousands=update_invalid(row['other_investments']),
        loans_local_government_thousands=update_invalid(row['loans_local_government']),
        country=row['country'],
        class_of_authority=row['class_of_authority'],
        ons_code=row['ons_code'],
        sheet_name=row['sheet_name'],
    )

    data_list.append(finance_investment)


def parse_row_borrow(row, data_list):
    finance_borrowing = FinanceBorrowing(
        local_government_finance_code=row['lgf_code'],
        local_authority_name=row['local_authority_name'],
        loans_short_term_banks_in_uk_thousands=update_invalid(row[
            'loans_short_term_banks_in_uk'
        ]),
        loans_short_term_building_societies_thousands=update_invalid(row[
            'loans_short_term_building_societies'
        ]),
        loans_short_term_other_financial_intermediaries_thousands=update_invalid(row[
            'loans_short_term_other_financial_intermediaries'
        ]),
        loans_short_term_public_corporations_thousands=update_invalid(row[
            'loans_short_term_public_corporations'
        ]),
        loans_short_term_private_nonfinancial_corporations_thousands=update_invalid(row[
            'loans_short_term_private_nonfinancial_corporations'
        ]),
        loans_short_term_central_government_thousands=update_invalid(row[
            'loans_short_term_central_government'
        ]),
        loans_short_term_households_sector_thousands=update_invalid(row[
            'loans_short_term_households_sector'
        ]),
        loans_short_term_other_sources_thousands=update_invalid(row[
            'loans_short_term_other_sources'
        ]),
        securities_negotiable_bonds_commercial_thousands=update_invalid(row[
            'securities_negotiable_bonds_&_commercial_paper'
        ]),
        securities_other_stock_issues_thousands=update_invalid(row[
            'securities_other_stock_issues'
        ]),
        loans_longerterm_pwlb_thousands=update_invalid(row[
            'loans_longerterm_pwlb[note_2]_[note_5]'
        ]),
        loans_longerterm_banks_in_uk_thousands=update_invalid(row[
            'loans_longerterm_banks_in_uk'
        ]),
        loans_longerterm_building_societies_thousands=update_invalid(row[
            'loans_longerterm_building_societies'
        ]),
        loans_longerterm_other_financial_intermediaries_thousands=update_invalid(row[
            'loans_longerterm_other_financial_intermediaries'
        ]),
        loans_longerterm_public_corporations_thousands=update_invalid(row[
            'loans_longerterm_public_corporations'
        ]),
        loans_longerterm_private_nonfinancial_corporations_thousands=update_invalid(row[
            'loans_longerterm_private_nonfinancial_corporations'
        ]),
        loans_longerterm_central_government_thousands=update_invalid(row[
            'loans_longerterm_central_government'
        ]),
        loans_longerterm_households_sector_thousands=update_invalid(row[
            'loans_longerterm_households_sector'
        ]),
        loans_longerterm_other_sources_thousands=update_invalid(row[
            'loans_longerterm_other_sources'
        ]),
        short_term_loans_local_authorities_thousands=update_invalid(row[
            'short_term_loans_local_authorities'
        ]),
        longer_term_loans_local_authorities_thousands=update_invalid(row[
            'longer_term_loans_local_authorities'
        ]),
        country=row['country'],
        class_of_authority=row['class_of_authority'],
        ons_code=row['ons_code'],
        sheet_name=row['sheet_name'],
    )

    data_list.append(finance_borrowing)


def clean_files(gov_finance_helper: FinancesUtil):
    unclean_CSVs = gov_finance_helper.uncleaned_csv
    
    LA_Investments_csv = [csvFile for type, csvFile in unclean_CSVs if type == 'LA_Investments']
    for unclean_csv in LA_Investments_csv:
        unclean_df_chunk = pd.read_csv(unclean_csv, chunksize=5000)

        chunk_index = 1
        for chunk in unclean_df_chunk:
            finance_df = pd.concat([chunk], ignore_index=True)

            data_list = []  # Reset for new chunk
            # taking advantage of mutable objects
            finance_df.apply(
                lambda row: parse_row_invest(row, data_list),  # type: ignore
                axis=1
            )

            FinanceInvestment.objects.bulk_create(data_list)
            print(f' Created DF chunk {chunk_index}')
            chunk_index += 1


    LA_Borrowing_csv = [csvFile for type, csvFile in unclean_CSVs if type == 'LA_Borrowing']
    for unclean_csv in LA_Borrowing_csv:
        unclean_df_chunk = pd.read_csv(unclean_csv,  chunksize=5000)

        chunk_index = 1
        for chunk in unclean_df_chunk:
            finance_df = pd.concat([chunk], ignore_index=True)

            data_list = []  # Reset for new chunk
            # taking advantage of mutable objects
            finance_df.apply(
                lambda row: parse_row_borrow(row, data_list),  # type: ignore
                axis=1
            )

            FinanceBorrowing.objects.bulk_create(data_list)
            print(f' Created DF chunk {chunk_index}')
            chunk_index += 1


gov_finance_helper = FinancesUtil()
used_gov_finance_helper = data_request(gov_finance_helper)
clean_files(used_gov_finance_helper)
