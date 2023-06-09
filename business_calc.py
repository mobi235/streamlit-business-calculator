"""Main app file"""
# link to app: https://billie-roi-calculator.streamlit.app/
import numpy as np
import pandas as pd
import streamlit as st

from layout import coalesce, get_assumptions, set_image, waterfall_fig, css
from sidebar import payment_info, sidebar_financial, billie_pricing  


def set_style(df, style):
    return df.style.set_properties(**{'text-align': 'left'}).set_table_styles(style, overwrite=True)
    

# -- Set page config
apptitle = "Billie ROI" 

st.set_page_config(page_title=apptitle, 
                   layout="wide",
                   initial_sidebar_state="expanded", # ["auto", "expanded", "collapsed"]
                   )

# Add Billie Logo
set_image()

# Padding between Logo and rest of the app
st.markdown("<p style='padding-top:50px'></p>", unsafe_allow_html=True)

# Choose mode ['Gross Profit Mode', 'Revenue Mode'] 
# TODO: how to make it dynamic, so that when it is accessed from Billie.io >> Default 'Revenue Mode' 
# esle >>> 'Gross Profit Mode' 
granularity = st.selectbox(
    "Choose impact granularity:",
    (
        "Gross Profit Mode",
        "Revenue Mode",
    ),
)

# Make assumption tab available for editiing 
adjust_assumptions = st.checkbox("Adjust Assumptions: ")

# Which mode is active 
high_level_view = True if granularity == "Revenue Mode" else False

# Plot sidebar items: 
financial = sidebar_financial(high_level=high_level_view)

# DataFrame CSS Styling 
# TODO Move to layout, and make more dynamic to choose from. i.e, make n styles, and user can choose from in function 
th_props = [
  ('font-size', '14px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#FFFFFF'),
  ('background-color', '#6600f5')
  ]
                               
td_props = [
  ('font-size', '12px'), 
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props),
  dict(selector="tbody td", props=[
                            #('font-size', '14px'),
                            ('text-align', 'center'),
                            #('font-weight', 'bold'),
                            ('color', '#1e1e1e'),
                            ('background-color', '#d8d8d8'), # '#fef1cc' 
                            ] ), 
  ]

styles_footer = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props),
  dict(selector="tbody tr:nth-child(8) td:nth-child(n+2)", props=[
                             #('font-size', '14px'),
                             ('text-align', 'center'),
                             ('font-weight', 'bolder'),
                             ('color', '#FFFFFF'),
                             ('background-color', '#7f7f7f'), # '#fef1cc' 
                             ] ), 
  dict(selector= "tbody tr:not(:last-child)",props=[
                             #('font-size', '14px'),
                             ('text-align', 'center'),
                             ('font-weight', 'normal'),
                             ('color', '#1e1e1e'),
                             ('background-color', '#d8d8d8'), # '#fef1cc' 
                             ]  ),
  dict(selector= "tbody tr:not(:last-child) td:nth-child(n+8)",props=[
                             #('font-size', '14px'),
                             ('text-align', 'center'),
                             ('font-weight', 'normal'),
                             ('color', '#1e1e1e'),
                             ('background-color', '#fef1cc'), # '#fef1cc' 
                             ]  ) if not high_level_view 
                             else 
    dict(selector= "tbody tr:not(:last-child) td:nth-child(n+5)",props=[
                             #('font-size', '14px'),
                             ('text-align', 'center'),
                             ('font-weight', 'normal'),
                             ('color', '#1e1e1e'),
                             ('background-color', '#fef1cc'), # '#fef1cc' 
                             ]  ), # last four columns excluding footer

  ]

# controls width & size of side bar 
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

# Title the app
st.title("Business Case Calculator")

# TODO add more description, or move description to help icon on each component 
st.markdown(
    """
 * Use the menu at left to input Merchant's information
 * Switch to 'Billie's Impact' Tab to check impact of Billie on Merchant's Revenue/Gross Profit
 * Switch to Visuals Tab for visualisation
"""
)

# Three tabular bars for the main app 
tab1, tab2, tab3 = st.tabs(["Merchant's Input", "Bille's Impact", "Visuals"])

st.markdown(css, unsafe_allow_html=True)
tab1.markdown(css, unsafe_allow_html=True)
tab2.markdown(css, unsafe_allow_html=True)


payment = payment_info(high_level=high_level_view)

## payment details: extracting values 
inhouse = payment[payment["Current B2B Online Payment Solutions"] == "Inhouse BNPL"][
    "Share of Total B2B Online Volume"
].iloc[0]
inhouse = float(inhouse.strip("%")) / 100

inhouse_cost = payment[
    payment["Current B2B Online Payment Solutions"] == "Inhouse BNPL"
]["Assumed Costs"].iloc[0]
inhouse_cost = float(inhouse_cost.strip("%")) / 100

external = payment[payment["Current B2B Online Payment Solutions"] == "External BNPL"][
    "Share of Total B2B Online Volume"
].iloc[0]
external = float(external.strip("%")) / 100

external_cost = payment[
    payment["Current B2B Online Payment Solutions"] == "External BNPL"
]["Assumed Costs"].iloc[0]
external_cost = float(external_cost.strip("%")) / 100

credit_card = payment[payment["Current B2B Online Payment Solutions"] == "Credit Card"][
    "Share of Total B2B Online Volume"
].iloc[0]
credit_card = float(credit_card.strip("%")) / 100

credit_cost = payment[payment["Current B2B Online Payment Solutions"] == "Credit Card"][
    "Assumed Costs"
].iloc[0]
credit_cost = float(credit_cost.strip("%")) / 100

debit_card = payment[payment["Current B2B Online Payment Solutions"] == "Debit Card"][
    "Share of Total B2B Online Volume"
].iloc[0]
debit_card = float(debit_card.strip("%")) / 100

debit_cost = payment[payment["Current B2B Online Payment Solutions"] == "Debit Card"][
    "Assumed Costs"
].iloc[0]
debit_cost = float(debit_cost.strip("%")) / 100

paypal = payment[payment["Current B2B Online Payment Solutions"] == "Paypal"][
    "Share of Total B2B Online Volume"
].iloc[0]
paypal = float(paypal.strip("%")) / 100

paypal_cost = payment[payment["Current B2B Online Payment Solutions"] == "Paypal"][
    "Assumed Costs"
].iloc[0]
paypal_cost = float(paypal_cost.strip("%")) / 100.0

other = payment[payment["Current B2B Online Payment Solutions"] == "Other"][
    "Share of Total B2B Online Volume"
].iloc[0]
other = float(other.strip("%")) / 100

other_cost = payment[payment["Current B2B Online Payment Solutions"] == "Other"][
    "Assumed Costs"
].iloc[0]
other_cost = float(other_cost.strip("%")) / 100

inhouse_bnpl_bool = payment[
    payment["Current B2B Online Payment Solutions"] == "Inhouse BNPL"
]["Yes/ No"].iloc[0]
external_bnpl_bool = payment[
    payment["Current B2B Online Payment Solutions"] == "External BNPL"
]["Yes/ No"].iloc[0]

# Controls whether a company has a bnpl, which is used to switch modes (acceptance rates vs. conversion rates) 
has_bnpl = (
    inhouse_bnpl_bool or external_bnpl_bool
)  # used to show acceptance rate uplift in df only when the merchant has a bnpl solution


if has_bnpl:
    st.sidebar.markdown("### BNPL Details (if applicable)")
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


if adjust_assumptions:
    st.sidebar.markdown("## Adjust Assumptions Variables")
    adoption_rate = st.sidebar.number_input(
        "Billie share of total B2B online payment solutions (%):",
        value=50.0,
        min_value=0.0,
        max_value=100.0,
        step=5.0,
    )

    adoption_rate = adoption_rate / 100
    billie_acceptance_rate = st.sidebar.number_input(
        "Billie Acceptance Rates (%):", value=90.0, min_value=0.0, max_value=100.0, step=5.0
    )

    billie_acceptance_rate = billie_acceptance_rate / 100
    buyers_not_accepted_for_bnpl_rate = st.sidebar.number_input(
        "Share of Buyers not accepted for BNPL (%):",
        value=50.0,
        min_value=0.0,
        max_value=100.0,
        step=5.0,
    ) 
    
    buyers_not_accepted_for_bnpl_rate = buyers_not_accepted_for_bnpl_rate / 100
    cart_abandon_rate = st.sidebar.number_input(
        "Cart Abandonment Rate (%):", value=30.0, min_value=0.0, max_value=100.0, step=5.0
    )  

    cart_abandon_rate = cart_abandon_rate / 100
    increase_basket_size = st.sidebar.number_input(
        "Increase in Average Basket Size (%):", value=20.0, step=5.0
    ) 

    increase_basket_size = increase_basket_size / 100
    increased_conversion_rate = st.sidebar.number_input(
        "Increase in Conversion Rate (%):", value=15.0, step=5.0
    ) 

    increased_conversion_rate = increased_conversion_rate / 100
    assumption = get_assumptions(
        adoption_rate=adoption_rate,
        billie_acceptance_rate=billie_acceptance_rate,
        buyers_not_accepted_for_bnpl_rate=buyers_not_accepted_for_bnpl_rate,
        cart_abandon_rate=cart_abandon_rate,
        increase_basket_size=increase_basket_size,
        increased_conversion_rate=increased_conversion_rate,
    )

else:
    assumption = get_assumptions()


## financial details
revenue = financial[financial["Metric"] == "B2B Revenues p.a. Online:"]["Value"].iloc[0].replace("€", "")
revenue = float(str(revenue).replace(",", ""))
gross_profit = financial[financial["Metric"] == "Gross Profit Margin:"]["Value"].iloc[0]
gross_profit = float(gross_profit.strip("%")) / 100
avg_basket_size = financial[financial["Metric"] == "Average Basket Size:"][
    "Value"
].iloc[0].replace("€", "")
avg_basket_size = float(str(avg_basket_size).replace(",", ""))

## pricing details & Conversion
fixed_fee = pricing[pricing["Metric"] == "Variable Fee:"]["Value"].iloc[0]
fixed_fee = float(fixed_fee.strip("%")) / 100
transaction_fee = pricing[pricing["Metric"] == "Fixed Fee:"]["Value"].iloc[0].replace("€","")
transaction_fee = float(transaction_fee)
blended_fee = (transaction_fee / avg_basket_size) + fixed_fee

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
    # else revenue * uplift_basket_size * max_share # TODO is needed? 
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
) 

revenue_abs_chg = (
    coalesce(revenue_chg_conversion_rate, 0)
    + coalesce(revenue_chg_acceptance_rate, 0)
    + coalesce(revenue_chg_basket_size, 0)
)

revenue_w_billie = revenue + revenue_abs_chg
gross_profit_amnt_wo_billie = revenue * gross_profit


### PRINT OUT INPUT:
new_raw = {
    "Metric": "Transaction Fee",
    "Value": "{:,.2%}".format(blended_fee),
    "is_high_level": high_level_view,
}
pricing = pricing.append(new_raw, ignore_index=True)


financial_df = financial[financial["is_high_level"] != True].drop(columns=["is_high_level"])

tab1.table(
    set_style(
        financial_df, 
        style =styles,
        )
)

payment = payment[["Current B2B Online Payment Solutions", "Share of Total B2B Online Volume" , "Assumed Costs"]] #

if high_level_view:
    tab1.table(
        set_style(
            payment.drop(
            columns=[
                "Assumed Costs",
            ]
        ),
        style = styles )
    )
else:
    tab1.table(
        set_style(
        payment,
        style = styles)
        )


if len(pricing[pricing["is_high_level"] != True]) > 0:
    tab1.table(set_style(pricing.drop(columns=["is_high_level"]), style=styles))

if adjust_assumptions:
    tab1.table(set_style(assumption, style = styles))
else:
    pass

impact_output_df = pd.DataFrame(
    [
        {
            "Billie Impact": "Higher average basket size",
            "Without Billie": "€{:,.0f}".format(avg_basket_size),
            "With Billie": "€{:,.0f}".format(avg_basket_size_w_billie),
            "Abs. chg": "€{:,.0f}".format(delta_basket_size),
            "Rel. chg (%)": "{:,.2%}".format(uplift_basket_size),
            "Change in Revenues": "€{:,.0f}".format(revenue_chg_basket_size), 
            "viewable": True,
        },
        {
            "Billie Impact": "Acceptance rate increase (existing BNPL)",
            "Without Billie": "{:,.2%}".format(acceptance_rate_wo_bilie),
            "With Billie": "{:,.2%}".format(acceptance_rate_w_billie),
            "Abs. chg": "{:,.2%}".format(acceptance_rate_delta),
            "Rel. chg (%)": "{:,.2%}".format(acceptance_rate_rel_chg),
            "Change in Revenues": "€{:,.0f}".format(revenue_chg_acceptance_rate),
            "viewable": has_bnpl,
        },
        {
            "Billie Impact": "Conversion Rate Increase",
            "Without Billie": "{:,.2%}".format(conversion_rate_wo_billie),
            "With Billie": "{:,.2%}".format(conversion_rate_w_billie),
            "Abs. chg": "{:,.2%}".format(conversion_rate_absolute_chg),
            "Rel. chg (%)": "{:,.2%}".format(conversion_rate_relative_chg),
            "Change in Revenues": "€{:,.0f}".format(revenue_chg_conversion_rate),
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

total_vol_share_w_billie = (
    billie_share
    + inhouse_share_w_billie
    + external_share_w_billie
    + credit_card_share_w_bilie
    + debit_card_share_w_billie
    + paypal_share_w_billie
    + other_share_w_billie
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
    (
        billie_amount * cost_billie
        + inhouse_amount_w_billie * inhouse_cost
        + external_amount_w_billie * external_cost
        + credit_card_amount_w_bilie * credit_cost
        + debit_card_amount_w_billie * debit_cost
        + paypal_amount_w_billie * paypal_cost
        + other_amount_w_billie * other_cost
    )
    / total_amount_w_billie
    if total_amount_w_billie != 0
    else 0
)

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

total_vol_share_wo_billie = (
    inhouse + external + debit_card + credit_card + paypal + other
)

total_vol_amt_wo_billie = (
    inhouse_amount_wo_billie
    + external_amount_wo_billie
    + debit_card_amount_wo_billie
    + credit_card_amount_wo_bilie
    + paypal_amount_wo_billie
    + other_amount_wo_billie
)

total_cost_share_wo_billie = (
    inhouse_cost + external_cost + debit_cost + credit_cost + paypal_cost + other_cost
)

total_cost_amt_wo_billie = (
    inhouse_cost_amnt_wo_billie
    + external_cost_amnt_wo_billie
    + debit_cost_amnt_wo_billie
    + credit_cost_amnt_wo_billie
    + paypal_cost_amnt_wo_billie
    + other_cost_amnt_wo_billie
)

total_vol_amn_w_billie = (
    billie_amount
    + inhouse_amount_w_billie
    + external_amount_w_billie
    + debit_card_amount_w_billie
    + credit_card_amount_w_bilie
    + paypal_amount_w_billie
    + other_amount_w_billie
)

total_cost_share_w_billie = (
    cost_billie
    + inhouse_cost
    + external_cost
    + debit_cost
    + credit_cost
    + paypal_cost
    + other_cost
)

total_cost_amt_w_billie = (
    billie_cost_amnt
    + inhouse_cost_amnt_w_billie
    + external_cost_amnt_w_billie
    + debit_cost_amnt_w_billie
    + credit_cost_amnt_w_billie
    + paypal_cost_amnt_w_billie
    + other_cost_amnt_w_billie
)

payment_output_df = pd.DataFrame(
    [
        {
            "Payment solution": "Billie",
            "Vol. Share w/o Billie": "{:,.0%}".format(0.0),
            "Vol. Amount w/o Billie": "€{:,.0f}".format(0),
            "Costs w/o Billie (%)": "{:,.2%}".format(0),
            "Costs w/o Billie (€)": "€{:,.0f}".format(0),
            "Gross Profits w/o Billie": "€{:,.0f}".format(0),  # todo
            "Vol. Share w/ Billie": "{:,.0%}".format(billie_share),
            "Vol. Amount w/ Billie": "€{:,.0f}".format(billie_amount),
            "Costs w/ Billie (%)": "{:,.2%}".format(cost_billie),
            "Costs w/ Billie (€)": "€{:,.0f}".format(billie_cost_amnt),
            "Gross Profits w/ Billie": "€{:,.0f}".format(
                billie_gross_profit_w_billie
            ),  
        },
        {
            "Payment solution": "Inhouse BNPL",
            "Vol. Share w/o Billie": "{:,.0%}".format(inhouse),
            "Vol. Amount w/o Billie": "€{:,.0f}".format(inhouse_amount_wo_billie),
            "Costs w/o Billie (%)": "{:,.2%}".format(inhouse_cost),
            "Costs w/o Billie (€)": "€{:,.0f}".format(inhouse_cost_amnt_wo_billie),
            "Gross Profits w/o Billie": "€{:,.0f}".format(inhouse_gross_profit_wo_billie),
            "Vol. Share w/ Billie": "{:,.0%}".format(inhouse_share_w_billie),
            "Vol. Amount w/ Billie": "€{:,.0f}".format(inhouse_amount_w_billie),
            "Costs w/ Billie (%)": "{:,.2%}".format(inhouse_cost),
            "Costs w/ Billie (€)": "€{:,.0f}".format(inhouse_cost_amnt_w_billie),
            "Gross Profits w/ Billie": "€{:,.0f}".format(
                inhouse_gross_profit_w_billie
            ),  
        },
        {
            "Payment solution": "External BNPL",
            "Vol. Share w/o Billie": "{:,.0%}".format(external),
            "Vol. Amount w/o Billie": "€{:,.0f}".format(external_amount_wo_billie),
            "Costs w/o Billie (%)": "{:,.2%}".format(external_cost),
            "Costs w/o Billie (€)": "€{:,.0f}".format(external_cost_amnt_wo_billie),
            "Gross Profits w/o Billie": "€{:,.0f}".format(
                external_gross_profit_wo_billie
            ),
            "Vol. Share w/ Billie": "{:,.0%}".format(external_share_w_billie),
            "Vol. Amount w/ Billie": "€{:,.0f}".format(external_amount_w_billie),
            "Costs w/ Billie (%)": "{:,.2%}".format(external_cost),
            "Costs w/ Billie (€)": "€{:,.0f}".format(external_cost_amnt_w_billie),
            "Gross Profits w/ Billie": "€{:,.0f}".format(
                external_gross_profit_w_billie
            ),  
        },
        {
            "Payment solution": "Credit Card",
            "Vol. Share w/o Billie": "{:,.0%}".format(credit_card),
            "Vol. Amount w/o Billie": "€{:,.0f}".format(credit_card_amount_wo_bilie),
            "Costs w/o Billie (%)": "{:,.2%}".format(credit_cost),
            "Costs w/o Billie (€)": "€{:,.0f}".format(credit_cost_amnt_wo_billie),
            "Gross Profits w/o Billie": "€{:,.0f}".format(credit_gross_profit_wo_billie),
            "Vol. Share w/ Billie": "{:,.0%}".format(credit_card_share_w_bilie),
            "Vol. Amount w/ Billie": "€{:,.0f}".format(credit_card_amount_w_bilie),
            "Costs w/ Billie (%)": "{:,.2%}".format(credit_cost),
            "Costs w/ Billie (€)": "€{:,.0f}".format(credit_cost_amnt_w_billie),
            "Gross Profits w/ Billie": "€{:,.0f}".format(
                credit_gross_profit_w_billie
            ),   
        },
        {
            "Payment solution": "Debit Card",
            "Vol. Share w/o Billie": "{:,.0%}".format(debit_card),
            "Vol. Amount w/o Billie": "€{:,.0f}".format(debit_card_amount_wo_billie),
            "Costs w/o Billie (%)": "{:,.2%}".format(debit_cost),
            "Costs w/o Billie (€)": "€{:,.0f}".format(debit_cost_amnt_wo_billie),
            "Gross Profits w/o Billie": "€{:,.0f}".format(debit_gross_profit_wo_billie),
            "Vol. Share w/ Billie": "{:,.0%}".format(debit_card_share_w_billie),
            "Vol. Amount w/ Billie": "€{:,.0f}".format(debit_card_amount_w_billie),
            "Costs w/ Billie (%)": "{:,.2%}".format(debit_cost),
            "Costs w/ Billie (€)": "€{:,.0f}".format(debit_cost_amnt_w_billie),
            "Gross Profits w/ Billie": "€{:,.0f}".format(
                debit_gross_profit_w_billie
            ),  
        },
        {
            "Payment solution": "Paypal",
            "Vol. Share w/o Billie": "{:,.0%}".format(paypal),
            "Vol. Amount w/o Billie": "€{:,.0f}".format(paypal_amount_wo_billie),
            "Costs w/o Billie (%)": "{:,.2%}".format(paypal_cost),
            "Costs w/o Billie (€)": "€{:,.0f}".format(paypal_cost_amnt_wo_billie),
            "Gross Profits w/o Billie": "€{:,.0f}".format(paypal_gross_profit_wo_billie),
            "Vol. Share w/ Billie": "{:,.0%}".format(paypal_share_w_billie),
            "Vol. Amount w/ Billie": "€{:,.0f}".format(paypal_amount_w_billie),
            "Costs w/ Billie (%)": "{:,.2%}".format(paypal_cost),
            "Costs w/ Billie (€)": "€{:,.0f}".format(paypal_cost_amnt_w_billie),
            "Gross Profits w/ Billie": "€{:,.0f}".format(
                paypal_gross_profit_w_billie
            ),  
        },
        {
            "Payment solution": "Other",
            "Vol. Share w/o Billie": "{:,.0%}".format(other),
            "Vol. Amount w/o Billie": "€{:,.0f}".format(other_amount_wo_billie),
            "Costs w/o Billie (%)": "{:,.2%}".format(other_cost),
            "Costs w/o Billie (€)": "€{:,.0f}".format(other_cost_amnt_wo_billie),
            "Gross Profits w/o Billie": "€{:,.0f}".format(other_gross_profit_wo_billie),
            "Vol. Share w/ Billie": "{:,.0%}".format(other_share_w_billie),
            "Vol. Amount w/ Billie": "€{:,.0f}".format(other_amount_w_billie),
            "Costs w/ Billie (%)": "{:,.2%}".format(other_cost),
            "Costs w/ Billie (€)": "€{:,.0f}".format(other_cost_amnt_w_billie),
            "Gross Profits w/ Billie": "€{:,.0f}".format(
                other_gross_profit_w_billie
            ),  
        },
        {
            "Payment solution": "Total",
            "Vol. Share w/o Billie": "{:,.0%}".format(total_vol_share_wo_billie),
            "Vol. Amount w/o Billie": "€{:,.0f}".format(total_vol_amt_wo_billie),
            "Costs w/o Billie (%)": "{:,.2%}".format(wavg_cost_wo_billie),
            "Costs w/o Billie (€)": "€{:,.0f}".format(total_cost_amt_wo_billie),
            "Gross Profits w/o Billie": "€{:,.0f}".format(gross_profit_amnt_wo_billie),
            "Vol. Share w/ Billie": "{:,.0%}".format(total_vol_share_w_billie),
            "Vol. Amount w/ Billie": "€{:,.0f}".format(total_vol_amn_w_billie),
            "Costs w/ Billie (%)": "{:,.2%}".format(wavg_cost_w_billie),
            "Costs w/ Billie (€)": "€{:,.0f}".format(total_cost_amt_w_billie),
            "Gross Profits w/ Billie": "€{:,.0f}".format(total_gross_profit_w_billie),
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

revenue_output_df = pd.DataFrame(
    [
        {
            "Billie Uplift Potential": "B2B Online Revenues p.a.",
            "Without Billie": "€{:,.0f}".format(revenue),
            "With Billie": "€{:,.0f}".format(revenue_w_billie),
            "Abs. chg": "€{:,.0f}".format(revenue_abs_chg),
            "Rel. chg (%)": "{:,.2%}".format(revenue_rel_chg),
            "is_high_level": False,
        },
        {
            "Billie Uplift Potential": "Gross Profits p.a.",
            "Without Billie": "€{:,.0f}".format(gross_profit_amnt_wo_billie),
            "With Billie": "€{:,.0f}".format(total_gross_profit_w_billie),
            "Abs. chg": "€{:,.0f}".format(gross_profit_abs_chg),
            "Rel. chg (%)": "{:,.2%}".format(gross_profit_rel_chg),
            "is_high_level": high_level_view,
        },
    ]
)

if not high_level_view:
    met1, met2, met3, met4 = tab2.columns(4) 
    met1.metric(
        label="Total Revenue Potential with Billie",
        value="€{:,.0f}".format(round(total_amount_w_billie, 0)),
        delta="{:,.2%}".format(amount_rel_chg),  # f"20%",
        delta_color="normal",
    )

    met1.metric(
        label="Total Revenues without Billie",
        value="€{:,.0f}".format(total_amount_wo_billie),
        delta_color="normal",
    )

    met2.metric(
        label="Total Gross Profits with Billie",
        value="€{:,.0f}".format(round(total_gross_profit_w_billie, 0)),  
        delta="{:,.2%}".format(gross_profit_rel_chg),  
    )

    met2.metric(
        label="Total Gross Profits without Billie",
        value="€{:,.0f}".format(total_gross_profit_wo_billie),
        delta_color="normal",
    )

    met3.metric(
        label="Average Basket Size with Billie",
        value="€{:,.0f}".format(round(avg_basket_size_w_billie, 0)),
        delta="{:,.2%}".format(uplift_basket_size),
        delta_color="normal",
        help = f"Average basket size increases with Billie from {avg_basket_size} to {avg_basket_size_w_billie}, the relative increase is {uplift_basket_size}.",
    )

    met3.metric(
        label="Average Basket Size without Billie",
        value="€{:,.0f}".format(round(avg_basket_size, 0)),
    )

    if has_bnpl:
        met4.metric(
            label="Acceptance Rate with Billie",
            value="{:,.2%}".format(acceptance_rate_w_billie),
            delta="{:,.2%}".format(acceptance_rate_rel_chg),
            delta_color="normal",
            help = f"Acceptance Rate increases with Billie from {acceptance_rate_wo_bilie} to {acceptance_rate_w_billie}, the relative increase is {acceptance_rate_rel_chg}.",
            )
        
        met4.metric(
            label="Acceptance Rate without Billie",
            value="{:,.2%}".format(acceptance_rate_wo_bilie),
            )

    else:
        met4.metric(
            label="Average Conversion Rate with Billie",
            value="{:,.2%}".format(conversion_rate_w_billie),
            delta="{:,.2%}".format(conversion_rate_relative_chg),
            delta_color="normal",
            help = f"Average Conversion Rate increases with Billie from {conversion_rate_wo_billie} to {conversion_rate_w_billie}, the relative increase is {conversion_rate_relative_chg}.",
        )

        met4.metric(
            label="Average Conversion Rate W/o Billie",
            value="{:,.2%}".format(conversion_rate_wo_billie),
        )

else: 
    met1, met2, met3 = tab2.columns(3)
    met1.metric(
        label="Total Revenue Potential with Billie",
        value="€{:,.0f}".format(round(total_amount_w_billie, 0)),
        delta="{:,.2%}".format(amount_rel_chg), 
        delta_color="normal",
    )

    met1.metric(
        label="Total Revenues without Billie",
        value="€{:,.0f}".format(total_amount_wo_billie),
        delta_color="normal",
    )

    met2.metric(
        label="Average Basket Size with Billie",
        value="€{:,.0f}".format(round(avg_basket_size_w_billie, 0)),
        delta="{:,.2%}".format(uplift_basket_size),
        delta_color="normal",
        help = f"Average basket size increases with Billie from {avg_basket_size} to {avg_basket_size_w_billie}, the relative increase is {uplift_basket_size}.",
    )

    met2.metric(
        label="Average Basket Size without Billie",
        value="€{:,.0f}".format(round(avg_basket_size, 0)),
    )

    if has_bnpl:
        met3.metric(
            label="Acceptance Rate with Billie",
            value="{:,.2%}".format(acceptance_rate_w_billie),
            delta="{:,.2%}".format(acceptance_rate_rel_chg),
            delta_color="normal",
            help = f"Acceptance Rate increases with Billie from {acceptance_rate_wo_bilie} to {acceptance_rate_w_billie}, the relative increase is {acceptance_rate_rel_chg}.",
            )
        
        met3.metric(
            label="Acceptance Rate without Billie",
            value="{:,.2%}".format(acceptance_rate_wo_bilie),
            )

    else:
        met3.metric(
            label="Average Conversion Rate with Billie",
            value="{:,.2%}".format(conversion_rate_w_billie),
            delta="{:,.2%}".format(conversion_rate_relative_chg),
            delta_color="normal",
            help = f"Average Conversion Rate increases with Billie from {conversion_rate_wo_billie} to {conversion_rate_w_billie}, the relative increase is {conversion_rate_relative_chg}.",
        )

        met3.metric(
            label="Average Conversion Rate without Billie",
            value="{:,.2%}".format(conversion_rate_wo_billie),
        )

impact_filtered_df = impact_output_df[impact_output_df["viewable"] == True].drop(
    columns=["viewable"]
)

####PAYMENT OUTPUT
tab2.table(
    set_style(revenue_output_df[revenue_output_df["is_high_level"] != True].drop(
        columns=["is_high_level"]
    ), style=styles)
)

tab2.table(
    set_style(
        impact_filtered_df,
        style = styles)
        )  #

if high_level_view:
    tab2.table(
        set_style(
            payment_output_df.drop(
            columns=[
                "Costs w/o Billie (%)",
                "Costs w/ Billie (%)",
                "Costs w/o Billie (€)",
                "Costs w/ Billie (€)",
                "Gross Profits w/o Billie",
                "Gross Profits w/ Billie",
            ]
        ),
        style = styles_footer )
    )
else:
    tab2.table(
        set_style(
        payment_output_df,
        style = styles_footer)
        )

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

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 