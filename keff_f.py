import streamlit as st
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd
plt.rcParams["font.weight"] = "bold"
plt.rcParams["font.size"] = 10

st.beta_set_page_config(page_icon="potable_water")

st.header("Hydraulic conductivity of layered aquifers")

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
     
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_xlim(0, 1.01); ax.set_ylim(0,1.01)
    ax.xaxis.set_ticks_position('top') 
    ax.xaxis.set_label_position('top') 
    ax.set_xlabel("Relative head [-]", fontsize=12)  
    ax.set_ylabel("Relative thickness [-]", fontsize=12)  
    plt.gca().invert_yaxis()
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    ax.axhline(y=0, color='r', linewidth=2)
    ax.axhline(y=RT2, color='r', linewidth=2)
    ax.axhline(y=RT3, color='r', linewidth=2)
    ax.axhline(y=RT4, color='r', linewidth=2)
    ax.plot(RH, RT)

    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    st.pyplot(fig)

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
    fig2 = plt.figure()
    plt.gca().invert_yaxis()
    ay = fig2.add_subplot(1,1,1)
    ay.barh(index, RD) 
    plt.xticks(np.arange(0, 1.1, 0.1))
    ay.set_xlabel("Relative discharge [-]", fontsize=12)
    ay.set_xlabel("Layer number", fontsize=12)
 
    st.pyplot(fig2)

    if st.checkbox("show additional results"):
    

        st.write("The **Effective Hydraulic Conductivity** is: {0:0.2e}".format(WHK_eff), "s/m")
        st.write("The **Approximate Effective Hydraulic Conductivity** is {0:0.2e}".format(WHK_eff_a), "s/m")
        st.write("The **Effective Hydraulic Resistance** is: {0:0.2e}".format(WHR_eff), "m/s")
        st.write("The **Approximate Effective Hydraulic Resistance** is: {0:0.2e}".format(WHR_eff_a), "m/s")
    
        #result table
        st.dataframe(df4)


About = st.sidebar.checkbox("About App")
if About:
    st.sidebar.markdown("Add created by PKY")
    st.sidebar.markdown("App created using Streamlit")
else:
    st.sidebar.text(" ")

