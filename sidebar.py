import streamlit as st
import pandas as pd

EXCLUDED_KEYS = {
    "inhouse_bool",
    "external_bool",
}


def check_completeness():
    # function used for callbacks in number_input, that checks the validity of inputs,
    # and make sure that the values of all payments sum up to 100%
    tot_sum = 0
    for k, v in st.session_state.items():
        if k not in EXCLUDED_KEYS:
            tot_sum = tot_sum + v

    if tot_sum > 100:
        st.session_state.other -= tot_sum - 100
        if st.session_state.other < 0:
            st.warning("All payment methods must add up to 100%.")
            st.session_state.other = 0
            # st.stop()
            # st.success('Thank you for inputting a name.')
    elif tot_sum < 100:
        st.session_state.other += 100 - tot_sum
        if st.session_state.other > 100:
            st.warning("All payment methods must add up to 100%")
            st.session_state.other = 100
    else:
        pass


def check_other():
    # function used for callbacks in number_input, that checks the validity of inputs,
    # and make sure that the values of all payments sum up to 100%
    # used in combination with check_completeness for others
    tot_sum = 0
    for k, v in st.session_state.items():
        if k not in EXCLUDED_KEYS:
            tot_sum = tot_sum + v

    if tot_sum > 100:
        st.warning("All payment methods must add up to 100%.")
    elif tot_sum < 100:
        st.warning("All payment methods must add up to 100%.")


def inhouse_callback():
    # makes sure that whennever the inhouse BNPL is checked, the value should be at least 1
    if st.session_state.inhouse == 0.0:
        st.session_state.inhouse += 1.0
        tot_sum = 0
        for k, v in st.session_state.items():
            if k not in EXCLUDED_KEYS:
                tot_sum = tot_sum + v
        if tot_sum > 100:
            st.session_state.other -= tot_sum - 100
        if st.session_state.other < 0:
            st.warning("All payment methods must add up to 100%.")
            st.session_state.other = 0
    elif st.session_state.inhouse == 1.0:
        st.session_state.inhouse -= 1.0
        st.session_state.other += 1
    elif st.session_state.inhouse > 1.0:

        st.session_state.other += st.session_state.inhouse
        st.session_state.inhouse = 0


def external_callback():
    # makes sure that whennever the external BNPL is checked, the value should be at least 1
    if st.session_state.external == 0.0:
        st.session_state.external += 1.0
        tot_sum = 0
        for k, v in st.session_state.items():
            if k not in EXCLUDED_KEYS:
                tot_sum = tot_sum + v
        if tot_sum > 100:
            st.session_state.other -= tot_sum - 100
        if st.session_state.other < 0:
            st.warning("All payment methods must add up to 100%.")
            st.session_state.other = 0
    elif st.session_state.external == 1.0:
        st.session_state.external -= 1.0
        st.session_state.other += 1
    elif st.session_state.external > 1.0:

        st.session_state.other += st.session_state.external
        st.session_state.external = 0


def billie_pricing(high_level=False):
    if not high_level:
        st.sidebar.markdown("### Billie Pricing")
        # -- Set time by GPS or event
        # avg_basket = st.sidebar.slider("Average Acceptance Rate: (in %)", 0.0, 1.0, 0.05)
        fixed_fee = st.sidebar.number_input(
            "Variable Fee (in %):", value=1.69, step=0.01
        )
        fixed_fee_formatted = "{:,.2%}".format(fixed_fee / 100)

        # display the inputs
        transaction_fee = st.sidebar.number_input(
            "Fixed Fee (in €):", value=0.5, step=0.1
        )
        transaction_fee_formatted = "€{:,.2f}".format(transaction_fee)
    else:
        fixed_fee = 0.0169
        fixed_fee_formatted = "{:,.2%}".format(fixed_fee / 100)
        transaction_fee = 0.5
        transaction_fee_formatted = "{:,.2f}".format(transaction_fee)

    # blended_fee = (transaction_fee / avg_basket) * 100 + fixed_fee
    # blended_fee_formatted = "{:,.2%}".format(blended_fee / 100)

    pricing_df = pd.DataFrame(
        [
            {
                "Metric": "Variable Fee:",
                "Value": fixed_fee_formatted,
                "is_high_level": high_level,
            },
            {
                "Metric": "Fixed Fee:",
                "Value": transaction_fee_formatted,
                "is_high_level": high_level,
            },
            # {"Metric": "Blended Fee", "value": blended_fee_formatted},
        ]
    )
    return pricing_df


def sidebar_financial(high_level=False):

    st.sidebar.markdown("## Select Input Variables - Merchant")
    st.sidebar.markdown("### Key Financials")

    b2b_rev = st.sidebar.number_input(
        "B2B Online Revenues p.a. (in €):",
        value=12_000_000,
        #help="Add Info",
        step=500_000,
        format="%d",  # "%0.2f"
    )
    b2b_rev_formatted = "€{:,.0f}".format(b2b_rev)

    if not high_level:
        gross_profit = st.sidebar.number_input(
            "Gross Profit Margin (in %):", value=20.0, step=5.0
        )
    else:
        gross_profit = 20.0
    gross_profit_formatted = "{:,.0%}".format(gross_profit / 100)
    #st.sidebar.markdown("### Order details - B2B Online")
    # -- Set time by GPS or event

    avg_basket = st.sidebar.number_input(
        "Average Basket Size (in €):", value=500, step=100
    )
    avg_basket_formatted = "€{:,.0f}".format(avg_basket)#

    financial_df = pd.DataFrame(
        [
            {
                "Metric": "B2B Revenues p.a. Online:",
                "Value": b2b_rev_formatted,
                "is_high_level": False,
            },
            {
                "Metric": "Gross Profit Margin:",
                "Value": gross_profit_formatted,
                "is_high_level": high_level,
            },
            {
                "Metric": "Average Basket Size:",
                "Value": avg_basket_formatted,
                "is_high_level": False,
            },
            # {"Metric": "Average Acceptance Rate:", "value": avg_acceptance_formatted},
        ]
    )
    financial_df = financial_df.reset_index(drop=True)

    return financial_df  # st.dataframe(financial_df, use_container_width=True)


def payment_info(high_level=False):

    ########  Payment detail input ########
    st.sidebar.markdown("### B2B Payment Details - Online")
    # -- Set time by GPS or event
    # avg_basket = st.sidebar.slider("Average Acceptance Rate: (in %)", 0.0, 1.0, 0.05)
    c1, c2, c3 = st.sidebar.columns(3)
    c1.write("Payment Method:")
    c2.write("Share of Checkout (in %):")
    if not high_level:
        c3.write("Assumed Cost (in %):")

    
    col1, col2, col3 = st.sidebar.columns(3)

    percent_inhouse = col2.number_input(
        label="1-Share of checkout (in %):",
        label_visibility="collapsed",
        value=0.0,
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        format="%0d",
        on_change=check_completeness,
        key="inhouse",
    )
    bool_inhouse = col1.checkbox(
        "Inhouse BNPL",
        value=True if percent_inhouse > 0 else False,
        on_change=inhouse_callback,
        key="inhouse_bool",
    )
    percent_inhouse_formatted = "{:,.0%}".format(percent_inhouse / 100)
    if not high_level:
        cost_inhouse = col3.number_input("1-Assumed Costs:",label_visibility="collapsed", value=0.0, step=1.0)
    else:
        cost_inhouse = 0.0
    cost_inhouse_formatted = "{:,.2%}".format(cost_inhouse / 100)
    # display the inputs
    # st.write("Boolean input:", bool_input)
    # st.write("Percentage input:", percent_input, "%")
    ext, ext_share, ext_cost = st.sidebar.columns(3)

    percent_ext = ext_share.number_input(
        "2-Share of checkout (in %):",
        label_visibility="collapsed",
        value=0.0,
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        format="%0d",
        on_change=check_completeness,
        key="external",
    )
    bool_ext = ext.checkbox(
        "External BNPL",
        value=True if percent_ext > 0 else False,
        on_change=external_callback,
        key="external_bool",
    )
    percent_ext_formatted = "{:,.0%}".format(percent_ext / 100)
    if not high_level:
        cost_ext = ext_cost.number_input("2-Assumed Costs:", label_visibility="collapsed",value=0.0, step=1.0)
    else:
        cost_ext = 0.0

    cost_ext_formatted = "{:,.2%}".format(cost_ext / 100)

    cred, cred_share, cred_cost = st.sidebar.columns(3)

    percent_credit = cred_share.number_input(
        "3-Share of checkout (in %):",
        label_visibility="collapsed",
        value=0.0,
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        format="%0d",
        on_change=check_completeness,
        key="credit",
    )
    bool_credit = cred.checkbox(
        "Credit Card", value=True if percent_credit > 0 else False
    )
    percent_credit_formatted = "{:,.0%}".format(percent_credit / 100)
    if not high_level:
        cost_credit = cred_cost.number_input("3-Assumed Costs:", label_visibility="collapsed",value=0.0, step=1.0)
    else:
        cost_credit = 0.0

    cost_credit_formatted = "{:,.2%}".format(cost_credit / 100)

    deb, deb_share, deb_cost = st.sidebar.columns(3)

    percent_debit = deb_share.number_input(
        "4-Share of checkout (in %):",
        label_visibility="collapsed",
        value=50.0,
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        format="%0d",
        on_change=check_completeness,
        key="debit",
    )
    bool_debit = deb.checkbox(
        "Direct Debit", value=True if percent_debit > 0 else False
    )
    percent_debit_formatted = "{:,.0%}".format(percent_debit / 100)
    if not high_level:
        cost_debit = deb_cost.number_input("4-Assumed Costs:",label_visibility="collapsed", value=0.2, step=1.0)
    else:
        cost_debit = 0.0

    cost_debit_formatted = "{:,.2%}".format(cost_debit / 100)

    pal, pal_share, pal_cost = st.sidebar.columns(3)

    percent_paypal = pal_share.number_input(
        "5-Share of checkout (in %):",
        label_visibility="collapsed",
        value=30.0,
        step=1.0,
        min_value=0.0,
        max_value=100.0,
        format="%0d",
        on_change=check_completeness,
        key="paypal",
    )
    bool_paypal = pal.checkbox("PayPal", value=True if percent_paypal > 0 else False)
    percent_paypal_formatted = "{:,.0%}".format(percent_paypal / 100)
    if not high_level:
        cost_paypal = pal_cost.number_input(
            "5-Assumed Costs:",label_visibility="collapsed", value=1.5, min_value=0.0, max_value=100.0, step=1.0
        )
    else:
        cost_paypal = 0.0

    cost_paypal_formatted = "{:,.2%}".format(cost_paypal / 100)

    oher, other_share, other_cost = st.sidebar.columns(3)

    percent_other = other_share.number_input(
        "6-Share of checkout (in %):",
        label_visibility="collapsed",
        value=20.0,
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        format="%0d",
        on_change=check_other,
        key="other",
    )
    bool_other = oher.checkbox(
        "Other", value=True if percent_other > 0 else False
    )
    percent_other_formatted = "{:,.0%}".format(percent_other / 100)
    if not high_level:
        cost_other = other_cost.number_input("6-Assumed Costs:",label_visibility="collapsed", value=0.0, step=1.0)
    else:
        cost_other = 0.0

    cost_other_formatted = "{:,.2%}".format(cost_other / 100)
    # check box to show/hide a dataframe
    payment_df = pd.DataFrame(
        [
            {
                "Current B2B Online Payment Solutions": "Inhouse BNPL",
                "Yes/ No": bool_inhouse,
                "Share of Total B2B Online Volume": percent_inhouse_formatted,
                "Assumed Costs": cost_inhouse_formatted,
            },
            {
                "Current B2B Online Payment Solutions": "External BNPL",
                "Yes/ No": bool_ext,
                "Share of Total B2B Online Volume": percent_ext_formatted,
                "Assumed Costs": cost_ext_formatted,
            },
            {
                "Current B2B Online Payment Solutions": "Credit Card",
                "Yes/ No": bool_credit,
                "Share of Total B2B Online Volume": percent_credit_formatted,
                "Assumed Costs": cost_credit_formatted,
            },
            {
                "Current B2B Online Payment Solutions": "Debit Card",
                "Yes/ No": bool_debit,
                "Share of Total B2B Online Volume": percent_debit_formatted,
                "Assumed Costs": cost_debit_formatted,
            },
            {
                "Current B2B Online Payment Solutions": "Paypal",
                "Yes/ No": bool_paypal,
                "Share of Total B2B Online Volume": percent_paypal_formatted,
                "Assumed Costs": cost_paypal_formatted,
            },
            {
                "Current B2B Online Payment Solutions": "Other",
                "Yes/ No": bool_other,
                "Share of Total B2B Online Volume": percent_other_formatted,
                "Assumed Costs": cost_other_formatted,
            },
        ]
    )

    ###-----------

    ###-----------
    return payment_df
