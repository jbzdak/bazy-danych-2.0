

Wykład 7: Object Relational Mapping
===================================


Zadanie do wykonania na ćwiczeniach
-----------------------------------

1. Opracowanie ORM dla schematu z trzecich zajęć.
2. Przetestowanie podanego schematu za pomocą ORM 

Wstęp teoretyczny
-----------------

Do komulniakcji aplikacji z systemem bazodanowym rzadko służy kod SQL pisany
przez programistę, najczęściej posługujemy się narzędziami, które pozwalają
na automatyczne generowanie kodu ``SQL``, oraz pozwalają na manipulowanie
zawartościa bazy danych za pomocą obiektów. Takie operowanie na obiektach ma
ma takie zalety:

* Po wybraniu danych z bazy danych możemy zapomnieć skąd one pochodzą,
  strona wyświetlająca dane o absolwencie nie wie w jakiej on jest tabeli,
  ani jak jest implementowana relacja między absolwentem a pracą dyplomową.
* Możemy łatwo separować poszczególne poziomy aplikacji --- osoba pisząca
  stronę WWW nie musi znać SQL, ani wiedzieć w jak dane przechowywane są w
  bazie danych.
* Pewne operacje pisze się szybciej za pomocą ORM niż SQL.
  * Na przykład stworzenie zapytania składającego się z 50 joinów, wymaga
  napisania pętli ``for``.
* W chwili wybierania danych z bazy nie musimy wiedzieć jakie dane będą
  potrzebne (mogą zostać pobrane później)
* Kod operujący na ORM z reguły może działać na wielu bazach danych, jest to
  istotne nie tyle dla twórców aplikacji (np. strony WWW), ale dla twórców
  bibliotek z których te aplikacje korzystają.


Wieloplatformowość ORM
----------------------

Systemy ``ORM`` pozwalają na współpracę jednego systemu z wieloma bazami danych,
w tym celu konieczne jest wykorzystanie dwóch oddzielnych elementów:

* Generatora kodu ``SQL`` na wiele platform (w wielu dialektach ``SQL``)
* Sterowników które pozwalają na łączenie się z różnymi bazami dancyh.

W Javie głównym narzędziem uzyskiwania dostępu do bazy danych jest interfejs
``JDBC`` oraz poszczególne sterowniki. W pythonie jest to `Database Api 2.0
<http://www.python.org/dev/peps/pep-0249/>`_.

.. figure:: /wyk7/schemat-orm.*

    ORM a sterowniki dostępu do bazy danych.



Język Python
============

Ponieważ ORM wykracza poza ``SQL`` musiałem wybrać jakiś inny język w jakim
będziemy pracować.

Z języków które Państwo znacie:

* W ``C`` nie ma żadnych rozwiązań ORM
* W ``C++`` są rozwiązania orm, ale szybkie ich przejrzenie pokazało mi że raczej
  nie da się zrobić w trzy godziny nic sensownego w tym temacie.
* W Javie jest bardzo dużo rozwiązań ORM, jednak najważniejsze narzędzie ``ORM``:
  `Java persistence API <http://en.wikipedia.org/wiki/Java_Persistence_API>`_,
  nie jest bardzo przyjazne użytkownikowi. Osobom zainteresowanym tym
  framweorkiem polecam książkę ``Enterprise Java Beans 3.0``
  (w bibliotece Wydziału).

Postanowiłem więc że poznacie Państwo ``ORM`` SQL Alchemy napisany w Pythonie.

Podstawy Pythona
----------------

Proszę zrobić zadania ze strony `Learn Python <http://www.learnpython.org/>`_ z
rozdziału Learn The Basics, oraz Exception Handling z następnego rodziału.

Warto też zapoznać się z sekcją: `Keyword Arguments <http://docs.python.org/release/3.2.5/tutorial/controlflow.html#keyword-arguments>`_
podanego dokumentu.

**Jest to bardzo ważne, jeśli macie akurat mało czasu to w ramach przygotowań zróbcie właśnie to**.

Testy jednostkowe
-----------------

Pojęcie testów jednostkowych nie jest bardzo ściśle związane z Pythonem, jednak
będziemy z nich korzystać. Testy jednostkowe to kawałki kodu,
które pozwalają na testowanie pojedyńczych zachowań testowanego systemu. Dokładna
lista zysków jest `przedstawiona na wikipedii
<http://en.wikipedia.org/w/index.php?title=Unit_testing&oldid=548838004>`_.

Test składa się z takich etapów:

1. Stworzenie środowiska do testów
2. Wykonanie inicjalizacji środowiska
3. Wykonanie testów
4. Zniszczenie środowiska testowego

Przykładowo to jest kod, który testował zadanie 2 z zajęć trzecich:


.. code-block:: python

    class TestSuite(Zaj3TestSuite):

        def test_create_students(self): # Test który testuje istnienie tabeli student.
            for _ in range(100): # Wykonujemy sto razy
                st = self.create_student() # Tworzymy testowego studenta
                self.session.add(st) # Zapisujemy go do sesji
                self.session.flush() # Zapisujemy do bazy danych

        def test_student_has_id_after_insert(self):
            for _ in range(3):
                st = self.create_student()
                self.session.add(st)
                self.session.flush()
                self.assertIsNotNone(st.id) # Sprawdzamy czy po
                    #dodaniu do bazy student ma ustawione ID

Wszystkie kroki związane z tworzeniem środowiska i jego kasowaniem są wykonywane
automatycznie.



Biblioteka unittest
-------------------

Jest to standatdowa biblioteka do przeprowadzania testów. Podstawową jednostką
pisania testów jest klasa, klasa taka zawiera jeden lub więcej testów:

.. literalinclude:: /examples/addition_test.py
   :linenos: 12-21

Jest to prostsze niż wygląda. Tesy to wszystkie metody których nazwy zaczynają
się od słowa ``test`` i są one automatycznie wykrywane i uruchamiane. W naszym
przykładzie są dwa testy.

Typowy test wygląda tak:

.. literalinclude:: /examples/addition_test.py
    :pyobject: TestMathematics.test_addition


Składa się on z dwócu etapów:

1. Wykonania testowanego kodu (linia 15)
2. Sprawdzenia jego wyników (linia 16)

Dodatkowo oprócz testów mamy metody które ustawiają środowisko i je usuwają.

Metoda ``setUp`` jest wykonywana każdorazowo przed każdym testem, metoda
``setUpClass`` przed uruchomieniem całej klasy testów.

Metoda ``tearDown`` jest wykonywana po każdym teście, a metoda ``tearDownClass``
uruchamiana jest po wykonaniu całej klasy testów.

Uruchamianie testów unittest
----------------------------

By uruchomić testy z pliku :download:`/examples/addition_test.py` należy pobrać go
i w katalogu w którym go pobrano wykonać polecenie:

.. code-block:: bash

    python -m unittest addition_test.py

SQL Alchemy
===========

SQL Alchemy jest jedną z bibliotek ORM w Pythonie, jest warta poznania ponieważ
nie nakłada żadnych ograniczeń na schemat jaki opisuje.

Sterowniki dostępu do bazy danych
---------------------------------

Do współpracy z bazą danych biblioteka potrzebuje sterowników do bazy danych
postgresql, sterownikiem takim jest`psycopg2
<http://initd.org/psycopg/install/>` (na zajeciach będzie zainstalowany).

Pojęcie modelu
--------------

Między językiem SQL a ORM można znaleźć takie tłumaczenie:

* Tabela -> Model (lub encja)
* Wiersz w tabeli -> instancja modelu
* Połączenie do bazy danych -> Sesja

Model to klasa która odwzorowuje tabelę, instancja danego modelu odwzorowuje
dany wiersz.

Przypomnienie schematu
----------------------

.. figure:: /wyk7/db-schema.*

Ustawienie modułu zawierającego encje
-------------------------------------

Najpierw importujemy potrzebne obiekty

.. literalinclude:: /examples/tag.py
    :lines: 1-8

Base jest dynamicznie generowaną klasą bazową dla naszych modeli.

Definiujemy klasę:

.. literalinclude:: /examples/tag.py
    :pyobject: Tag


Klasa ta dziedziczy po Base:

.. literalinclude:: /examples/tag.py
    :lines: 10

Następnie definiujemy że klasa ta odwzorowuje dane w tabeli "TAG":

.. literalinclude:: /examples/tag.py
    :lines: 11

Oraz zawiera dwie kolumny: ``key`` oraz ``label`` które zawierają typ ``character
varying``.

.. literalinclude:: /examples/tag.py
    :lines: 12-13

Dalsze definicje **nie mają nic wspólnego z ``ORM``**, są użyte dla wygody i
wspomagają pisanie testów.

Metoda ``__init__`` (od inicjalizacjja) definiuje konstruktor obiektu,
metoda ``__eq__`` (jej nazwa pochodzi od equals) określa
działanie operatora ``==``, a metoda ``__repr__`` określa jak dany obiekt będzie
wyświetlany na konsoli.


Uzyskiwanie połączenia z bazą danych
------------------------------------

Wykonanie operacji na bazie danych za pomocą SQL Alchemy można wykonać
za pomocą takich kroków:

1. Uzyskanie `'silnika' <http://docs.sqlalchemy.org/en/rel_0_8/core/engines.html>`_
   silnik uzyskuje połączenia z bazą danych.
2. Uzyskanie `sesji <http://docs.sqlalchemy.org/en/latest/orm/session.html>`_
   za pomocą silnika.
3. Wykonanie zapytań za pomocą sesji.

Uzyskanie silnika
-----------------

Silniki uzyskuje się za pomocą metody ``create_engine``, która przyjmuje adres
bazy danych w następujacym formacie:

.. code-block:: none

    postgresql+psycopg2://scott:tiger@localhost/mydatabase
    ^          ^          ^     ^      ^        ^
    baza danych|          użtkow|nik   host     baza danych
               sterownik        hasło


Na przykład

.. code-block:: python

    engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')

Uzyskanie sesji
---------------

Najpierw tworzymy klasę sesji:

.. code-block:: python

    Session = sessionmaker(bind=some_engine)z

Następnie możemy stworzyć instancję sesji:

.. code-block:: python

    session = Session()

Zapisanie tagu do bazy danych:

.. code-block:: python

    session.add(Tag("status:student",  "Student")) # Tag dodany do sesji
    session.commit() # Tag wysłany do bazy danych i zapisany

Wykonanie zapytania
-------------------

Do wykonywania zapytań służy metoda ``query`` na obiekcie ``session``:

.. code-block:: python

    session.query(Tag).all()

Pełny przykład :download:`/examples/tag.py`

Wykonanie przykładu
-------------------

1. Należy zainstalować pythona
2. Należy zainstalować `SQL Alchemy <http://www.sqlalchemy.org/download.html>`_
3. Proszę wykonać: ``python tag.py``.

Zadania na wejściówce
=====================

1. Prawodopodobnie będzie kilka zadań z Pythona.

Zadanie do zrobienia na zajęciach
=================================

Podaje zgrubny opis żebyście Państwo nie panikowali

1. Dopisanie modeli dla studenta i pracownika (wraz z relacjami)
2. Napisanie kodu testującego schematy (przy czym bazę danych ustawiam ja)


