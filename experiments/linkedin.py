from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
# Authenticate using any Linkedin account credentials
api = Linkedin(os.getenv('LINKEDIN_EMAIL'), os.getenv('LINKEDIN_PASS'))
print("hah")
# GET a profile
profile = api.get_profile('bismamandasamsu')

with open ('profile.json', 'w') as f:
    json.dump(profile, f, indent=4)
    
print("hah 2")
