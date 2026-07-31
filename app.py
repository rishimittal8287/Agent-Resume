#load modules
from google.genai.types import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt # for ocr
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np

#=======================

st.set_page_config(layout="wide")
#=======================
st.title("AI RESUME GENERATOR")
st.write("""this app helps user to build customized professional resume with latest job apply links""")
st.image("https://raw.githubusercontent.com/rishimittal8287/Agent-Resume/refs/heads/main/bg.png")
st.sidebar.title("Fill Important Details")
st.sidebar.image("https://raw.githubusercontent.com/rishimittal8287/Agent-Resume/refs/heads/main/bg.png")

# ======================

GOOGLE_API_KEY = st.sidebar.text_input("Gemini-API",type = "password")
GROQ_API_KEY = st.sidebar.text_input("Groq-API",type = "password")
TAVILY_API_KEY = st.sidebar.text_input("Tavily-API",type = "password")

all_API = [GOOGLE_API_KEY,GROQ_API_KEY,TAVILY_API_KEY ]
if not all(all_API):
    st.error("Must give all API keys")
    st.stop()
elif all(all_API):
    st.success("API KEYS LOADED SUCCESSFULLY")

    model = ChatGoogleGenerativeAI(
        model = 'gemini-3.5-flash-lite',
        google_api_key = GOOGLE_API_KEY)
else:
    st.info("PASS ALL API-KEYS")

# MULTISELECT OPTION
options = ["delhi","mumbai","pune","banglore"]
location = st.sidebar.multiselect("Select Location",
                                  options = options)
profile_op = ["Data Analysts","AI Engineer","Gen AI Developer"]
profile = st.sidebar.multiselect("Select job profile",
                                 options = profile_op)
st.markdown("""### GET USER INFO""")
user_info = st.text_area("""Write your Resume Description:""")

#=========================
# response=model.invoke("hello buddy!")
# response.content[-1]['text']
# =============================
def search_latest__news_jobs(query):
  """This function helps to fetch the latest news and jobs related using tavily"""
  Client = TavilyClient(
      api_key = TAVILY_API_KEY)
  response = Client.search(query)
  return response
#========================
agent = create_agent(
model=model,
tools = [search_latest__news_jobs])
# agent
#============================
def main_agent(agent, query):
  """This is main agent, or leader agent orchestrate sub agents"""
  prompt = """You are AI assistant and below given is to give detailed prompt for this.
  you are a professional Resume generetor where users will give their personalinfo,
  you have to create detailed resume  for students or professional one,
  it must be with dynamic ui and ux and,
  with advanced css professional Designing make sure to give output in HTML formalonly no markdown allowed """

  response = agent.invoke({'messages':[{'role':'user',
                                        'content':prompt}]})
  detailed_prompt = response['messages'][-1].content[-1]['text']
  # SAVE PROMPT USING FILE HANDLING
  with open('prompt.txt', 'w') as f:
    f.write(detailed_prompt)
  user_details = f"""Below Given it is a user details generate Resume based on that, if not given keep: default resume:
  python developer user details: {query}"""

  final_prompt = prompt + detailed_prompt + user_details
     # code generation
  response = agent.invoke({'messages':[{'role':'user',
                                       'content':final_prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code

#========================
# code = main_agent(agent,"RISHI MITTAL, GEN AI EXPERT")
# from IPython import display as DISPLAY
# DISPLAY.HTML(code)

#==============================
def get_jobs(agent,
             Location="Noida,Delhi",
             Profile="Data Analysts, AI Engineer"):
    Location = "Delhi,noida,gurugram"
    Profile = "Data Analysts, AI Engineer"

    prompt = f"""Based on user given Job profile,
fetch latest jobs or job apply article
using Naukri, Linkedin, Indeed, or all popular
Job apply platforms, Show Results with
JOB PROFILE NAME, LOCATION, SALARY, COMPANY NAME,
SHOW jobs only related to given
{Location} and {Profile}.
 Output must be in
Professional HTML Naukri theme cards with Dynamic Design,
Show atleast Top 10-20 results with direct apply link"""

    response = agent.invoke({'messages': [{'role': 'user',
                                           'content': prompt}]})
    code = response['messages'][-1].content[-1]['text']

    return code

# code = get_jobs(agent)
# DISPLAY.HTML(code)

if st.button("Generate Resume"):
             code = main_agent(agent,user_info)
             st.html(code,width="stretch",
             unsafe_allow_javascript=True)
st.divider()
job_code = get_jobs(agent,location,profile)
st.html(job_code, width="stretch",
        unsafe_allow_javascript=True)
