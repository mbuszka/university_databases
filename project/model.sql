CREATE TABLE employees 
  ( id INT PRIMARY KEY
  , passwd TEXT
  , data TEXT
  , path TEXT
  , parent INT REFERENCES employees(id) ON DELETE CASCADE
  );

CREATE INDEX ON employees (path);

CREATE ROLE app;
ALTER ROLE app LOGIN PASSWORD 'qwerty';
GRANT ALL ON TABLE employees TO app;