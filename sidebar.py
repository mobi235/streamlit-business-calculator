import streamlit as st
import pandas as pd


def sidebar_financial():

    st.sidebar.markdown("## Select Input Variables - Merchant")
    st.sidebar.markdown("### Key Financials")

    b2b_rev = st.sidebar.number_input(
        "B2B revenues p.a. Online: (in €)", value=12000000, step=500000
    )
    b2b_rev_formatted = "{:,.2f}".format(b2b_rev)

    gross_profit = st.sidebar.number_input(
        "Gross profit margin: (in %)", value=20.0, step=5.0
    )
    gross_profit_formatted = "{:,.1%}".format(gross_profit / 100)
    st.sidebar.markdown("### Order details - B2B Online")
    # -- Set time by GPS or event

    avg_basket = st.sidebar.number_input(
        "Average Basket Size: (in €)", value=500, step=100
    )
    avg_basket_formatted = "{:,.2f}".format(avg_basket)
    # display the float value entered by the user
    # st.write("You entered:", b2b_rev)

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

    financial_df = pd.DataFrame(
        [
            {"Metric": "B2B revenues p.a. Online:", "value": b2b_rev_formatted},
            {"Metric": "Gross profit margin:", "value": gross_profit_formatted},
            {"Metric": "Average Basket Size:", "value": avg_basket_formatted},
            {"Metric": "Average Acceptance Rate:", "value": avg_acceptance_formatted},
        ]
    )
    financial_df = financial_df.reset_index(drop=True)
    ######  Billie pricing ########
    st.sidebar.markdown("### Billie pricing")
    # -- Set time by GPS or event
    # avg_basket = st.sidebar.slider("Average Acceptance Rate: (in %)", 0.0, 1.0, 0.05)
    fixed_fee = st.sidebar.number_input("Fixed Fee: (in %)", value=1.69, step=0.01)
    fixed_fee_formatted = "{:,.1%}".format(fixed_fee / 100)

    # display the inputs
    transaction_fee = st.sidebar.number_input(
        "Transaction Fee: (in €)", value=0.5, step=0.1
    )
    transaction_fee_formatted = "{:,.2f}".format(transaction_fee)

    blended_fee = (transaction_fee / avg_basket) * 100 + fixed_fee
    blended_fee_formatted = "{:,.2%}".format(blended_fee / 100)

    pricing_df = pd.DataFrame(
        [
            {"Metric": "Fixed Fee:", "value": fixed_fee_formatted},
            {"Metric": "Transaction Fee:", "value": transaction_fee_formatted},
            {"Metric": "Blended Fee", "value": blended_fee_formatted},
        ]
    )

    return (
        financial_df,
        pricing_df,
    )  # st.dataframe(financial_df, use_container_width=True)


def on_number_input_changed(new_value):
    if new_value > 0:
        checkbox_value = True
        checkbox.checkbox(checkbox_value)
    else:
        checkbox_value = False
        checkbox.checkbox(checkbox_value)


def payment_info():

    ########  Payment detail input ########
    st.sidebar.markdown("### B2B payment details - Online")
    # -- Set time by GPS or event
    # avg_basket = st.sidebar.slider("Average Acceptance Rate: (in %)", 0.0, 1.0, 0.05)
    col1, col2, col3 = st.sidebar.columns(3)

    percent_inhouse = col2.number_input("1-Share of Vol. (%):", value=0.0, step=1.0)
    bool_inhouse = col1.checkbox(
        "Inhouse BNPL", value=True if percent_inhouse > 0 else False
    )
    percent_inhouse_formatted = "{:,.1%}".format(percent_inhouse / 100)
    cost_inhouse = col3.number_input("1-Assumed Costs:", value=0.0, step=1.0)
    cost_inhouse_formatted = "{:,.1%}".format(cost_inhouse / 100)
    # display the inputs
    # st.write("Boolean input:", bool_input)
    # st.write("Percentage input:", percent_input, "%")
    ext, ext_share, ext_cost = st.sidebar.columns(3)

    percent_ext = ext_share.number_input("2-Share of Vol. (%):", value=0.0, step=1.0)
    bool_ext = ext.checkbox("External BNPL", value=True if percent_ext > 0 else False)
    percent_ext_formatted = "{:,.1%}".format(percent_ext / 100)
    cost_ext = ext_cost.number_input("2-Assumed Costs:", value=0.0, step=1.0)
    cost_ext_formatted = "{:,.1%}".format(cost_ext / 100)

    cred, cred_share, cred_cost = st.sidebar.columns(3)

    percent_credit = cred_share.number_input(
        "3-Share of Vol. (%):", value=0.0, step=1.0
    )
    bool_credit = cred.checkbox(
        "Credit Card", value=True if percent_credit > 0 else False
    )
    percent_credit_formatted = "{:,.1%}".format(percent_credit / 100)
    cost_credit = cred_cost.number_input("3-Assumed Costs:", value=0.0, step=1.0)
    cost_credit_formatted = "{:,.1%}".format(cost_credit / 100)

    deb, deb_share, deb_cost = st.sidebar.columns(3)

    percent_debit = deb_share.number_input("4-Share of Vol. (%):", value=50.0, step=1.0)
    bool_debit = deb.checkbox(
        "Direct Debit", value=True if percent_debit > 0 else False
    )
    percent_debit_formatted = "{:,.1%}".format(percent_debit / 100)
    cost_debit = deb_cost.number_input("4-Assumed Costs:", value=0.2, step=1.0)
    cost_debit_formatted = "{:,.1%}".format(cost_debit / 100)

    pal, pal_share, pal_cost = st.sidebar.columns(3)

    percent_paypal = pal_share.number_input(
        "5-Share of Vol. (%):", value=30.0, step=1.0
    )
    bool_paypal = pal.checkbox("PayPal", value=True if percent_paypal > 0 else False)
    percent_paypal_formatted = "{:,.1%}".format(percent_paypal / 100)
    cost_paypal = pal_cost.number_input("5-Assumed Costs:", value=1.5, step=1.0)
    cost_paypal_formatted = "{:,.1%}".format(cost_paypal / 100)

    oher, other_share, other_cost = st.sidebar.columns(3)

    percent_other = other_share.number_input(
        "6-Share of Vol. (%):", value=20.0, step=1.0
    )
    bool_other = oher.checkbox(
        "Other (please specify)", value=True if percent_other > 0 else False
    )
    percent_other_formatted = "{:,.1%}".format(percent_other / 100)
    cost_other = other_cost.number_input("6-Assumed Costs:", value=0.0, step=1.0)
    cost_other_formatted = "{:,.1%}".format(cost_other / 100)
    # check box to show/hide a dataframe
    payment_df = pd.DataFrame(
        [
            {
                "Current B2B online payment solutions": "Inhouse BNPL",
                "Yes/ No": bool_inhouse,
                "Share of total B2B online volume": percent_inhouse_formatted,
                "Assumed costs": cost_inhouse_formatted,
            },
            {
                "Current B2B online payment solutions": "External BNPL",
                "Yes/ No": bool_ext,
                "Share of total B2B online volume": percent_ext_formatted,
                "Assumed costs": cost_ext_formatted,
            },
            {
                "Current B2B online payment solutions": "Credit Card",
                "Yes/ No": bool_credit,
                "Share of total B2B online volume": percent_credit_formatted,
                "Assumed costs": cost_credit_formatted,
            },
            {
                "Current B2B online payment solutions": "Debit Card",
                "Yes/ No": bool_debit,
                "Share of total B2B online volume": percent_debit_formatted,
                "Assumed costs": cost_debit_formatted,
            },
            {
                "Current B2B online payment solutions": "Paypal",
                "Yes/ No": bool_paypal,
                "Share of total B2B online volume": percent_paypal_formatted,
                "Assumed costs": cost_paypal_formatted,
            },
            {
                "Current B2B online payment solutions": "Other",
                "Yes/ No": bool_other,
                "Share of total B2B online volume": percent_other_formatted,
                "Assumed costs": cost_other_formatted,
            },
        ]
    )

    ###-----------

    ###-----------
    return payment_df
