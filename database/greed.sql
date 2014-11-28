-- MySQL Script generated by MySQL Workbench
-- 11/25/14 19:57:48
-- Model: database    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema greed
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema greed
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `greed` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `greed` ;

-- -----------------------------------------------------
-- Table `greed`.`account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`account` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`username` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `greed`.`stock`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`stock` (
  `symbol` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`symbol`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `greed`.`competition`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`competition` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `owner_account_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `entryfee` DECIMAL(13,2) UNSIGNED NOT NULL,
  `unixtime_start` INT UNSIGNED NOT NULL,
  `unixtime_length` INT UNSIGNED NOT NULL,
  `cancelled` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `fk_competition_account1_idx` (`owner_account_id` ASC),
  CONSTRAINT `fk_competition_account1`
    FOREIGN KEY (`owner_account_id`)
    REFERENCES `greed`.`account` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `greed`.`super_portfolio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`super_portfolio` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `account_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `initial_cash` DECIMAL(13,2) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_super_portfolio_account1_idx` (`account_id` ASC),
  UNIQUE INDEX `account_name_UNIQUE` (`account_id` ASC, `name` ASC),
  CONSTRAINT `fk_super_portfolio_account1`
    FOREIGN KEY (`account_id`)
    REFERENCES `greed`.`account` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `greed`.`sub_portfolio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`sub_portfolio` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `super_portfolio_id` INT NOT NULL,
  `competition_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_portfolio_competition1_idx` (`competition_id` ASC),
  INDEX `fk_portfolio_super_portfolio1_idx` (`super_portfolio_id` ASC),
  UNIQUE INDEX `super_portfolio_id_competiton_id_UNIQUE` (`super_portfolio_id` ASC, `competition_id` ASC),
  CONSTRAINT `fk_portfolio_competition1`
    FOREIGN KEY (`competition_id`)
    REFERENCES `greed`.`competition` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_portfolio_super_portfolio1`
    FOREIGN KEY (`super_portfolio_id`)
    REFERENCES `greed`.`super_portfolio` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `greed`.`transaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`transaction` (
  `sub_portfolio_id` INT NOT NULL,
  `unixtime` INT UNSIGNED NOT NULL,
  `stock_symbol` VARCHAR(45) NOT NULL,
  `stock_count` INT UNSIGNED NOT NULL,
  `stock_value` DECIMAL(13,2) UNSIGNED NOT NULL,
  `type` ENUM('p','s') NOT NULL,
  INDEX `fk_transation_stock1_idx` (`stock_symbol` ASC),
  PRIMARY KEY (`sub_portfolio_id`, `unixtime`, `stock_symbol`),
  INDEX `fk_transaction_sub_portfolio1_idx` (`sub_portfolio_id` ASC),
  CONSTRAINT `fk_transation_stock1`
    FOREIGN KEY (`stock_symbol`)
    REFERENCES `greed`.`stock` (`symbol`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_transaction_sub_portfolio1`
    FOREIGN KEY (`sub_portfolio_id`)
    REFERENCES `greed`.`sub_portfolio` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

USE `greed` ;

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`stock_value`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`stock_value` (`symbol` INT, `value` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`portfolio_value_cash`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`portfolio_value_cash` (`id` INT, `initial_cash` INT, `cash` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`portfolio_stocks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`portfolio_stocks` (`id` INT, `stock_symbol` INT, `stock_count` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`portfolio_value_stock`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`portfolio_value_stock` (`id` INT, `cash` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`comp_portfolio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`comp_portfolio` (`id` INT, `super_portfolio_id` INT, `competition_id` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`main_portfolio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`main_portfolio` (`id` INT, `super_portfolio_id` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`competition_ext`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`competition_ext` (`id` INT, `unixtime_start` INT, `datetime_start` INT, `unixtime_end` INT, `datetime_end` INT);

-- -----------------------------------------------------
-- View `greed`.`stock_value`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`stock_value`;
USE `greed`;
CREATE  OR REPLACE VIEW stock_value AS
SELECT
	stock.symbol AS symbol,
	100 AS value
FROM stock;

-- -----------------------------------------------------
-- View `greed`.`portfolio_value_cash`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`portfolio_value_cash`;
USE `greed`;
CREATE  OR REPLACE VIEW portfolio_value_cash AS
SELECT
	transaction.sub_portfolio_id AS id,
	IF(competition_id IS NULL, super_portfolio.initial_cash, competition.entryfee) as initial_cash,
	initial_cash + SUM(IF(transaction.type = 's', transaction.stock_value, transaction.stock_value * -1) * transaction.stock_count) AS cash
FROM transaction
JOIN sub_portfolio ON sub_portfolio_id = sub_portfolio.id
JOIN super_portfolio ON super_portfolio_id = super_portfolio.id
LEFT JOIN competition ON competition_id = competition.id
GROUP BY transaction.sub_portfolio_id;

-- -----------------------------------------------------
-- View `greed`.`portfolio_stocks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`portfolio_stocks`;
USE `greed`;
CREATE  OR REPLACE VIEW portfolio_stocks AS
SELECT
	transaction.sub_portfolio_id AS id,
	transaction.stock_symbol AS stock_symbol,
	SUM(IF(transaction.type = 'p', transaction.stock_count, transaction.stock_count * -1)) AS stock_count
FROM transaction
GROUP BY transaction.sub_portfolio_id, stock_symbol;

-- -----------------------------------------------------
-- View `greed`.`portfolio_value_stock`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`portfolio_value_stock`;
USE `greed`;
CREATE  OR REPLACE VIEW portfolio_value_stock AS
SELECT
	transaction.sub_portfolio_id AS id,
	SUM(IF(transaction.type = 'p', stock_value.value, stock_value.value * -1) * transaction.stock_count) AS cash
FROM transaction
JOIN stock_value ON stock_symbol = stock_value.symbol
GROUP BY transaction.sub_portfolio_id;

-- -----------------------------------------------------
-- View `greed`.`comp_portfolio`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`comp_portfolio`;
USE `greed`;
CREATE  OR REPLACE VIEW comp_portfolio AS
SELECT
	id,
	super_portfolio_id,
    competition_id
FROM sub_portfolio
WHERE NOT competition_id IS NULL;

-- -----------------------------------------------------
-- View `greed`.`main_portfolio`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`main_portfolio`;
USE `greed`;
CREATE  OR REPLACE VIEW main_portfolio AS
SELECT
	id,
	super_portfolio_id
FROM sub_portfolio
WHERE competition_id IS NULL;

-- -----------------------------------------------------
-- View `greed`.`competition_ext`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`competition_ext`;
USE `greed`;
CREATE  OR REPLACE VIEW competition_ext AS
SELECT
	id,
    unixtime_start,
    FROM_UNIXTIME(unixtime_start) AS datetime_start,
    unixtime_start + unixtime_length AS unixtime_end,
	FROM_UNIXTIME(unixtime_start + unixtime_length) AS datetime_end
FROM competition;
USE `greed`;

DELIMITER $$
USE `greed`$$
CREATE TRIGGER greed.super_portfolio_AFTER_INSERT AFTER INSERT ON super_portfolio FOR EACH ROW
BEGIN
	INSERT INTO sub_portfolio (super_portfolio_id) VALUES (NEW.id);
END;$$

USE `greed`$$
CREATE TRIGGER greed.sub_portfolio_BEFORE_INSERT BEFORE INSERT ON sub_portfolio FOR EACH ROW
BEGIN
	IF (NEW.competition_id IS NULL) THEN
		IF (EXISTS(SELECT super_portfolio_id FROM sub_portfolio WHERE super_portfolio_id = NEW.super_portfolio_id AND competition_id IS NULL)) THEN
			SIGNAL SQLSTATE '23000'
            SET MESSAGE_TEXT = 'Duplicate entry',
            MYSQL_ERRNO = 1062;
        END IF;
	END IF;
END;$$

USE `greed`$$
CREATE TRIGGER greed.sub_portfolio_BEFORE_UPDATE BEFORE UPDATE ON sub_portfolio FOR EACH ROW
BEGIN
	IF (NEW.competition_id IS NULL) THEN
		IF (EXISTS(SELECT super_portfolio_id FROM sub_portfolio WHERE super_portfolio_id = NEW.super_portfolio_id AND competition_id IS NULL)) THEN
			SIGNAL SQLSTATE '23000'
            SET MESSAGE_TEXT = 'Duplicate entry',
            MYSQL_ERRNO = 1062;
        END IF;
	END IF;
END;$$


DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

