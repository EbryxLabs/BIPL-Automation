import json
from datetime import datetime, timedelta
import datetime
import datetime as dt_module
from datetime import timedelta
import requests
from sharepoint import *
from secret import *
from new_sheet import *
#from get_month import *
import datetime
import pytz
server_time_utc = datetime.datetime.utcnow()
pakistan_timezone = pytz.timezone('Asia/Karachi')
server_time_pakistan = server_time_utc.replace(tzinfo=pytz.utc).astimezone(pakistan_timezone)
current_month = server_time_pakistan.strftime('%B-%Y')


def find_cell(slack_date,shift,analyst_name):
    # Replace with your actual access token and drive ID
    print("=====Inside find_cell func=======")
    access_token = get_access_token()
    sheet_id = "01BKVRNBWBIC23CDE22ZA2SCIUIHFGUD5A"
    drive_id = "b!XcKD9SsGZEK3SX2Re2yqZYwlPfTg7GpHocABjTWYF9WkfydFlwygSp0DSKMVD8Pb"
    url = f"https://graph.microsoft.com/v1.0/drives/b!vYJC7AWj1U-BBKsXSOO9QPcjrGEEt8BNqnFfggDucfCv8-o53MKpT6IHQeUa9kdU/items/01BKVRNBU5N4NYQDB3A5F2EIMYUE5XU7RH/workbook/worksheets('"+current_month+"')/usedRange"
    print(url)
#    exit()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    #print(access_token)

    response = requests.get(url, headers=headers)
    print ("=====Get Sheet=====")
    print (response.status_code)
    print (response.content)
    if response.status_code == 404:
        create_sheet_if_not_exists(current_month)


    if response.status_code == 200:
        print("==========Response Code OK=============")

        drive_info = response.json()
        data = drive_info.get("values", [])
        for row_number, row in enumerate(data, start=1):  # Start with index 1
            if row and isinstance(row[0], int):  # Assuming dates are in Excel's serial date format
                serial_date = row[0]
                excel_start_date = dt_module.datetime(1900, 1, 1)
                python_date = excel_start_date + timedelta(days=serial_date - 2)
                cell_date = python_date.strftime('%Y-%m-%d')
#                get_current_month()
                print(f"Checking row {row_number} - Slack Date: {slack_date}, Cell Date: {cell_date}")

                if slack_date == cell_date:
                    print("Match found!")
                    print("Cell Date:", cell_date)
                    print("Matching Row Number:", row_number)  # Print row number
                    print("adding :", analyst_name, "in cell :", cell_date, " and shift is :", shift, "Thats all")
                    variable= update_cell(cell_date, shift, analyst_name,row_number)
                    return variable
    else:
        print("Error:", response.status_code)
        #   print(response.text)

# Call the function

def update_cell(cell_date,shift,analyst_name,row_number):
 print("========update cell func==========")
 print(shift)
 if shift == "*Morning*":
#    current_month = (datetime.now() + timedelta(days=1)).strftime('%B-%Y')
    cell_date_datetime = dt_module.datetime.strptime(cell_date, '%Y-%m-%d')
    cell_date_datetime += timedelta(days=1)
    cell_date = cell_date_datetime.strftime('%Y-%m-%d')
    print("======morning shift here======")
    print(cell_date,shift,analyst_name,row_number)
    access_token = get_access_token()
    drive_id = "b!XcKD9SsGZEK3SX2Re2yqZYwlPfTg7GpHocABjTWYF9WkfydFlwygSp0DSKMVD8Pb"
    print(row_number)
    cell_address = f"D{row_number}"

# Construct the URL with the formatted cell address and row number
    updated_url="https://graph.microsoft.com/v1.0/drives/b!vYJC7AWj1U-BBKsXSOO9QPcjrGEEt8BNqnFfggDucfCv8-o53MKpT6IHQeUa9kdU/items//01BKVRNBU5N4NYQDB3A5F2EIMYUE5XU7RH/workbook/worksheets('"+current_month+"')/range(address='$B${}')/".format(row_number)
    print(updated_url)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data= {
    "values": [
        [
            analyst_name
        ]
    ]
}
    json_data = json.dumps(data)
    print(updated_url)
    response = requests.patch(updated_url, headers=headers, data=json_data)

    if response.status_code == 200:
        print("Cell updated successfully")
        return 1
    else:
        print("Error:", response.status_code)
        print(response.text)

 if shift == "*Evening*":
    print(cell_date,shift,analyst_name,row_number)
    access_token = get_access_token()
    drive_id = "b!XcKD9SsGZEK3SX2Re2yqZYwlPfTg7GpHocABjTWYF9WkfydFlwygSp0DSKMVD8Pb"
    print(row_number)
    cell_address = f"D{row_number}"

# Construct the URL with the formatted cell address and row number
    updated_url="https://graph.microsoft.com/v1.0/drives/b!vYJC7AWj1U-BBKsXSOO9QPcjrGEEt8BNqnFfggDucfCv8-o53MKpT6IHQeUa9kdU/items//01BKVRNBU5N4NYQDB3A5F2EIMYUE5XU7RH/workbook/worksheets('"+current_month+"')/range(address='$C${}')/".format(row_number)
    print(updated_url)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data= {
    "values": [
        [
            analyst_name
        ]
    ]
}
    json_data = json.dumps(data)

    response = requests.patch(updated_url, headers=headers, data=json_data)

    if response.status_code == 200:
        print("Cell updated successfully")
        return 1
    else:
        print("Error:", response.status_code)
        print(response.text)

 if shift == "*Night*":
    print(cell_date,shift,analyst_name,row_number)
    access_token = get_access_token()
    drive_id = "b!XcKD9SsGZEK3SX2Re2yqZYwlPfTg7GpHocABjTWYF9WkfydFlwygSp0DSKMVD8Pb"
    print(row_number)
    cell_address = f"D{row_number}"

# Construct the URL with the formatted cell address and row number
    updated_url="https://graph.microsoft.com/v1.0/drives/b!vYJC7AWj1U-BBKsXSOO9QPcjrGEEt8BNqnFfggDucfCv8-o53MKpT6IHQeUa9kdU/items//01BKVRNBU5N4NYQDB3A5F2EIMYUE5XU7RH/workbook/worksheets('"+current_month+"')/range(address='$D${}')/".format(row_number)
    print(updated_url)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data= {
    "values": [
        [
            analyst_name
        ]
    ]
}
    json_data = json.dumps(data)

    response = requests.patch(updated_url, headers=headers, data=json_data)

    if response.status_code == 200:
        print("Cell updated successfully")
        return 1
    else:
        print("Error:", response.status_code)
        print(response.text)
