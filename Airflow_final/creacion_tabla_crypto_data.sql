-- Este script fue generado por DBeaver y se utilizó para crear la tabla en Amazon Redshift.
-- La tabla fue creada manualmente a través de la interfaz de DBeaver.

CREATE TABLE IF NOT EXISTS gasparduarte_2001_coderhouse.crypto_data
(
	id INTEGER NOT NULL DEFAULT "identity"(945907, 0, '1,1'::text) ENCODE az64
	,coin_name VARCHAR(100) NOT NULL DEFAULT 0 ENCODE lzo
	,symbol VARCHAR(10) NOT NULL DEFAULT 0 ENCODE lzo
	,price NUMERIC(18,2) NOT NULL DEFAULT 0 ENCODE az64
	,price_change NUMERIC(18,2) NOT NULL DEFAULT 0 ENCODE az64
	,price_movement VARCHAR(10) NOT NULL DEFAULT 0 ENCODE lzo
	,data_extraction_time TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,PRIMARY KEY (id)
	,UNIQUE (coin_name)
	,UNIQUE (symbol)
)
DISTSTYLE AUTO
;
ALTER TABLE gasparduarte_2001_coderhouse.crypto_data owner to gasparduarte_2001_coderhouse;