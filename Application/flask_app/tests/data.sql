INSERT INTO user (username, email, password)
VALUES
    ('test', 'test@gmail.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
    ('other', 'other@gmail.com', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO predictions (user_id, created, MasVnrArea, GarAreaPerCar, TotalHouseSF, TotalFullBath, InitHouseAge,
RemodHouseAge, IsRemod, GarageAge, TotalPorchSF, Overall_Qual, Overall_Cond, SalePrice)
VALUES 
(1,'2018-01-01 00:00:00', 0.0, 216.5, 3378.0, 2.0, 1.0, 1.0, 1, 1.0, 0.0, 39.0, 6.0, 231713) 