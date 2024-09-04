# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

#install external libraries to use google sheet API:
#access and update data from spreadsheet
import gspread
#use creds.json for the autentication of the google clous
from google.oauth2.service_account import Credentials

#set the scope
#IAM configuration list the api that the program should access
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json") 
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():
    """
    get sales input from user
    """
    print("enter sales data from the last market")
    print("the data entered should be six numbers separated by commas")
    print("example: 10,20,30,40,50,60\n")

    #values are collected as strings
    data_str = input("Enter your data here: ")
    ##convert the string value into a list of values (still strings - need to be converted into integer)
    #split methods break at the commas
    sales_data = data_str.split(",")
    #the function below is calling the validate data fucntion
    validate_data(sales_data)

def validate_data(values):
    """inside the try convert all string values in integer. raises valueerror if strings cannot be
    converted or if there are no exact 6 values"""
    try:
        #1. conversion attempt from string to integer - provide error if it cannot be converted (es cat):
        [int(value) for value in values]
        #2. validation of the 6 numbers given
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 value required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again.\n")
    


get_sales_data()