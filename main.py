import requests
import time

import pandas as pd
import streamlit as st

# ////////////////////////////build DB////////////////////////////
@st.cache
def get_acft_data() -> pd.DataFrame:
    # get aircraft data via icao.net with requests module
    with st.spinner("Getting aircraft data form icao.net. Please wait a moment."):
        icao_doc_8643_url = "https://www4.icao.int/doc8643/External/AircraftTypes"
        res = requests.post(url=icao_doc_8643_url)
        return pd.DataFrame().from_dict(res.json())

@st.cache
def read_ap_csv() -> pd.DataFrame:
    return pd.read_csv("./airport-codes_csv.csv")


# ////////////////////////////build page////////////////////////////
def ap_page():
    st.sidebar.subheader("Airport Info")
    # text_input
    ap_icao = st.sidebar.text_input(label="ICAO code").upper()

    # col select
    df_ap_options = st.sidebar.multiselect(
        label="Select show columns.", 
        options=st.session_state["df_ap"].columns,
        default=["ident", "type", "name", "iso_country"],
        )

    # subtitle
    st.header("Airport Information")

    # show dataframe
    df_ap:pd.DataFrame = st.session_state["df_ap"][df_ap_options]
    if ap_icao:
        df_ap = df_ap.query(f"ident == '{ap_icao}'")
    else:
        df_ap = df_ap.head(15)
    st.dataframe(df_ap)


def acft_page():
    st.sidebar.subheader("Aircraft Designator")
    # text_input
    acft_input = st.sidebar.text_input(label="Serch by Aircraft Designator").upper()

    # col select 
    df_acft_options = st.sidebar.multiselect(
        label="Select show columns.", 
        options=st.session_state["df_acft"].columns,
        default=["Designator", "ModelFullName", "ManufacturerCode", "EngineType"],
        )

    # subtitle
    st.header("Aircraft Designator")

    # show Dataframe
    df_acft:pd.DataFrame = st.session_state["df_acft"][df_acft_options]
    if acft_input:
        df_acft = df_acft.query(f"Designator == '{acft_input}'")
    else:
        df_acft = df_acft.head(15)
    st.dataframe(df_acft)
        


def cs_page():
    # will be written

    st.sidebar.subheader("Airline Callsign")
    
    # subtitile
    st.header("Airline Callsign")
    st.write("Will be written")


# to do: reset btn
# sel show rows length
# likely serch

def change_page():
    # for python v3.10 or later
    # match st.session_state["sel_page"]:
    #     case "Airport Info":
    #         ap_page()
    #     case "Aircraft Info":
    #         acft_page()
    #     case "Aircraft Callsign":
    #         cs_page()

    # for python v3.9 or older
    if st.session_state["sel_page"] == "Airport Info":
        ap_page()
    if st.session_state["sel_page"] == "Aircraft Info":
        acft_page()
    if st.session_state["sel_page"] == "Aircraft Callsign":
        cs_page()



# ////////////////////////////init////////////////////////////
def init_sess_val():
    st.session_state["sel_page"] = "Airport Info"
    
    # read data
    st.session_state["df_acft"] = get_acft_data()
    st.session_state["df_ap"] = read_ap_csv()
    # st.session_state["df_cs"]

    st.session_state["is_setup"] = "1"



# ////////////////////////////sidebar nav////////////////////////////
def build_nav_sidebar():
    select_page = st.sidebar.radio(
        label="Select Page",
        options=["Airport Info", "Aircraft Info", "Aircraft Callsign"]
        )

    if select_page:    
        st.session_state['sel_page'] = select_page



# ////////////////////////////main////////////////////////////
def atc_utils():
    # init
    st.set_page_config()
    if "is_setup" not in st.session_state:
        init_sess_val()

    st.title("ATC Tools")
    build_nav_sidebar()
    change_page()

    # st.subheader("Contacts")




if __name__ == "__main__":
    atc_utils()
