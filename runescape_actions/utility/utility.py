import json 
import inspect
import ast



def generate_function_whose_output_is_the_argument(argument):
    """
    Generates a function that returns the argument passed to it.
    :returns : function: A function that, when called, returns the argument.
    """
    def function_to_return():
        return argument
    return function_to_return


def replace_unset_with_none(input_d):
    """
    Replace all values that are 'unset' with None in the given dictionary.
    Args:
        input_d (dict): The input dictionary
    transforms the input dictionary in place, does not return anything
    this is required because when sending None through the network, all the None values must be turned to string, you 
     may want to turn them back to None, for consistency, however, BEWARE, and take notice of the dangers of this approach
    """
    for key, val in input_d.items():
        if isinstance(val, dict):
            for inner_k, value in val.items():
                if value == 'unset':
                    val[inner_k] = None
                elif isinstance(value, (dict, list)):
                    val[inner_k] = replace_unset_with_none(value)
        elif isinstance(val, list):
            for i, item in enumerate(val):
                if item == 'unset':
                    val[i] = None
                elif isinstance(item, (dict, list)):
                    val[i] = replace_unset_with_none(item)
        else:
            if val == 'unset':
                input_d[key] = None
 
 
def parse_to_json(dict_to_parse):
   json_format = json.dumps(dict_to_parse)
   # add b'\r\n' at the end to send as a line
   # json_format = json_format + b'\r\n'
   json_format = bytes(json_format, encoding="ascii")
   return json_format
 
 
def json_to_dict(json_msg):
   """
   .loads() is different from .load()
   """
   return json.loads(json_msg)
 
 
def load_raw_json_message_to_dict(raw_json_msg):
   """
   loads raw message (bytes) to json and then to dict
   """
   json_msg = raw_json_msg.decode("ascii")
   return json_to_dict(json_msg)


def find_variable_details() -> tuple:
    """
    finds the name of the first argument variable from two frames above
     this is meant only to be called like in the following example:
        def test_func(a):
            print(find_variable_name())  # find_variable_name frame above var name is: "a" and two above it is: "test_var"
        test_var = "test"
        test_func() # prints test_var
      **notice that there is NO argument, that's because it always gets the first argument
    :returns tuple with (name of variable, line number, file name)
    """
    frame = inspect.currentframe()
    try:
        caller_frame = frame.f_back
        caller_caller_frame = caller_frame.f_back

        if caller_caller_frame is None:
            return None

        caller_lineno = caller_caller_frame.f_lineno
        caller_filename = caller_caller_frame.f_code.co_filename
        caller_function_name = caller_frame.f_code.co_name

        with open(caller_filename, 'r') as f:
            source = f.read()

        # Parse the entire file
        tree = ast.parse(source)

        # Find the function call on the specific line
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and
                    hasattr(node, 'lineno') and
                    node.lineno == caller_lineno):

                # Check if this is a call to our caller function
                if (isinstance(node.func, ast.Name) and
                        node.func.id == caller_function_name and
                        node.args):

                    # Get the first argument (assuming that's what we want)
                    first_arg = node.args[0]
                    if isinstance(first_arg, ast.Name):
                        return (first_arg.id, caller_lineno, caller_filename)

        return None
    except Exception:
        return None
    finally:
        del frame

 
def dictionary_readeable_print(temp_dict, exception_list=None, depth=0, is_printing=True):
    temp_tup = find_variable_details()
    if temp_tup:
        var_name, line, file = temp_tup
        print(f"dictionary readeable print called, with variable name: {var_name}, from line: {line}, from file: {file}")
        print(f"search for: dictionary_readeable_print({var_name}), in file: {file}")
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
            ret_str += str('\t' * (depth + 1)) + "another iterable inside current iterable"
            if isinstance(val, list):
                ret_str += "(list)"
            elif isinstance(val, tuple):
                ret_str += "(tuple)"
            elif isinstance(val, dict):
                ret_str += "(dict)"
            ret_str += ":" + "\n"
            if isinstance(val, list) or isinstance(val, tuple):
                ret_str += dictionary_readeable_print_aux(val, exception_list, depth=depth)
            elif isinstance(val, dict):
                ret_str += dictionary_readeable_print_aux(val, exception_list, depth=(depth + 1))
            ret_str += str('\t' * (depth + 1)) + "done with current iterable:" + "\n\n"
        else:
            ret_str += str('\t' * (depth + 1)) + str(val) + "\n"
    return ret_str


