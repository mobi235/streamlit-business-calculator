"""Main app file"""
# import plotly.graph_objects as go

import numpy as np
import pandas as pd
import streamlit as st

from layout import coalesce, get_assumptions, set_image, waterfall_fig, css

# plotly==5.11.0
# import matplotlib.pyplot as plt
from sidebar import payment_info, sidebar_financial, billie_pricing  # , set_image

# import subprocess

# subprocess.run([f"{sys.executable}", "streamlit_app.py"])

# sys.path.append("/Users/moe/Documents/streamlit/")
# import requests, os

# from copy import deepcopy
# import base64

# color_map = {"col1": "#FFDAB9", "col2": "#FFA07A", "col3": "#FF7F50"}

# -- Set page config
apptitle = "GW Quickview"  # 6600f5

# st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

# with open("style.css") as css:
#     st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

set_image()

granularity = st.selectbox(
    "Choose impact granularity:",
    (
        "Gross Profit Mode",
        "Revenue Mode",
    ),
)

st.sidebar.markdown(
    """
       <style>
       [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 30%;
           max-width: 40%;
       }
       """,
    unsafe_allow_html=True,
)

high_level_view = True if granularity == "Revenue Mode" else False


# Title the app
st.title("Business Case Calculator")

st.markdown(
    """
 * Use the menu at left to input Merchant's information
 * Switch to Output Tab to check impact of Billie on Merchant's Revenue/Gross Profit
 * Switch to Visuals Tab for visualisation
"""
)

tab1, tab2, tab3 = st.tabs(["Merchant's Input", "Bille's Impact", "Visuals"])

tab1.markdown(css, unsafe_allow_html=True)
tab2.markdown(css, unsafe_allow_html=True)

financial = sidebar_financial(high_level=high_level_view)

payment = payment_info(high_level=high_level_view)

assumption = get_assumptions()


##---------------------------


## payment details
inhouse = payment[payment["Current B2B online payment solutions"] == "Inhouse BNPL"][
    "Share of total B2B online volume"
].iloc[0]
inhouse = float(inhouse.strip("%")) / 100
inhouse_cost = payment[
    payment["Current B2B online payment solutions"] == "Inhouse BNPL"
]["Assumed costs"].iloc[0]
inhouse_cost = float(inhouse_cost.strip("%")) / 100
external = payment[payment["Current B2B online payment solutions"] == "External BNPL"][
    "Share of total B2B online volume"
].iloc[0]
external = float(external.strip("%")) / 100
external_cost = payment[
    payment["Current B2B online payment solutions"] == "External BNPL"
]["Assumed costs"].iloc[0]
external_cost = float(external_cost.strip("%")) / 100
credit_card = payment[payment["Current B2B online payment solutions"] == "Credit Card"][
    "Share of total B2B online volume"
].iloc[0]
credit_card = float(credit_card.strip("%")) / 100
credit_cost = payment[payment["Current B2B online payment solutions"] == "Credit Card"][
    "Assumed costs"
].iloc[0]
credit_cost = float(credit_cost.strip("%")) / 100
debit_card = payment[payment["Current B2B online payment solutions"] == "Debit Card"][
    "Share of total B2B online volume"
].iloc[0]
debit_card = float(debit_card.strip("%")) / 100
debit_cost = payment[payment["Current B2B online payment solutions"] == "Debit Card"][
    "Assumed costs"
].iloc[0]
debit_cost = float(debit_cost.strip("%")) / 100
paypal = payment[payment["Current B2B online payment solutions"] == "Paypal"][
    "Share of total B2B online volume"
].iloc[0]
paypal = float(paypal.strip("%")) / 100
paypal_cost = payment[payment["Current B2B online payment solutions"] == "Paypal"][
    "Assumed costs"
].iloc[0]
paypal_cost = float(paypal_cost.strip("%")) / 100.0
other = payment[payment["Current B2B online payment solutions"] == "Other"][
    "Share of total B2B online volume"
].iloc[0]
other = float(other.strip("%")) / 100
other_cost = payment[payment["Current B2B online payment solutions"] == "Other"][
    "Assumed costs"
].iloc[0]
other_cost = float(other_cost.strip("%")) / 100

inhouse_bnpl_bool = payment[
    payment["Current B2B online payment solutions"] == "Inhouse BNPL"
]["Yes/ No"].iloc[0]
external_bnpl_bool = payment[
    payment["Current B2B online payment solutions"] == "External BNPL"
]["Yes/ No"].iloc[0]

has_bnpl = (
    inhouse_bnpl_bool or external_bnpl_bool
)  # used to show acceptance rate uplift in df only when the merchant has a bnpl solution


if has_bnpl:
    st.sidebar.markdown("### BNPL Details (if applicable)")
    # -- Set time by GPS or event
    avg_acceptance = st.sidebar.slider(
        "Average Acceptance Rate: (in %)",
        value=60.0,
        min_value=0.0,
        max_value=100.0,
        step=1.0,
    )
    avg_acceptance_formatted = "{:,.1%}".format(avg_acceptance / 100)
    avg_acceptance_rate = float(avg_acceptance_formatted.strip("%")) / 100


pricing = billie_pricing(high_level=high_level_view)


## financial details
revenue = financial[financial["Metric"] == "B2B revenues p.a. Online:"]["Value"].iloc[0]
revenue = float(str(revenue).replace(",", ""))
gross_profit = financial[financial["Metric"] == "Gross profit margin:"]["Value"].iloc[0]
gross_profit = float(gross_profit.strip("%")) / 100
avg_basket_size = financial[financial["Metric"] == "Average Basket Size:"][
    "Value"
].iloc[0]
avg_basket_size = float(str(avg_basket_size).replace(",", ""))
# avg_acceptance_rate = financial[financial["Metric"] == "Average Acceptance Rate:"][
#     "value"
# ].iloc[0]
# avg_acceptance_rate = float(avg_acceptance_rate.strip("%")) / 100 # TODO revert to old logic here


## pricing details & Conversion
fixed_fee = pricing[pricing["Metric"] == "Variable Fee:"]["Value"].iloc[0]
fixed_fee = float(fixed_fee.strip("%")) / 100
transaction_fee = pricing[pricing["Metric"] == "Fixed Fee:"]["Value"].iloc[0]
transaction_fee = float(transaction_fee)


blended_fee = (transaction_fee / avg_basket_size) + fixed_fee
# blended_fee_formatted = "{:,.3%}".format(blended_fee_calc / 100)

# blended_fee = pricing[pricing["Metric"] == "Blended Fee"]["value"].iloc[0]
# blended_fee = float(blended_fee_formatted.strip("%")) * 100

## assumption details
adoption_rate = assumption[
    assumption["Assumptions"] == "% Billie of total B2B online payment solutions"
]["Value"].iloc[0]
adoption_rate = float(adoption_rate.strip("%")) / 100
acceptance_rate = assumption[assumption["Assumptions"] == "Billie acceptance rates:"][
    "Value"
].iloc[0]
acceptance_rate = float(acceptance_rate.strip("%")) / 100
buyer_not_accepted_bnpl = assumption[
    assumption["Assumptions"] == "Buyers not accepted for BNPL:"
]["Value"].iloc[0]
buyer_not_accepted_bnpl = float(buyer_not_accepted_bnpl.strip("%")) / 100
cart_abandonment_rate = assumption[
    assumption["Assumptions"] == "Cart abandonment rate:"
]["Value"].iloc[0]
cart_abandonment_rate = float(cart_abandonment_rate.strip("%")) / 100
uplift_basket_size = assumption[
    assumption["Assumptions"] == "Increase in average basket size:"
]["Value"].iloc[0]
uplift_basket_size = float(uplift_basket_size.strip("%")) / 100
uplift_conversion_rate = assumption[
    assumption["Assumptions"] == "Increase in conversion rate:"
]["Value"].iloc[0]
uplift_conversion_rate = float(uplift_conversion_rate.strip("%")) / 100

### impoact of Billie on KPIs

##### OUTPUT METRICS ######
avg_basket_size_w_billie = avg_basket_size * (1 + uplift_basket_size)
delta_basket_size = avg_basket_size_w_billie - avg_basket_size
total_bnpl = inhouse + external
max_share = max(total_bnpl, adoption_rate)
total_non_bnpl = credit_card + debit_card + paypal + other
acceptance_rate_wo_bilie = 0 if total_bnpl == 0 else avg_acceptance_rate
acceptance_rate_w_billie = acceptance_rate
acceptance_rate_delta = acceptance_rate_w_billie - acceptance_rate_wo_bilie

acceptance_rate_abs_chg = (
    np.nan if total_bnpl == 0 else acceptance_rate_w_billie - acceptance_rate_wo_bilie
)
acceptance_rate_rel_chg = (
    np.nan
    if (total_bnpl == 0 and acceptance_rate_wo_bilie == 0)
    else acceptance_rate_abs_chg / acceptance_rate_wo_bilie
)

conversion_rate_wo_billie = np.nan if total_bnpl > 0 else 1 - cart_abandonment_rate
conversion_rate_w_billie = (
    np.nan
    if total_bnpl > 0
    else min(conversion_rate_wo_billie * (1 + uplift_conversion_rate), 1)
)
conversion_rate_absolute_chg = (
    np.nan if total_bnpl > 0 else conversion_rate_w_billie - conversion_rate_wo_billie
)
conversion_rate_relative_chg = np.nan if total_bnpl > 0 else uplift_conversion_rate

revenue_chg_basket_size = (
    (max_share - total_bnpl)
    * uplift_basket_size
    * revenue
    # if total_bnpl > 0
    # else revenue * uplift_basket_size * max_share
)


revenue_chg_acceptance_rate = (
    (
        revenue * total_bnpl / acceptance_rate_wo_bilie
        if acceptance_rate_wo_bilie != 0
        else np.nan
    )
    * coalesce(acceptance_rate_abs_chg, 0)
    * (1 - coalesce(buyer_not_accepted_bnpl, 0))
)

revenue_chg_conversion_rate = (
    0 if total_bnpl > 0 else revenue * uplift_conversion_rate
)  # revenue * (1 + uplift_conversion_rate) - revenue

revenue_abs_chg = (
    coalesce(revenue_chg_conversion_rate, 0)
    + coalesce(revenue_chg_acceptance_rate, 0)
    + coalesce(revenue_chg_basket_size, 0)
)

revenue_w_billie = revenue + revenue_abs_chg
gross_profit_amnt_wo_billie = revenue * gross_profit
## gross_profit_amnt_w_billie ## TODO

### PRINT OUT INPUT:

new_raw = {
    "Metric": "Transaction Fee",
    "Value": "{:,.2%}".format(blended_fee),
    "is_high_level": high_level_view,
}
pricing = pricing.append(new_raw, ignore_index=True)
tab1.table(
    financial[financial["is_high_level"] != True].drop(columns=["is_high_level"])
)

tab1.table(payment)


if len(pricing[pricing["is_high_level"] != True]) > 0:
    tab1.table(pricing.drop(columns=["is_high_level"]))

tab1.table(assumption)


impact_output_df = pd.DataFrame(
    [
        {
            "Impact of Billie": "Higher average basket size",
            "Without Billie": "{:,.0f}".format(avg_basket_size),
            "With Billie": "{:,.0f}".format(avg_basket_size_w_billie),
            "Abs. chg": "{:,.0f}".format(delta_basket_size),
            "Rel. chg (%)": "{:,.2%}".format(uplift_basket_size),
            "Change in Revneue": "{:,.0f}".format(revenue_chg_basket_size),  # todo
            "viewable": True,
        },
        {
            "Impact of Billie": "Acceptance rate increase (existing BNPL)",
            "Without Billie": "{:,.2%}".format(acceptance_rate_wo_bilie),
            "With Billie": "{:,.2%}".format(acceptance_rate_w_billie),
            "Abs. chg": "{:,.2%}".format(acceptance_rate_delta),
            "Rel. chg (%)": "{:,.2%}".format(acceptance_rate_rel_chg),
            "Change in Revneue": "{:,.0f}".format(revenue_chg_acceptance_rate),
            "viewable": has_bnpl,
        },
        {
            "Impact of Billie": "CR Increase (No existing BNPL)",
            "Without Billie": "{:,.2%}".format(conversion_rate_wo_billie),
            "With Billie": "{:,.2%}".format(conversion_rate_w_billie),
            "Abs. chg": "{:,.2%}".format(conversion_rate_absolute_chg),
            "Rel. chg (%)": "{:,.2%}".format(conversion_rate_relative_chg),
            "Change in Revneue": "{:,.0f}".format(revenue_chg_conversion_rate),
            "viewable": not has_bnpl,
        },
    ]
)


inhouse_amount_wo_billie = inhouse * revenue
external_amount_wo_billie = external * revenue
credit_card_amount_wo_bilie = credit_card * revenue
debit_card_amount_wo_billie = debit_card * revenue
paypal_amount_wo_billie = paypal * revenue
other_amount_wo_billie = other * revenue
total_amount_wo_billie = (
    inhouse_amount_wo_billie
    + external_amount_wo_billie
    + credit_card_amount_wo_bilie
    + debit_card_amount_wo_billie
    + paypal_amount_wo_billie
    + other_amount_wo_billie
)

billie_share = max_share
inhouse_share_w_billie = 0  # billie to take all the share
external_share_w_billie = 0  # billie to take all the share
credit_card_share_w_bilie = (
    (1 - billie_share) * credit_card / total_non_bnpl if total_non_bnpl != 0 else 0
)
debit_card_share_w_billie = (
    (1 - billie_share) * debit_card / total_non_bnpl if total_non_bnpl != 0 else 0
)
paypal_share_w_billie = (
    (1 - billie_share) * paypal / total_non_bnpl if total_non_bnpl != 0 else 0
)
other_share_w_billie = (
    (1 - billie_share) * other / total_non_bnpl if total_non_bnpl != 0 else 0
)

billie_amount = billie_share * revenue_w_billie
inhouse_amount_w_billie = inhouse_share_w_billie * revenue_w_billie
external_amount_w_billie = external_share_w_billie * revenue_w_billie
credit_card_amount_w_bilie = credit_card_share_w_bilie * revenue_w_billie
debit_card_amount_w_billie = debit_card_share_w_billie * revenue_w_billie
paypal_amount_w_billie = paypal_share_w_billie * revenue_w_billie
other_amount_w_billie = other_share_w_billie * revenue_w_billie

total_amount_w_billie = (
    billie_amount
    + inhouse_amount_w_billie
    + external_amount_w_billie
    + credit_card_amount_w_bilie
    + debit_card_amount_w_billie
    + paypal_amount_w_billie
    + other_amount_w_billie
)

cost_billie = blended_fee

inhouse_cost_amnt_wo_billie = inhouse_amount_wo_billie * inhouse_cost
external_cost_amnt_wo_billie = external_amount_wo_billie * external_cost
credit_cost_amnt_wo_billie = credit_card_amount_wo_bilie * credit_cost
debit_cost_amnt_wo_billie = debit_card_amount_wo_billie * debit_cost
paypal_cost_amnt_wo_billie = paypal_amount_wo_billie * paypal_cost
other_cost_amnt_wo_billie = other_amount_wo_billie * other_cost
total_cost_amnt_wo_billie = (
    inhouse_cost_amnt_wo_billie
    + external_cost_amnt_wo_billie
    + credit_cost_amnt_wo_billie
    + debit_cost_amnt_wo_billie
    + paypal_cost_amnt_wo_billie
    + other_cost_amnt_wo_billie
)

billie_cost_amnt = cost_billie * billie_amount
inhouse_cost_amnt_w_billie = inhouse_amount_w_billie * inhouse_cost
external_cost_amnt_w_billie = external_amount_w_billie * external_cost
credit_cost_amnt_w_billie = credit_card_amount_w_bilie * credit_cost
debit_cost_amnt_w_billie = debit_card_amount_w_billie * debit_cost
paypal_cost_amnt_w_billie = paypal_amount_w_billie * paypal_cost
other_cost_amnt_w_billie = other_amount_w_billie * other_cost
total_cost_amnt_w_billie = (
    billie_cost_amnt
    + inhouse_cost_amnt_w_billie
    + external_cost_amnt_w_billie
    + credit_cost_amnt_w_billie
    + debit_cost_amnt_w_billie
    + paypal_cost_amnt_w_billie
    + other_cost_amnt_w_billie
)

wavg_cost_wo_billie = (
    (
        inhouse_amount_wo_billie * inhouse_cost
        + external_amount_wo_billie * external_cost
        + credit_card_amount_wo_bilie * credit_cost
        + debit_card_amount_wo_billie * debit_cost
        + paypal_amount_wo_billie * paypal_cost
        + other_amount_wo_billie * other_cost
    )
    / total_amount_wo_billie
    if total_amount_wo_billie != 0
    else 0
)

wavg_cost_w_billie = (
    billie_amount * cost_billie
    + inhouse_amount_w_billie * inhouse_cost
    + external_amount_w_billie * external_cost
    + credit_card_amount_w_bilie * credit_cost
    + debit_card_amount_w_billie * debit_cost
    + paypal_amount_w_billie * paypal_cost
    + other_amount_w_billie * other_cost
)
# total_cost_w_billie = cost_billie +

# delta_revenue = (max_share - total_bnpl) * uplift_basket_size * revenue

inhouse_gross_profit_wo_billie = inhouse_amount_wo_billie * (
    gross_profit - (inhouse_cost - wavg_cost_wo_billie)
)
external_gross_profit_wo_billie = external_amount_wo_billie * (
    gross_profit - (external_cost - wavg_cost_wo_billie)
)
credit_gross_profit_wo_billie = credit_card_amount_wo_bilie * (
    gross_profit - (credit_cost - wavg_cost_wo_billie)
)
debit_gross_profit_wo_billie = debit_card_amount_wo_billie * (
    gross_profit - (debit_cost - wavg_cost_wo_billie)
)
paypal_gross_profit_wo_billie = paypal_amount_wo_billie * (
    gross_profit - (paypal_cost - wavg_cost_wo_billie)
)
other_gross_profit_wo_billie = other_amount_wo_billie * (
    gross_profit - (other_cost - wavg_cost_wo_billie)
)
total_gross_profit_wo_billie = (
    inhouse_gross_profit_wo_billie
    + external_gross_profit_wo_billie
    + credit_gross_profit_wo_billie
    + debit_gross_profit_wo_billie
    + paypal_gross_profit_wo_billie
    + other_gross_profit_wo_billie
)

billie_gross_profit_w_billie = billie_amount * (
    gross_profit - (cost_billie - wavg_cost_wo_billie)
)
inhouse_gross_profit_w_billie = inhouse_amount_w_billie * (
    gross_profit - (inhouse_cost - wavg_cost_wo_billie)
)
external_gross_profit_w_billie = external_amount_w_billie * (
    gross_profit - (external_cost - wavg_cost_wo_billie)
)
credit_gross_profit_w_billie = credit_card_amount_w_bilie * (
    gross_profit - (credit_cost - wavg_cost_wo_billie)
)
debit_gross_profit_w_billie = debit_card_amount_w_billie * (
    gross_profit - (debit_cost - wavg_cost_wo_billie)
)
paypal_gross_profit_w_billie = paypal_amount_w_billie * (
    gross_profit - (paypal_cost - wavg_cost_wo_billie)
)
other_gross_profit_w_billie = other_amount_w_billie * (
    gross_profit - (other_cost - wavg_cost_wo_billie)
)
total_gross_profit_w_billie = (
    billie_gross_profit_w_billie
    + inhouse_gross_profit_w_billie
    + external_gross_profit_w_billie
    + credit_gross_profit_w_billie
    + debit_gross_profit_w_billie
    + paypal_gross_profit_w_billie
    + other_gross_profit_w_billie
)


# "{:,.2%}".format(
# "{:,.0f}".format(
payment_output_df = pd.DataFrame(
    [
        {
            "Payment solution": "Billie",
            "Vol. Share w/o Billie": "{:,.0%}".format(0.0),
            "Vol. Amount w/o Billie": "{:,.0f}".format(0),
            "Cost Share w/o Billie": "{:,.2%}".format(0),
            "Cost Amount w/o Billie": "{:,.0f}".format(0),
            "Gross Profit w/o Billie": "{:,.0f}".format(0),  # todo
            "Vol. Share w Billie": "{:,.0%}".format(billie_share),
            "Vol. Amount w Billie": "{:,.0f}".format(billie_amount),
            "Cost Share w Billie": "{:,.2%}".format(cost_billie),
            "Cost Amount w Billie": "{:,.0f}".format(billie_cost_amnt),
            "Gross Profit w Billie": "{:,.0f}".format(
                billie_gross_profit_w_billie
            ),  # todo
            # "is_high_level": high_level_view,
        },
        {
            "Payment solution": "Inhouse BNPL",
            "Vol. Share w/o Billie": "{:,.0%}".format(inhouse),
            "Vol. Amount w/o Billie": "{:,.0f}".format(inhouse_amount_wo_billie),
            "Cost Share w/o Billie": "{:,.2%}".format(inhouse_cost),
            "Cost Amount w/o Billie": "{:,.0f}".format(inhouse_cost_amnt_wo_billie),
            "Gross Profit w/o Billie": "{:,.0f}".format(inhouse_gross_profit_wo_billie),
            "Vol. Share w Billie": "{:,.0%}".format(inhouse_share_w_billie),
            "Vol. Amount w Billie": "{:,.0f}".format(inhouse_amount_w_billie),
            "Cost Share w Billie": "{:,.2%}".format(inhouse_cost),
            "Cost Amount w Billie": "{:,.0f}".format(inhouse_cost_amnt_w_billie),
            "Gross Profit w Billie": "{:,.0f}".format(
                inhouse_gross_profit_w_billie
            ),  # todo
        },
        {
            "Payment solution": "External BNPL",
            "Vol. Share w/o Billie": "{:,.0%}".format(external),
            "Vol. Amount w/o Billie": "{:,.0f}".format(external_amount_wo_billie),
            "Cost Share w/o Billie": "{:,.2%}".format(external_cost),
            "Cost Amount w/o Billie": "{:,.0f}".format(external_cost_amnt_wo_billie),
            "Gross Profit w/o Billie": "{:,.0f}".format(
                external_gross_profit_wo_billie
            ),
            "Vol. Share w Billie": "{:,.0%}".format(external_share_w_billie),
            "Vol. Amount w Billie": "{:,.0f}".format(external_amount_w_billie),
            "Cost Share w Billie": "{:,.2%}".format(external_cost),
            "Cost Amount w Billie": "{:,.0f}".format(external_cost_amnt_w_billie),
            "Gross Profit w Billie": "{:,.0f}".format(
                external_gross_profit_w_billie
            ),  # todo
        },
        {
            "Payment solution": "Credit Card",
            "Vol. Share w/o Billie": "{:,.0%}".format(credit_card),
            "Vol. Amount w/o Billie": "{:,.0f}".format(credit_card_amount_wo_bilie),
            "Cost Share w/o Billie": "{:,.2%}".format(credit_cost),
            "Cost Amount w/o Billie": "{:,.0f}".format(credit_cost_amnt_wo_billie),
            "Gross Profit w/o Billie": "{:,.0f}".format(credit_gross_profit_wo_billie),
            "Vol. Share w Billie": "{:,.0%}".format(credit_card_share_w_bilie),
            "Vol. Amount w Billie": "{:,.0f}".format(credit_card_amount_w_bilie),
            "Cost Share w Billie": "{:,.2%}".format(credit_cost),
            "Cost Amount w Billie": "{:,.0f}".format(credit_cost_amnt_w_billie),
            "Gross Profit w Billie": "{:,.0f}".format(
                credit_gross_profit_w_billie
            ),  # todo # todo
        },
        {
            "Payment solution": "Debit Card",
            "Vol. Share w/o Billie": "{:,.0%}".format(debit_card),
            "Vol. Amount w/o Billie": "{:,.0f}".format(debit_card_amount_wo_billie),
            "Cost Share w/o Billie": "{:,.2%}".format(debit_cost),
            "Cost Amount w/o Billie": "{:,.0f}".format(debit_cost_amnt_wo_billie),
            "Gross Profit w/o Billie": "{:,.0f}".format(debit_gross_profit_wo_billie),
            "Vol. Share w Billie": "{:,.0%}".format(debit_card_share_w_billie),
            "Vol. Amount w Billie": "{:,.0f}".format(debit_card_amount_w_billie),
            "Cost Share w Billie": "{:,.2%}".format(debit_cost),
            "Cost Amount w Billie": "{:,.0f}".format(debit_cost_amnt_w_billie),
            "Gross Profit w Billie": "{:,.0f}".format(
                debit_gross_profit_w_billie
            ),  # todo
        },
        {
            "Payment solution": "Paypal",
            "Vol. Share w/o Billie": "{:,.0%}".format(paypal),
            "Vol. Amount w/o Billie": "{:,.0f}".format(paypal_amount_wo_billie),
            "Cost Share w/o Billie": "{:,.2%}".format(paypal_cost),
            "Cost Amount w/o Billie": "{:,.0f}".format(paypal_cost_amnt_wo_billie),
            "Gross Profit w/o Billie": "{:,.0f}".format(paypal_gross_profit_wo_billie),
            "Vol. Share w Billie": "{:,.0%}".format(paypal_share_w_billie),
            "Vol. Amount w Billie": "{:,.0f}".format(paypal_amount_w_billie),
            "Cost Share w Billie": "{:,.2%}".format(paypal_cost),
            "Cost Amount w Billie": "{:,.0f}".format(paypal_cost_amnt_w_billie),
            "Gross Profit w Billie": "{:,.0f}".format(
                paypal_gross_profit_w_billie
            ),  # todo
        },
        {
            "Payment solution": "Other",
            "Vol. Share w/o Billie": "{:,.0%}".format(other),
            "Vol. Amount w/o Billie": "{:,.0f}".format(other_amount_wo_billie),
            "Cost Share w/o Billie": "{:,.2%}".format(other_cost),
            "Cost Amount w/o Billie": "{:,.0f}".format(other_cost_amnt_wo_billie),
            "Gross Profit w/o Billie": "{:,.0f}".format(other_gross_profit_wo_billie),
            "Vol. Share w Billie": "{:,.0%}".format(other_share_w_billie),
            "Vol. Amount w Billie": "{:,.0f}".format(other_amount_w_billie),
            "Cost Share w Billie": "{:,.2%}".format(other_cost),
            "Cost Amount w Billie": "{:,.0f}".format(other_cost_amnt_w_billie),
            "Gross Profit w Billie": "{:,.0f}".format(
                other_gross_profit_w_billie
            ),  # todo
        },
        {
            "Payment solution": "Total",
            "Vol. Share w/o Billie": "{:,.0%}".format(0),
            "Vol. Amount w/o Billie": "{:,.0f}".format(0),
            "Cost Share w/o Billie": "{:,.2%}".format(0),
            "Cost Amount w/o Billie": "{:,.0f}".format(0),
            "Gross Profit w/o Billie": "{:,.0f}".format(0),
            "Vol. Share w Billie": 0,
            "Vol. Amount w Billie": "{:,.0f}".format(0),
            "Cost Share w Billie": "{:,.2%}".format(0),
            "Cost Amount w Billie": "{:,.0f}".format(0),
            "Gross Profit w Billie": "{:,.0f}".format(0),
        },
    ]
)


gross_profit_abs_chg = total_gross_profit_w_billie - gross_profit_amnt_wo_billie
gross_profit_rel_chg = gross_profit_abs_chg / gross_profit_amnt_wo_billie
revenue_rel_chg = revenue_abs_chg / revenue

amount_rel_chg = (
    total_amount_w_billie - total_amount_wo_billie
) / total_amount_wo_billie

cost_rel_chg = (
    total_cost_amnt_w_billie - total_cost_amnt_wo_billie
) / total_cost_amnt_w_billie

# "{:,.2%}".format(
# "{:,.0f}".format(
revenue_output_df = pd.DataFrame(
    [
        {
            "Uplift Potential w. Billie": "Revenues p.a.",
            "Without Billie": "{:,.0f}".format(revenue),
            "With Billie": "{:,.0f}".format(revenue_w_billie),
            "Abs. chg": "{:,.0f}".format(revenue_abs_chg),
            "Rel. chg (%)": "{:,.1%}".format(revenue_rel_chg),
            "is_high_level": False,
        },
        {
            "Uplift Potential w. Billie": "Gross profits p.a.",
            "Without Billie": "{:,.0f}".format(gross_profit_amnt_wo_billie),
            "With Billie": "{:,.0f}".format(total_gross_profit_w_billie),
            "Abs. chg": "{:,.0f}".format(gross_profit_abs_chg),
            "Rel. chg (%)": "{:,.1%}".format(gross_profit_rel_chg),
            "is_high_level": high_level_view,
        },
    ]
)

### Metrics
met1, met2, met3 = tab2.columns(3)
# vol
met1.metric(
    label="Total Vol. w Billie",
    value="{:,.0f}".format(round(total_amount_w_billie, 0)),
    delta="{:,.1%}".format(amount_rel_chg),  # f"20%",
    delta_color="normal",
)

met1.metric(
    label="Total Vol. w/o Billie",
    value="{:,.0f}".format(total_amount_wo_billie),
    delta_color="normal",
)
# revenue_chg_basket_size
# revenue_chg_acceptance_rate
# revenue_chg_conversion_rate

# cost
met2.metric(
    label="Basket Size Increase",
    value="{:,.0f}".format(round(avg_basket_size_w_billie, 0)),
    delta="{:,.1%}".format(uplift_basket_size),
    delta_color="normal",
)
if has_bnpl:
    met2.metric(
        label="Rev Chg. Acceptance",
        value="{:,.0f}".format(revenue_chg_acceptance_rate),
        delta="{:,.1%}".format(acceptance_rate_rel_chg),
        delta_color="normal",
    )
else:
    met2.metric(
        label="Rev Chg. Conversion",
        value="{:,.0f}".format(revenue_chg_conversion_rate),
        delta="{:,.1%}".format(conversion_rate_relative_chg),
        delta_color="normal",
    )
# gross profit
if not high_level_view:
    met3.metric(
        label="Total GP w Billie",
        value="{:,.0f}".format(round(total_gross_profit_w_billie, 0)),  # "2,904,000",
        delta="{:,.1%}".format(gross_profit_rel_chg),  #
        # delta_color="inverse",
    )

    met3.metric(
        label="Total GP w/o Billie",
        value="{:,.0f}".format(total_gross_profit_wo_billie),
        delta_color="normal",
    )


# Set the default page config with the CSS style


impact_filtered_df = impact_output_df[impact_output_df["viewable"] == True].drop(
    columns=["viewable"]
)


####PAYMENT OUTPUT
tab2.table(
    revenue_output_df[revenue_output_df["is_high_level"] != True].drop(
        columns=["is_high_level"]
    )
)

# tab2.markdown('<div class="custom-table">', unsafe_allow_html=True)
tab2.table(impact_filtered_df)  #
# tab2.markdown("</div>", unsafe_allow_html=True)


if high_level_view:
    tab2.table(
        payment_output_df.drop(
            columns=[
                "Cost Share w/o Billie",
                "Cost Share w Billie",
                "Cost Amount w/o Billie",
                "Cost Amount w Billie",
                "Gross Profit w/o Billie",
                "Gross Profit w Billie",
            ]
        )
    )
else:
    tab2.table(payment_output_df)

# tab2.write(inhouse)
# tab2.write(credit_card)

tab3.plotly_chart(
    waterfall_fig(
        revenue=revenue,
        revenue_chg_basket_size=revenue_chg_basket_size,
        revenue_chg_conversion_rate=revenue_chg_conversion_rate,
        revenue_chg_acceptance_rate=revenue_chg_acceptance_rate,
        revenue_w_billie=revenue_w_billie,
        has_bnpl=has_bnpl,
    ),
    theme="streamlit",
    use_container_width=True,
)


# tab2.write(revenue_w_billie)
# tab2.write(debit_card_amount_w_billie)
# tab2.write(debit_card_share_w_billie)
# tab2.write()
