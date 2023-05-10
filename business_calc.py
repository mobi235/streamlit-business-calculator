"""Main app file"""
# import plotly.graph_objects as go

import numpy as np
import pandas as pd
import streamlit as st

from layout import coalesce, get_assumptions, set_image, waterfall_fig

# plotly==5.11.0
# import matplotlib.pyplot as plt
from sidebar import payment_info, sidebar_financial  # , set_image

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

with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

set_image()

# Title the app
st.title("Business Case Calculator")

st.markdown(
    """
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
"""
)

tab1, tab2, tab3 = st.tabs(["Input", "Output", "Visuals"])

financial, pricing = sidebar_financial()

payment = payment_info()

assumption = get_assumptions()

##---------------------------
tab1.dataframe(financial)
# tab1.markdown(
#     style_dataframe(financial).to_html(
#         table_uuid="table_1",
#     ),
#     unsafe_allow_html=True,
# )
# tab1.write("")
##---------------------------

# tab1.table(style_dataframe(payment))  # , use_container_width=True
# tab1.markdown(
#     style_dataframe(payment).to_html(table_uuid="table_1"), unsafe_allow_html=True
# )
# tab1.write(" ")
tab1.dataframe(payment)

##---------------------------

# tab1.table(style_dataframe(pricing))  # , use_container_width=True
# tab1.markdown(
#     style_dataframe(pricing).to_html(
#         index=False, index_names=False, table_uuid="table_1"
#     ),
#     unsafe_allow_html=True,
# )
# tab1.write(" ")
tab1.dataframe(pricing)

##---------------------------

# tab1.table(style_dataframe(assumption))  # , use_container_width=True
# tab1.markdown(
#     style_dataframe(assumption).to_html(table_uuid="table_1"), unsafe_allow_html=True
# )
# tab1.write(" ")
tab1.dataframe(assumption)

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

## financial details
revenue = financial[financial["Metric"] == "B2B revenues p.a. Online:"]["value"].iloc[0]
revenue = float(str(revenue).replace(",", ""))
gross_profit = financial[financial["Metric"] == "Gross profit margin:"]["value"].iloc[0]
gross_profit = float(gross_profit.strip("%")) / 100
avg_basket_size = financial[financial["Metric"] == "Average Basket Size:"][
    "value"
].iloc[0]
avg_basket_size = float(avg_basket_size)
avg_acceptance_rate = financial[financial["Metric"] == "Average Acceptance Rate:"][
    "value"
].iloc[0]
avg_acceptance_rate = float(avg_acceptance_rate.strip("%")) / 100

## pricing details & Conversion
fixed_fee = pricing[pricing["Metric"] == "Fixed Fee:"]["value"].iloc[0]
fixed_fee = float(fixed_fee.strip("%")) / 100
transaction_fee = pricing[pricing["Metric"] == "Transaction Fee:"]["value"].iloc[0]
transaction_fee = float(transaction_fee)
blended_fee = pricing[pricing["Metric"] == "Blended Fee"]["value"].iloc[0]
blended_fee = float(blended_fee.strip("%")) / 100

## assumption details
adoption_rate = assumption[
    assumption["Assumptions"] == "% Billie of total B2B online payment solutions"
]["value"].iloc[0]
adoption_rate = float(adoption_rate.strip("%")) / 100
acceptance_rate = assumption[assumption["Assumptions"] == "Billie acceptance rates:"][
    "value"
].iloc[0]
acceptance_rate = float(acceptance_rate.strip("%")) / 100
buyer_not_accepted_bnpl = assumption[
    assumption["Assumptions"] == "Buyers not accepted for BNPL:"
]["value"].iloc[0]
buyer_not_accepted_bnpl = float(buyer_not_accepted_bnpl.strip("%")) / 100
cart_abandonment_rate = assumption[
    assumption["Assumptions"] == "Cart abandonment rate:"
]["value"].iloc[0]
cart_abandonment_rate = float(cart_abandonment_rate.strip("%")) / 100
uplift_basket_size = assumption[
    assumption["Assumptions"] == "Increase in average basket size:"
]["value"].iloc[0]
uplift_basket_size = float(uplift_basket_size.strip("%")) / 100
uplift_conversion_rate = assumption[
    assumption["Assumptions"] == "Increase in conversion rate:"
]["value"].iloc[0]
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

impact_output_df = pd.DataFrame(
    [
        {
            "Impact of Billie": "Higher average basket size",
            "Without Billie": avg_basket_size,
            "With Billie": avg_basket_size_w_billie,
            "Abs. chg": delta_basket_size,
            "Rel. chg (%)": uplift_basket_size,
            "Change in Revneue": revenue_chg_basket_size,  # todo
            "viewable": True,
        },
        {
            "Impact of Billie": "Acceptance rate increase (existing BNPL)",
            "Without Billie": acceptance_rate_wo_bilie,
            "With Billie": acceptance_rate_w_billie,
            "Abs. chg": acceptance_rate_delta,
            "Rel. chg (%)": acceptance_rate_rel_chg,
            "Change in Revneue": revenue_chg_acceptance_rate,
            "viewable": has_bnpl,
        },
        {
            "Impact of Billie": "CR Increase (No existing BNPL)",
            "Without Billie": conversion_rate_wo_billie,
            "With Billie": conversion_rate_w_billie,
            "Abs. chg": conversion_rate_absolute_chg,
            "Rel. chg (%)": conversion_rate_relative_chg,
            "Change in Revneue": revenue_chg_conversion_rate,
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

payment_output_df = pd.DataFrame(
    [
        {
            "Payment solution": "Billie",
            "Vol. Share w/o Billie": 0,
            "Vol. Share w Billie": billie_share,
            "Vol. Amount w/o Billie": 0,
            "Vol. Amount w Billie": billie_amount,
            "Cost Share w/o Billie": 0,
            "Cost Share w Billie": cost_billie,
            "Cost Amount w/o Billie": 0,
            "Cost Amount w Billie": billie_cost_amnt,
            "Gross Profit w/o Billie": 0,  # todo
            "Gross Profit w Billie": billie_gross_profit_w_billie,  # todo
        },
        {
            "Payment solution": "Inhouse BNPL",
            "Vol. Share w/o Billie": inhouse,
            "Vol. Share w Billie": inhouse_share_w_billie,
            "Vol. Amount w/o Billie": inhouse_amount_wo_billie,
            "Vol. Amount w Billie": inhouse_amount_w_billie,
            "Cost Share w/o Billie": inhouse_cost,
            "Cost Share w Billie": inhouse_cost,
            "Cost Amount w/o Billie": inhouse_cost_amnt_wo_billie,
            "Cost Amount w Billie": inhouse_cost_amnt_w_billie,
            "Gross Profit w/o Billie": inhouse_gross_profit_wo_billie,
            "Gross Profit w Billie": inhouse_gross_profit_w_billie,  # todo
        },
        {
            "Payment solution": "External BNPL",
            "Vol. Share w/o Billie": external,
            "Vol. Share w Billie": external_share_w_billie,
            "Vol. Amount w/o Billie": external_amount_wo_billie,
            "Vol. Amount w Billie": external_amount_w_billie,
            "Cost Share w/o Billie": external_cost,
            "Cost Share w Billie": external_cost,
            "Cost Amount w/o Billie": external_cost_amnt_wo_billie,
            "Cost Amount w Billie": external_cost_amnt_w_billie,
            "Gross Profit w/o Billie": external_gross_profit_wo_billie,
            "Gross Profit w Billie": external_gross_profit_w_billie,  # todo
        },
        {
            "Payment solution": "Credit Card",
            "Vol. Share w/o Billie": credit_card,
            "Vol. Share w Billie": credit_card_share_w_bilie,
            "Vol. Amount w/o Billie": credit_card_amount_wo_bilie,
            "Vol. Amount w Billie": credit_card_amount_w_bilie,
            "Cost Share w/o Billie": credit_cost,
            "Cost Share w Billie": credit_cost,
            "Cost Amount w/o Billie": credit_cost_amnt_wo_billie,
            "Cost Amount w Billie": credit_cost_amnt_w_billie,
            "Gross Profit w/o Billie": credit_gross_profit_wo_billie,
            "Gross Profit w Billie": credit_gross_profit_w_billie,  # todo # todo
        },
        {
            "Payment solution": "Debit Card",
            "Vol. Share w/o Billie": debit_card,
            "Vol. Share w Billie": debit_card_share_w_billie,
            "Vol. Amount w/o Billie": debit_card_amount_wo_billie,
            "Vol. Amount w Billie": debit_card_amount_w_billie,
            "Cost Share w/o Billie": debit_cost,
            "Cost Share w Billie": debit_cost,
            "Cost Amount w/o Billie": debit_cost_amnt_wo_billie,
            "Cost Amount w Billie": debit_cost_amnt_w_billie,
            "Gross Profit w/o Billie": debit_gross_profit_wo_billie,
            "Gross Profit w Billie": debit_gross_profit_w_billie,  # todo
        },
        {
            "Payment solution": "Paypal",
            "Vol. Share w/o Billie": paypal,
            "Vol. Share w Billie": paypal_share_w_billie,
            "Vol. Amount w/o Billie": paypal_amount_wo_billie,
            "Vol. Amount w Billie": paypal_amount_w_billie,
            "Cost Share w/o Billie": paypal_cost,
            "Cost Share w Billie": paypal_cost,
            "Cost Amount w/o Billie": paypal_cost_amnt_wo_billie,
            "Cost Amount w Billie": paypal_cost_amnt_w_billie,
            "Gross Profit w/o Billie": paypal_gross_profit_wo_billie,
            "Gross Profit w Billie": paypal_gross_profit_w_billie,  # todo
        },
        {
            "Payment solution": "Other",
            "Vol. Share w/o Billie": other,
            "Vol. Share w Billie": other_share_w_billie,
            "Vol. Amount w/o Billie": other_amount_wo_billie,
            "Vol. Amount w Billie": other_amount_w_billie,
            "Cost Share w/o Billie": other_cost,
            "Cost Share w Billie": other_cost,
            "Cost Amount w/o Billie": other_cost_amnt_wo_billie,
            "Cost Amount w Billie": other_cost_amnt_w_billie,
            "Gross Profit w/o Billie": other_gross_profit_wo_billie,
            "Gross Profit w Billie": other_gross_profit_w_billie,  # todo
        },
        {
            "Payment solution": "Total",
            "Vol. Share w/o Billie": 0,
            "Vol. Share w Billie": 0,
            "Vol. Amount w/o Billie": 0,
            "Vol. Amount w Billie": 0,
            "Cost Share w/o Billie": 0,
            "Cost Share w Billie": 0,
            "Cost Amount w/o Billie": 0,
            "Cost Amount w Billie": 0,
            "Gross Profit w/o Billie": 0,
            "Gross Profit w Billie": 0,
        },
    ]
)

test_button = True


gross_profit_abs_chg = total_gross_profit_w_billie - gross_profit_amnt_wo_billie
gross_profit_rel_chg = gross_profit_abs_chg / gross_profit_amnt_wo_billie
revenue_rel_chg = revenue_abs_chg / revenue

amount_rel_chg = (
    total_amount_w_billie - total_amount_wo_billie
) / total_amount_w_billie

cost_rel_chg = (
    total_cost_amnt_w_billie - total_cost_amnt_wo_billie
) / total_cost_amnt_w_billie

revenue_output_df = pd.DataFrame(
    [
        {
            "Uplift Potential w. Billie": "Revenues p.a.",
            "Without Billie": revenue,
            "With Billie": revenue_w_billie,
            "Abs. chg": revenue_abs_chg,
            "Rel. chg (%)": revenue_rel_chg,
        },
        {
            "Uplift Potential w. Billie": "Gross profits p.a.",
            "Without Billie": gross_profit_amnt_wo_billie,
            "With Billie": total_gross_profit_w_billie,
            "Abs. chg": gross_profit_abs_chg,
            "Rel. chg (%)": gross_profit_rel_chg,
        },
    ]
)

### Metrics
met1, met2, met3 = tab2.columns(3)
# vol
met1.metric(
    label="Total Vol. w Billie",
    value="{:,}".format(round(total_amount_w_billie, 0)),
    delta="{:,.1%}".format(amount_rel_chg),  # f"20%",
    # delta_color="inverse",
)

met1.metric(
    label="Total Vol. w/o Billie",
    value="{:,}".format(total_amount_wo_billie),
    delta_color="off",
)
# cost
met2.metric(
    label="Total Cost. w Billie",
    value="{:,}".format(round(total_cost_amnt_w_billie, 0)),
    delta="{:,.1%}".format(cost_rel_chg),
    delta_color="inverse",
)

met2.metric(
    label="Total Cost. w/o Billie",
    value="{:,}".format(total_cost_amnt_wo_billie),
    delta_color="off",
)
# gross profit
met3.metric(
    label="Total GP w Billie",
    value="{:,}".format(round(total_gross_profit_w_billie, 0)),  # "2,904,000",
    delta="{:,.1%}".format(gross_profit_rel_chg),  #
    # delta_color="inverse",
)

met3.metric(
    label="Total GP w/o Billie",
    value="{:,}".format(total_gross_profit_wo_billie),
    delta_color="off",
)


css = """
    <style>
    table {
        font-family: "Times New Roman", Times, serif;
        border: 1px solid #FFFFFF;
        width: 350px;
        height: 200px;
        text-align: center;
        border-collapse: collapse;

        }

            td, th {
                border: 1px solid #FFFFFF;
                padding: 3px 2px;
            }

            tbody td {
                font-size: 13px;
            }

            td:nth-child(even) {
                background: #EBEBEB;
            }

            thead {
                background: #6600d8;
                border-bottom: 1px solid #ffffff;
                color:#FFFFFF;
                font-size:16px;
            }

            thead th {
                font-size: 16px;
                font-weight: bold;
                color: #FFFFFF;
                text-align: center;
                border-left: 1px solid #FFFFFF;
            }

            thead th:first-child {
                border-left: none;
                color: #FFFFFF;
            }

            tfoot {
                font-size: 12px;
                font-weight: bold;
                color: #1E1E1E;
                background: #7F7F7F;
            }

            tfoot td {
                font-size: 12px;
            }
    </style>
"""

# Set the default page config with the CSS style
st.markdown(css, unsafe_allow_html=True)


impact_filtered_df = impact_output_df[impact_output_df["viewable"] == True].drop(
    columns=["viewable"]
)
####PAYMENT OUTPUT
tab2.table(revenue_output_df)
tab2.markdown('<div class="custom-table">', unsafe_allow_html=True)
tab2.table(impact_filtered_df)  #
tab2.markdown("</div>", unsafe_allow_html=True)
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
