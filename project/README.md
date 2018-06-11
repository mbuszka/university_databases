# Model konceptualny

  | Kolumna | Typ | Dodatkowe wymagania |
  | ---     | --- | --- |
  | id | INT | klucz główny |
  | passwd | TEXT | zaszyfrowane hasło |
  | data | TEXT | |
  | path | TEXT | śćieżka od korzenia, postaci `"n1.n2.n3.n4"` |
  | parent | INT | klucz obcy na `id` |

# Uprawnienia użytkowników

- `init` - może tworzyć użytkowników i tabele, oraz modyfikować dane w tabelach

- `app` - może modyfikować dane w tabelach

# działanie wybranych funkcji

1.  `ancestors(X)`
   
    wierzchołki `Y` takie, że `path(Y)` jest prefiksem właściwym `path(X)`

2.  `descendants(X)`

    wierzchołki `Y` takie, że `path(X)` jest prefiksem właściwym `path(Y)`

3.  `ancestor(X, Y)`

    `path(X)` jest właściwym prefiksem `path(Y)`

# uruchomienie

 `./main.py --init` lub `./main.py`