import MetaTrader5 as mt5

from config import (
    ACCOUNT_RISK_PERCENT,
    SYMBOL
)


def get_account():
    """
    Return MT5 account information.
    """

    return mt5.account_info()


def get_balance():
    """
    Return current account balance.
    """

    account = get_account()

    if account is None:
        return 0.0

    return account.balance


def get_risk_amount():
    """
    Dollar amount to risk.
    """

    balance = get_balance()

    return balance * (ACCOUNT_RISK_PERCENT / 100)


def get_symbol_info():

    return mt5.symbol_info(SYMBOL)


def get_volume_limits():

    info = get_symbol_info()

    return {
        "min": info.volume_min,
        "max": info.volume_max,
        "step": info.volume_step
    }


def print_risk_report():

    balance = get_balance()

    risk = get_risk_amount()

    volume = get_volume_limits()

    print("\n" + "=" * 45)
    print("RISK REPORT")
    print("=" * 45)

    print(f"Balance        : ${balance:.2f}")
    print(f"Risk %         : {ACCOUNT_RISK_PERCENT}%")
    print(f"Risk Amount    : ${risk:.2f}")
    print(f"Minimum Lot    : {volume['min']}")
    print(f"Maximum Lot    : {volume['max']}")
    print(f"Lot Step       : {volume['step']}")

    print("=" * 45)