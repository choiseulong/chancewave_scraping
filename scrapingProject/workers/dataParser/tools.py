def iterable_factor_element_true_check(factor):
    '''
        all([]) -> True
        all([1, 2, 3]) -> True
        all([1, 2, 0]) -> False
    '''
    return all(factor)
