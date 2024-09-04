# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

#install external libraries to use google sheet API:
#access and update data from spreadsheet
import gspread
#use creds.json for the autentication of the google clous
from google.oauth2.service_account import Credentials
#install the alternative print method:
from pprint import pprint

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
    #create a while loop to restart the code if the data are not valid
    while True:
        print("enter sales data from the last market")
        print("the data entered should be six numbers separated by commas")
        print("example: 10,20,30,40,50,60\n")

        #values are collected as strings:
        data_str = input("Enter your data here: ")
        ##convert the string value into a list of values (still strings - need to be converted into integer)
        #split methods break at the commas
        sales_data = data_str.split(",")
        #the function below is calling the validate data fucntion:
        if validate_data(sales_data):
            print("data is valid")
            break
    #return data to be addded in the sheet:
    return sales_data
        

def validate_data(values):
    """inside the try convert all string values in integer. raises valueerror if strings cannot be
    converted or if there are no exact 6 values"""
    try:
        #1. conversion attempt from string to integer - provide error if it cannot be converted (es cat):
        [int(value) for value in values]
        #2. validation of the 6 numbers given:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 value required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again.\n")
        return False
    return True
'''
def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    #open the sales worksheet from google :
    sales_worksheet = SHEET.worksheet("sales")
    #add the entered value in the given sheet as a row:
    sales_worksheet.append_row(data)
    #visual feedback for the user:
    print("Sales worksheet updated successfully.\n")

def update_surplus_worksheet(new_surplus_data):
    """
    this function will update the surplus sheet with the updated data
    this data will be the difference between sales and stock data
    """
    print("update surplus worksheet with the new data...\n")
    # open the surplus worksheet and assign it to a variable:
    surplus_worksheet = SHEET.worksheet("surplus")
    # append the surplus data calculated in the func above as a row
    surplus_worksheet.append_row(new_surplus_data)
    print("surplus data has been updated\n")
    #print(new_surplus_data) you can see the list of value added 
'''

def update_worksheet(data, worksheet):
    '''
    update worksheet with the data provided (sales/surplus)
    this func will be shared for update all the sheets
    '''
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")



def calculate_surplus_data(sales_row):
    '''
    compare sales data with stock data and calculate the surplus for each item type
    positive surplus indicates wastes
    negative surplus indicated extra made after soldout
    '''
    print("calculate surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    #pprent will return data more readable as a list of lists (each list is a row)
    stock_row = stock[-1]
    #pprint(stock) show the data as list of lists - each list is a row in the sheet

    #create an empty list to add the difference values between sales and stock:
    surplus_data = []
    #iterate between the two lists at the same times using zip method:
    for stock, sales in zip(stock_row, sales_row):
        #convert the stock value in integer before the operation:
        #print(f"{stock}, {sales}") you can see both the list iterated
        surplus = int(stock) - sales
        #add the difference value to a 3rd list:
        surplus_data.append(surplus)
    return surplus_data



def main():
    '''main function that run all the program functions'''
    # create a variable "data" that collect the user input:
    data = get_sales_data()
    # transform the data from strings to integer again:
    sales_data = [int(num) for num in data]
    # call the function for updating the sheet:
    update_worksheet(sales_data, "sales")
    #call the fuction to calculate surplus data:
    new_surplus_data = calculate_surplus_data(sales_data)
    #call the function to update the sheet surplus
    update_worksheet(new_surplus_data, "surplus")

print("welcome to the love sandwiches data automation")

#call the main function for call all of them 
main()