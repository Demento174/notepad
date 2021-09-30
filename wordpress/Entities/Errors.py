ERRORS = {
    'NotImplemented':'Method must be overridden',
    'TypeNotExist':" {0} type does not exist",
    'EntityNotExistID':"Query entity does not exist,type={0},id={1}",
    'EntityNotExistSlug':"Query entity does not exist,type={0},slug={1}",
    'EntitiesNotFound':"Query entities  not found, type={0}",
    'TermIsNotValidType':"Query term is not right type, term_type={0}, query_type={1}"
}

def errors_handler(ERROR,*args,**kwargs):
    return ERROR.format(*args)