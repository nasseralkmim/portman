"""extract dividends from trades

"""
import pandas as pd


def get_cia_details(portfolio, cad_cia_file, cia_cnpj_file):
    """get company details

    TODO: get this data from an official repository

    Args:
        portfolio: DataFrame with portfolio data
        cad_cia_file: string file with company data, specificaly the CVM code
        cia_cnpj_file: string file with company cnpj data

    Returns:
        DataFrame with cnpj and CVM code columns
    """
    cia_data_cvm = pd.read_csv(cad_cia_file, sep=";", engine="python", encoding='unicode_escape')
    cia_cnpj = pd.read_csv(cia_cnpj_file, sep=",")

    pf_detail = portfolio.copy()
    pf_detail["cnpj"] = pf_detail.apply(
        lambda x: cia_cnpj.CNPJ[cia_cnpj["Código"].str.contains(x.name)].values[0],
        axis=1,
    )
    pf_detail["cd_cvm"] = pf_detail.apply(
        lambda x: cia_data_cvm.CD_CVM[
            (cia_data_cvm["CNPJ_CIA"].str.contains(x.cnpj))
            & (cia_data_cvm["SIT"] == "ATIVO")
        ].values[0],
        axis=1,
    )
    return pf_detail


def get_dividends_data(ticker, cd_cvm):
    """get dividend data from bmf

    Args:
        ticker (str): company ticker
        cd_cvm (int): CVM code number

    Returns:
        DataFrame with dividend data from BMF&BOVESPA site

    """
    site = f"http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoProventosDinheiro.aspx?codigoCvm={cd_cvm}&tab=3.1&idioma=pt-br"

    dividends_data = pd.read_html(
        site, decimal=",", thousands=".", parse_dates={"date_com": ["Últ. Dia 'Com'"]}
    )[0]
    return dividends_data


def volume_at_dividend(dividends, trades, ticker):
    """Compute stock volume at dividend date

    In order to gain dividends you should hold the stock before the
    'date_com' date.

    """
    if dividends.shape[0] > 0:  # if there is dividends approved
        # filter by date and ticker, then sum
        dividends["vol_liq"] = dividends.apply(
            lambda row: trades.vol_adj[
                (trades.date <= row.date_com)  # in order to gain the dividends
                & (trades.ticker == ticker)
            ].sum(),
            axis=1,
        )
    else:
        dividends["vol_liq"] = 0
    return dividends


def extract_dividends(ticker, trades, cd_cvm, last_date):
    """extract dividends for each ticker

    1. filter out old dividend data
    2. filter ON or PN ticker
    3. add ticker as index
    4. compute volume at dividend approvation date
    5. rename columns
    6. remove unwanted columns
    7. compute total dividend

    Optimization:
        1. remove all dates already registred in the dividends file

    Args:
        ticker (str): company ticker
        trades (DataFrame): trade data
        cd_cvm (str): CVM code
        last_dividend (datetime.date): date of last dividend registred

    Returns:
        DataFrame with total dividends received for each dividend approved
    """
    dividends = get_dividends_data(ticker, cd_cvm)
    # remove old unecessary data
    dividends = dividends[
        dividends.date_com >= trades.date[trades.ticker == ticker].min()
    ]

    # only dividens not yet on the record (dividends.csv)
    dividends = dividends[dividends.date_com > last_date]

    # filter by ON and PN
    if "3" in ticker:
        dividends = dividends[dividends["Tipo de Ativo"] == "ON"]
    elif "4" in ticker:
        dividends = dividends[dividends["Tipo de Ativo"] == "PN"]

    # add ticker as index (multiindex)
    # so we can later append all dividends from multiple companies
    dividends = dividends.set_index(
        pd.Index([ticker] * dividends.shape[0]).set_names(["ticker"]), append=True
    )

    dividends = volume_at_dividend(dividends, trades, ticker)

    # rename columns
    dividends = dividends.rename(
        columns={"Valor do Provento (R$)": "value", "Tipo do Provento (II)": "type"}
    )
    dividends = dividends[["date_com", "value", "type", "vol_liq"]]

    # compute total dividend on the approved date
    dividends["total"] = dividends.value * dividends.vol_liq

    # corrects for taxes (15%)
    dividends["total"] = dividends.apply(lambda row:
                                         row.total * 0.85
                                         if row['type'] == 'JRS CAP PROPRIO'
                                         else row.total, axis=1)

    return dividends


def process_dividends(portfolio, trades):
    """process dividends for all portfolio holdings

    Optimization:
    1. check if dividends.csv file exists
    2. get last date for each ticker

    Args:
        portfolio (DataFrame): created with portfolio.process_portfolio
        trades (DataFrame): created with trades.process_trades()
    Returns:
        DataFrame with dividends data for each company and each day
        pividend were approved
    """
    portfolio_details = get_cia_details(portfolio, "cad_cia_aberta.csv", "cia_cnpj.csv")

    try:
        dividends = pd.read_csv("dividends.csv", index_col=[0, "ticker"])
        # last date registred on file so we update only newer events
        # drop level because tickers are unique
        # tail gets the last date
        last_date_port = (
            dividends.sort_values("date_com").groupby("ticker").tail(1).droplevel(None)['date_com']
        )


        # loop over each unique stock in the portfolio
        for [ticker, cd_cvm] in zip(portfolio_details.index, portfolio_details.cd_cvm):
            # if stock in portfolio has not paid any dividends yet
            # it will not be in last_date
            if ticker in last_date_port.index:
                last_date = last_date_port[ticker]
            else:
                last_date = pd.Timestamp(0)
            dividends = dividends.append(
                extract_dividends(ticker, trades, cd_cvm, last_date)
            )

    except FileNotFoundError:   # if file does not exist
        dividends = pd.DataFrame()
        last_date = pd.Timestamp(0)

        # loop over each unique stock in the portfolio
        for [ticker, cd_cvm] in zip(portfolio_details.index, portfolio_details.cd_cvm):
            dividends = dividends.append(
                extract_dividends(ticker, trades, cd_cvm, last_date)
            )

    dividends.to_csv("dividends.csv")

    return dividends
