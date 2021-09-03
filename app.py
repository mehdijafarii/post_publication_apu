import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime

file1 = "23rd August 2021 (with grouping).csv"
file2 = "30th August 2021 (with grouping).csv"

# TODO: below lists are used in change_analysis() function
intakes_list_f2=[]
module_list_f2=[]

# TODO: below variables are used in intake_analysis() function
unique_intakes = []
intake_dic_timetable = {}
final_dict = {}
total_morning = {}


def removing_doub(file_name):
    output_name = "uniq " + file_name
    initial_file = pd.read_csv(file_name)
    keep_col = ['DAY','TIMEIN','TIMEOUT','INTAKE','SUBJECT','LECTURER']
    new_f = initial_file[keep_col]
    sorted_f = new_f.sort_values(["DAY","TIMEIN","INTAKE","LECTURER", "SUBJECT"])
    removed_doub = sorted_f.drop_duplicates(subset=["DAY", "TIMEIN", "LECTURER"], keep='first')
    removed_doub.to_csv(output_name, index=False)
    return removed_doub.values.tolist()


def change_analysis(file1_name, file2_name):
    """This function would call removing_doub() and after
    make unique files it would compares two unque file"""
    unique_f1 = removing_doub(file1_name)
    unique_f2 = removing_doub(file2_name)
    changes=[]
    for row in unique_f2:
        if row[3] not in intakes_list_f2:
            intakes_list_f2.append(row[3])
        if row[4] not in module_list_f2:
            module_list_f2.append(row[4])
    for f1_row in unique_f1:
        if f1_row not in unique_f2:
            if f1_row[3] in intakes_list_f2:
                if 'APUMP' not in f1_row[3]:
                    if f1_row[4] in module_list_f2:
                        changes.append(f1_row)
    print(changes)
    print(f"Total changes: {len(changes)} from total classes: {len(unique_f1)}")
    print(f"Change percentage is equal to {len(changes) * 100 / len(unique_f1)} %")


def intake_analysis(file_name):
    """ The function input csv file and then,
    sort the file and drops the unwanted coloumns
    """
    initial_file = pd.read_csv(file_name)
    unique_intakes = initial_file['INTAKE'].drop_duplicates()
    csv_as_list = initial_file.values.tolist()

    for intake in unique_intakes:
        intake_dic_timetable[intake] = []
        for row in csv_as_list:
            if row[5] == intake:
                intake_dic_timetable[intake].append(row)

    for intake in intake_dic_timetable:
        counter = 0
        for timetable_intake in intake_dic_timetable[intake]:
            if (timetable_intake[1] == '08:30' or 
                timetable_intake[1] == '08:45' or 
                timetable_intake[1] == '09:00' or 
                timetable_intake[1] == '09:15' or
                timetable_intake[1] == '09:30' or
                timetable_intake[1] == '09:45'):
                counter += 1
            total_morning[intake] = counter

        g1_timetable = []
        g2_timetable = []
        g3_timetable = []
        g4_timetable = []
        for row in intake_dic_timetable[intake]:
            if row[9] == 'G1' and (row[1] == '08:30' or
                                    row[1] == '08:45' or  row[1] == '09:00' or
                                    row[1] == '09:15' or  row[1] == '09:30' or
                                    row[1] == '09:45'):
                g1_timetable.append(row)
            elif row[9] == 'G2' and (row[1] == '08:30' or
                                    row[1] == '08:45' or  row[1] == '09:00' or
                                    row[1] == '09:15' or  row[1] == '09:30' or
                                    row[1] == '09:45'):
                g2_timetable.append(row)
            elif row[9] == 'G3' and (row[1] == '08:30' or
                                    row[1] == '08:45' or  row[1] == '09:00' or
                                    row[1] == '09:15' or  row[1] == '09:30' or
                                    row[1] == '09:45'):
                g3_timetable.append(row)
                # print(g3_timetable)
            elif row[9] == 'G4' and (row[1] == '08:30' or
                                    row[1] == '08:45' or  row[1] == '09:00' or
                                    row[1] == '09:15' or  row[1] == '09:30' or
                                    row[1] == '09:45'):
                g4_timetable.append(row)
        if g4_timetable != []:
            final_dict[intake] = {'G1':len(g1_timetable) , 'G2':len(g2_timetable), 'G3':len(g3_timetable), 'G4':len(g4_timetable)}
        elif g3_timetable != []:
            final_dict[intake] = {'G1':len(g1_timetable), 'G2':len(g2_timetable), 'G3':len(g3_timetable)}
        elif g2_timetable != []:
            final_dict[intake] = {'G1':len(g1_timetable), 'G2':len(g2_timetable)}
        elif g1_timetable != []:
            final_dict[intake] = {'G1':len(g1_timetable)}

    a_file = open('temp_'+file_name, "w")
    header_dict = {"Intake Code": "Number of morning classes"}
    # ? updates the header_dict and append the  final_dic to it.
    header_dict.update(final_dict)
    writer = csv.writer(a_file)
    for key, value in header_dict.items():
        writer.writerow([key, value])
    a_file.close()

    list_to_csv = []
    second_f = pd.read_csv('temp_'+file_name)
    csv2_as_list = second_f.values.tolist()
    for row in csv2_as_list:
        row.append(total_morning[row[0]])
        list_to_csv.append(row)

    fields = ['Intake code', 'Splits of intake groups', 'Total morning classes'] 
    with open('morning_analysis_'+file_name, 'w',newline='') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(list_to_csv)
        
    os.remove('temp_'+file_name)


def population_report(file_name):

    pop_init_f = pd.read_csv(file_name)
    keep_col = ['DAY','TIMEIN','TIMEOUT','ROOM','INTAKE','SUBJECT','LECTURER', 'KEYCODE']
    pop_new_f = pop_init_f[keep_col]
    pop_sorted_f = pop_new_f.sort_values(["DAY","TIMEIN","INTAKE","LECTURER", "SUBJECT"])
    pop_uniq = pop_sorted_f.drop_duplicates(subset=["DAY", "TIMEIN", "LECTURER"], keep='first')
    pop_list_f = pop_uniq.values.tolist()

    on_campus_pop = {
        'Mon': {}, 'Tue':{}, 'Wed':{}, 'Thu':{}, 'Fri':{}
    }

    day_times = ['08:30','08:45','09:00','9:15','9:30','9:45','10:00','10:15','10:30','10:45','11:00','11:15','11:30','11:45',
    '12:00', '12:15','12:30','12:45','13:00','13:15','13:30','13:45','14:00','14:15','14:30','14:45','15:00','15:15','15:30','15:45',
    '16:00','16:15','16:30','16:45','17:00','17:15','17:30','17:45','18:00', '18:15', '18:30', '18:45', '19:00', '19:15', '19:30',
    '19:45', '20:00', '20:15', '20:30', '20:45', '21:00', '21:15', '21:30','21:45', '22:00', '22:15', '22:30','22:45', '23:00']

    for day in on_campus_pop:
        for time in day_times:
            on_campus_pop[day][time] = 0;
    
    for day in on_campus_pop:
        for row in pop_list_f:
            if row[0] == day:
                if 'Online' not in row[3] or 'ONLMCO3' not in row[3]:
                    for time in day_times:
                        if row[1] == time :
                            on_campus_pop[day][time] = on_campus_pop[day][time]+int(row[7])
                        elif datetime.strptime(row[2], "%H:%M") >= datetime.strptime(time, "%H:%M") and datetime.strptime(row[1], "%H:%M") < datetime.strptime(time, "%H:%M"):
                            on_campus_pop[day][time] = on_campus_pop[day][time]+int(row[7])

    df = pd.DataFrame(on_campus_pop)
    bar_chart_output = "barchart_" + file_name+'.png'
    line_chart_output ="linechart_" + file_name+'.png'
    csv_output= "population_"+file_name
    print(df)
    df.plot(kind="bar",figsize=(15,10))
    plt.ylabel('Number of students')
    plt.xlabel('Day time')
    plt.savefig(bar_chart_output)

    df.plot(figsize=(15,10))
    plt.ylabel('Number of students')
    plt.xlabel('Day time')
    plt.savefig(line_chart_output)

    df.to_csv(csv_output)


def camp_reopen_rm_doub(file_name):
    output_name = "uniq " + file_name
    initial_file = pd.read_csv(file_name)
    keep_col = ['DAY','TIMEIN','TIMEOUT','ROOM','INTAKE','SUBJECT','LECTURER']
    new_f = initial_file[keep_col]
    sorted_f = new_f.sort_values(["DAY","TIMEIN","INTAKE","LECTURER", "SUBJECT"])
    removed_doub = sorted_f.drop_duplicates(subset=["DAY", "TIMEIN", "LECTURER"], keep='first')
    removed_doub.to_csv(output_name, index=False)
    return removed_doub.values.tolist()


def camp_reopen_onl_classes(file_name):
    initial_count = 0
    online_lab = 0
    unique_file = camp_reopen_rm_doub(file_name)
    for uni_class in unique_file:
        if 'ONLMCO3' in uni_class[3] or 'Online' in uni_class[3]:
            if 'LAB' in uni_class[5]: 
                online_lab +=1
            initial_count +=1
    print(f"Total classes in virtual rooms are: {initial_count}")
    print(f"Lab classes in virtual rooms are: {online_lab}")



if __name__ == '__main__':
    print("-----------Morning file-----------")
    intake_analysis(file2)
    print("-----------change analysis-----------")
    change_analysis(file1, file2)
    print("-----------population report-----------")
    population_report(file2)
    print("-----------campus re-open-----------")
    camp_reopen_onl_classes(file1)

