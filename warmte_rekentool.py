#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 21:29:31 2024

@author: maxpronk
"""
import os
import streamlit as st
import pandas as pd
import numpy as np

st.image('logo.png', width=200)

st.title('Rekentool Huibertstroom')

# Apply custom CSS for wider columns, lines between sections, larger titles, and black table lines
st.markdown("""
    <style>
    body:before {
        content: "";
        display: block;
        width: 100%;
        height: 20px;
        background-color: lightblue;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
    }
    body:after {
        content: "";
        display: block;
        width: 100%;
        height: 20px;
        background-color: darkblue;
        position: fixed;
        bottom: 0;
        left: 0;
        z-index: 9999;
    }
    .stSlider label, .stRadio label, .stMultiSelect label {
        font-size: 1.2rem;
    }
    .stSlider {
        margin-bottom: 20px;
    }
    .stRadio, .stMultiSelect {
        margin-bottom: 20px;
    }
    .stTable {
        margin-top: 20px;
        border-top: 2px solid black;
        padding-top: 20px;
        border-collapse: collapse;
    }
    .stTable th, .stTable td {
        border: 1px solid black !important;
    }
    .css-1lcbmhc {
        flex: 1.5 !important;
        max-width: 1.5 !important;
    }
    .full-width-line {
        border-top: 2px solid black;
        margin: 20px 0;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 150%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

# Create two columns with increased width
col1, col2 = st.columns([1.5, 1.5])

# Sliders in the first column
with col1:
    slider_gasverbruik = st.slider("Totaal verbruik gas (in m3)", min_value=1, max_value=5000, step=1)
    slider_gastarief = st.slider("Totale jaarkosten gasverbruik (in euro)", min_value=0, max_value=7500, step=5)
    
    # Calculate the product of slider_gasverbruik and slider_gastarief
    kosten_value = slider_gastarief

# Calculate the value for 'Situatie warmtenet' under 'Totale kosten'
calculated_value = (slider_gasverbruik * 0.03517) * 45.2
calculated_value = round(calculated_value, 2)

# Radio buttons and conditional multiselect in the second column
with col2:
    selectie_koken = st.radio("Waar kookt u op?",
                              ["Gas", "Elektrisch"])
    selectie_woning = st.radio("In wat voor een huis woont u?",
                               ["Koop woning", "Huur woning"])

# Add a full-width black line below the multiselect widget or radio button if multiselect is not shown
st.markdown("<hr class='full-width-line'>", unsafe_allow_html=True)

# Define data for the table
data = {
    'Aspect': ['Eenmalig', 'Totale kosten', 'Ketel / Afleverset', 'Elektrisch koken', 'Totaal', 'Verschil'],
    'Huidige situatie': ['-', '-', '-', '-', '-', '-'],
    'Situatie warmtenet': ['-', '-', '-', '-', '-', '-']
}

# Create DataFrame from the data
df_results = pd.DataFrame(data)

# Update selected values based on user input
df_results.loc[df_results['Aspect'] == 'Eenmalig', 'Huidige situatie'] = 'N.V.T.'
df_results.loc[df_results['Aspect'] == 'Totale kosten', 'Huidige situatie'] = kosten_value
df_results.loc[df_results['Aspect'] == 'Ketel / Afleverset', 'Huidige situatie'] = 30
df_results.loc[df_results['Aspect'] == 'Elektrisch koken', 'Huidige situatie'] = 'N.V.T'
df_results.loc[df_results['Aspect'] == 'Totaal', 'Huidige situatie'] = 0
df_results.loc[df_results['Aspect'] == 'Verschil', 'Huidige situatie'] = ''  # Empty cell

# Update selected values based on user input
df_results.loc[df_results['Aspect'] == 'Eenmalig', 'Situatie warmtenet'] = 0 #nog te bepalen
df_results.loc[df_results['Aspect'] == 'Totale kosten', 'Situatie warmtenet'] = calculated_value # GJ price
df_results.loc[df_results['Aspect'] == 'Ketel / Afleverset', 'Situatie warmtenet'] = 0
df_results.loc[df_results['Aspect'] == 'Elektrisch koken', 'Situatie warmtenet'] = 10
df_results.loc[df_results['Aspect'] == 'Totaal', 'Situatie warmtenet'] = 0
df_results.loc[df_results['Aspect'] == 'Verschil', 'Situatie warmtenet'] = ''  # Empty cell

# Calculate the sum for 'Totaal', 'Huidige situatie'
sum_current_situation = (
    df_results.loc[df_results['Aspect'] != 'Verschil', 'Huidige situatie']
    .dropna()  # Drop NaN values
    .apply(lambda x: float(x) if str(x).replace('.', '', 1).replace('-', '', 1).isdigit() else 0)  # Convert to float if it's a valid number
    .sum()
)

# Add 'Totale kosten', 'Huidige situatie' to the sum
#sum_current_situation += float(df_results[df_results['Aspect'] == 'Totale kosten']['Huidige situatie'].values[0].replace('€', ''))

# Update the 'Totaal', 'Huidige situatie' row in the DataFrame
df_results.loc[df_results['Aspect'] == 'Totaal', 'Huidige situatie'] = round(sum_current_situation, 2)

# Calculate the sum for 'Totaal', 'Situatie warmtenet'
sum_situatie_warmtenet = (
    df_results.loc[df_results['Aspect'] != 'Verschil', 'Situatie warmtenet']
    .dropna()  # Drop NaN values
    .apply(lambda x: float(x) if str(x).replace('.', '', 1).replace('-', '', 1).isdigit() else 0)  # Convert to float if it's a valid number
    .sum()
)

# Add 'Totale kosten', 'Situatie warmtenet' to the sum
# sum_situatie_warmtenet += float(df_results[df_results['Aspect'] == 'Totale kosten']['Situatie warmtenet'].values[0])

# Update the 'Totaal', 'Situatie warmtenet' row in the DataFrame
df_results.loc[df_results['Aspect'] == 'Totaal', 'Situatie warmtenet'] = round(sum_situatie_warmtenet, 2)

# Calculate the difference for 'Verschil' row
verschil_value = round(sum_situatie_warmtenet - sum_current_situation, 2)

# Update the 'Verschil' row in the DataFrame
df_results.loc[df_results['Aspect'] == 'Verschil', 'Situatie warmtenet'] = round(verschil_value, 2)

# Add a '+' sign and make the 'Verschil' value bold black if it's positive
if verschil_value > 0:
    df_results.loc[df_results['Aspect'] == 'Verschil', 'Situatie warmtenet'] = f'+{verschil_value}'
    df_results.loc[df_results['Aspect'] == 'Verschil', 'Aspect'] = 'Verschil'

# Define the cells where '€' should be added
cells_to_add_euro = [
    ('Totale kosten', 'Huidige situatie'),
    ('Ketel / Afleverset', 'Huidige situatie'),
    ('Totaal', 'Huidige situatie'),
    ('Eenmalig', 'Situatie warmtenet'),
    ('Variabel', 'Situatie warmtenet'),
    ('Totale kosten', 'Situatie warmtenet'),
    ('Ketel / Afleverset', 'Situatie warmtenet'),
    ('Elektrisch koken', 'Situatie warmtenet'),
    ('Totaal', 'Situatie warmtenet'),
    ('Verschil', 'Situatie warmtenet')
]

# Add '€' to the selected cells
for cell in cells_to_add_euro:
    df_results.loc[df_results['Aspect'] == cell[0], cell[1]] = df_results.loc[df_results['Aspect'] == cell[0], cell[1]].astype(str) + ' €'

# Display the table below the full-width line
st.subheader("Kosten overzicht per maand")
st.table(df_results.set_index('Aspect'))

#st.write("You selected:", options)

# Deze command in de Python Terminal runnen, niet via dit script. Path naar het script ook aanpassen naar je eigen mappen
#streamlit run /Users/maxpronk//Python/Rekentool/Streamlit/Nieuw/warmte_rekentool.py