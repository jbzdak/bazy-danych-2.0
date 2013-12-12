
.. testsetup:: *

    import orm
    import settings
    from operator import attrgetter

    orm.Base.metadata.drop_all(settings.engine)
    TAGS = [
        orm.Tag("status:student",  "Student"),
        orm.Tag("status:doktorant",  "Doktorant"),
        orm.Tag("status:absolwent",  "Absolwent"),
        orm.Tag("praca:inz",  "Praca Inżynierska"),
        orm.Tag("praca:mgr",  "Praca Magisterska"),
        orm.Tag("praca:dr",  "Praca Doktorska")
    ]

    TAGS = sorted(TAGS, key=attrgetter("key"))

    from sqlalchemy.schema import CreateTable
    from sqlalchemy.orm import relationship

ORM (zajęcia 8 i 9)
===================


Wstęp
------

1. IDE do pythona proszę użyć dowolne (ja polecam spydera ---
   powinien być zainstalowany). Osoby zainteresowane mogą profesjonalny edytor
   pycharm w wersji open-source: `stąd <https://www.jetbrains.com/pycharm/download/index.html>`_.
2. Startowy projekt: :download:`/data/zaj_7_initial_stud.zip`

Część A: Stworzenie ORM (zajęcia 8)
===================================

Cześć A polega na stworzeniu klas ORM. Zadanie to nie będzie podlegało
formalnemu sprawdzeniu, tj. nie będzie oceniane, jednak jego prawidłowe wykonanie
będzie konieczne do sprawdzenia dalszej części prac

.. figure:: /wyk7/db-schema.*

Wykonanie zadania w domu
------------------------

1. Należy zainstalować pythona w wersji 2.7.3 (nie znalazłem używalnego
   darmowego ide działającego pod pythonem 3). Przykłady powinny działać
   zarówno w 2.7.x jak i w 3.3
2. Należy zainstalować `SQL Alchemy <http://www.sqlalchemy.org/download.html>`_
3. Należy zainstalować sterownik dostępu do bazy danych postgres
   `psycopg2 <http://initd.org/psycopg/download/>`_
4. Dobrze jest zainstalować sobie jakieś IDE do pythona
 a. Może być to `spyder <http://code.google.com/p/spyderlib/>`_
 b. Może być to `pycharm https://www.jetbrains.com/pycharm/download/index.html`_

Zadanie A.1: Używanie ORM z konsoli pythona
-------------------------------------------

Proszę przejśc do katalogu w którym rozpakowaliście Państwo paczkę powitalną.

Proszę uruchomić interpreter pythona LUB środowisko spyder.

.. code-block:: bash

    python

Interpreter proszę uruchomić w katalogu ``zaj_7_initial`` w spyderze proszę
do wskazanego katalogu przejść.

Proszę wykonać po kolei wszystkie polecenia. W razie wątpliwości proszę pytać.

.. code-block:: python

    >>> import orm # import przykładowych modułów
    >>> import settings
    >>> sess = settings.Session() #Tworzymy sesję
    >>> sess.query(orm.Tag).all() #Wybieramy wszystkie tagi z bazy danych doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/usr/lib/python2.7/dist-packages/sqlalchemy/engine/default.py", line 331, in do_execute
        cursor.execute(statement, parameters)
    ProgrammingError: (ProgrammingError) relation "TAG" does not exist
    LINE 2: FROM "TAG"
         ^
    'SELECT "TAG".key AS "TAG_key", "TAG".label AS "TAG_label" \nFROM "TAG"' {}

Podany błąd był przewidywany! Generalnie chodzi o to że w bazie do której
się łączymy nie ma tabeli ``TAG``. Musimy zatem ją stworzyć.

Stworzenie wszystkich tabel w module ``orm`` (na razie jest to tylko ``Tag``)
odbywa się za pomocą polecenia:

.. code-block:: python

    >>> orm.Base.metadata.create_all(settings.engine)

Gdybyśmy chcieli skasować wszystkie tabele należy wykonać:

.. code-block:: python

    >>> orm.Base.metadata.create_all(settings.engine)
    >>> orm.Base.metadata.drop_all(settings.engine) # doctest: +SKIP

Możemy teraz wrócić do wybierania danych:

.. code-block:: python

    >>> sess.query(orm.Tag).all() #Wybieramy wszystkie tagi z bazy danych doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/usr/lib/python2.7/dist-packages/sqlalchemy/engine/default.py", line 331, in do_execute
        cursor.execute(statement, parameters)
    InternalError: (InternalError) current transaction is aborted, commands ignored until end of transaction block
     'SELECT "TAG".key AS "TAG_key", "TAG".label AS "TAG_label" \nFROM "TAG"' {}

Jeszcze jeden problem: poprzedni błąd spowodował że sesja (a raczej
odpowiadające jej połączenie bazodanowe jest w stanie w którym należy
najpierw wykonać polecenie rollback:

.. code-block:: python

    >>> sess.rollback()
    >>> sess.query(orm.Tag).all() #Wybieramy wszystkie tagi z bazy danych doctest: +IGNORE_EXCEPTION_DETAIL
    []

Nasze polecenie zwraca pustą listę, co znaczy że w bazie danych ``TAG``ów nie ma
(co raczej nie powinno dziwić, skoro przed chwilą stworzyliśmy tą tabelę.

Stwórzmy więc jakieś tagi:

.. code-block:: python

    >>> sess.add(orm.Tag("status:student",  "Student"))
    >>> sess.add(orm.Tag("status:doktorant",  "Doktorant"))
    >>> sess.query(orm.Tag).all()
    ['<Tag status:student:Student>', '<Tag status:doktorant:Doktorant>']

Wreszcie udało nam się coś wybrać z bazy danych. Ale dane jeszcze nie trafiły do
bazy danych, by się o tym przekonać otwórzmy nową sesję.

.. code-block:: python

    >>> sess2 = settings.Session()
    >>> sess2.query(orm.Tag).all()
    []

Druga sesja nie widzi zmian. Musimy jeszcze skomitować pierwszą sesję:


.. code-block:: python

    >>> sess.commit()
    >>> sess2.query(orm.Tag).all()
    ['<Tag status:student:Student>', '<Tag status:doktorant:Doktorant>']
    >>> sess.query(orm.Tag).filter(orm.Tag.key.like("status:st%")).all()
    ['<Tag status:student:Student>']
    >>> sess2.close()


Zadanie A.2: Dodanie wierszy do tabeli TAG
------------------------------------------

Zadanie:

1. Proszę stworzyć listę zawierającą wszystkie potrzebne wiersze z tabeli tag.
2. Proszę dodać wszystkie ``TAG`` do bazy danych
3. **challenge:** proszę wykonać funkcję (która będzie automatycznie wykonywana
   przy starcie programu) która będzie wykonywać takie rzeczy:
   a. Jeśli nie ma tabel dla modeli tworzy je
   b. Dodaje do bazy danych wszystkie potrzebne tagi (jeśli ich nie ma)


**Lista tagów**

======================== ============================
key                      label
======================== ============================
status:student           Student
status:doktorant         Doktorant
status:absolwent         Absolwent
praca:inz                Praca Inżynierska
praca:mgr                Praca Magisterska
praca:dr                 Praca Doktorska
======================== ============================


Sprawdzenie zadania A.2
-----------------------

Kasujemy wcześniej stworzone tagi i tworzymy pełny zestaw:

.. code-block:: python

    >>> sess.query(orm.Tag).delete()
    2
    >>> for t in TAGS: # <- to jest przykład, musicie stworzyć Własne tagi!
    ...     sess.add(t)
    >>> sess.commit()

Proszę sprawdzić czy macie podobny wynik:

.. code-block:: python

    >>> sess.query(orm.Tag).order_by('key').all() # doctest: +NORMALIZE_WHITESPACE
    ['<Tag praca:dr:Praca Doktorska>', '<Tag praca:inz:Praca In\u017cynierska>',
     '<Tag praca:mgr:Praca Magisterska>', '<Tag status:absolwent:Absolwent>',
     '<Tag status:doktorant:Doktorant>', '<Tag status:student:Student>']

Proszę jeszcze sprawdzić czy dane na pewno są w bazie danych za pomocą
polecenia ``psql``. Nasz ORM może nawet wygenerować Wam SQL:

.. code-block:: python

    >>> print(sess.query(orm.Tag).order_by('key')) # doctest: +NORMALIZE_WHITESPACE
    SELECT "TAG".key AS "TAG_key", "TAG".label AS "TAG_label"
    FROM "TAG" ORDER BY key

Zadanie A.3 Stworzenie klas odwzorowujących studenta, pracownika i pracę dyplomową
----------------------------------------------------------------------------------


Tworzenie modeli w SQL Alchemy
------------------------------

By stworzyć model tworzymy klasę dziedziczącą po Base:

.. testcode::

    from orm import *

    class TabA(Base):

        __tablename__ = "TAB_A" #Określa tabelę którą odwzorowujemy

        id = Column(Integer(), primary_key = True) # Klucz główny określamy za pomocą keyword argument
        foo = Column(String()) # Jakaś kolumna

Obejrzyjmy sobie wygenerowany kod SQL :


.. code-block:: python

    >>> from sqlalchemy.schema import CreateTable
    >>> print(CreateTable(TabA.__table__)) # doctest: +NORMALIZE_WHITESPACE
    CREATE TABLE "TAB_A" (
    	id INTEGER NOT NULL,
    	foo VARCHAR,
    	PRIMARY KEY (id)
    )


By pokazać definiowanie kluczy swórzmy drugą tabelę:

.. testcode::

    class TabB(Base):

        __tablename__ = "TAB_B"

        id = Column(Integer(), primary_key = True)
        bar = Column(String())
        a = Column(Integer(), ForeignKey("TAB_A.id", name = "tab_a_fkey"))
        a_inst = relationship("TabA", backref ="b_inst")


Obejrzyjmy sobie wygenerowany kod SQL :


.. code-block:: python

    >>> print(CreateTable(TabB.__table__)) # doctest: +NORMALIZE_WHITESPACE
    CREATE TABLE "TAB_B" (
    	id INTEGER NOT NULL,
    	bar VARCHAR,
    	a INTEGER,
    	PRIMARY KEY (id),
    	CONSTRAINT tab_a_fkey FOREIGN KEY(a) REFERENCES "TAB_A" (id)
    )



Treść polecenia
----------------

Proszę stworzyć modele odwzorowujące tabele student i pracownik

1. Klucze główne obu tabel są typu ``SERIAL`` w bazie danych (to akurat jest proste
   bo starczy napisać że kolumna jest typu ``Integer`` i jest kluczem głównym).
2. Wszystkie kolumny które powiny być ``non-null`` są non-null
3. Pole ``status`` w modelu ``Student`` jest kluczem obcym do tabeli
4. **challenge:** Pola które powinny mieć ograncizenia, które implementowaliśmy
   za pomocą ograniczenia ``CHECK`` mają to ograniczenie zdefiniowane.



Sprawdzenie zadania A.3
-----------------------

**Poprawne dane**

Najpierw czyścimy sesję (tak te przykłady *są wykonywane*):

Państwo w tym momencie restartują interpreter.

.. code-block:: python

    >>> sess.close()
    >>> sess = settings.Session()

Tworzymy studenta:

.. code-block:: python

    >>> s = orm.Student(name="Jacek", surname="Bzdak", gender=0, status="status:doktorant")
    >>> sess.add(s)
    >>> print(s.id)
    None

na razie jego ID jest puste (``None`` to odpowiednik ``null`` w Pythonie).
Jest puste ponieważ odpowiednia instrukcja ``INSERT`` nie trafiła jeszcze
do bazy danych. SQL Alchemy stara się dotykać do bazy danych jak najrzadziej,
więc czeka a nóż pojawi się więcej obiektów, które zostaną dodane za jednym
razem.

By wymusić wysłanie danych należy wykonać:

.. code-block:: python

    >>> sess.flush()
    >>> s.id is not None
    True
    >>> print(s.id)
    1

Dane ciągle nie są zapisane do bazy do tego musimy wykonać:

.. code-block:: python

    >>> sess.commit()


Proszę dodać jeszcze paru studentów (najlepiej zapisać kod ich dodający!).


**Niepoprawne dane**

.. code-block:: python

    >>> s = orm.Student(name="Jacek", surname="Bzdak", gender=0, status="zly staus")
    >>> sess.add(s)
    >>> sess.commit() # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    IntegrityError: (IntegrityError) insert or update on table "STUDENT" violates foreign key constraint "STUDENT_status_fkey"
    DETAIL:  Key (status)=(zly staus) is not present in table "TAG".
     'INSERT INTO "STUDENT" (name, surname, gender, status, message) VALUES (%(name)s, %(surname)s, %(gender)s, %(status)s, %(message)s) RETURNING "STUDENT".id' {'status': 'zly staus', 'gender': 0, 'message': None, 'surname': 'Bzdak', 'name': 'Jacek'}

    >>> sess.rollback()
    >>> sess.add(orm.Student())
    >>> sess.commit() # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    IntegrityError: (IntegrityError) null value in column "name" violates not-null constraint
     'INSERT INTO "STUDENT" (name, surname, gender, status, message) VALUES (%(name)s, %(surname)s, %(gender)s, %(status)s, %(message)s) RETURNING "STUDENT".id' {'status': None, 'gender': None, 'message': None, 'surname': None, 'name': None}

Zadanie A.4: Obsługa relacji
----------------------------

Mamy już tabele, które zawierają klucze obce.
Teraz wypadałoby do nich dodać relacje.


Co to relacje
-------------

Relacja (termin mniej lub bardziej ustalony) oznacza metodę dostęp do wierszy
które są powiązane za pomocą bazodanowych relacji (zatem i kluczy obcych)

Na poziomie bazy danych wiemy że w kolumnie ``status`` w tabeli ``STUDENT``
mamy klucz obcy do kolumny ``key`` w tabeli ``TAG``. Relacje pozwalają nam
na obiektowy dostęp do tych zdalnych wierszy.

Relację ustawialiśmy już w poprzednim przykładie:

.. code-block:: python

    class TabB(Base):

        __tablename__ = "TAB_B"

        id = Column(Integer(), primary_key = True)
        bar = Column(String())
        a = Column(Integer(), ForeignKey("TAB_A.id", name = "tab_a_fkey"))
        a_inst = relationship("TabA", backref = "b_inst")

Tabele są tak połączone że w ``TabB`` w kolumnie ``a`` jest klucz obcy do ``TabA``,
relacje pozwalają nam na udawanie że te klucze obce zawierają odniesienia do
obiektów.

Tworzymy tabele A i B:

.. code-block:: python

    >>> orm.Base.metadata.create_all(settings.engine)
    >>> sess.close()

Tworzymy nową sesję, dwa obiekty i zapisujemy je do bazy danych

.. code-block:: python

    >>> sess = settings.Session()
    >>> a = TabA()
    >>> b = TabB()
    >>> sess.add(a)
    >>> sess.add(b)
    >>> sess.flush()

Sprawdzamy ID pierwszej tabeli:

.. code-block:: python

    >>> a_id = a.id

Przypisuje do wiersza w tabeli ``TabB`` do kolumny ``a`` klucz główny do tabeli
``TabA``.

.. code-block:: python

    >>> b.a = a_id
    >>> sess.add(b)
    >>> sess.flush()

Od tej chwili w instancji ``b`` w artybucie ``a_inst`` siedzi *obiekt* którego klucz
jest w kolumnie ``a``

.. code-block:: python

    >>> print(b.a_inst) # doctest: +ELLIPSIS
    <TabA object at 0x...>

Podana relacja jest dwustronna, obiekt ``a`` *wie* że ``b`` się do niego odnosi:

.. code-block:: python

    >>> a.b_inst # doctest: +ELLIPSIS
    [<TabB object at 0x...>]

To pod jaką nazwą dostępna jest relacja wsteczna w naszym przykładzie ```b_inst```,
wynika z podania argumentu o nazwie ```backref```. 

Podsumowanie relacji
--------------------

Relacje to coś co pozwala nam odnosić się do innych obiektów, które powiązane są


Treść polecenia
----------------

1. Proszę dodać relacje między studentem a pracą dyplomową.
2. Proszę dodać relację między pracownikiem a pracą dyplomową


Sprawdzenie
-----------

.. code-block:: python

    >>> s = orm.Student(name="Jacek", surname="Bzdak", gender=0, status="status:doktorant")
    >>> p = orm.Pracownik(name="Jacek", surname="Bzdak", gender=0, status="status:doktorant")
    >>> sess.add(s)
    >>> sess.add(p)
    >>> sess.flush()

Dodajemy pracę dyplomową odnoszącą się do ``s`` i ``p``:

    >>> pd = orm.PracaDyplomowa(tytul="Badanie Foo!", type = "praca:inz")
    >>> pd.dyplomant = s
    >>> pd.promotor = p
    >>> sess.add(pd)
    >>> sess.flush()

Sprawdzamy czy student *wie* już o pracy która się do niego odnosi:

    >>> s.prace_dyplomowe # doctest: +ELLIPSIS
    [<orm.PracaDyplomowa object at ...>]
    >>> p.prace_promowane
    [<orm.PracaDyplomowa object at ...>]


Challenge
---------

Dodać relacje Wiele-do-Wieku, między studentem a pracownikiem poprzez
pracę dyplomową.

Część B: Użycie ORM (zajęcia 9)
================================

Zapoznanie z kodem
------------------

Klasa bazowa testów znajduje się w pliku ``tester.py``

.. code-block:: python

    class SchemaUnittest(object):

        SCHEMA_FILE = "model_schema.sql"

        DATABASE = "bd"

        def setUp(self):
            load_script(StringIO("DROP SCHEMA public CASCADE;"), self.DATABASE)
            load_script(StringIO("CREATE SCHEMA public;"), self.DATABASE)
            load_script(self.SCHEMA_FILE, self.DATABASE)


        def tearDown(self):
            load_script(StringIO("DROP SCHEMA public CASCADE;"), self.DATABASE)
            load_script(StringIO("CREATE SCHEMA public;"), self.DATABASE)

Państwa testy muszą dziedziczyć po tym obiekcie i w poszczególnych metodach
powinny wykonywać testy.

By podmienić schemat który sprawdzamy należy zamienić wartość ``SCHEMA_FILE``.

Test sprawdzający czy ta się zapisać studenta:

.. code-block::python

    class CheckSchemaTestCase(tester.SchemaUnittest, unittest.TestCase):

        def test_create_student(self):
            sess = settings.Session()
            sess.add(orm.Student(name="Jacek", surname="Bzdak", gender=0, status="status:doktorant", message="foo"))
            sess.commit()


Testy pozytywne
===============

Są to testy w których sprawdzamy czy baza danych reaguje prawidłowo na
prawidłowe zapytania.

Do sprawdzenia:

1. Dodanie studenta
2. Dodanie pracownika
3. Sprawdzenie czy po dodaniu do bazy danych student ma nadane id
4. Sprawdzenie czy po dodaniu do bazy danych pracownik ma nadane id
5. Dodanie pracy dyplomowej

Asercje w testach
-----------------

Czasem możemy uznać ze test się udał, jeśli test nie zgłosił wyjątków,
czasem musimy wykonać odpowiednią asercję.

Asercje wykonujemy za pomocą metod wbudowanych w unittesta:

.. code-block:: python

    class CheckSchemaTestCase(unittest.TestCase):

        def test_addition_works(self):

            self.assertEqual(1+1, 2)
            self.assertTrue(1+1 == 2)
            self.assertFalse(1+1 == 3)
            self.assertNotEqual(1+1, 3)
            self.assertIsNone(1+1)
            self.assertIsNone(None)

Zamykanie sesji
---------------

Proszę pamiętać o zamykaniu sesji:

.. code-block:: python

    class CheckSchemaTestCase(tester.SchemaUnittest, unittest.TestCase):

        def test_create_student(self):
            sess = settings.Session()
            try:
                sess.add(orm.Student(name="Jacek", surname="Bzdak", gender=0, status="status:doktorant", message="foo"))
                sess.commit()
            finally:
                sess.close()


Challenge
---------

1. Stworzyć nadklasę która automatycznie otwiera i zamyka sesję.

2. W ramach testów dodać po 1000 studentów, pracowników i prac dyplomowych,
mających sensownie brzmiące i niepowtarzalne imiona i nazwiska.


Testy negatywne
===============

Są to testy w których testujemy jak baza danych reaguje na nieprawidłowe dane
(powinna zgłaszać wyjątek).

Jak sprawdzać czy baza danych zgłasza błąd.
-------------------------------------------

Jeśli wykonamy operację która powoduje błąd na poziomie bazy danych to
system ORM zgłosi nam wyjątek, teraz w naszych testach musimy wymagać by
podany wyjątek został zgłoszony:

.. code-block:: python

    class CheckSchemaTestCase(tester.SchemaUnittest, unittest.TestCase):

          def test_create_student_empty_name(self):
            """


            """
            raised_exception = False
            sess = settings.Session()
            try:
                sess.add(orm.Student(name=None, surname="Bzdak", gender=0, status="status:doktorant", message="foo"))
                sess.commit()
            except IntegrityError:
                raised_exception = True
            finally:
                sess.close()

            self.assertTrue(raised_exception)

Zadanie
-------

1. Sprawdzić czy da się stworzyć studenta z pustym: imieniem, nazwiskiem, statusem i wiadomością.
2. Sprawdzić czy da się stworzyć pracownika z pustym: imieniem, nazwiskiem i telefonem
3. Sprawdzić czy da się stworzyć pracownika z telefonem który wygląda niepoprawnie (10 różnych telefoów)
4. Sprawdzić czy da się stworzyć studenta ze statusem który nie ma odwzorowania w tabeli ``Tag``
5. Sprawdzić czy da się stworzyć pracę dyplomową, która odnosi się do nieistniejącego studenta i promotora
6. Sprawdzić czy da się stworzyć dwie prace dyplomowa które mają ten sam typ, studenta i promotora.


Challenge
---------

Zrobić klasę testów które przetestują migrację danych.

