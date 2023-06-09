"""new"""
import streamlit as st
from PIL import Image
import pandas as pd
import math

import plotly.graph_objects as go


def coalesce(value, replacement):
    if math.isnan(value):
        return replacement
    else:
        return value


def style_dataframe(df):
    # Define the styles for the dataframe
    styles = [
        {
            "selector": "th",
            "props": [("background-color", "#1e1e1e"), ("color", "white")],
        },
        {
            "selector": "th:not(:nth-child(2))",
            "props": [("background-color", "#d8d8d8"), ("color", "black")],
        },
        {
            "selector": "td:fist-child",
            "props": [("background-color", "#d8d8d8"), ("color", "black")],
        },
        {
            "selector": "td:nth-child(2)",
            "props": [("background-color", "#d8d8d8"), ("color", "black")],
        },
        # {
        #     "selector": "td:first-child",
        #     "props": [("background-color", "#7r7r7r"), ("color", "#1e1e1e")],
        # },
        {
            "selector": "td:not(:first-child):not(:nth-child(2))",
            "props": [("background-color", "#f3f3f3"), ("color", "black")],
        },
        ##
        # {
        #     "selector": "td:not(:first-child):not(:nth-child(odd))",
        #     "props": [("background-color", "#6600f5"), ("color", "white")],
        # },
    ]

    # Create a Styler object and apply the styles
    styled_df = df.style.set_table_styles(styles)

    return styled_df


def set_image():

    image = Image.open("billie_new_logo.png")
    width, height = image.size
    new_size = (int(width / 3), int(height / 3))  # Resize to half the original size
    resized_image = image.resize(new_size)

    # Display the image with a custom height using HTML/CSS
    st.image(resized_image, caption="", use_column_width=False )


def get_assumptions(
    adoption_rate=0.5,
    billie_acceptance_rate=0.9,
    buyers_not_accepted_for_bnpl_rate=0.5,
    cart_abandon_rate=0.3,
    increase_basket_size=0.2,
    increased_conversion_rate=0.15,
):
    # adoption_rate = adoption_rate
    adoption_rate_formatted = "{:,.0%}".format(adoption_rate)

    # billie_acceptance_rate = billie_acceptance_rate
    billie_acceptance_rate_formatted = "{:,.0%}".format(billie_acceptance_rate)

    # buyers_not_accepted_for_bnpl_rate = buyers_not_accepted_for_bnpl_rate
    buyers_not_accepted_for_bnpl_rate_formatted = "{:,.0%}".format(
        buyers_not_accepted_for_bnpl_rate
    )

    # cart_abandon_rate = cart_abandon_rate
    cart_abandon_rate_formatted = "{:,.0%}".format(cart_abandon_rate)

    increase_basket_size = increase_basket_size
    increase_basket_size_formatted = "{:,.0%}".format(increase_basket_size)

    # increased_conversion_rate = 0.15
    increased_conversion_rate_formatted = "{:,.0%}".format(increased_conversion_rate)

    assumption_df = pd.DataFrame(
        [
            {
                "Assumptions": "% Billie of total B2B online payment solutions",
                "Value": adoption_rate_formatted,
            },
            {
                "Assumptions": "Billie acceptance rates:",
                "Value": billie_acceptance_rate_formatted,
            },
            {
                "Assumptions": "Buyers not accepted for BNPL:",
                "Value": buyers_not_accepted_for_bnpl_rate_formatted,
            },
            {
                "Assumptions": "Cart abandonment rate:",
                "Value": cart_abandon_rate_formatted,
            },
            {
                "Assumptions": "Increase in average basket size:",
                "Value": increase_basket_size_formatted,
            },
            {
                "Assumptions": "Increase in conversion rate:",
                "Value": increased_conversion_rate_formatted,
            },
        ]
    )
    assumption_df = assumption_df.reset_index(drop=True)
    return assumption_df


def waterfall_fig(
    is_high_level=False,
    revenue=0,
    revenue_chg_basket_size=0,
    revenue_chg_acceptance_rate=0,
    revenue_chg_conversion_rate=0,
    revenue_w_billie=0,
    has_bnpl=True,
):

    if not is_high_level:
        fig = go.Figure(
            go.Waterfall(
                name="20",
                orientation="v",
                x=[
                    "Current B2B Online Revenues",
                    "Uplift potential - Higher basket size",
                    "Uplift potential - Higher Acceptance rates",
                    # "Uplift potential - Higher conversion rates",
                    "B2B Online Revenues Potential with Billie",
                ]
                if has_bnpl
                else [
                    "Current B2B Online Revenues",
                    "Uplift potential - Higher basket size",
                    # "Uplift potential - Higher Acceptance rates",
                    "Uplift potential - Higher conversion rates",
                    "B2B Online Revenues Potential with Billie",
                ],
                textposition="inside",
                measure=[
                    "absolute",
                    "relative",
                    "relative",
                    # "relative",
                    "total",
                ]
                if has_bnpl
                else [
                    "absolute",
                    "relative",
                    "relative",
                    # "relative",
                    "total",
                ],  # TODO no need for if statement if that's the logic that Sales Team wants
                # text = ["NET_FEE_RATE", "NET_DEFAULT_RATE", "MONTHLY_MERCHANT_REFI_COST", "INSURANCE_COST", "SCORING_COST_MARGIN", "TRANSACTION_BANKING_COST"],
                text=[
                    revenue,
                    revenue_chg_basket_size,
                    revenue_chg_acceptance_rate,  # .round(4)*100,
                    # revenue_chg_conversion_rate,
                    revenue_w_billie,
                ]
                if has_bnpl
                else [
                    revenue,
                    revenue_chg_basket_size,
                    # revenue_chg_acceptance_rate,  # .round(4)*100,
                    revenue_chg_conversion_rate,
                    revenue_w_billie,
                ],
                y=[
                    revenue,
                    revenue_chg_basket_size,
                    revenue_chg_acceptance_rate,  # .round(4)*100,
                    # revenue_chg_conversion_rate,
                    revenue_w_billie,
                ]
                if has_bnpl
                else [
                    revenue,
                    revenue_chg_basket_size,
                    # revenue_chg_acceptance_rate,  # .round(4)*100,
                    revenue_chg_conversion_rate,
                    revenue_w_billie,
                ],
                base=0.0,
                decreasing={
                    "marker": {"color": "Maroon"}
                },  # , "line":{"color":"red", "width":2}
                increasing={"marker": {"color": "#6600f5"}},
                totals={"marker": {"color":"#7f7f7f"}} #  "deep sky blue"
                # connector = {"line":{"color":"rgb(63, 63, 63)"}},
                # connector = {"visible": False,
                #            "line":{"color":"rgb(63, 63, 63)"}
                #            },
            )
        )

        fig.update_layout(
            title="Billie Uplift Potential",
            showlegend=False,
            margin=dict(l=30, r=30, t=30, b=30),
        )
        fig.update_traces(texttemplate="%{text:,}")
        return fig
    else:
        fig = go.Figure(
            go.Waterfall(
                name="20",
                orientation="v",
                x=[
                    "Current B2B Online Revenues",
                    "Uplift potential - Higher basket size",
                    "B2B Online Revenues Potential with Billie",
                ],
                textposition="outside",
                measure=[
                    "relative",
                    "relative",
                    "total",
                ],
                # text = ["NET_FEE_RATE", "NET_DEFAULT_RATE", "MONTHLY_MERCHANT_REFI_COST", "INSURANCE_COST", "SCORING_COST_MARGIN", "TRANSACTION_BANKING_COST"],
                text=[
                    revenue,
                    revenue_chg_basket_size,
                    revenue_w_billie,
                ],
                y=[
                    revenue,
                    revenue_chg_basket_size,
                    revenue_w_billie,
                ],
                base=0.0,
                decreasing={
                    "marker": {"color": "Maroon"}
                },  # , "line":{"color":"red", "width":2}
                increasing={"marker": {"color": "Teal"}},
                totals={"marker": {"color": "deep sky blue"}}
                # connector = {"line":{"color":"rgb(63, 63, 63)"}},
                # connector = {"visible": False,
                #            "line":{"color":"rgb(63, 63, 63)"}
                #            },
            )
        )

        fig.update_layout(title="Billie Uplift Potential", showlegend=False)
        fig.update_traces(texttemplate="%{text:,}")
        return fig
    # fig.layout.yaxis.tickformat = ",.2%"
#  #D8D8D8

css = """
    <style>
            thead tr th:first-child {
                    display:none
            }
            tbody th {
                display:none
            }
    </style>
"""
