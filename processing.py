import calls


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
