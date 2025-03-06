from gigachat import GigaChat



def create_birt():
  with GigaChat(credentials="MDQ0MjUyM2QtYjQzYi00NDYyLWE5MjAtNjc4ZjNlYTcxNTIzOjA2OWFiMGZlLTJiODYtNGJlYS05ZmQzLTc4Nzc4MzhiM2QzYQ==", verify_ssl_certs=False) as giga:
      response = giga.chat("Составь поздравление с днем рождения для имени Анна")
      return (response.choices[0].message.content)

