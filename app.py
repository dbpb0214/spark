from collections import deque
import csv


def main():
    # 1. open slcsp.csv file to get data
    headers = []
    curr_slcsp_data = deque()
    with open("slcsp/slcsp.csv", "r") as file:
        rows = csv.reader(file)
        header = next(rows)
        headers.append(header)
        for row in rows:
            curr_slcsp_data.append(row)
    
    # 1.2 open zip.csv and get zip code data
    zip_code_data = {}
    with open("slcsp/zips.csv", "r") as file:
        rows = csv.reader(file)
        next(rows) # skip header
        for row in rows:
            if row[0] in zip_code_data: 
                zip_code_data[row[0]].append(row)
            else:
                zip_code_data[row[0]] = [row]

    # 1.3 filter zip_code_data by zipcodes in the curr_slcsp_data
    filtered_zip_code_data_by_zip_code = {}
    for slcsp in curr_slcsp_data:
        zip_code = slcsp[0]
        if zip_code in zip_code_data:
            filtered_zip_code_data_by_zip_code[zip_code] = zip_code_data[zip_code]

    # 1.4 open plans.csv and get all plans
    plan_data = {}
    with open("slcsp/plans.csv", "r") as file:
        rows = csv.reader(file)
        next(rows) # skip header
        for row in rows:
            state = row[1]
            if state in plan_data:
                plan_data[state].append(row)
            else:
                plan_data[state] = [row] 
    
    # 1.5 using the STATE value from filtered_zip_code_data_by_zip_code 
    # grab the relevant rows from plan_data
    # additionally filter by METAL_LEVEL and RATE_AREA
    plan_data_filtered = {}
    for key, val in filtered_zip_code_data_by_zip_code.items():
        metal_level = "Silver"
        rate_areas = val # can be multiple areas
        filtered_plan_data_by_metal_and_rate_area = []
        dedupe_rate_areas = [] # hold unique rate_area ids

        for ra in rate_areas:
            if ra[4] not in dedupe_rate_areas:
                dedupe_rate_areas.append(ra[4])
        
        for ra in dedupe_rate_areas:
            state = val[0][1] # assumes at least one item in list AND only one state to consider
            if state in plan_data:
                for pd in plan_data[state]:
                    if pd[2] == metal_level and pd[4] == ra:
                        filtered_plan_data_by_metal_and_rate_area.append(pd)
            else:
                print(f"NO STATE: {state} FOR ZIPCODE {key} IN PLAN_DATA!")
                continue
        
        if key not in plan_data_filtered:
            plan_data_filtered[key] = filtered_plan_data_by_metal_and_rate_area
    
    # 1.6 sort the plan_data_filtered data
    plan_data_sorted = {}
    for key, val in plan_data_filtered.items():
        sorted_slcsp = sorted(val, key=lambda x:float(x[3]))
        if key not in plan_data_sorted:
            plan_data_sorted[key] = sorted_slcsp

    # 1.7 - grab the 2nd one (represents the second lowest cost silver plan)
    slcsp_rate_results = {}
    for key in plan_data_sorted.keys():
        if len(plan_data_sorted[key]) > 2:
            if key not in slcsp_rate_results:
                slcsp_rate_results[key] = plan_data_sorted[key][1][3]
        else:
            slcsp_rate_results[key] = ''

    # 2. Use new data to create new file
    with open("new_updated_csv.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers[0])
        for row in curr_slcsp_data:
            zip_code = row[0]
            if zip_code:
                slcsp_area = slcsp_rate_results[zip_code]
                if slcsp_area:
                    row[1] = format(float(slcsp_rate_results[zip_code]), '.2f')
            writer.writerow(row)

main()