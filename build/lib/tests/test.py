import functions

function_dict = {
    "CompareModel" = functions.CompareModel_test
}

def test_x(function_name):
    """
    params function_name(str): name of functions 
    
    return 0 if successful 
    """
    return function_dict[function_name]()