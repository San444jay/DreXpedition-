import re
import requests
from flask import Flask, render_template, request, session, send_file,send_from_directory
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json
import uuid
import os
import json
import base64
import requests
from face_voice_api import function_video_verification,function_video_enrollment
from datetime import datetime
import pytz
import subprocess
import os

import json

import google.generativeai as genai
genai.configure(api_key="AIzaSyC1geUNJ4LkZSfCt1BpUOiaI25rumi8nDo")

model = genai.GenerativeModel("gemini-1.5-pro-latest",generation_config={"response_mime_type": "application/json"})

###SUPPORTIVE FUNCTIONS###
def company_requirements(requirements, n_questions):

  prompt = "Please generate" + str(n_questions)+ "technical question for the following job requirements in json format  = {'questions': []} and if the job requirements entered is not correct or has hallucinations involved then return = {'questions':NA} Company requirements: """ + requirements
  
  response = model.generate_content(prompt)

  output_json = json.loads(response.text)
  return (output_json) 

def convert_mp4_to_audio(video_path, audio_save_path):
  p = subprocess.Popen(['ffmpeg',"-i", video_path,"-ac",'1',"-ar",'16000',"-vn","-acodec","pcm_s16le",audio_save_path], stdout = subprocess.PIPE)
  (output, err) = p.communicate()
  p_status = p.wait()
  print('Done with wav file')
  
def AI_result(question, answer):
  ASR_text = answer
  if (len(ASR_text.split(' '))) >= 10:
    prompt = """"You are a friendly interview feedback provider, Based on the question and the answer given by the candidate using Automatic Recognition system(you need to ignore typos) you will provide score out of 10 for Domain Knowledge, Articulation, Communication Skills also you need to provide Justification for Score and Feedback. You will provide me with the best interview answer for the given question. You need to provide Pros and Cons based on the candidate reply. Return the output in json format = {"Report" : {"Domain Knowledge" :[ {"Score" :,"Justification for Score" :,"Feedback":} ] ,"Articulation":[ { "Score" : , "Justification for Score":,"Feedback":}],"Communication Skills":[ {"Score":,"Justification for Score":,"Feedback":} ],"Best Interview Answer":,"Pros":[],"Cons":[]}} """ + 'Interview question :'+ question + " Candidate Reply :" + answer
  
    response = model.generate_content(prompt)
    print(response.text)
    output_json = json.loads(response.text)
    print(output_json)
    return (output_json)
    
  else:
    return ('Hello, Please speak for more than 5 words to give you a better feedback on your interview answer')
    

@app.route('/dashboard')
def dash():
    return render_template("index_dash.html",name=session["name"])

