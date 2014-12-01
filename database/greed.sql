-- MySQL Script generated by MySQL Workbench
-- 12/01/14 17:12:36
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


-- -----------------------------------------------------
-- Table `greed`.`stock_value`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`stock_value` (
  `stock_symbol` VARCHAR(45) NOT NULL,
  `unixtime` INT UNSIGNED NOT NULL,
  `value` DECIMAL(13,2) UNSIGNED NOT NULL,
  PRIMARY KEY (`stock_symbol`, `unixtime`),
  CONSTRAINT `fk_stock_has_value_stock1`
    FOREIGN KEY (`stock_symbol`)
    REFERENCES `greed`.`stock` (`symbol`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `greed` ;

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`portfolio_value_cash`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`portfolio_value_cash` (`id` INT, `super_portfolio_id` INT, `cash` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`portfolio_stocks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`portfolio_stocks` (`id` INT, `stock_symbol` INT, `stock_count` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`portfolio_value_stock`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`portfolio_value_stock` (`id` INT, `net_value` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`competition_ext`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`competition_ext` (`id` INT, `owner_account_id` INT, `name` INT, `entryfee` INT, `unixtime_start` INT, `unixtime_length` INT, `cancelled` INT, `unixtime_end` INT, `datetime_end` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`transaction_ext`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`transaction_ext` (`sub_portfolio_id` INT, `unixtime` INT, `stock_symbol` INT, `stock_count` INT, `type` INT, `stock_unixtime` INT, `value` INT, `net_value` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`stock_value_latest`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`stock_value_latest` (`stock_symbol` INT, `unixtime` INT, `value` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`portfolio_value_total`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`portfolio_value_total` (`id` INT, `value_stock` INT, `value_cash` INT, `value_comp` INT, `total_value` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`portfolio_value_comp`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`portfolio_value_comp` (`id` INT, `comp_value` INT);

-- -----------------------------------------------------
-- Placeholder table for view `greed`.`sub_portfolio_ext`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `greed`.`sub_portfolio_ext` (`id` INT, `super_portfolio_id` INT, `competition_id` INT, `super_portfolio_name` INT, `competition_name` INT, `value_stock` INT, `value_cash` INT, `value_comp` INT, `total_value` INT);

-- -----------------------------------------------------
-- View `greed`.`portfolio_value_cash`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`portfolio_value_cash`;
USE `greed`;
CREATE  OR REPLACE VIEW portfolio_value_cash AS
SELECT
	sub_portfolio.id AS id,
    super_portfolio.id AS super_portfolio_id,
	/* IF(competition_id IS NULL, super_portfolio.initial_cash, competition.entryfee) AS initial_cash, */
	IFNULL(initial_cash + SUM(IF(transaction_ext.type = 's', transaction_ext.net_value, transaction_ext.net_value * -1)) - portfolio_value_comp.comp_value, IF(competition_id IS NULL, super_portfolio.initial_cash, competition.entryfee))
        AS cash
FROM sub_portfolio
JOIN super_portfolio ON super_portfolio_id = super_portfolio.id
LEFT JOIN transaction_ext ON sub_portfolio.id = transaction_ext.sub_portfolio_id
LEFT OUTER JOIN competition ON competition_id = competition.id
LEFT JOIN portfolio_value_comp ON sub_portfolio.id = portfolio_value_comp.id
GROUP BY sub_portfolio.id;

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
	sub_portfolio.id AS id,
    IFNULL(SUM(portfolio_stocks.stock_count * stock_value_latest.value), 0) AS net_value
FROM sub_portfolio
LEFT JOIN portfolio_stocks ON sub_portfolio.id = portfolio_stocks.id
LEFT JOIN stock_value_latest ON portfolio_stocks.stock_symbol = stock_value_latest.stock_symbol
GROUP BY sub_portfolio.id
;

-- -----------------------------------------------------
-- View `greed`.`competition_ext`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`competition_ext`;
USE `greed`;
CREATE  OR REPLACE VIEW competition_ext AS
SELECT
	competition.*,
    competition.unixtime_start + competition.unixtime_length AS unixtime_end,
    FROM_UNIXTIME(competition.unixtime_start + competition.unixtime_length) AS datetime_end
FROM competition;

-- -----------------------------------------------------
-- View `greed`.`transaction_ext`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`transaction_ext`;
USE `greed`;
CREATE  OR REPLACE VIEW transaction_ext AS
SELECT
	transaction.*,
    stock_value.unixtime AS stock_unixtime,
    stock_value.value AS value,
    (transaction.stock_count * stock_value.value) AS net_value
FROM transaction
JOIN stock_value
	ON transaction.stock_symbol = stock_value.stock_symbol AND transaction.unixtime >= stock_value.unixtime
LEFT OUTER JOIN stock_value sv
	ON stock_value.stock_symbol = sv.stock_symbol AND stock_value.unixtime < sv.unixtime AND transaction.unixtime >= sv.unixtime
WHERE sv.stock_symbol IS NULL;

-- -----------------------------------------------------
-- View `greed`.`stock_value_latest`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`stock_value_latest`;
USE `greed`;
CREATE  OR REPLACE VIEW stock_value_latest AS
SELECT
	stock_value.stock_symbol AS stock_symbol,
    stock_value.unixtime AS unixtime,
    stock_value.value AS value
    FROM stock_value
LEFT OUTER JOIN stock_value sv
ON (stock_value.stock_symbol = sv.stock_symbol AND stock_value.unixtime < sv.unixtime)
WHERE sv.stock_symbol IS NULL;

-- -----------------------------------------------------
-- View `greed`.`portfolio_value_total`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`portfolio_value_total`;
USE `greed`;
CREATE  OR REPLACE VIEW portfolio_value_total AS
SELECT
	portfolio_value_stock.id AS id,
    portfolio_value_stock.net_value AS value_stock,
    portfolio_value_cash.cash AS value_cash,
    portfolio_value_comp.comp_value AS value_comp,
    portfolio_value_stock.net_value + portfolio_value_cash.cash  + IFNULL(portfolio_value_comp.comp_value, 0) AS total_value
FROM portfolio_value_stock
JOIN portfolio_value_cash ON portfolio_value_stock.id = portfolio_value_cash.id
JOIN portfolio_value_comp ON portfolio_value_stock.id = portfolio_value_comp.id
;

-- -----------------------------------------------------
-- View `greed`.`portfolio_value_comp`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`portfolio_value_comp`;
USE `greed`;
CREATE  OR REPLACE VIEW portfolio_value_comp AS
SELECT
    sub_portfolio.id,
    IF(sub_portfolio.competition_id IS NULL, IFNULL(SUM(competition.entryfee), 0), NULL) AS comp_value
FROM sub_portfolio
LEFT JOIN sub_portfolio comp_sub_portfolio
	ON sub_portfolio.id != comp_sub_portfolio.id
    AND sub_portfolio.super_portfolio_id = comp_sub_portfolio.super_portfolio_id
    AND sub_portfolio.competition_id IS NULL
LEFT JOIN competition
	ON comp_sub_portfolio.competition_id = competition.id
    AND competition.unixtime_start + competition.unixtime_length > UNIX_TIMESTAMP(NOW())
GROUP BY sub_portfolio.id;

-- -----------------------------------------------------
-- View `greed`.`sub_portfolio_ext`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `greed`.`sub_portfolio_ext`;
USE `greed`;
CREATE  OR REPLACE VIEW sub_portfolio_ext AS
SELECT
	sub_portfolio.id,
	sub_portfolio.super_portfolio_id,
    sub_portfolio.competition_id,
    super_portfolio.name AS super_portfolio_name,
    competition.name AS competition_name,
    portfolio_value_total.value_stock AS value_stock,
    portfolio_value_total.value_cash AS value_cash,
    portfolio_value_total.value_comp AS value_comp,
    portfolio_value_total.total_value AS total_value
FROM sub_portfolio
JOIN super_portfolio ON sub_portfolio.super_portfolio_id = super_portfolio.id
LEFT JOIN competition ON sub_portfolio.competition_id = competition.id
JOIN portfolio_value_total ON sub_portfolio.id = portfolio_value_total.id
GROUP BY sub_portfolio.id
;
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

