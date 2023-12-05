# System rezerwacji sal - Warszawa


Dokument w którym przedstawimy działanie naszej aplikacji internetowej napisanej w Django na Hackaton Data for City 2023.
Zdecydowałyśmy się na nazwę „Rezerwacja obiektów sportowych Warszawa”, pomysł został zaczerpnięty z listy wyzwań miejskich „Rejestr sal w jednostkach/lokalizacjach miejskich” z uwagą „Np. możliwość sprawdzenia możliwości wynajęcia sali gimnastycznej, etc.”. 
Postanowiłyśmy trochę zinterpretować to wyzwanie w inny sposób i skupić się na salach sportowych oraz innych obiektach przeznaczonych lub niezbędnych do uprawniania różnorakich dyscyplin sportowych.  
Dzielimy użytkowników na 2 grupy: użytkownicy zainteresowani wynajmem, którzy ze swojego konta będą mogli wysyłać formularze rezerwacyjne na wybrany z dostępnych terminów, oraz użytkownicy właściciele, w tej grupie wyróżniamy też osobno szkoły z powodu różnicy w sposobie tworzenia konta. Różnica polega na tym, że adresy szkół są pozyskiwane z api "Otwarte dane - czyli dane po warszawsku".
Właściciele dodają obiekty, które muszą być zatwierdzone przez administratora. Dla danego obiektu mogą dodać dostępne terminy. Wynajemcy mogą wysłać formularze z prośbą o wynajem i wtedy mogą być one akceptowane przez właścicieli. Jeśli są zaakceptowane, to wyświetlają się w tabelce, gdzie są wszytskie zaakceptowane terminy, żeby inni użytkownicy mogli zobaczyć że ten termin jest już zajęty.
Osoby niezarejestrowane także mogą wyszukiwać obiekty i zobaczyć dostępne terminy, tylko nie mogą wysłać formularza z prośbą o wynajem.

