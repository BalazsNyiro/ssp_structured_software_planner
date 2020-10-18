#!/usr/bin/env python3
# -*- coding: utf-8 -*-


AccBob        = {"owner": "Bob", "Balance": 124, "Currency": "EUR"}
AccJim        = {"owner": "Jim", "Balance": 163, "Currency": "USD"}
AccLtd        = {"owner": "Ltd", "Balance": 12345678, "Currency": "GBP"}
AccRestaurant = {"owner": "Restaurant", "Balance": 12345678, "Currency": "GBP"}

Rates = {("EUR", "GBP") : 0.6,
         ("EUR", "USD") : 1.2,
         ("GBP", "EUR") : 1.5,
         ("GBP", "USD") : 1.5,
         ("USD", "EUR") : 0.7,
         ("USD", "GBP") : 0.6 }

def change(AmountFrom, CurrencyFrom, CurrencyTo):
    if CurrencyFrom == CurrencyTo:
        return AmountFrom
    AmountTo = AmountFrom * Rates[(CurrencyFrom, CurrencyTo)]
    print(f"  {AmountFrom} {CurrencyFrom} -> {AmountTo:.2f} {CurrencyTo}")
    return AmountTo

def acc_info(Acc):
    print(Acc["owner"], Acc["Balance"], Acc["Currency"])

def transfer(From, To, Amount, CurrencyOfTransaction):

    acc_info(From)
    print(f" -> {Amount} {CurrencyOfTransaction}")
    acc_info(To)

    AmountFrom = change(Amount, CurrencyOfTransaction, From["Currency"])
    AmountTo = change(Amount, CurrencyOfTransaction, To["Currency"])

    To["Balance"] += AmountTo
    From["Balance"] -= AmountFrom

    acc_info(From)
    acc_info(To)
    print()
    return "transfer"

def main(PrgArgs=[]):
    print("PRGARGS", PrgArgs)

    # Salary from Ltd to Bob and Jim:
    transfer(AccLtd, AccBob, 26.5, "USD")
    transfer(AccLtd, AccJim, 23.2, "EUR")

    # dinner party, Jim pay Bob+Jim costs
    transfer(AccJim, AccRestaurant, 1, "EUR")

    # dinner party, Bob pay his bill to Jim
    TransferReply = transfer(AccBob, AccJim, 0.4, "GBP")

    return "End"

if __name__ == "__main__":
    main()
