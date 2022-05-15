	
import subprocess
import json
import sys
import os
 
serialNumber = "arn:aws:iam::848569320300:mfa/shah.muhammad_cli@careem.com"
tokenCode = sys.argv[1]
profile = sys.argv[2]
# profile = "prod"
#newProfile = sys.argv[3]
newProfile = "default"
 
command = "aws sts get-session-token --duration-seconds 129600 --serial-number "+serialNumber+" --token-code "+tokenCode+" --profile "+profile
proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
(out, err) = proc.communicate()
#print(out,err)
output = json.loads(out)
 
secretAccessKey = output['Credentials']['SecretAccessKey']
accessKeyId = output['Credentials']['AccessKeyId']
sessionToken = output['Credentials']['SessionToken']
 
command1 = "aws configure set aws_access_key_id "+accessKeyId+" --profile "+newProfile
os.system(command1)
 
command2 = "aws configure set aws_secret_access_key "+secretAccessKey+" --profile "+newProfile
os.system(command2)
 
command3 = "aws configure set aws_session_token "+sessionToken+" --profile "+newProfile
os.system(command3)
 
print("*** Keys Updated ***")