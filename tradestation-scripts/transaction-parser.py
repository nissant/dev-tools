import os
import sys
import platform
import typer
import pandas

app = typer.Typer()


@app.command()
def join(input_dir_path: str = typer.Option(None, prompt=False),
         output_file_type: str = typer.Option("json", prompt=True)):
    files: list[str] = get_data_files(input_dir_path)
    transactions_df: pandas.DataFrame = get_data_from_files(files)
    clean_transaction_data(transactions_df)
    write_transaction_file_wrapper(transactions_df, input_dir_path, output_file_type)


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

        files = [os.path.join(input_dir_path, f) for f in os.listdir(input_dir_path) if os.path.isfile(os.path.join(input_dir_path, f))]

    if not len(files) > 0:
        raise typer.BadParameter(f"no files found to join, check input folder or streamed input paths")
    return files


def clean_transaction_data(df):
    df['Amt'] = pandas.to_numeric(df['Amt'].str.replace(r'([^0-9.])', "", regex=True))


def get_data_from_files(files: list[str]) -> pandas.DataFrame:
    df = pandas.DataFrame()
    for file in files:
        file_name, file_extension = os.path.splitext(file)
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
    df.reset_index(drop=True, inplace=True)
    return df


def write_transaction_file_wrapper(df: pandas.DataFrame, dir_path: str, output_file_type: str):
    if dir_path is None:
        dir_path = os.getcwd()
    out_folder_path = os.path.join(dir_path, 'output')

    if not os.path.exists(out_folder_path):
        os.mkdir(out_folder_path)
    out_file_path = os.path.join(out_folder_path, f"joined_transactions.{output_file_type}")
    write_transactions_file(df, out_file_path)


def write_transactions_file(df: pandas.DataFrame, out_file_path: str):
    output_file_type = os.path.splitext(out_file_path)[1]
    if os.path.exists(out_file_path):
        os.remove(out_file_path)
    if output_file_type == ".json":
        df.to_json(out_file_path, orient="records")
    elif output_file_type == ".xlsx":
        df.to_excel(out_file_path, orient="records")
    elif output_file_type == ".csv":
        df.to_csv(out_file_path)
    print(out_file_path)


@app.command()
def label(input_file_path: str = typer.Option(..., prompt=True)):
    # TODO - Implement a generic declarative rule engine read from input file
    def get_label(desc: str):
        transfer_desc = ['CASH RECEIVED ACH', 'CRYPTO', 'CASH DISBURSED ACH']
        interest_desc = ['FPL']
        expense_desc = ['FOR SEC WITHHOLD', 'ADR']
        if any(sub in desc for sub in transfer_desc):
            return 'transfer'
        elif any(sub in desc for sub in interest_desc):
            return 'interest'
        elif any(sub in desc for sub in expense_desc):
            return 'expense'
        else:
            return 'dividend'

    df = get_data_from_files([input_file_path])
    df['Type'] = df.apply(lambda x: get_label(x.Description), axis=1)
    write_transactions_file(df, input_file_path)


if __name__ == "__main__":
    app()
