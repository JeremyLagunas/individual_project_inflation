from lib2to3.pgen2.pgen import DFAState
import pandas as pd
import numpy as np
from datetime import timedelta, datetime

### Acquire
def acquire_inflation():
# CPI less food and energy
    cpi_less_food_energy = pd.read_csv('cpi_lessfoodenergy_fred.csv')
# CPI rate of change
    cpi_rate = pd.read_csv('cpi_rate_total_monthly_percent.csv')
# monetary base
    monetary_base = pd.read_csv('FRB_H3_monthly.csv')
# M2 money supply
    m2 = pd.read_csv('m2_nonseasonal_monthly_billions.csv')
# personal savings rate
    personal_savings_rate = pd.read_csv('personal_savings_rate_monthly_seasonal_percent.csv')
# unemployment rate
    unemployment_rate = pd.read_csv('unemployment_nonseasonal_monthly.csv')
# workforce participation rate
    workforce_participation_rate = pd.read_csv('workforce_participation_rate_nonseasonal_monthly.csv')
    return cpi_less_food_energy, cpi_rate, monetary_base, m2, personal_savings_rate, unemployment_rate, workforce_participation_rate



### Prepare
def prep_inflation(cpi_less_food_energy, cpi_rate, monetary_base, m2, personal_savings_rate, unemployment_rate, workforce_participation_rate):
# This function will rename columns to make them more clear and easier to work with as well as change the DATE columns from objects to datetimes.
# CPI less food and energy
    cpi_less_food_energy.rename(columns={'CPILFENS':'cpi_less_food_energy'}, inplace=True)
    cpi_less_food_energy.DATE = pd.to_datetime(cpi_less_food_energy.DATE)
# CPI rate of change
    cpi_rate.rename(columns={'CPALTT01USM659N':'cpi_rate'}, inplace=True)
    cpi_rate.DATE = pd.to_datetime(cpi_rate.DATE)
# Monetary Base
    monetary_base.rename(columns={(monetary_base.columns)[-1]:'circulation',
    (monetary_base.columns)[-2]: 'monetary_base_total_balances_maintained',
    (monetary_base.columns)[-3]: 'monetary_base_total',
    (monetary_base.columns)[-4]: 'DATE'}, inplace=True)
# Drops the first five rows of monetary_base which did not contain actual relevant data.
    monetary_base.drop([0,1,2,3,4], inplace=True)
# Adds a '01' to the end of DATE, representing the day of the month that monetary_base was originally missing. 
    monetary_base.DATE = monetary_base.DATE+'-01'
    monetary_base.DATE = pd.to_datetime(monetary_base.DATE)
# M2 money supply
    m2.rename(columns = {'M2NS':'m2'}, inplace=True)
    m2.DATE = pd.to_datetime(m2.DATE)
# personal savings
    personal_savings_rate.rename(columns = {'PSAVERT':'personal_savings_rate'}, inplace=True)
    personal_savings_rate.DATE = pd.to_datetime(personal_savings_rate.DATE)
# unemployment rate
    unemployment_rate.rename(columns = {'UNRATENSA':'unemployment_rate'}, inplace=True)
    unemployment_rate.DATE = pd.to_datetime(unemployment_rate.DATE)
# workforce participation rate
    workforce_participation_rate.rename(columns = {'LNU01300000':'workforce_participation_rate'}, inplace=True)
    workforce_participation_rate.DATE = pd.to_datetime(workforce_participation_rate.DATE)
    return


### Make one dataframe
def make_df(cpi_less_food_energy, cpi_rate, monetary_base, m2, personal_savings_rate, unemployment_rate, workforce_participation_rate):
# Merges all data into one df
    df = workforce_participation_rate.merge(unemployment_rate, on='DATE')
    df = df.merge(personal_savings_rate, on='DATE')
    df = df.merge(m2, on='DATE')
    df = df.merge(cpi_rate, on='DATE')
    df = df.merge(cpi_less_food_energy, on='DATE')
    df = df.merge(monetary_base, on='DATE')
# renames the total money in circulation column from the monetary base data set. The renaming would not work the way I tried first. 
    df.rename(columns={list(df.columns)[-1]:'circulation'}, inplace=True)
# Changes the data type for circulation, monetary base total, and monetary base total balances maintained from objects to integers.
    df['circulation'] = df['circulation'].astype(int)
    df['monetary_base_total'] = df['monetary_base_total'].astype(int)
    df['monetary_base_total_balances_maintained'] = df['monetary_base_total_balances_maintained'].astype(int)
# Sets the index of the df to the DATE column
    df = df.set_index('DATE').sort_index()
    return df








