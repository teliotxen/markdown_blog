def get_restapi_data(res):
    return eval(list(res.dict().keys())[0])
