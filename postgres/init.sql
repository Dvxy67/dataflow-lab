CREATE TABLE evenements (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    source TEXT NOT NULL,
    valeur INTEGER,
    date_message TIMESTAMP,
    recu_le TIMESTAMP DEFAULT NOW()
);

CREATE TABLE alertes (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    valeur INTEGER,
    date_message TIMESTAMP,
    recu_le TIMESTAMP DEFAULT NOW()
);
