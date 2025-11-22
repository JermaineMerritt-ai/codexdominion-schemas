from engines import (
    crown_engine,
    continuum_engine,
    custodian_engine,
    concord_engine,
    transmission_engine,
    reflection_engine,
    blessing_engine
)

def test_engines():
    df = {}
    cycle_map = {'cycle': 'alpha'}
    custodian_registry = {'custodian': 'main'}
    df = crown_engine(df)
    df = continuum_engine(df, cycle_map)
    df = custodian_engine(df, custodian_registry)
    df = concord_engine(df)
    df = transmission_engine(df)
    df = reflection_engine(df)
    df = blessing_engine(df)
    print("Final df:", df)

if __name__ == "__main__":
    test_engines()
