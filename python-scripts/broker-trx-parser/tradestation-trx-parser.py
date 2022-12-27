import os
import sys
import platform
import typer
import pandas
from datetime import datetime

JOINED_DIR = 'joined'

app = typer.Typer()


@app.command()
def join(input_dir_path: str = typer.Option(None, prompt=False),
         output_dir_path: str = typer.Option(None, prompt=False),
         output_file_type: str = typer.Option("json", prompt=False),
         label_trx: bool = typer.Option(False, prompt=False)):
    files: list[str] = get_data_files(input_dir_path)
    transactions_df: pandas.DataFrame = get_data_from_files(files)
    clean_transaction_data(transactions_df)
    if label_trx:
        label_transactions(transactions_df)
    write_transaction_file_join_wrapper(transactions_df, input_dir_path, output_dir_path, output_file_type)


@app.command()
def label(input_file_path: str = typer.Option(..., prompt=False)):
    df = get_data_from_files([input_file_path])
    label_transactions(df)
    write_transactions_file(df, input_file_path)


def label_transactions(df: pandas.DataFrame):
    # TODO - Implement a generic declarative rule engine read from input file
    def get_label(desc: str):
        transfer_desc = ['CASH RECEIVED ACH', 'CRYPTO', 'CASH DISBURSED ACH']
        interest_desc = ['FPL']
        tax_desc = ['FOR SEC WITHHOLD']
        adr_desc = ['ADR']
        if any(sub in desc for sub in transfer_desc):
            return 'transfer'
        elif any(sub in desc for sub in interest_desc):
            return 'income - interest'
        elif any(sub in desc for sub in tax_desc):
            return 'expense - tax'
        elif any(sub in desc for sub in adr_desc):
            return 'expense - tax'
        else:
            return 'income - dividend'

    df['Type'] = df.apply(lambda x: get_label(x.Description), axis=1)


def get_data_files(input_dir_path) -> list[str]:
    files = []
    if input_dir_path is None:
        if "linux" in platform.system().lower():
            for line in sys.stdin:
                if os.path.exists(line):
                    files.append(line)
                else:
                    print(f"path not found: {line} skipping ...")
    else:
        if not os.path.exists(input_dir_path):
            raise typer.BadParameter("directory path not found")

        files = [os.path.join(input_dir_path, f) for f in os.listdir(input_dir_path)
                 if os.path.isfile(os.path.join(input_dir_path, f))]

    if not len(files) > 0:
        raise typer.BadParameter(f"no files found to join, check input folder or streamed input paths")
    return files


def clean_transaction_data(df: pandas.DataFrame):
    if df['Amt'].dtypes == object:
        df['Amt'] = pandas.to_numeric(df['Amt'].str.replace(r'([^0-9.])', "", regex=True))
    if df['Entry Date'].dtypes == object:
        df['Entry Date'] = pandas.to_datetime(df['Entry Date'])
    df.sort_values(by='Entry Date', inplace=True)


def get_data_from_files(files: list[str]) -> pandas.DataFrame:
    df = pandas.DataFrame()
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        try:
            if file_extension == ".json":
                df = pandas.concat([df, pandas.read_json(file)])
            elif file_extension == ".xlsx":
                df = pandas.concat([df, pandas.read_excel(file, engine='openpyxl')])
            elif file_extension == ".xls":
                df = pandas.concat([df, pandas.read_html(file)[0]])
            elif file_extension == ".csv":
                df = pandas.concat([df, pandas.read_csv(file)[0]])
            else:
                print(f"file type: {file_extension} not supported, skipping file: {file}")
        except ValueError:
            print(f"no transactions found in file: {file}, skipping ...")
    df.reset_index(drop=True, inplace=True)
    return df


def get_joined_file_name(df: pandas.DataFrame) -> str:
    start_trx_date = df['Entry Date'].iloc[0]
    end_trx_date = df['Entry Date'].iloc[-1]
    return f"{start_trx_date.month}_{start_trx_date.year}-{end_trx_date.month}_{end_trx_date.year}_transactions"


def write_transaction_file_join_wrapper(df: pandas.DataFrame, input_dir_path: str, output_dir_path: str,
                                        output_file_type: str):
    if output_dir_path:
        out_path = output_dir_path
    elif input_dir_path:
        out_path = os.path.join(input_dir_path, JOINED_DIR)
    else:
        out_path = os.path.join(os.getcwd(), JOINED_DIR)

    if not os.path.exists(out_path):
        os.mkdir(out_path)
        
    joined_file_name = get_joined_file_name(df)
    out_file_path = os.path.join(out_path, f"{joined_file_name}.{output_file_type}")
    write_transactions_file(df, out_file_path)


def write_transactions_file(df: pandas.DataFrame, out_file_path: str):
    output_file_type = os.path.splitext(out_file_path)[1]
    if os.path.exists(out_file_path):
        os.remove(out_file_path)
    if output_file_type == ".json":
        df.to_json(out_file_path, orient="records", date_format='iso')
    elif output_file_type == ".xlsx":
        df.to_excel(out_file_path, orient="records", date_format='iso')
    elif output_file_type == ".csv":
        df.to_csv(out_file_path, date_format='iso')
    print(out_file_path)


if __name__ == "__main__":
    app()
