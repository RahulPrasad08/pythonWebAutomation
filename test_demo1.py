import pytest

@pytest.mark.pre
def test_m1():
    a = 3
    b = 4
    assert a+1 == b, "test failed"
    assert a==b, "test failed as a is not equal to b"

@pytest.mark.pre
def test_m2():
    name = ("selenium")
    assert name.upper()=="SELENIUM"

@pytest.mark.pre
def test_m3():
    assert True

def test_m4():
    assert False

@pytest.mark.pre
def test_m5():
    assert 100 == 100

def test_m6():
    assert 100 == 90

def test_Login():
    print("Ranchi")
