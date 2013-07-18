DROP TABLE IF EXISTS items;

CREATE TABLE items
  ( 
     code         	 	VARCHAR(50) NOT NULL, 
     description   	TEXT, 
     designer     	VARCHAR(50), 
     gbp_price     	FLOAT, 
     gender        	VARCHAR(1), 
     image_urls    	TEXT, 
     name          	VARCHAR(50), 
     raw_color     	VARCHAR(20) NOT NULL, 
     sale_discount 	FLOAT, 
     source_url    	TEXT, 
     stock_status 	TEXT, 
     last_updated  	DATE, 
     type          		VARCHAR(1),
     CONSTRAINT pk_CodeColor PRIMARY KEY (code, raw_color)
  ); 
