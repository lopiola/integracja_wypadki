Analiza przyczyn wypadków drogowych
=============================

Projekt dotyczący analizy przyczyn śmiertelnych wypadków drogowych z wykorzystaniem danych z USA i Wielkiej Brytanii.
Wszystkie pliki i katalogi zawarte w tym opisie znajdują się na płycie DVD z projektem.

Wymagania
---------------
Do uruchomienia projektu potrzebe sa następujące biblioteki:
    - python ( > 2.7)
        - pakiet psycopg2
        - pakiet sas7bdat 
    - PostgreSQL
Należy również dodać ścieżkę do katalogu głównego projektu do zmiennej środowiskowej PYTHONPATH.

Zawartość płyty
---------------

Płyta zorganizowana jest w następujący sposób:

DVD
 |
 |- fars_examples - przykładowe dane pobrane z zasobów FARS (USA) w formacie csv
 |
 |- gb_examples - przykładowe dane pobrane z zasobów STATS19 (WB) w formacie csv
 |
 |- hipotheses - wyniki przeprowadzonych weryfikacji hipotez i wykresy
 |
 |- scripts - skypty używane podczas trwania projektu
 |
 |- statistics - wyniki przeprowadzonych analiz statystycznych i wykresy
 |
 |- accidents.sql - kompletny zrzut bazy danych (PostreSQL)
 |
 |- dokumentacja.pdf - dokumentacja ostateczna
 |
 |- Prezentacja 1.pdf - pierwsza prezentacja z koncpecją projektu w formacie pdf
 |
 |- Prezentacja 1.pptx - pierwsza prezentacja z koncpecją projektu w formacie pptx
 |
 |- Prezentacja 2.pdf - prezentacja ostateczna wyników prac w formacie pdf
 |
 |- Prezentacja 2.pptx - prezentacja ostateczna wyników prac w formacie pptx
 |
 |- raport_z_prac.pdf - podsumowanie podziału prac pomiędzy autorów projektu
 |
 |- README.txt - ten plik


Baza danych
-----------------
Baza danych z danymi z USA i Wielkiej Brytanii jest zawarta w pliku accidents.sql. Baza została stworzona w PostgreSQL. W celu utworzenia bazy należy wywołać następujące komendy:
~$ createdb accidents
~$ psql -f accidents.sql -U <nazwa_użytkownika> accidents


Skrypty
------------------------

Skrypty używane podczas trwania projektu znajdują się w katalogu scripts. Zawartość katalogu jest następująca:

scripts - zbiór skryptów, które zostały użyte do sparsowania danych
 |
 |- db_api - skrypty pozwalające na programowy dostęp do danych w bazie (w pliku common.py można skonfigurować nazwę użytkownika bazy danych i nazwę bazy danych)
 |
 |- parsing - skrypty pomocnicze przy parsowaniu bazy
 |
 |- statistics - skrypty generujące wyniki analiz przeprowadzonych w projekcie


Wyniki
---------
Wyniki przeprowadzonych analiz zostały zgromadzone w katalogach statistics i hipotheses. Katalog statistics zawiera proste statystyki nie podpięte pod zaawansowane hipotezy, katalog hipotheses zawiera wyniki pod kątem konkretnych hipotez. Wszystkie te wyniki zawarte są w dokumentacji końcowej projektu.
