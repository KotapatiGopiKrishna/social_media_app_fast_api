import pytest
from social_media_app.calculations import InsufficientFunds, add, subtract, multiply, divide,BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3,5,8),
    (45,55,100),
    (13,25,38),
    (15,30,45)
    ])
def test_add(num1, num2, expected):
    assert add(num1,num2) == expected

def test_subtract():
    assert subtract(9,3) == 6

def test_multiply():
    assert multiply(5,3) == 15
    assert multiply(15,3) == 45

def test_divide():
    assert divide(15,3) == 5

def test_bank_set_inital_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(25)
    assert bank_account.balance == 25
    
def test_deposit(bank_account):
    bank_account.deposit(25)
    assert bank_account.balance == 75

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,2) == 55



@pytest.mark.parametrize("deposit, withdraw, expected", [
    (200,100,100),
    (55,45,10),
    (25,25,0),
    (100,30,70)
    ])
def test_bank_transaction(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

@pytest.mark.parametrize("withdraw", [
    (100),
    (55)
    ])
def test_insufficient_funds(bank_account,withdraw):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(withdraw)