import calls
from datetime import datetime, timedelta


'''
'''
def get_orders_top():
    get_array = list(calls.get_orders_top())
    loop_array = []
    return_array = []
    for element in get_array:
        loop_array.append(element["orderID"])
        loop_array.append(element["dateOpen"])
        loop_array.append(element["level"])
        loop_array.append(element["subject"])
        loop_array.append(element["status"])
        loop_array.append(element["contract"]["commitment"])
        loop_array.append(element["contract"]["finalPrice"])
        return_array.append(loop_array)
        loop_array = []
    return return_array


'''
INCOMPLETE
WHERE IS THIS?
'''
def get_user_record(email, password):
    user_record = calls.get_user_record(email, password)
    if user_record == {"error": "no record found"}:
        return {}
    else:
        return user_record


'''
INCOMPLETE: 
NEED TO VERIFY ALL INPUT HERE BEFORE SENDING TO CALLS
good return = array of validated form data
'''
def process_new_contract(form_dict):
    # handle a malformed dictionary...
    print_arr = []
    user_obj = {}
    bounty = form_dict['c_f_bounty']
    user_obj.update({"bounty": bounty})
    e_f_bonus = form_dict['c_f_efbonus']
    if e_f_bonus == "":
        e_f_bonus = 0
    user_obj.update({"e_f_bonus": e_f_bonus})
    e_g_bonus = form_dict['c_f_egbonus']
    if e_g_bonus == "":
        e_g_bonus = 0
    user_obj.update({"e_g_bonus": e_g_bonus})
    g_deadline = form_dict['c_f_t_g_deadline']
    if g_deadline != "":
        g_deadline = datetime.fromisoformat(form_dict['c_f_t_g_deadline'] + 'T' + form_dict['c_f_t_g_d_time'] + ':00.000000')
    user_obj.update({"g_deadline": g_deadline})
    lostudy = form_dict['c_f_lostudy']
    user_obj.update({"lostudy": lostudy})
    sample = form_dict['c_f_sample']
    user_obj.update({"sample": sample})
    specialization = form_dict['c_f_specialization']
    user_obj.update({"specialization": specialization})
    stall_iso = datetime.fromisoformat(form_dict['c_f_t_stall'] + 'T' + form_dict['c_f_t_s_time'] + ':00')
    user_obj.update({"stall_iso": stall_iso})
    start_iso = datetime.fromisoformat(datetime.now().isoformat()[:-7])
    user_obj.update({"start_iso": start_iso})
    type_contract = form_dict['c_f_type']
    user_obj.update({"type_contract": type_contract})
    print_arr.append(bounty)
    print_arr.append(e_f_bonus)
    print_arr.append(e_g_bonus)
    print_arr.append(g_deadline)
    print_arr.append(lostudy)
    print_arr.append(sample)
    print_arr.append(specialization)
    print_arr.append(stall_iso)
    print_arr.append(start_iso)
    print_arr.append(type_contract)
    if type_contract == 'assignment':
        a_deadline_iso = datetime.fromisoformat(form_dict['c_f_t_a_deadline'] + 'T' + form_dict['c_f_t_a_d_time'] + ':00')
        user_obj.update({"a_deadline_iso": a_deadline_iso})
        print_arr.append(a_deadline_iso)
        print(print_arr)
        return user_obj
    if type_contract == 'test':
        t_start_iso = datetime.fromisoformat(form_dict['c_f_t_t_start'] + 'T' + form_dict['c_f_t_t_s_time'] + ':00')
        user_obj.update({"t_start_iso": t_start_iso})
        t_end_iso = datetime.fromisoformat(form_dict['c_f_t_t_end'] + 'T' + form_dict['c_f_t_t_e_time'] + ':00')
        user_obj.update({"t_end_iso": t_end_iso})
        print_arr.append(t_start_iso)
        print_arr.append(t_end_iso)
        print(print_arr)
        return user_obj
    return None


if __name__ == '__main__':
    print(get_user_record('theman@gmail.com', 'passwordpass'))