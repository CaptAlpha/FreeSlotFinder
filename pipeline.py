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
    (th_matrix+lb_matrix).to_csv('tt.csv', index=False)

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
    1: [0, 10],
    2: [0, 10],
    3: [12, 21],
    4: [12, 21],
    5: [23, 32],
    6: [23, 32],
    7: [36, 46],
    8: [36, 46],
    9: [48, 57],
    10: [48, 57],
    11: [59, 68],
    12: [59, 68],
}

main(lab_template, theory_template, timetable)
