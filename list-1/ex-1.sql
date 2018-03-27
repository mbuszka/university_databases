WITH the_semester AS (
  SELECT semestr_id FROM semestr WHERE nazwa = 'Semestr zimowy 2010/2011'
),
  the_przedmiot AS (
    SELECT kod_przed FROM przedmiot WHERE nazwa = 'Matematyka dyskretna (M)'
  ),
proxy AS (
  SELECT *
  FROM
    grupa natural join the_przedmiot
          natural join przedmiot_semestr
          natural join the_semester
          natural join uzytkownik
  WHERE rodzaj_zajec in ('C', 'c')
  ORDER BY nazwisko
) SELECT string_agg(proxy.nazwisko, ',') FROM proxy
