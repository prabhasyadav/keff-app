import streamlit as st
import numpy as np 
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import Span, Range1d


st.beta_set_page_config(page_icon="potable_water")

st.header("**Hydraulic conductivity of layered aquifers**")

st.markdown("The site can be used to calculate the effective hydraulic conductivity of the layered aquifers." )


st.markdown("You steps for calculations are:\n \n1. Input layer thickness and conductivity data in the boxes in the sidebar\n 2. Check the boxes to see the results  ",  unsafe_allow_html=True)
st.text("") # to add free space

st.warning("Make sure to be consistent with the UNITS of input data")

st.sidebar.header("The input data")

M1 = st.sidebar.number_input("Thickness Layer 1 (m):", value =1.0, step=0.1)
M2 = st.sidebar.number_input("Thickness Layer 2 (m):",value = 2.0, step=0.1)
M3 = st.sidebar.number_input("Thickness Layer 3 (m):",value = 3.0, step=0.1)
    
K1 = st.sidebar.number_input("Hydraulic Conductivity Layer 1 (m/s):", value=2e-2, format='%e')
K2 = st.sidebar.number_input("Hydraulic Conductivity Layer 2 (m/s):", value=2e-3, format='%e')
K3 = st.sidebar.number_input("Hydraulic Conductivity Layer 3 (m/s):", value=2e-4, format='%e')

K = [K1, K2, K3]
K_f = ["%0.2e" %elem for elem in K]

# making input table
INPUT = {"Thickness [L]": [M1, M2, M3], "Hydraulic Conductivity [L/T]": K_f}
index = ["Layer 1", "Layer 2", "Layer 3"]
df = pd.DataFrame(INPUT, index=index)

"### The input data"
st.dataframe(df)

# relative thickness
tt = M1+M2 + M3  # m, totial thickness

RL1, RL2, RL3 = M1/tt, M2/tt, M3/tt 
HRL1, HRL2, HRL3 = 1/K1, 1/K2, 1/K3 
WHK1, WHK2, WHK3 = RL1*K1, RL2*K2,RL3*K3
WHR1,WHR2, WHR3 = RL1/K1, RL2/K2, RL3/K3 


RL =  [RL1, RL2, RL3]
HRL = [HRL1, HRL2, HRL3]
WHK = [WHK1, WHK2, WHK3]
WHR = [WHR1,WHR2, WHR3]


RL_f = [ '%.2f' %elem for elem in RL ]
HRL_f = [ '%.2e' %elem for elem in HRL ]
WHK_f = [ '%.2e' %elem for elem in WHK ]
WHR_f = [ '%.2e' %elem for elem in WHR ]

# making int. calculation table
index2 = ["Layer 1", "Layer 2", "Layer 3", "Sum"]
CAL1 = {"Relative Thickness [-]":RL_f, "Hydraulic Resistance [T/L]":HRL_f, 
"Weighted Hyd. Cond. [L/T]": WHK_f, "Weighted Hyd. Resistance [T/L]": WHR_f}
df2 = pd.DataFrame(CAL1)

if st.checkbox("Show intermediate calculations"):
    st.dataframe(df2, height=1000)

# Model Output

HR_eff = sum(WHR)
HR_eff_a = max(WHR)

HC_eff = 1/HR_eff
HC_eff_a = 1/HR_eff_a


RT1 = 0 
RT2 = RT1+RL1
RT3 = RT2+RL2
RT4 = 1

RT = [RT1, RT2, RT3, RT4]
RT_f = ["%0.2f" %elem for elem in RT]


RH1 = 1
RH2 = 1-HC_eff*WHR1
RH3 = HC_eff*WHR3 
RH4 = 0

RH = [RH1, RH2, RH3, RH4]
RH_f = ["%0.2f" %elem for elem in RH]

df3 = {"Relative Thickness [-]": RT_f, "Relative Head [-]": RH_f}

st.markdown("### Results")


if st.checkbox("Show results: Flow perpendicular to layer"):

    # results text

    st.write("The **Effective Hydraulic Conductivity** is: {0:0.2e}".format(HC_eff), "m/s")
    
    #plot

    TOOLS = "save,pan,box_zoom,reset,wheel_zoom, crosshair"

    p = figure(
    x_axis_label='Relative head [-]',
    y_axis_label='Relative thickness [-]',
    plot_width=350, 
    plot_height=400,
    x_axis_location="above",
    tools = TOOLS)

    p.y_range.flipped = True
    p.line(RH, RT, line_width=2 )
    sp1 = Span(location=0, dimension='width', line_color='red', line_width=4)
    sp2 = Span(location=RT2, dimension='width', line_color='red', line_width=2)
    sp3 = Span(location=RT3, dimension='width', line_color='red', line_width=2)
    sp4 = Span(location=RT4, dimension='width', line_color='red', line_width=2)

    p.add_layout(sp1)
    p.add_layout(sp2)
    p.add_layout(sp3)
    p.add_layout(sp4)
    p.y_range = Range1d(1.01, 0)
    p.x_range = Range1d(0, 1.02)
    p.xaxis.axis_label_text_font_size = "10pt"
    p.axis.axis_label_text_font_style = 'bold'
    p.yaxis.major_label_text_font_size = "10pt"
    p.xaxis.major_label_text_font_size = "10pt"
    p.xaxis.major_label_text_font_style = 'bold'
    p.yaxis.major_label_text_font_style = 'bold'

    yticks = np.arange(0,1.1, 0.1)
    p.yaxis.ticker = yticks
    p.xaxis.ticker = yticks

    st.bokeh_chart(p, use_container_width=False)

    if st.checkbox("Show additional results"):

        st.write("The **Effective Hydraulic Conductivity** is: {0:0.2e}".format(HC_eff), "m/s")
        st.write("The **Approximate Effective Hydraulic Conductivity** is: {0:0.2e}".format(HC_eff_a), "m/s")
        st.write("The **Effective Hydraulic Resistance** is: {0:0.2e}".format(HR_eff), "s/m")
        st.write("The **Approximate Effective Hydraulic Resistance** is {0:0.2e}".format(HR_eff_a), "s/m")


            #result table
        st.dataframe(df3)


# results perpendicular flow
WHK_eff = sum(WHK)
WHK_eff_a = max(WHK)

WHR_eff = 1/WHK_eff
WHR_eff_a = 1/WHK_eff_a

RD1 = WHK1/WHK_eff
RD2 = WHK2/WHK_eff
RD3 = WHK3/WHK_eff

RD = [RD1, RD2, RD3]

df4 = pd.DataFrame({"Relative Discharge [-]": RD}, index= index)


if st.checkbox("Show results: Flow parallel to the layer"):

    st.write("The **Effective Hydraulic Conductivity** is: {0:0.2e}".format(WHK_eff), "s/m")
    
    p2 = figure(y_range = index, plot_height = 250) # makes figure
    p2.hbar(y=index, right= RD, height = 0.5) # plots bar graph

    #customizing chart
    yticks = np.arange(0,1.1, 0.1)
    p2.xaxis.ticker = yticks
    p2.xaxis.axis_label_text_font_size = "10pt"
    p2.axis.axis_label_text_font_style = 'bold'
    p2.xaxis.major_label_text_font_size = "10pt"
    p2.xaxis.major_label_text_font_style = 'bold'
    p2.yaxis.major_label_text_font_size = "10pt"
    p2.yaxis.major_label_text_font_style = 'bold'

    # figure to website.
    st.bokeh_chart(p2, use_container_width=False)

    if st.checkbox("show additional results"):
    

        st.write("The **Effective Hydraulic Conductivity** is: {0:0.2e}".format(WHK_eff), "s/m")
        st.write("The **Approximate Effective Hydraulic Conductivity** is {0:0.2e}".format(WHK_eff_a), "s/m")
        st.write("The **Effective Hydraulic Resistance** is: {0:0.2e}".format(WHR_eff), "m/s")
        st.write("The **Approximate Effective Hydraulic Resistance** is: {0:0.2e}".format(WHR_eff_a), "m/s")
    
        #result table
        st.dataframe(df4)


About = st.sidebar.checkbox("About App")
if About:
    st.sidebar.markdown("App created by PKY")
    st.sidebar.markdown("App created using [Streamlit](www.streamlit.io)")
else:
    st.sidebar.text(" ")
