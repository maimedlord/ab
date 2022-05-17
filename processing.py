import calls


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
'''
def get_user_record(email, pass_word):
    user_record = calls.get_user_record(email, pass_word)
    if user_record == {"error": "no record found"}:
        return {}
    else:
        return user_record


if __name__ == '__main__':
    print(get_user_record('theman@gmail.com', 'passwordpass'))