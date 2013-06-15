SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `jugi` ;
CREATE SCHEMA IF NOT EXISTS `jugi` DEFAULT CHARACTER SET utf8 ;
USE `jugi` ;

-- -----------------------------------------------------
-- Table `jugi`.`Section`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jugi`.`Section` ;

CREATE  TABLE IF NOT EXISTS `jugi`.`Section` (
  `id_section` INT NOT NULL ,
  `name` TEXT NOT NULL ,
  `canton` CHAR(2) NULL ,
  PRIMARY KEY (`id_section`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `jugi`.`Category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jugi`.`Category` ;

CREATE  TABLE IF NOT EXISTS `jugi`.`Category` (
  `category` ENUM('MJ','MA','MB','MC','MD','ME','MF','KJ','KA','KB','KC','KD','KE','KF') NOT NULL ,
  `age_cohort` INT NOT NULL ,
  `age` INT NULL ,
  `category_code` ENUM('J','A','B','C','D','E','F') NULL ,
  `sex` ENUM('f','m') NULL ,
  `sprint_distance` DECIMAL(5,0) NULL DEFAULT 0 ,
  `has_longjump` TINYINT(1) NULL ,
  `has_highjump` TINYINT(1) NULL ,
  `has_shotput` TINYINT(1) NULL ,
  `has_ball` TINYINT(1) NULL ,
  PRIMARY KEY (`category`, `age_cohort`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `jugi`.`Athlete`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jugi`.`Athlete` ;

CREATE  TABLE IF NOT EXISTS `jugi`.`Athlete` (
  `id_athlete` INT NOT NULL AUTO_INCREMENT ,
  `number` INT NULL DEFAULT NULL ,
  `firstname` TEXT NOT NULL ,
  `lastname` TEXT NOT NULL ,
  `section` INT NOT NULL DEFAULT 0 ,
  `year_of_birth` INT(11) NOT NULL ,
  `sex` ENUM('f','m') NOT NULL ,
  `category` ENUM('MJ','MA','MB','MC','MD','ME','MF','KJ','KA','KB','KC','KD','KE','KF') NOT NULL ,
  `category_code` ENUM('J','A','B','C','D','E','F') NOT NULL ,
  `sprint_result` DECIMAL(5,2) NULL DEFAULT NULL ,
  `longjump_result` DECIMAL(5,2) NULL DEFAULT NULL ,
  `highjump_result` DECIMAL(5,2) NULL DEFAULT NULL ,
  `shotput_result` DECIMAL(5,2) NULL DEFAULT NULL ,
  `ball_result` DECIMAL(5,2) NULL DEFAULT NULL ,
  `sprint_points` INT NULL DEFAULT NULL ,
  `longjump_points` INT NULL DEFAULT NULL ,
  `highjump_points` INT NULL DEFAULT NULL ,
  `shotput_points` INT NULL ,
  `ball_points` INT NULL DEFAULT NULL ,
  `total_points` INT NOT NULL DEFAULT 0 ,
  `award` ENUM('GOLD','SILVER','BRONZE') NULL DEFAULT NULL ,
  `qualify` TINYINT(1) NOT NULL DEFAULT FALSE ,
  `rank` INT NULL DEFAULT NULL ,
  `verified` TINYINT(1) NULL DEFAULT FALSE ,
  PRIMARY KEY (`id_athlete`) ,
  UNIQUE INDEX `number_UNIQUE` (`number` ASC) ,
  INDEX `category_idx` (`category` ASC) ,
  INDEX `categorycode_idx` (`category_code` ASC) ,
  INDEX `fk_Athlete_Section` (`section` ASC) ,
  INDEX `fk_Athlete_Category` (`category` ASC, `year_of_birth` ASC) ,
  CONSTRAINT `fk_Athlete_Section`
    FOREIGN KEY (`section` )
    REFERENCES `jugi`.`Section` (`id_section` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Athlete_Category`
    FOREIGN KEY (`category` , `year_of_birth` )
    REFERENCES `jugi`.`Category` (`category` , `age_cohort` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


CREATE USER `jugiuser` IDENTIFIED BY 'jugi';


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `jugi`.`Section`
-- -----------------------------------------------------
START TRANSACTION;
USE `jugi`;
INSERT INTO `jugi`.`Section` (`id_section`, `name`, `canton`) VALUES (1, 'Neuhausen', 'SH');
INSERT INTO `jugi`.`Section` (`id_section`, `name`, `canton`) VALUES (2, 'Schaffhausen', 'SH');
INSERT INTO `jugi`.`Section` (`id_section`, `name`, `canton`) VALUES (3, 'Dachsen', 'ZH');
INSERT INTO `jugi`.`Section` (`id_section`, `name`, `canton`) VALUES (4, 'Oerlikon', 'ZH');
INSERT INTO `jugi`.`Section` (`id_section`, `name`, `canton`) VALUES (5, 'Dürnten', 'ZH');
INSERT INTO `jugi`.`Section` (`id_section`, `name`, `canton`) VALUES (6, 'Frauenfeld', 'TG');
INSERT INTO `jugi`.`Section` (`id_section`, `name`, `canton`) VALUES (7, 'Kreuzlingen', 'TG');
INSERT INTO `jugi`.`Section` (`id_section`, `name`, `canton`) VALUES (8, 'Herisau', 'AR');

COMMIT;

-- -----------------------------------------------------
-- Data for table `jugi`.`Category`
-- -----------------------------------------------------
START TRANSACTION;
USE `jugi`;
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MF', 2007, 6, 'F', 'f', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MF', 2006, 7, 'F', 'f', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KF', 2007, 6, 'F', 'm', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KF', 2006, 7, 'F', 'm', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('ME', 2005, 8, 'E', 'f', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('ME', 2004, 9, 'E', 'f', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KE', 2005, 8, 'E', 'm', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KE', 2004, 9, 'E', 'm', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MD', 2003, 10, 'D', 'f', 60, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MD', 2002, 11, 'D', 'f', 60, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KD', 2003, 10, 'D', 'm', 60, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KD', 2002, 11, 'D', 'm', 60, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MC', 2001, 12, 'C', 'f', 60, 1, 1, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MC', 2000, 13, 'C', 'f', 60, 1, 1, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KC', 2001, 12, 'C', 'm', 60, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KC', 2000, 13, 'C', 'm', 60, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MB', 1999, 14, 'B', 'f', 80, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MB', 1998, 15, 'B', 'f', 80, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KB', 1999, 14, 'B', 'm', 80, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KB', 1998, 15, 'B', 'm', 80, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MA', 1997, 16, 'A', 'f', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MA', 1996, 17, 'A', 'f', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KA', 1997, 16, 'A', 'm', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KA', 1996, 17, 'A', 'm', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MJ', 1995, 18, 'J', 'f', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MJ', 1994, 19, 'J', 'f', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KJ', 1995, 18, 'J', 'm', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KJ', 1994, 19, 'J', 'm', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MF', 2008, 5, 'F', 'f', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `age_cohort`, `age`, `category_code`, `sex`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KF', 2008, 5, 'F', 'm', 50, 1, 0, 0, 1);

COMMIT;
