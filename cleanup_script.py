import pandas as pd

def read_data(file_path):
    df = pd.read_excel(file_path)
    if len(df.columns) == 1:
        df = df[df.columns[0]].str.split(",", expand=True)
        df = df.loc[:, ~df.columns.duplicated()]
        df = df.dropna(axis=1, how="all")
        df = df.iloc[:, :5]
        df.columns = ["name", "email", "signup_date", "plan", "notes"]

    return df

def remove_invalid_records(df):
    quarantine_conditions = (
        df["name"].isna() |
        df["email"].isna() |
        (~df["email"].str.contains("@", na=False)) |
        (df["name"].str.lower().str.contains("test", na=False)) |
        (df["email"].str.lower().str.contains("test", na=False))
    )

    quarantine_df = df[quarantine_conditions].copy()
    clean_df = df[~quarantine_conditions].copy()

    return clean_df, quarantine_df


def format_dates(df, quarantine_df):
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
    invalid_dates = df["signup_date"].isna()
    quarantine_df = pd.concat([quarantine_df, df[invalid_dates]])
    df = df[~invalid_dates]
    df["signup_date"] = df["signup_date"].dt.strftime("%Y-%m-%d")

    return df, quarantine_df


def  handle_duplicate(df):
    df = df.sort_values("signup_date", ascending=False)
    df["is_multi_plan"] = df.duplicated("email", keep=False)
    df = df.drop_duplicates(subset="email", keep="first")
    
    return df


def main():
    file_path = "signup.xls"
    df = read_data(file_path)

    original_count = len(df)
    df, quarantine_df = remove_invalid_records(df)
    df, quarantine_df = format_dates(df, quarantine_df)
    df =  handle_duplicate(df)
    final_count = len(df)
    quarantine_count = len(quarantine_df)

    df.to_csv("members_final.csv", index=False)
    quarantine_df.to_csv("quarantine.csv", index=False)

    print("Cleanup completed successfully.")
    print(f"Total: {original_count} | Clean: {final_count} | Quarantined: {quarantine_count}")


if __name__ == "__main__":
    main()
