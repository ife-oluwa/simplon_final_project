DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS predictions;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    MasVnrArea FLOAT NOT NULL,
    GarAreaPerCar FLOAT NOT NULL,
    TotalHouseSF FLOAT NOT NULL,
    TotalFullBath FLOAT NOT NULL,
    InitHouseAge INTEGER NOT NULL,
    RemodHouseAge FLOAT NOT NULL,
    IsRemod INTEGER NOT NULL,
    GarageAge INTEGER NOT NULL,
    TotalPorchSF FLOAT NOT NULL,
    Overall_Qual INTEGER NOT NULL,
    Overall_Cond INTEGER NOT NULL,
    SalePrice FLOAT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

