DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS groups;
CREATE TABLE contacts (contact_id VARCHAR(100) PRIMARY KEY NOT NULL, 
  first_name TEXT NOT NULL, 
  last_name  TEXT NOT NULL, 
  phone      TEXT NOT NULL, 
  group_id   TEXT NOT NULL  );

CREATE TABLE groups (group_id VARCHAR(100) PRIMARY KEY NOT NULL, 
   group_name         TEXT NOT NULL,
   group_description  TEXT NOT NULL); 
