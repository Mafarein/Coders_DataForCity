t# Projekt Interdyscyplinarny

## System rezerwacji sal sportowych Warszawa

### Opis wstępny
Aplikacja sieciowa napisana w django umożliwiająca rezerwację sali gimnastycznej lub innego obiektu sportowego przez zarejestrowanych użytkowników (użytkownik-wynajmujący).
Sale sportowe zostają wpisane i są zarządzane ze specjalnych zarejestrowanych kont (użytkownik-właściciel), może on mieć w ramach jednego konta wiecej niż jedną salę do wynajmu. 
użytkownik-właściciel ma dostęp do opisu swoich sal oraz kalendarza dostępności gdzie mogą zaznaczać kiedy już ich wybrana sala jest zajęta.
Termin jest dostępny dopóki użytkownik-właściciel nie zaznaczy inaczej (w takim wypadku może zaznaczyć niedostępność, także jeśli wynajął sale poza aplikacją lub jest ona niedostępna z innych powodów). 
W opisie sali znajduje się: 
adres,
adres mail oraz numer telefonu do kontaktu,
cena za wynajem w stawce godzinowej albo informacja że wynajem jest bezpłatny,
informacja dla których dyscyplin sportu sala jest przeznaczona/dostosowana,
a także dłuższy opis który może być umieszczony przez użytkownika-właściciela w którym przedstawia dodatkowe informacje odnośnie sali (np. zasadach które muszą być przestrzegane przez wynajmujących).

Dla użytkownika-wynajmującego dostępna jest mapa z zaznaczonymi obiektami oraz możliwością filtrowania sal względem kategorii dyscypliny sportowej do której szukają sali oraz filtrowania względem dostępności w wybranym przez nich terminie (data albo data z przedziałem czasowym). Możliwe jest także wyszukiwanie dokładnej sali (np. wybierając z dostępnej listy nazwę szkoły).
Ten użytkownik po znalezieniu sali otwiera informację dotyczące danej sali wraz z jej opisem i kalendarzem dostępności. 
Użytkownicy-wynajmujący mogą zobaczyć ten kalendarz oraz się zapisać na daną godzinę dopóki jest ona dostępna.
Widzą także ile innych osób stara się o zapisanie na ten termin przed nimi, ale nie zostali jeszcze zatwierdzeni, dlatego termin jest jeszcze oznaczony jako dostępny. 
Mogą przez aplikację wysłać maila na adres mail przypisany do kontaku odnośnie danej sali, jednakże mają też dostęp do przypisanego numeru telefonu, gdyby chcieli zadzwonić.

#### i tutaj jeszcze o rejestracji kont użytkowników 
