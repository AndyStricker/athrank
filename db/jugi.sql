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
-- Table `jugi`.`Athlete`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jugi`.`Athlete` ;

CREATE  TABLE IF NOT EXISTS `jugi`.`Athlete` (
  `id_athlete` INT NOT NULL AUTO_INCREMENT ,
  `number` INT NOT NULL DEFAULT 0 ,
  `firstname` TEXT NOT NULL ,
  `lastname` TEXT NOT NULL ,
  `section` INT NOT NULL DEFAULT 0 ,
  `year_of_birth` INT(11) NOT NULL ,
  `sex` ENUM('w','m') NOT NULL ,
  `category` ENUM('MJ','MA','MB','MC','MD','ME','MF','KJ','KA','KB','KC','KD','KE','KF') NOT NULL ,
  `category_code` ENUM('J','A','B','C','D','E','F') NOT NULL ,
  `sprint_result` DECIMAL NULL DEFAULT NULL ,
  `longjump_result` DECIMAL NULL DEFAULT NULL ,
  `highjump_result` DECIMAL NULL DEFAULT NULL ,
  `shotput_result` DECIMAL NULL DEFAULT NULL ,
  `ball_result` DECIMAL NULL DEFAULT NULL ,
  `sprint_points` INT NULL DEFAULT NULL ,
  `longjump_points` INT NULL DEFAULT NULL ,
  `highjump_points` INT NULL DEFAULT NULL ,
  `ball_points` INT NULL DEFAULT NULL ,
  `total_points` INT NOT NULL DEFAULT 0 ,
  `award` ENUM('GOLD','SILVER','BRONZE') NULL DEFAULT NULL ,
  `qualify` TINYINT(1) NOT NULL DEFAULT FALSE ,
  PRIMARY KEY (`id_athlete`) ,
  UNIQUE INDEX `number_UNIQUE` (`number` ASC) ,
  INDEX `category_idx` (`category` ASC) ,
  INDEX `categorycode_idx` (`category_code` ASC) ,
  INDEX `fk_Athlete_Section` (`section` ASC) ,
  CONSTRAINT `fk_Athlete_Section`
    FOREIGN KEY (`section` )
    REFERENCES `jugi`.`Section` (`id_section` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


CREATE USER `jugiuser` IDENTIFIED BY 'jugi';


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
