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
  `sprint_distance` DECIMAL(5,0) NULL DEFAULT 0 ,
  `has_longjump` TINYINT(1) NULL ,
  `has_highjump` TINYINT(1) NULL ,
  `has_shotput` TINYINT(1) NULL ,
  `has_ball` TINYINT(1) NULL ,
  PRIMARY KEY (`category`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `jugi`.`AgeCategory`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jugi`.`AgeCategory` ;

CREATE  TABLE IF NOT EXISTS `jugi`.`AgeCategory` (
  `age_cohort` INT NOT NULL ,
  `sex` ENUM('f','m') NOT NULL ,
  `category` ENUM('MJ','MA','MB','MC','MD','ME','MF','KJ','KA','KB','KC','KD','KE','KF') NOT NULL ,
  `age` INT NOT NULL ,
  PRIMARY KEY (`age_cohort`, `sex`) ,
  INDEX `fk_AgeCategory_Category` (`category` ASC) ,
  CONSTRAINT `fk_AgeCategory_Category`
    FOREIGN KEY (`category` )
    REFERENCES `jugi`.`Category` (`category` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


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
  `award` ENUM('GOLD','SILVER','BRONZE','AWARD') NULL DEFAULT NULL ,
  `qualify` TINYINT(1) NOT NULL DEFAULT FALSE ,
  `rank` INT NULL DEFAULT NULL ,
  `verified` TINYINT(1) NULL DEFAULT FALSE ,
  PRIMARY KEY (`id_athlete`) ,
  UNIQUE INDEX `number_UNIQUE` (`number` ASC) ,
  INDEX `category_idx` (`category` ASC) ,
  INDEX `fk_Athlete_Section` (`section` ASC) ,
  INDEX `fk_Athlete_Category` (`category` ASC, `year_of_birth` ASC) ,
  INDEX `fk_Athlete_AgeCategory` (`year_of_birth` ASC, `sex` ASC) ,
  CONSTRAINT `fk_Athlete_Section`
    FOREIGN KEY (`section` )
    REFERENCES `jugi`.`Section` (`id_section` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Athlete_Category`
    FOREIGN KEY (`category` )
    REFERENCES `jugi`.`Category` (`category` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Athlete_AgeCategory`
    FOREIGN KEY (`year_of_birth` , `sex` )
    REFERENCES `jugi`.`AgeCategory` (`age_cohort` , `sex` )
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
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MF', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KF', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('ME', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KE', 50, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MD', 60, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KD', 60, 1, 0, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MC', 60, 1, 1, 0, 1);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KC', 60, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MB', 80, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KB', 80, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MA', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KA', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('MJ', 100, 1, 1, 1, 0);
INSERT INTO `jugi`.`Category` (`category`, `sprint_distance`, `has_longjump`, `has_highjump`, `has_shotput`, `has_ball`) VALUES ('KJ', 100, 1, 1, 1, 0);

COMMIT;

-- -----------------------------------------------------
-- Data for table `jugi`.`AgeCategory`
-- -----------------------------------------------------
START TRANSACTION;
USE `jugi`;
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1994, 'm', 'KJ', 19);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1994, 'f', 'MJ', 19);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1995, 'm', 'KJ', 18);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1995, 'f', 'MJ', 18);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1996, 'm', 'KA', 17);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1996, 'f', 'MA', 17);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1997, 'm', 'KA', 16);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1997, 'f', 'MA', 16);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1998, 'm', 'KB', 15);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1998, 'f', 'MB', 15);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1999, 'm', 'KB', 14);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (1999, 'f', 'MB', 14);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2000, 'm', 'KC', 13);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2000, 'f', 'MC', 13);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2001, 'm', 'KC', 12);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2001, 'f', 'MC', 12);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2002, 'm', 'KD', 11);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2002, 'f', 'MD', 11);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2003, 'm', 'KD', 10);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2003, 'f', 'MD', 10);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2004, 'm', 'KE', 9);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2004, 'f', 'ME', 9);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2005, 'm', 'KE', 8);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2005, 'f', 'ME', 8);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2006, 'm', 'KF', 7);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2006, 'f', 'MF', 7);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2007, 'm', 'KF', 6);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2007, 'f', 'MF', 6);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2008, 'm', 'KF', 5);
INSERT INTO `jugi`.`AgeCategory` (`age_cohort`, `sex`, `category`, `age`) VALUES (2008, 'f', 'MF', 5);

COMMIT;
