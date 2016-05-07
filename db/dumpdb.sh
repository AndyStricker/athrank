CONNECT_INFO='-h localhost -p 5432 -U jugiuser'
pg_dump $CONNECT_INFO --schema=public --schema-only -f athrank.sql athrank
pg_dump $CONNECT_INFO --schema=public --data-only -f categories.sql --table=categories athrank
pg_dump $CONNECT_INFO --schema=public --data-only -f sexes.sql --table=sexes athrank
pg_dump $CONNECT_INFO --schema=public --data-only -f awards.sql --table=awards athrank
pg_dump $CONNECT_INFO --schema=public --data-only -f sections.sql --table=section athrank
pg_dump $CONNECT_INFO --schema=public --data-only -f category.sql --table=category athrank
pg_dump $CONNECT_INFO --schema=public --data-only -f agecategory.sql --table=agecategory athrank

