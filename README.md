t# Projekt Interdyscyplinarny

## System rezerwacji sal sportowych Warszawa

### Opis wstępny
Aplikacja sieciowa napisana w django umożliwiająca rezerwację sali gimnastycznej lub innego obiektu sportowego przez zarejestrowanych użytkowników (użytkownik-wynajmujący).
Sale sportowe zostają wpisane i są zarządzane ze specjalnych zarejestrowanych kont (użytkownik-właściciel), może on mieć w ramach jednego konta wiecej niż jedną salę do wynajmu. 
użytkownik-właściciel ma dostęp do opisu swoich sal oraz kalendarza dostępności gdzie mogą zaznaczać kiedy już ich wybrana sala jest zajęta.
Termin jest dostępny dopóki użytkownik-właściciel nie zaznaczy inaczej (w takim wypadku może zaznaczyć niedostępność, także jeśli wynajął sale poza aplikacją lub jest ona niedostępna z innych powodów). 
W opisie sali znajduje się: 
adres,=
informacja dla których dyscyplin sportu sala jest przeznaczona/dostosowana,
a także dłuższy opis który może być umieszczony przez użytkownika-właściciela w którym przedstawia dodatkowe informacje odnośnie sali (np. zasadach które muszą być przestrzegane przez wynajmujących, kosztach wynajęcia, możliwości bezpośredniego kontaktu np. numer telefonu).

Dla użytkownika-wynajmującego dostępna jest mapa z zaznaczonymi obiektami oraz możliwością filtrowania sal względem kategorii dyscypliny sportowej do której szukają sali oraz filtrowania względem dostępności w wybranym przez nich terminie (data albo data z przedziałem czasowym). 
Ten użytkownik po znalezieniu sali otwiera informację dotyczące danej sali wraz z jej opisem i kalendarzem dostępności. 
Użytkownicy-wynajmujący mogą zobaczyć dostępne terminy oraz wysłać formularz, którego zaakceptowanie przez użytkownika-właścicela znaczy że obiekt jest wynajęty.
