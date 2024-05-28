#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 21:29:31 2024

@author: maxpronk
"""

import streamlit as st
import pandas as pd
import numpy as py

st.title('Rekentool Huibertstroom')

slider_gasverbruik = st.slider("Gasverbruik per jaar", min_value = 10, max_value = 3500, step = 10)

slider_gastarief = st.slider("Kosten gas per iets?", min_value = 0.5, max_value = 5.0, step = 0.05)

slider_vastrechtgas = st.slider("Vastrechtgas", min_value = 50, max_value = 500, step = 2)

selectie_isoleren = st.radio("Bent u van plan te gaan isoleren?", 
                             ["Ja", "Nee", "Weet ik nog niet"])

selectie_isoleerplannen = st.multiselect(
    "Wat wilt u gaan isoleren?",
    ["Gevel", "Kozijnen", "Dak", "Bodem"])

#st.write("You selected:", options)

# Deze command in de Python Terminal runnen, niet via dit script. Path naar het script ook aanpassen naar je eigen mappen
#streamlit run /Users/maxpronk/Documents/Python/Rekentool/Streamlit/warmte_rekentool.py