--
-- Disable foreign keys
--
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

--
-- Set SQL mode
--
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


DROP DATABASE wheat_processing;
CREATE DATABASE IF NOT EXISTS `wheat_processing`;
USE `wheat_processing`;

--
-- Create tables
--
create table changes
(
    TableName  varchar(255)                        not null
        primary key,
    LastChange timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create table flour_grade
(
    FlourGradeId   int auto_increment
        primary key,
    FlourGradeName varchar(40) charset utf8 not null
)
    comment 'Сорт муки';

create definer = root@localhost trigger on_flour_grade_deleted
    after delete
    on flour_grade
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('flour_grade', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_flour_grade_inserted
    after insert
    on flour_grade
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('flour_grade', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_flour_grade_updated
    after update
    on flour_grade
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('flour_grade', CURRENT_TIMESTAMP);
END;

create table grinding_grade
(
    GrindingGradeId   int auto_increment
        primary key,
    GrindingGradeName varchar(40) charset utf8 not null
)
    comment 'Помол отрубей';

create definer = root@localhost trigger on_grinding_grade_deleted
    after delete
    on grinding_grade
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('grinding_grade', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_grinding_grade_inserted
    after insert
    on grinding_grade
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('grinding_grade', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_grinding_grade_updated
    after update
    on grinding_grade
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('grinding_grade', CURRENT_TIMESTAMP);
END;

create table legal_entity
(
    LegalEntityId   int auto_increment
        primary key,
    ContactPhone    varchar(15) charset utf8  null,
    Address         varchar(255) charset utf8 null,
    LegalEntityName varchar(60) charset utf8  not null
)
    comment 'Юридическое лицо (поставщик/заказчик)';

create table contract
(
    ContractId    int auto_increment
        primary key,
    LegalEntityId int                                      not null,
    CreationTime  timestamp  default CURRENT_TIMESTAMP     not null,
    DeadlineTime  timestamp  default '0000-00-00 00:00:00' not null,
    IsFinished    tinyint(1) default 0                     not null,
    IsViolated    tinyint(1) default 0                     not null,
    Price         double                                   not null,
    constraint contract_ibfk_1
        foreign key (LegalEntityId) references legal_entity (LegalEntityId) on delete cascade
)
    comment 'Договор о купле/продаже';

create definer = root@localhost trigger on_contract_deleted
    after delete
    on contract
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('contract', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_contract_inserted
    after insert
    on contract
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('contract', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_contract_updated
    after update
    on contract
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('contract', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_legal_entity_deleted
    after delete
    on legal_entity
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('legal_entity', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_legal_entity_inserted
    after insert
    on legal_entity
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('legal_entity', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_legal_entity_updated
    after update
    on legal_entity
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('legal_entity', CURRENT_TIMESTAMP);
END;

create table machine_type
(
    MachineTypeId   int auto_increment
        primary key,
    MachineTypeName varchar(40) charset utf8 not null
)
    comment 'Тип промышленного механизма';

create table machine
(
    MachineId     int auto_increment
        primary key,
    IsPowered     tinyint(1) default 0 not null,
    MachineTypeId int                  not null,
    constraint machine_ibfk_1
        foreign key (MachineTypeId) references machine_type (MachineTypeId) on delete cascade
)
    comment 'Промышленный механизм';

create definer = root@localhost trigger on_machine_deleted
    after delete
    on machine
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('machine', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_machine_inserted
    after insert
    on machine
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('machine', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_machine_updated
    after update
    on machine
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('machine', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_machine_type_deleted
    after delete
    on machine_type
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('machine_type', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_machine_type_inserted
    after insert
    on machine_type
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('machine_type', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_machine_type_updated
    after update
    on machine_type
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('machine_type', CURRENT_TIMESTAMP);
END;

create table resource_type
(
    ResourceTypeId   int auto_increment
        primary key,
    IsProducible     tinyint(1) default 0     not null,
    ResourceTypeName varchar(40) charset utf8 not null
)
    comment 'Тип продукции или закупаемого ресурса';

create definer = root@localhost trigger on_resource_type_deleted
    after delete
    on resource_type
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('resource_type', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_resource_type_inserted
    after insert
    on resource_type
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('resource_type', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_resource_type_updated
    after update
    on resource_type
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('resource_type', CURRENT_TIMESTAMP);
END;

create table role
(
    RoleId   int auto_increment
        primary key,
    RoleName varchar(40) charset utf8 not null
)
    comment 'Должность работника';

create definer = root@localhost trigger on_role_deleted
    after delete
    on role
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('role', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_role_inserted
    after insert
    on role
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('role', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_role_updated
    after update
    on role
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('role', CURRENT_TIMESTAMP);
END;

create table standard
(
    StandardId          int auto_increment
        primary key,
    StandardName        varchar(40) charset utf8   not null,
    StandardDescription varchar(2000) charset utf8 not null
)
    comment 'Стандарт или рецепт (ГОСТ, местный) производства';

create table production_line
(
    ProductionLineId     int auto_increment
        primary key,
    StandardId           int                                 not null,
    ProductionStartTime  timestamp default CURRENT_TIMESTAMP not null,
    ProductionFinishTime timestamp                           null,
    constraint production_line_ibfk_1
        foreign key (StandardId) references standard (StandardId) on delete cascade,
    constraint production_line_ibfk_2
        foreign key (StandardId) references standard (StandardId) on delete cascade
)
    comment 'Линия производства мучных изделий';

create table machine_to_production_line
(
    MachineId        int not null,
    ProductionLineId int not null,
    primary key (MachineId, ProductionLineId),
    constraint machine_to_production_line_ibfk_1
        foreign key (MachineId) references machine (MachineId) on delete cascade,
    constraint machine_to_production_line_ibfk_2
        foreign key (ProductionLineId) references production_line (ProductionLineId) on delete cascade
);

create definer = root@localhost trigger on_machine_to_production_line_deleted
    after delete
    on machine_to_production_line
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('machine_to_production_line', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_machine_to_production_line_inserted
    after insert
    on machine_to_production_line
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('machine_to_production_line', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_machine_to_production_line_updated
    after update
    on machine_to_production_line
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('machine_to_production_line', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_production_line_deleted
    after delete
    on production_line
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('production_line', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_production_line_inserted
    after insert
    on production_line
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('production_line', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_production_line_updated
    after update
    on production_line
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('production_line', CURRENT_TIMESTAMP);
END;

create table resource
(
    ResourceId             int auto_increment
        primary key,
    ResourceTypeId         int                       not null,
    ProductionLineId       int                       null,
    ParentProductionLineId int                       null,
    Description            varchar(255) charset utf8 null,
    FlourGradeId           int                       null,
    Vitreousness           tinyint                   null comment 'Стекловидность пшеницы',
    Contamination          tinyint                   null comment 'Загрязнённость пшеницы',
    GrindingGradeId        int                       null,
    ContractId             int                       null,
    constraint resource_ibfk_1
        foreign key (ResourceTypeId) references resource_type (ResourceTypeId) on delete cascade,
    constraint resource_ibfk_2
        foreign key (ProductionLineId) references production_line (ProductionLineId) on delete cascade,
    constraint resource_ibfk_3
        foreign key (ParentProductionLineId) references production_line (ProductionLineId) on delete cascade,
    constraint resource_ibfk_4
        foreign key (FlourGradeId) references flour_grade (FlourGradeId) on delete cascade,
    constraint resource_ibfk_5
        foreign key (GrindingGradeId) references grinding_grade (GrindingGradeId) on delete cascade,
    constraint resource_ibfk_6
        foreign key (ContractId) references contract (ContractId) on delete cascade
)
    comment 'Продукция завода или ресурс, закупаемый извне';

create definer = root@localhost trigger on_resource_deleted
    after delete
    on resource
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('resource', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_resource_inserted
    after insert
    on resource
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('resource', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_resource_updated
    after update
    on resource
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('resource', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_standard_deleted
    after delete
    on standard
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('standard', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_standard_inserted
    after insert
    on standard
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('standard', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_standard_updated
    after update
    on standard
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('standard', CURRENT_TIMESTAMP);
END;

create table worker
(
    WorkerId   int auto_increment
        primary key,
    ChiefId    int                      null,
    RoleId     int                      not null,
    WorkerName varchar(60) charset utf8 not null,
    constraint worker_ibfk_1
        foreign key (ChiefId) references worker (WorkerId) on delete set null,
    constraint worker_ibfk_2
        foreign key (RoleId) references role (RoleId) on delete cascade
)
    comment 'Работник';

create definer = root@localhost trigger on_worker_deleted
    after delete
    on worker
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('worker', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_worker_inserted
    after insert
    on worker
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('worker', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_worker_updated
    after update
    on worker
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('worker', CURRENT_TIMESTAMP);
END;

create table worker_to_production_line
(
    ProductionLineId int not null,
    WorkerId         int not null,
    primary key (ProductionLineId, WorkerId),
    constraint worker_to_production_line_ibfk_1
        foreign key (ProductionLineId) references production_line (ProductionLineId) on delete cascade,
    constraint worker_to_production_line_ibfk_2
        foreign key (WorkerId) references worker (WorkerId) on delete cascade
);

create definer = root@localhost trigger on_worker_to_production_line_deleted
    after delete
    on worker_to_production_line
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('worker_to_production_line', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_worker_to_production_line_inserted
    after insert
    on worker_to_production_line
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('worker_to_production_line', CURRENT_TIMESTAMP);
END;

create definer = root@localhost trigger on_worker_to_production_line_updated
    after update
    on worker_to_production_line
    for each row
BEGIN
    REPLACE INTO changes (TableName, LastChange) VALUES ('worker_to_production_line', CURRENT_TIMESTAMP);
END;


--
-- Dumping data for table role
--
INSERT INTO role VALUES
(1, 'Оператор зернотчищающей машины'),
(2, 'Оператор мукомольной машины'),
(3, 'Специалист по техническому обслуживанию'),
(4, 'Оператор тестомешалки'),
(5, 'Пекарь');

--
-- Dumping data for table legal_entity
--
INSERT INTO legal_entity VALUES
(1, '79122311331', NULL, 'Ассоциация фермеров "Зелёное Подмосковье"'),
(2, '780055535535', 'г. Москва ул. Новокузнецкая строение 14', 'ИП Анатолий Овчинников'),
(3, '71233214521', NULL, 'ООО "Рога и Копыта"'),
(4, '76142343215', 'Москва, Автозаводская улица, 8', 'ТМ «У Палыча»');

--
-- Dumping data for table standard
--
INSERT INTO standard VALUES
(1, 'ГОСТ 31491-2012', 'https://docs.cntd.ru/document/1200095477\r\n\r\nМягкая мука для макоронных изделий'),
(2, 'Внутренние правила по помолу пшеницы', 'Помол производится исключительно после очистки\r\n(загрязнённость должна быть менее 5%)\r\nПомол производится по внутренней технологии компании, \r\nс сохранением большей части отрубей для дальнейшей реализации\r\n(Должен быть соблюдён ГОСТ https://docs.cntd.ru/document/1200157423)'),
(3, 'Рецепт приготовления коржа', 'Предоставлен заказчиком https://palich.ru/');

--
-- Dumping data for table machine_type
--
INSERT INTO machine_type VALUES
(1, 'Очиститель зерна'),
(2, 'Мукомольный аппарат'),
(3, 'Тестозамешивающая машина'),
(4, 'Пекарная печь');

--
-- Dumping data for table worker
--
INSERT INTO worker VALUES
(1, NULL, 1, 'Евгений Сергеевич'),
(2, NULL, 1, 'Антон Семёнович'),
(3, 4, 3, 'Фёдор Юрьевич'),
(4, NULL, 3, 'Сергей Павлович'),
(5, 4, 3, 'Василий Генадьевич'),
(6, 4, 3, 'Андрей Витальевич'),
(7, NULL, 2, 'Галина Викторовна'),
(8, 10, 5, 'Михаил Антонович'),
(9, 10, 5, 'Василиса Андреевна'),
(10, NULL, 5, 'Денис Петрович'),
(11, NULL, 4, 'Виталий Кузьмич');

--
-- Dumping data for table resource_type
--
INSERT INTO resource_type VALUES
(1, 0, 'Пшеница'),
(2, 1, 'Отруби'),
(3, 1, 'Мука'),
(4, 1, 'Мучное изделие'),
(5, 0, 'Ингридиент рецепта');

--
-- Dumping data for table grinding_grade
--
INSERT INTO grinding_grade VALUES
(1, 'Тонкий'),
(2, 'Крупный'),
(3, 'Грубый'),
(4, 'Мелкий');

--
-- Dumping data for table flour_grade
--
INSERT INTO flour_grade VALUES
(1, 'Высший сорт'),
(2, 'Крупчатка'),
(3, 'Первый сорт'),
(4, 'Второй сорт'),
(5, 'Обойная');

--
-- Dumping data for table contract
--
INSERT INTO contract VALUES
(1, 1, '2021-10-12 16:39:27', '2021-10-13 00:00:00', 0, 0, 1100),
(2, 1, '2021-10-12 16:46:23', '2021-10-12 18:45:16', 1, 0, 1200),
(3, 3, '2021-10-12 17:18:03', '2021-10-13 00:00:00', 1, 0, 800),
(4, 2, '2021-10-12 17:37:03', '2021-10-12 17:40:35', 1, 0, 980),
(5, 4, '2021-10-12 18:08:56', '2021-10-13 00:00:00', 1, 0, 2200),
(6, 2, '2021-10-06 00:00:00', '2021-10-11 00:00:00', 1, 1, 680),
(7, 3, '2021-10-12 18:26:36', '2021-10-13 00:00:00', 1, 0, 750),
(8, 2, '2021-10-12 18:27:45', '2021-10-13 00:00:00', 1, 0, 840);

--
-- Dumping data for table production_line
--
INSERT INTO production_line VALUES
(1, 2, '2021-10-12 17:02:10', '2021-10-12 17:03:01'),
(2, 3, '2021-10-12 17:27:46', '2021-10-12 17:45:32'),
(3, 1, '2021-10-12 18:20:35', '2021-10-12 18:30:28');

--
-- Dumping data for table machine
--
INSERT INTO machine VALUES
(1, 1, 1),
(2, 0, 1),
(3, 1, 2),
(4, 1, 3),
(5, 1, 4);

--
-- Dumping data for table worker_to_production_line
--
INSERT INTO worker_to_production_line VALUES
(3, 1),
(1, 2),
(1, 3),
(1, 5),
(1, 7),
(3, 7),
(2, 9),
(2, 10),
(2, 11);

--
-- Dumping data for table resource
--
INSERT INTO resource VALUES
(1, 1, NULL, NULL, NULL, NULL, 95, 12, NULL, 1),
(2, 1, 1, NULL, NULL, NULL, 90, 16, NULL, 2),
(3, 2, NULL, 1, NULL, NULL, NULL, NULL, 4, 3),
(4, 3, 2, 1, NULL, 1, NULL, NULL, NULL, NULL),
(5, 3, 2, 1, NULL, 2, NULL, NULL, NULL, NULL),
(6, 5, 2, NULL, 'Сливочное масло 120 г\r\nСахар 200 г\r\nЯйцо 3 шт\r\nСоль\r\nРазрыхлитель 2 Чайных ложки\r\nМолоко 1 Стакан\r\nВанильный экстракт 1 Чайная ложка\r\nВзять 10 раз на партию к 20', NULL, NULL, NULL, NULL, 4),
(7, 4, NULL, 2, 'Корж для торта', NULL, NULL, NULL, NULL, 5),
(8, 1, 3, NULL, NULL, NULL, 23, 65, NULL, 6),
(9, 2, NULL, 3, NULL, NULL, NULL, NULL, 3, 7),
(10, 3, NULL, 3, NULL, 5, NULL, NULL, NULL, 8),
(11, 3, NULL, 3, NULL, 4, NULL, NULL, NULL, 8);

--
-- Dumping data for table machine_to_production_line
--
INSERT INTO machine_to_production_line VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 2),
(5, 2),
(1, 3),
(3, 3);

--
-- Create views
--
CREATE VIEW view_worker AS
SELECT WorkerId, WorkerName, RoleName, (
    SELECT COUNT(*) FROM worker other
    WHERE other.ChiefId = worker.WorkerId
) AS SubordinatesCount
FROM worker
INNER JOIN role ON worker.RoleId = role.RoleId
ORDER BY RoleName, WorkerName;

CREATE VIEW view_machine AS
SELECT MachineId, MachineTypeName, IsPowered FROM machine
INNER JOIN machine_type type ON machine.MachineTypeId = type.MachineTypeId;

CREATE VIEW view_legal_entity AS
SELECT LegalEntityId, LegalEntityName, Address, ContactPhone, (
    (
        SELECT count(contract.ContractId)
        FROM legal_entity
             INNER JOIN contract
                ON contract.LegalEntityId = legal_entity.LegalEntityId
             INNER JOIN resource
                ON resource.ContractId = contract.ContractId
        WHERE legal_entity.LegalEntityId = l.LegalEntityId
            AND contract.IsFinished = 1
            AND resource.Contamination < 20
            AND resource.Vitreousness > 80
    ) - (
        SELECT count(contract.ContractId)
        FROM legal_entity
        INNER JOIN contract
            ON contract.LegalEntityId = legal_entity.LegalEntityId
        INNER JOIN resource
            ON resource.ContractId = contract.ContractId
        WHERE legal_entity.LegalEntityId = l.LegalEntityId
            AND (contract.IsViolated = 1 OR resource.Contamination > 20)
    )
) AS ProviderRating
FROM legal_entity l
ORDER BY ProviderRating DESC;

CREATE VIEW view_production_line AS
SELECT ProductionLineId, StandardName,
   TIMEDIFF(ProductionFinishTime, ProductionStartTime)
   AS ProductionDuration
FROM production_line pl
INNER JOIN standard s ON pl.StandardId = s.StandardId;

CREATE VIEW view_contract AS
SELECT c.ContractId, le.LegalEntityName, CreationTime,
       DeadlineTime, IsFinished, IsViolated,
       (SELECT IF(IsProducible = 0, -Price, Price))
FROM contract c
INNER JOIN legal_entity le ON c.LegalEntityId = le.LegalEntityId
INNER JOIN resource r ON c.ContractId = r.ContractId
INNER JOIN resource_type rt ON r.ResourceTypeId = rt.ResourceTypeId;

CREATE VIEW view_resource AS
SELECT ResourceId, ResourceTypeName,
   (SELECT IF(FlourGradeName IS NULL,
       (SELECT IF(GrindingGradeName IS NULL,
            Description,
           GrindingGradeName
   )), FlourGradeName
   )) AS Comment, IsProducible,
   (SELECT IF(IsProducible=1,
       parent_pl.ProductionFinishTime IS NOT NULL
       AND resource.ContractId IS NULL
       AND resource.ProductionLineId IS NULL,
       c.IsFinished = 1
       AND c.IsViolated = 0
       AND resource.ProductionLineId IS NULL
   )) AS IsAvailable,
   (SELECT IF(IsProducible=1,
       resource.ParentProductionLineId IS NULL
       AND resource.ContractId IS NULL
       AND resource.ProductionLineId IS NULL,
       resource.ContractId IS NULL
   )) AS IsPlanned
FROM resource
LEFT JOIN flour_grade fg on resource.FlourGradeId = fg.FlourGradeId
LEFT JOIN grinding_grade gg on resource.GrindingGradeId = gg.GrindingGradeId
INNER JOIN resource_type rt on resource.ResourceTypeId = rt.ResourceTypeId
LEFT JOIN production_line parent_pl on resource.ParentProductionLineId = parent_pl.ProductionLineId
LEFT JOIN contract c on resource.ContractId = c.ContractId;

--
-- Restore previous SQL mode
--
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;

--
-- Enable foreign keys
--
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;