from enum import Enum
from datetime import datetime
from uuid import uuid4
from json import dumps



class TxType(Enum):
  debit = 0
  credit = 1



class Tx:

  def __init__(self, amount, tx_type):
    self.amount = amount
    self.tx_type = tx_type
    self.__uuid = uuid4()
    self.created_at = datetime.now()

  def to_json(self):
    data = {
      "uuid": f"{self.__uuid}",
      "tx_type": self.tx_type.value,
      "amount": self.amount,
      "created_at": self.created_at.isoformat(),
    }
    return dumps(data)

  def get_uuid(self):
    return self.__uuid

  def to_line(self):
    amount = ""
    if self.tx_type == TxType.debit:
      amount = f"+{self.amount}"
    else:
      amount = f"-{self.amount}"
    line = f"{self.created_at}\t{self.__uuid}\t{amount}"
    return line

  def __str__(self):
    return f"Tx(uuid='{self.__uuid}', tx_type='{self.tx_type}', created_at='{self.created_at}', amount='{self.amount}')"



class Account:

  def __init__(self, name, balance=1000):
    self.name = name
    self.balance = balance
    self.__uuid = uuid4()
    self.__txs = []

  def __update_balance(self, amount):
    self.balance += amount

  def __create_tx(self, amount, tx_type):
    tx = Tx(amount, tx_type)
    self.__txs.append(tx)
    return tx



  def withdraw(self, amount):
    if self.balance < amount:
      raise Exception("Ошибка. Недостаточно средств.")
    tx = None
    try:
      tx =self.__create_tx(amount, TxType.credit)
      self.__update_balance(-amount)
    except:
      raise Exception("Проихошла непредвиденная ошибка") 
    return tx


  def deposit(self, amount):
    tx = None
    try:
      tx =self.__create_tx(amount, TxType.debit)
      self.__update_balance(amount)
    except:
      raise Exception("Произошла непредвиденная ошибка") 
    return tx



  def get_tx(self, uuid):
    for tx in self.__txs:
      if tx.get_uuid() == uuid:
        return tx
    return None



  def print_statement(self):
    for tx in self.__txs:
      print(tx.to_line())



  def dump_statement(self):
    with open("statement.json", "w+") as file:
      comma = ""
      file.write("[")
      for tx in self.__txs:
        file.write(f"{comma}{tx.to_json()}")
        if comma == "":
          comma = ", "
      file.write("]")



  def __str__(self):
    return f"Account(uuid='{self.__uuid}', name='{self.name}', balance='{self.balance}')"



def main():
  print("Создаем новый аккаунт.")
  account = Account("Мой аккаунт")
  print(f"\nНовый аккаунт создан: {account}")

  print(f"\nПроверяем баланс: {account.balance}")

  print("\nСовершаем операции.")
  account.deposit(200)
  account.withdraw(300)
  account.deposit(20)
  account.withdraw(334)
  account.withdraw(571)
  account.deposit(712)
  print(f"\nСнова проверяем баланс: {account.balance}")

  print("\nСмотрим выписку.")
  account.print_statement()

  print("\nСохраняем выписку в файл statement.json в формате json.")
  account.dump_statement()

  print("\nПробуем вывести больше чем есть.")
  try: 
    account.withdraw(999999)
  except Exception as e:
    print(e)

  print("\nДобавляем на счет 1 и запоминаем uuid операции, чтобы использовать в дальнейшем.")
  tx = account.deposit(1)
  uuid = tx.get_uuid()
  print(f"uuid операции: {uuid}")

  print("Получаем данные по совершенной операции по uuid.")
  print(account.get_tx(uuid))



main()


