import os
import pandas as pd
import yaml
from tier_data.models import PlanningApplications

# BASE_DIR = ("utils/parsers" if os.getenv('IN_DOCKER')
#             else os.path.dirname(__file__))
BASE_DIR = "utils/parsers"

with open(os.path.join(BASE_DIR, 'datalinks.yml')) as file:
    config = yaml.safe_load(file)


class PlanningApplicationStatsUtil:
    def __init__(self) -> None:
        self.name = 'PLANNING_APPLICATION_STATISTICS'
        self.uncleaned_csv = []
        self.clean_csv = []
        self.column_list = ['Region', 'LPANM', 'LPACD', 'Quarter', 'F_Year',
                            'Total decisions; grand total (all)',
                            'Total granted; grand total (all)',
                            'Total refused; grand total (all)']

    def set_unclean_csv(self, filepath):
        self.uncleaned_csv.append(filepath)

    def set_clean_csv(self, filepath):
        self.clean_csv.append(filepath)


def data_request(os_openname_helper: PlanningApplicationStatsUtil):
    data_links = config[os_openname_helper.name]

    for data_link in data_links:
        planning_application_df = pd.read_csv(data_link,
                                              encoding='latin1',
                                              skiprows=2,
                                              )

        file_name = str(data_link).split('/')[-1]

        planning_application_df_req = planning_application_df[
            os_openname_helper.column_list
        ]

        planning_application_df_req.columns = (
            planning_application_df_req.columns
            .str.lower()
            .str.strip()
            .str.replace(';', '')
            .str.replace('(', '')
            .str.replace(')', '')
            .str.replace(' ', '_')
        )

        planning_application_df_req.to_csv(
            os.path.join(BASE_DIR, file_name)
        )

        os_openname_helper.set_unclean_csv(os.path.join(BASE_DIR, file_name))

    return os_openname_helper


def parse_row(row, data_list):

    planning_applicatin = PlanningApplications(
        region=row['region'],
        local_planning_authority_name=row['lpanm'],
        local_planning_authority_code=row['lpacd'],
        quarter=row['quarter'],
        fiscal_year=row['f_year'],
        total_decisions_grand_total_all=row['total_decisions_grand_total_all'],
        total_granted_grand_total_all=row['total_granted_grand_total_all'],
        total_refused_grand_total_all=row['total_refused_grand_total_all'],
    )
    data_list.append(planning_applicatin)


def clean_files(os_openname_helper: PlanningApplicationStatsUtil):

    unclean_CSVs = os_openname_helper.uncleaned_csv

    for unclean_csv in unclean_CSVs:
        unclean_df_chunk = pd.read_csv(unclean_csv, chunksize=5)

        chunk_index = 1
        for chunk in unclean_df_chunk:
            planning_application_df = pd.concat([chunk], ignore_index=True)

            data_list = []  # Reset for new chunk
            planning_application_df.apply(
                lambda row: parse_row(row, data_list),  # type: ignore
                axis=1
            )

            PlanningApplications.objects.bulk_create(data_list)
            print(f' Created DF chunk {chunk_index}')
            chunk_index += 1


os_openname_helper = PlanningApplicationStatsUtil()
used_os_openname_helper = data_request(os_openname_helper)
data_load = clean_files(used_os_openname_helper)
