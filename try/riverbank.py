#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, os

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

def trx_time():
    return int(time.time())

def change(AmountFrom, CurrencyFrom, CurrencyTo):
    if CurrencyFrom == CurrencyTo:
        AmountTo = AmountFrom
    else:
        Rate = Rates[(CurrencyFrom, CurrencyTo)]
        AmountTo = AmountFrom * Rate
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

    return trx_time()

def main(PrgArgs=[]):
    # Files, Something = files_abspath_collect_from_dir(".")
    # for File in Files:
    #     print(File, Something)
    # return Files


    print("PRGARGS", PrgArgs)
    Logs = []
    # direct test, simple calc fun
    # Change = change(2, "GBP", "USD")
    # return Change

    # Salary from Ltd to Bob and Jim:
    transfer(AccLtd, AccBob, 26.5, "USD")
    transfer(AccLtd, AccJim, 23.2, "EUR")

    # dinner party, Jim pay Bob+Jim costs
    transfer(AccJim, AccRestaurant, 1, "EUR")

    # dinner party, Bob pay his bill to Jim
    transfer(AccBob, AccJim, 0.4, "GBP")


    return files_abspath_collect_from_dir(".")

def files_abspath_collect_from_dir(DirRoot, Recursive=False):
    FilesAbsPath = []
    for DirPath, DirNames, FileNames in os.walk(DirRoot):
        for Elem in ([os.path.join(DirPath, File) for File in FileNames]):
            FilesAbsPath.append(Elem)

        # https://stackoverflow.com/questions/4117588/non-recursive-os-walk
        if not Recursive:
            break
    return FilesAbsPath


if __name__ == "__main__":
    main()
