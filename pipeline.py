import pandas as pd
import numpy as np

def get_timetable(timetable):
    # print(timetable)
    timetable = timetable.splitlines()
    timetable = [x.split('\t') for x in timetable]
    timetable = pd.DataFrame(timetable)
    timetable = timetable.set_index(0)
    return timetable

def get_theory_slots(time_df):
    theory_slots = []
    for i in range(0, len(time_df), 2):
        theory_slots.append(time_df.iloc[i])

    theory_df = pd.concat(theory_slots, axis=1)
    #drop the first row
    # theory_df = theory_df.drop(theory_df.index[0])
    
    return theory_df.T

def get_lab_slots(time_df):
    lab_slots = []
    for i in range(1, len(time_df), 2):
        lab_slots.append(time_df.iloc[i])

    lab_df = pd.concat(lab_slots, axis=1)

    return lab_df.T

def remove_th_empty_columns(th):
    th = th.drop(columns=[1])
    th = th.drop(columns=[8])
    th = th.drop(columns=[14])
    return th

def remove_lb_empty_columns(th):
    th = th.drop(columns=[7])
    th = th.drop(columns=[14])
    th = th.drop(columns=[15])
    return th

# create a 7x72 matrix with 0s
def create_lab_matrix():
    lab_matrix = np.zeros((7, 72))
    return lab_matrix   

# For 1 in lb, mark 1 in lab1 based on lab_template
def mark_slots(lb, lab1, lab_template):
    for i in range(lb.shape[0]):
        for j in range(lb.shape[1]):
            if lb.iloc[i, j] == 1:
                # print(i,j)
                lab1.iloc[i,lab_template[j+1][0]:lab_template[j+1][1]] = 1
    
    return lab1

def create_empty_matrix():
    matrix = np.zeros((7, 72))
    return matrix

# Convert matrix to df
def convert_matrix_to_df(matrix):
    matrix = pd.DataFrame(matrix)

    return matrix

def mark_theory_slots(th):
    th = th.replace(np.nan, '', regex=True)
    th = th.applymap(lambda x: 1 if len(x) > 4 else 0)
    return th

def main(lab_template, theory_template, timetable):
    time_df = get_timetable(timetable)

    # mark theory slots
    theory = get_theory_slots(time_df)
    
    theory = mark_theory_slots(theory)
    theory = remove_th_empty_columns(theory)
    theory.columns = [1,2,3,4,5,6,7,8,9,10,11,12]
    
    th_matrix = create_empty_matrix()
    th_matrix = pd.DataFrame(th_matrix)
    th_matrix = mark_slots(theory, th_matrix, theory_template)
    

    # mark lab slots
    lb = get_lab_slots(time_df)

    lb = mark_theory_slots(lb)
    lb = remove_lb_empty_columns(lb)
    lb.columns = [1,2,3,4,5,6,7,8,9,10,11,12]
    
    lb_matrix = create_empty_matrix()
    lb_matrix = pd.DataFrame(lb_matrix)
    lb_matrix = mark_slots(lb, lb_matrix, lab_template)

    # Lab and Theory to a csv
    final_timetable = (th_matrix+lb_matrix)
    final = final_timetable.copy()
    # final.columns = ['8:30-9:30', '9:30-10:30', '10:30-11:30', '11:30-12:30', '12:30-1:30', '1:30-2:30', '2:30-3:30', '3:30-4:30', '4:30-5:30', '5:30-6:30', '6:30-7:30', '7:30-8:30']

    final_timetable.to_csv('tt.csv', index=False)

    return final

def nor_lab_template(final_timetable1, final_timetable2):
    # Convert float to int
    final_timetable1 = final_timetable1.astype(int)
    final_timetable2 = final_timetable2.astype(int)

    # Add the two dataframes final_timetable1 and final_timetable2
    final_timetable = final_timetable1 | final_timetable2

    # invert the dataframe
    final_timetable = final_timetable.applymap(lambda x: 0 if x == 1 else 1)

    
    # COnvert to csv
    final_timetable.to_csv('final_tt.csv', index=False)
    final_timetable.to_json('final_tt.json', orient='split')
    return final_timetable
    # print(final_timetable)

def build_heatmap(final_timetable):
    # heatmap with plotly
    import plotly.graph_objects as go
    import plotly.express as px
    import plotly.figure_factory as ff
    import numpy as np

    # Create a figure
    fig = ff.create_annotated_heatmap(z=final_timetable.values, x=list(final_timetable.columns), y=list(final_timetable.index), colorscale='plotly3', showscale=False)

    # Add title
    fig.update_layout(
        title_text='Timetable',
        xaxis_nticks=36
    )

    # Add custom xaxis title
    fig.update_xaxes(title_text="Time")
    
    # Add custom yaxis title
    fig.update_yaxes(title_text="Day")

    # Show grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='black')

    # Reverse yaxis
    fig.update_yaxes(autorange="reversed")
    

    fig.show()

def change_col_time(final_timetable):
    # Change the column names to time
    final_timetable.columns = ['8', '8:10', '8:20', '8:30', '8:40', '8:50', '9', '9:10', '9:20', '9:30', '9:40', '9:50', '10', '10:10', '10:20', '10:30', '10:40', '10:50', '11', '11:10', '11:20', '11:30', '11:40', '11:50', '12', '12:10', '12:20', '12:30', '12:40', '12:50', '1', '1:10', '1:20', '1:30', '1:40', '1:50', '2', '2:10', '2:20', '2:30', '2:40', '2:50', '3', '3:10', '3:20', '3:30', '3:40', '3:50', '4', '4:10', '4:20', '4:30', '4:40', '4:50', '5', '5:10', '5:20', '5:30', '5:40', '5:50', '6', '6:10', '6:20', '6:30', '6:40', '6:50', '7', '7:10', '7:20', '7:30', '7:40', '7:50']
    # Change Day to Day of the week
    final_timetable.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    return final_timetable

    







timetable = """MON	THEORY	A1	F1	D1-STS3201-SS-SJT305-ALL	TB1	TG1	-	Lunch	A2-CSE1006-TH-SJT603-ALL	F2-CSE3501-ETH-SJT522-ALL	D2-CSE2006-ETH-SJT424-ALL	TB2	TG2	-	V3
LAB	L1	L2	L3	L4	L5-CSE3501-ELA-SJT418-ALL	L6-CSE3501-ELA-SJT418-ALL	Lunch	L31	L32	L33	L34	L35	L36	-
TUE	THEORY	B1	G1	E1-FRE1001-TH-SJT702-ALL	TC1	TAA1	-	Lunch	B2-CSE3001-ETH-SJT311-ALL	G2	E2	TC2	TAA2	-	V4
LAB	L7-CSE3002-ELA-SJT516-ALL	L8-CSE3002-ELA-SJT516-ALL	L9	L10	L11	L12	Lunch	L37	L38	L39	L40	L41	L42	-
WED	THEORY	C1	A1	F1	V1	V2	-	Lunch	C2-CSE3002-ETH-SJT422-ALL	A2-CSE1006-TH-SJT603-ALL	F2-CSE3501-ETH-SJT522-ALL	TD2	TBB2	-	V5
LAB	L13-CSE3001-ELA-SJT417-ALL	L14-CSE3001-ELA-SJT417-ALL	L15	L16	L17	L18	Lunch	L43	L44	L45	L46	L47	L48	-
THU	THEORY	D1-STS3201-SS-SJT305-ALL	B1	G1	TE1	TCC1	-	Lunch	D2-CSE2006-ETH-SJT424-ALL	B2-CSE3001-ETH-SJT311-ALL	G2	TE2	TCC2	-	V6
LAB	L19	L20	L21-CSE2006-ELA-SJT515-ALL	L22-CSE2006-ELA-SJT515-ALL	L23	L24	Lunch	L49	L50	L51	L52	L53	L54	-
FRI	THEORY	E1-FRE1001-TH-SJT702-ALL	C1	TA1	TF1	TD1-STS3201-SS-SJT305-ALL	-	Lunch	E2	C2-CSE3002-ETH-SJT422-ALL	TA2-CSE1006-TH-SJT603-ALL	TF2	TDD2	-	V7
LAB	L25	L26	L27	L28	L29	L30	Lunch	L55	L56	L57	L58	L59	L60	-
SAT	THEORY	V8	X11	X12	Y11	Y12	-	Lunch	X21	Z21	Y21	W21	W22	-	V9
LAB	L71	L72	L73	L74	L75	L76	Lunch	L77	L78	L79	L80	L81	L82	-
SUN	THEORY	V10	Y11	Y12	X11	X12	-	Lunch	Y21	Z21	X21	W21	W22	-	V11
LAB	L83	L84	L85	L86	L87	L88	Lunch	L89	L90	L91	L92	L93	L94	-"""

bbs_table = """MON	THEORY	A1-CSE1008-ETH-SJT301-UGF	F1-EEE1001-ETH-SJT301-UGF	D1-MAT1017-TH-SJT301-UGF	TB1-ENG1013-ETH-SJT301-UGF	TG1-MAT1004-TH-SJT301-UGF	-	Lunch	A2	F2	D2	TB2	TG2	-	V3
LAB	L1	L2	L3	L4	L5	L6	Lunch	L31	L32	L33-ENG1902-LO-SJTG20-UGF	L34-ENG1902-LO-SJTG20-UGF	L35	L36	-
TUE	THEORY	B1-HUM1021-TH-SJT301-UGF	G1-MAT1004-TH-SJT301-UGF	E1-PHY1005-ETH-SJT301-UGF	TC1-CHY1002-TH-SJT301-UGF	TAA1	-	Lunch	B2	G2	E2	TC2	TAA2	-	V4
LAB	L7	L8	L9	L10	L11	L12	Lunch	L37	L38	L39	L40	L41	L42	-
WED	THEORY	C1-CHY1002-TH-SJT301-UGF	A1-CSE1008-ETH-SJT301-UGF	F1-EEE1001-ETH-SJT301-UGF	V1	V2	-	Lunch	C2	A2	F2	TD2	TBB2	-	V5
LAB	L13	L14	L15	L16	L17	L18	Lunch	L43-ENG1013-ELA-SJT519-UGF	L44-ENG1013-ELA-SJT519-UGF	L45-ENG1902-LO-SJTG20-UGF	L46-ENG1902-LO-SJTG20-UGF	L47	L48	-
THU	THEORY	D1-MAT1017-TH-SJT301-UGF	B1-HUM1021-TH-SJT301-UGF	G1-MAT1004-TH-SJT301-UGF	TE1-PHY1005-ETH-SJT301-UGF	TCC1	-	Lunch	D2	B2	G2	TE2	TCC2	-	V6
LAB	L19	L20	L21	L22	L23	L24	Lunch	L49-PHY1005-ELA-TT436-UGF	L50-PHY1005-ELA-TT436-UGF	L51-EEE1001-ELA-TT045-UGF	L52-EEE1001-ELA-TT045-UGF	L53	L54	-
FRI	THEORY	E1-PHY1005-ETH-SJT301-UGF	C1-CHY1002-TH-SJT301-UGF	TA1-CSE1008-ETH-SJT301-UGF	TF1	TD1-MAT1017-TH-SJT301-UGF	-	Lunch	E2	C2	TA2	TF2	TDD2	-	V7
LAB	L25	L26	L27	L28	L29	L30	Lunch	L55	L56	L57-CSE1008-ELA-SJT317-UGF	L58-CSE1008-ELA-SJT317-UGF	L59	L60	-
SAT	THEORY	V8	X11	X12	Y11	Y12	-	Lunch	X21	Z21	Y21	W21	W22	-	V9
LAB	L71	L72	L73	L74	L75	L76	Lunch	L77	L78	L79	L80	L81	L82	-
SUN	THEORY	V10	Y11	Y12	X11	X12	-	Lunch	Y21	Z21	X21	W21	W22	-	V11
LAB	L83	L84	L85	L86	L87	L88	Lunch	L89	L90	L91	L92	L93	L94	-"""

theory_template = {
    1: [0, 5],
    2: [6, 11],
    3: [12, 17],
    4: [18, 23],
    5: [24, 29],
    6: [30, 35],
    7: [36, 41],
    8: [42, 47],
    9: [48, 53],
    10: [54, 59],
    11: [60, 65],
    12: [66, 71]
}

lab_template = {
    1: [0, 9],
    2: [0, 9],
    3: [11, 20],
    4: [11, 20],
    5: [22, 31],
    6: [22, 31],
    7: [36, 45],
    8: [36, 45],
    9: [47, 56],
    10: [47, 56],
    11: [58, 67],
    12: [58, 67],
}

arhit_timetable = main(lab_template, theory_template, timetable)
viral_timetable = main(lab_template, theory_template, bbs_table)

arhit_timetable = change_col_time(final_timetable=arhit_timetable)
viral_timetable = change_col_time(final_timetable=viral_timetable)

final_timetable = nor_lab_template(viral_timetable, arhit_timetable)
build_heatmap(final_timetable)