CREATE DATABASE  IF NOT EXISTS `stock` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `stock`;
-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: stock
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `financial`
--

DROP TABLE IF EXISTS `financial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financial` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol_id` int NOT NULL,
  `year` int NOT NULL,
  `quarter` int NOT NULL,
  `quarter_end_date` datetime NOT NULL,
  `file_date` datetime DEFAULT NULL,
  `market_cap` decimal(18,2) DEFAULT NULL,
  `revenue` decimal(18,2) DEFAULT NULL,
  `gross_profit` decimal(18,2) DEFAULT NULL,
  `operating_income` decimal(18,2) DEFAULT NULL,
  `net_income` decimal(18,2) DEFAULT NULL,
  `current_assets` decimal(18,2) DEFAULT NULL,
  `ttl_assets` decimal(18,2) DEFAULT NULL,
  `current_liabilities` decimal(18,2) DEFAULT NULL,
  `ttl_liabilities` decimal(18,2) DEFAULT NULL,
  `ttl_equity` decimal(18,2) DEFAULT NULL,
  `revenue_growth` decimal(18,2) DEFAULT NULL,
  `revenue_qq_growth` decimal(18,2) DEFAULT NULL,
  `nopat_growth` decimal(18,2) DEFAULT NULL,
  `nopat_qq_growth` decimal(18,2) DEFAULT NULL,
  `net_income_growth` decimal(18,2) DEFAULT NULL,
  `net_income_qq_growth` decimal(18,2) DEFAULT NULL,
  `free_cash_flow` decimal(18,2) DEFAULT NULL,
  `current_ratio` decimal(18,2) DEFAULT NULL,
  `debt_to_equity_ratio` decimal(18,2) DEFAULT NULL,
  `pe_ratio` decimal(18,2) DEFAULT NULL,
  `pb_ratio` decimal(18,2) DEFAULT NULL,
  `div_payout_ratio` decimal(18,2) DEFAULT NULL,
  `roe` decimal(18,2) DEFAULT NULL,
  `roa` decimal(18,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financial`
--

LOCK TABLES `financial` WRITE;
/*!40000 ALTER TABLE `financial` DISABLE KEYS */;
/*!40000 ALTER TABLE `financial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_price_daily`
--

DROP TABLE IF EXISTS `stock_price_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_price_daily` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol_id` int NOT NULL,
  `price_date` datetime NOT NULL,
  `open_price` decimal(18,2) NOT NULL,
  `high_price` decimal(18,2) NOT NULL,
  `low_price` decimal(18,2) NOT NULL,
  `close_price` decimal(18,2) NOT NULL,
  `volume` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `unique_index_stock_price_daily` (`symbol_id`,`price_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_price_daily`
--

LOCK TABLES `stock_price_daily` WRITE;
/*!40000 ALTER TABLE `stock_price_daily` DISABLE KEYS */;
/*!40000 ALTER TABLE `stock_price_daily` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `symbol_master`
--

DROP TABLE IF EXISTS `symbol_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `symbol_master` (
  `id` int NOT NULL,
  `symbol` varchar(15) NOT NULL,
  `name` varchar(200) NOT NULL,
  `status` int NOT NULL,
  `instrument` varchar(50) NOT NULL,
  `sector` varchar(200) DEFAULT NULL,
  `industry` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `etf_price_daily`
--

DROP TABLE IF EXISTS `etf_price_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `etf_price_daily` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol_id` int NOT NULL,
  `price_date` datetime NOT NULL,
  `open_price` decimal(18,2) NOT NULL,
  `high_price` decimal(18,2) NOT NULL,
  `low_price` decimal(18,2) NOT NULL,
  `close_price` decimal(18,2) NOT NULL,
  `volume` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `unique_index_etf_price_daily` (`symbol_id`,`price_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trade_order`
--

DROP TABLE IF EXISTS `trade_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trade_order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stock_price_daily_id` int NOT NULL,
  `strategy` varchar(50) NOT NULL,
  `alpaca_id` varchar(200) DEFAULT NULL,
  `status` int NOT NULL,
  `action` varchar(50) NOT NULL,
  `qty` int NOT NULL,
  `order_type` varchar(50) DEFAULT NULL,
  `time_in_force` varchar(50) DEFAULT NULL,
  `target_price` decimal(18,2) DEFAULT NULL,
  `stop_loss` decimal(18,2) DEFAULT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `exit_stock_price_daily_id` int DEFAULT NULL,
  `exit_alpaca_id` varchar(200) DEFAULT NULL,
  `actual_qty` int DEFAULT NULL,
  `actual_entry_price` decimal(18,2) DEFAULT NULL,
  `actual_exit_price` decimal(18,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE VIEW `vw_symbol_stock_price_daily` AS
    SELECT 
        `s`.`id` AS `symbol_id`,
        `s`.`symbol` AS `symbol`,
        `s`.`name` AS `symbol_name`,
        `s`.`status` AS `status`,
        `s`.`instrument` AS `instrument`,
        `spd`.`id` AS `stock_price_daily_id`,
        `spd`.`price_date` AS `price_date`,
        `spd`.`open_price` AS `open_price`,
        `spd`.`high_price` AS `high_price`,
        `spd`.`low_price` AS `low_price`,
        `spd`.`close_price` AS `close_price`,
        `spd`.`volume` AS `volume`
    FROM
        (`symbol_master` `s`
        LEFT JOIN `stock_price_daily` `spd` ON ((`s`.`id` = `spd`.`symbol_id`)))
    WHERE
        (`spd`.`id` IS NOT NULL)
    ORDER BY `spd`.`symbol_id` , `spd`.`price_date`

CREATE VIEW `vw_symbol_etf_price_daily` AS
    SELECT 
        `s`.`id` AS `symbol_id`,
        `s`.`symbol` AS `symbol`,
        `s`.`name` AS `symbol_name`,
        `s`.`status` AS `status`,
        `s`.`instrument` AS `instrument`,
        `etf`.`id` AS `etf_price_daily_id`,
        `etf`.`price_date` AS `price_date`,
        `etf`.`open_price` AS `open_price`,
        `etf`.`high_price` AS `high_price`,
        `etf`.`low_price` AS `low_price`,
        `etf`.`close_price` AS `close_price`,
        `etf`.`volume` AS `volume`
    FROM
        (`symbol_master` `s`
        LEFT JOIN `etf_price_daily` `etf` ON ((`s`.`id` = `etf`.`symbol_id`)))
    WHERE
        (`etf`.`id` IS NOT NULL)
    ORDER BY `etf`.`symbol_id` , `etf`.`price_date`

ALTER USER 'xxxx'@'xxxx' IDENTIFIED WITH mysql_native_password BY 'xxxx';
SET GLOBAL max_allowed_packet=67108864;