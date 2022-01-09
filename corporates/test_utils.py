from django_project.config import Config as c


def get_all_data_from_csv(sheet_names):

    pd_dict = {}

    for sheetname in sheet_names:
        csv_path = os.path.join(BASE_DIR_XL_DB, sheetname + '.csv')
        pd_dict[sheetname] = pd.read_csv(csv_path)
    return pd_dict

def get_scores_summary(company_id, all_data=None):

    score_data = [0] * 13

    scores_summary_data = all_data[all_data[c.FIELDS.COMPANY_ID] == company_id]
    for i in range(1, 14):
        score_data[i - 1] = scores_summary_data.iloc[0, i]

    score_data_dict = c.SCORES.STRUCTURE

    for category in score_data_dict.keys():
        for score in score_data_dict[category]["details"]:
            score["score"] = scores_summary_data.loc[score["field"]]
        score_data_dict[category]["total"]["score"] = scores_summary_data.loc[score_data_dict[category]["total"]["field"]]

    """

    score_data_dict = {
        'transparency': {
            'details': [[
                c.SCORES.METHODOLOGY.PRINCIPLES_REF[i], c.SCORES.METHODOLOGY.PRINCIPLES_DESC[i],
                score_data[i], c.SCORES.METHODOLOGY.MAX_SCORES[i], ''
            ] for i in range(0, 3)],
            'total':
            score_data[3],
        },
        'commitments': {
            'details': [[
                c.SCORES.METHODOLOGY.PRINCIPLES_REF[i], c.SCORES.METHODOLOGY.PRINCIPLES_DESC[i],
                score_data[i], c.SCORES.METHODOLOGY.MAX_SCORES[i], ''
            ] for i in range(4, 8)],
            'total':
            score_data[8],
        },
        'actions': {
            'details': [[
                c.SCORES.METHODOLOGY.PRINCIPLES_REF[i], c.SCORES.METHODOLOGY.PRINCIPLES_DESC[i],
                score_data[i], c.SCORES.METHODOLOGY.MAX_SCORES[i], ''
            ] for i in range(9, 12)],
            'total':
            score_data[12],
        },
    }
    """

    print (score_data_dict)
    
    return score_data_dict

sheet_names = [
            'ghg_quant', 'corp_scores', 'score_summary', 'targets_quant',
            'score_details', 'library_db', 'reporting'
        ]

all_data = get_all_data_from_csv(sheet_names)

get_scores_summary(
    company_id=14,
    all_data=all_data['score_summary'])