CREATE TABLE "search_results" (
	"mp_id"	TEXT,
	"document_id"	INTEGER,
	"score"	NUMERIC
);

CREATE TABLE "label_mapping" (
	"document_id"	INTEGER,
	"label"	TEXT,
	PRIMARY KEY("document_id")
);