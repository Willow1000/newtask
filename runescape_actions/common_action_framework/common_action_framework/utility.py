
def dictionary_readeable_print(temp_dict, exception_list=None, depth=0, is_printing=True):
    ret_str = ""
    if depth == 0:
        ret_str += "\n"
        ret_str += "printing dictionary properly:\n"
    ret_str += dictionary_readeable_print_aux(temp_dict, exception_list=exception_list, depth=0)
    if depth == 0:
        ret_str += "readeable dictionary printed" + "\n"
        ret_str += "\n"
    if is_printing:
        print(ret_str)
    return ret_str


def dictionary_readeable_print_aux(temp_dict, exception_list=None, depth=0):
    ret_str = ""
    if temp_dict is None:
        return str(temp_dict)
    for k in temp_dict:
        if isinstance(temp_dict, list) or isinstance(temp_dict, tuple):
            val = k
        elif isinstance(temp_dict, dict):
            val = temp_dict[k]
            ret_str += str('\t' * depth) + str(k) + "\n"
        else:
            # for unpredictable types just print
            ret_str += "unknown type of the following thing, printing as is the following line:\n"
            ret_str += str(temp_dict)
            ret_str += "\n"
            return ret_str
        if exception_list is not None:
            if k in exception_list:
                ret_str += str('\t' * depth) + str(k) + "\n"
                ret_str += "value: " + k + " in exception list, not printing further" + "\n"
                continue
        if val is None:
            print(f"val for key: {k} is null")
        if isinstance(val, dict) or isinstance(val, list) or isinstance(val, tuple):
            ret_str += str('\t' * (depth + 1)) + "another iterable inside current iterable:" + "\n"
            if isinstance(val, list) or isinstance(val, tuple):
                ret_str += dictionary_readeable_print_aux(val, exception_list, depth=depth)
            elif isinstance(val, dict):
                ret_str += dictionary_readeable_print_aux(val, exception_list, depth=(depth + 1))
            ret_str += str('\t' * (depth + 1)) + "done with current iterable:" + "\n"
        else:
            ret_str += str('\t' * (depth + 1)) + str(val) + "\n"
    return ret_str

