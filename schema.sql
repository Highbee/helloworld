CREATE DATABASE  IF NOT EXISTS `ayodele` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ayodele`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: ayodele
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `bleaching_process`
--

DROP TABLE IF EXISTS `bleaching_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bleaching_process` (
  `idbleaching_process` int NOT NULL AUTO_INCREMENT,
  `production_chemist_employee_id` int NOT NULL,
  `batch_number` varchar(9) DEFAULT NULL,
  `date` date NOT NULL,
  `shift` varchar(9) NOT NULL,
  `comments` varchar(255) NOT NULL,
  `number_of_cakes_to_rebleached` int NOT NULL,
  `number_of_rebleach_added` int NOT NULL,
  PRIMARY KEY (`idbleaching_process`),
  UNIQUE KEY `batch_number_UNIQUE` (`batch_number`),
  KEY `bleaching_process_to_employees_idx` (`production_chemist_employee_id`),
  CONSTRAINT `bleaching_process_production_chemist_id_to_employees` FOREIGN KEY (`production_chemist_employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bleaching_process`
--

LOCK TABLES `bleaching_process` WRITE;
/*!40000 ALTER TABLE `bleaching_process` DISABLE KEYS */;
INSERT INTO `bleaching_process` VALUES (3,5,'0825DC01N','2025-08-01','Night','Good',0,0),(4,7,'0825DC01A','2025-08-01','Afternoon','Good',0,0),(5,7,'0825DC02A','2025-08-02','Afternoon','Good',0,0),(6,5,'0825DC04N','2025-08-04','Night','Good',0,0),(7,7,'0825DC04M','2025-08-04','Morning','Good',0,0),(8,5,'0825DC05N','2025-08-05','Night','Good',0,0),(9,7,'0825DC05M','2025-08-05','Morning','Good',0,0),(10,5,'0825DC05A','2025-08-05','Afternoon','Good',0,0),(11,4,'0825DC06N','2025-08-06','Night','Good',0,0),(12,5,'0825DC07M','2025-08-07','Morning','Good',0,0);
/*!40000 ALTER TABLE `bleaching_process` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `employee_id` int NOT NULL AUTO_INCREMENT,
  `status_id` int NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `gender` char(1) NOT NULL,
  PRIMARY KEY (`employee_id`),
  KEY `fk_employees_status1_idx` (`status_id`),
  CONSTRAINT `fk_employees_status1` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,1,'Sarat','Oseni','f'),(2,2,'Titilayo','Abdulkabir','f'),(3,1,'Taiye','Ibrahim','m'),(4,1,'Olayemi','Oyeniyi','m'),(5,1,'Joel','Afuye','m'),(6,1,'Olaoye','Emmanuel','m'),(7,1,'Azeez','Kabiru','m');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kier_processors`
--

DROP TABLE IF EXISTS `kier_processors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kier_processors` (
  `batch_number` varchar(9) NOT NULL,
  `employee_id` int NOT NULL,
  PRIMARY KEY (`batch_number`,`employee_id`),
  CONSTRAINT `bp_kp_batch_number` FOREIGN KEY (`batch_number`) REFERENCES `bleaching_process` (`batch_number`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kier_processors`
--

LOCK TABLES `kier_processors` WRITE;
/*!40000 ALTER TABLE `kier_processors` DISABLE KEYS */;
INSERT INTO `kier_processors` VALUES ('0825DC06N',4),('0825DC06N',5),('0825DC07M',5),('0825DC07M',6),('0825DC07M',7);
/*!40000 ALTER TABLE `kier_processors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productions`
--

DROP TABLE IF EXISTS `productions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productions` (
  `production_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `supervisor_employee_id` int NOT NULL,
  `date` date NOT NULL,
  `batch_number` varchar(10) NOT NULL,
  `shift` varchar(15) NOT NULL DEFAULT 'NA',
  `production_line` varchar(1) NOT NULL,
  `quantity_produced` int NOT NULL,
  `packaging_supervisor` varchar(45) NOT NULL,
  `notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`production_id`),
  KEY `fk_productions_employees1_idx` (`supervisor_employee_id`),
  KEY `fk_productions_products1_idx` (`product_id`),
  CONSTRAINT `fk_productions_employees1` FOREIGN KEY (`supervisor_employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_productions_products1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=480 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productions`
--

LOCK TABLES `productions` WRITE;
/*!40000 ALTER TABLE `productions` DISABLE KEYS */;
INSERT INTO `productions` VALUES (1,1,1,'2025-07-01','0625DC29M','NA','A',16,'1',NULL),(2,3,1,'2025-07-01','0625DC29M','NA','A',2,'1','This was the WIP from 30th of  June  Afternoon shiift (Package by Mr Mutiu from Knitting Section, counted by Ibrahim, I. O)'),(3,2,1,'2025-07-01','0625DC30N','NA','A',15,'1',NULL),(4,3,1,'2025-07-01','0625DC30N','NA','A',8,'1',NULL),(5,2,1,'2025-07-01','0625DC30M','NA','A',27,'1',NULL),(6,4,1,'2025-07-01','0625DC30M','NA','A',13,'1',NULL),(7,1,2,'2025-07-01','0625DC29M','NA','B',10,'2',NULL),(8,1,2,'2025-07-01','0625DC30N','NA','B',27,'2',NULL),(9,3,2,'2025-07-01','0625DC30N','NA','B',4,'2',NULL),(10,1,2,'2025-07-01','0625DC30M','NA','B',20,'2',NULL),(11,2,2,'2025-07-01','0625DC30M','NA','B',11,'2',NULL),(12,4,2,'2025-07-01','0625DC30M','NA','B',8,'2',NULL),(13,2,1,'2025-07-02','0625DC30M','NA','A',24,'1',NULL),(14,2,1,'2025-07-02','0725DC01N','NA','A',16,'1',NULL),(15,2,1,'2025-07-02','0725DC01M','NA','A',17,'1',NULL),(16,4,1,'2025-07-02','0625DC30M','NA','A',10,'1',NULL),(17,4,1,'2025-07-02','0725DC01N','NA','A',2,'1',NULL),(18,1,2,'2025-07-02','0725DC01M','NA','B',24,'2',NULL),(19,1,2,'2025-07-02','0725DC01N','NA','B',12,'2',NULL),(20,4,2,'2025-07-02','0725DC01M','NA','B',5,'2',NULL),(21,4,2,'2025-07-02','0725DC01N','NA','B',5,'2',NULL),(22,4,2,'2025-07-02','0725DC02N','NA','B',6,'2',NULL),(23,1,2,'2025-07-02','0725DC02N','NA','B',16,'2',NULL),(24,1,1,'2025-07-03','0725DC01M','NA','B',18,'1','Mr Oseni Supervised but production line. Reason, Mrs Abdulkabir lost a brother'),(25,3,1,'2025-07-03','0725DC01M','NA','B',4,'1','Mr Oseni Supervised but production line. Reason, Mrs Abdulkabir lost a brother'),(26,4,1,'2025-07-03','0725DC01M','NA','B',3,'1','Mr Oseni Supervised but production line. Reason, Mrs Abdulkabir lost a brother'),(27,1,1,'2025-07-03','0725DC02M','NA','B',28,'1','Mr Oseni Supervised but production line. Reason, Mrs Abdulkabir lost a brother'),(28,3,1,'2025-07-03','0725DC02M','NA','B',10,'1','Mr Oseni Supervised but production line. Reason, Mrs Abdulkabir lost a brother'),(29,3,1,'2025-07-03','0725DC03N','NA','B',2,'1','Mr Oseni Supervised but production line. Reason, Mrs Abdulkabir lost a brother'),(30,1,1,'2025-07-03','0725DC03N','NA','B',5,'1','Mr Oseni Supervised but production line. Reason, Mrs Abdulkabir lost a brother'),(31,2,1,'2025-07-03','0725DC01M','NA','A',18,'1',NULL),(47,4,1,'2025-07-03','0725DC01M','NA','A',6,'1',NULL),(48,2,1,'2025-07-03','0725DC02N','NA','A',35,'1',NULL),(49,4,1,'2025-07-03','0725DC02N','NA','A',4,'1',NULL),(50,3,1,'2025-07-03','0725DC02N','NA','A',2,'1',NULL),(51,2,1,'2025-07-03','0725DC03N','NA','A',10,'1',NULL),(52,3,1,'2025-07-04','0725DC03N','NA','A',13,'1',NULL),(53,2,1,'2025-07-04','0725DC04N','NA','A',22,'1',NULL),(54,6,1,'2025-07-04','0725DC04N','NA','A',6,'1',NULL),(55,3,1,'2025-07-04','0725DC03N','NA','B',18,'1','Mrs Abdulkabir lost a brother, so Mrs Oseni supervised both sections'),(56,2,1,'2025-07-04','0725DC04N','NA','B',9,'1','Mrs Abdulkabir lost a brother, so Mrs Oseni supervised both sections'),(57,3,1,'2025-07-04','0725DC04N','NA','B',2,'1','Mrs Abdulkabir lost a brother, so Mrs Oseni supervised both sections'),(58,2,1,'2025-07-04','0725DC03N','NA','B',5,'1','Mrs Abdulkabir lost a brother, so Mrs Oseni supervised both sections'),(59,1,1,'2025-07-05','0725DC04N','NA','A',14,'1','We had two transfer for this day at both section; these products were tranferred with first '),(60,1,1,'2025-07-05','0725DC04N','NA','A',3,'1','We had two transfer for this day at both section; these products were tranferred with first '),(61,3,1,'2025-07-05','0725DC04N','NA','A',12,'1','We had two transfer for this day at both section; these products were tranferred with first '),(62,1,1,'2025-07-05','0725DC04M','NA','A',20,'1','We had two transfer for this day at both section; these products were tranferred with first '),(63,3,1,'2025-07-05','0725DC04M','NA','A',6,'1','We had two transfer for this day at both section; these products were tranferred with first '),(64,1,1,'2025-07-05','0725DC05N','NA','A',6,'1','We had two transfer for this day at both section; these products were tranferred with first '),(65,3,1,'2025-07-05','0725DC05N','NA','A',1,'1','We had two transfer for this day at both section; these products were tranferred with first '),(66,1,2,'2025-07-05','0725DC03N','NA','B',13,'2','Line BTransfer 1 of 2 for the day'),(73,1,2,'2025-07-05','0725DC04N','NA','B',18,'2','Went with transfer 1 of 2 for the day'),(74,1,2,'2025-07-05','0725DC04M','NA','B',25,'2','Went with transfer 1 of 2 for the day'),(75,3,2,'2025-07-05','0725DC03N','NA','B',2,'2','Went with transfer 1 of 2 for the day'),(76,6,2,'2025-07-05','0725DC03N','NA','B',5,'2','Went with transfer 1 of 2 for the day'),(78,3,2,'2025-07-05','0725DC04N','NA','B',6,'2','Transfer 2 of 2'),(79,1,1,'2025-07-05','0725DC05N','NA','A',6,'1','Transfer 2 of 2'),(80,3,1,'2025-07-05','0725DC05N','NA','A',1,'1','Transfer 2 of 2'),(81,1,2,'2025-07-07','0725DC05N','NA','B',35,'2',NULL),(82,1,2,'2025-07-07','0725DC05M','NA','B',14,'2',NULL),(83,4,2,'2025-07-07','0725DC05M','NA','B',17,'2',NULL),(84,3,2,'2025-07-07','0725DC05M','NA','B',6,'2',NULL),(85,1,1,'2025-07-07','0725DC05N','NA','A',6,'1',NULL),(86,2,1,'2025-07-07','0725DC05N','NA','A',28,'1',NULL),(87,3,1,'2025-07-07','0725DC05N','NA','A',10,'1',NULL),(88,1,1,'2025-07-07','0725DC05M','NA','A',21,'1',NULL),(89,4,1,'2025-07-07','0725DC05M','NA','A',12,'1',NULL),(90,1,1,'2025-07-08','0725DC07M','NA','A',19,'1',NULL),(91,2,1,'2025-07-08','0725DC07N','NA','A',35,'1',NULL),(92,2,1,'2025-07-08','0725DC07M','NA','A',3,'1',NULL),(93,2,1,'2025-07-08','0725DC05M','NA','A',6,'1',NULL),(94,4,1,'2025-07-08','0725DC05M','NA','A',2,'1',NULL),(95,4,1,'2025-07-08','0725DC07N','NA','A',6,'1',NULL),(96,4,1,'2025-07-08','0725DC07M','NA','A',1,'1',NULL),(97,6,1,'2025-07-08','0725DC07M','NA','A',10,'1',NULL),(98,1,2,'2025-07-08','0725DC07N','NA','B',31,'2',NULL),(99,1,2,'2025-07-08','0725DC07M','NA','B',39,'2',NULL),(100,4,2,'2025-07-08','0725DC05M','NA','B',3,'2',NULL),(101,4,2,'2025-07-08','0725DC07N','NA','B',8,'2',NULL),(102,6,2,'2025-07-08','0725DC07M','NA','B',14,'2','Line B did transfer twice and this was the only product in transfer 2 of 2. Line A transferred just once'),(103,1,1,'2025-07-09','0725DC07M','NA','A',12,'2',NULL),(104,4,1,'2025-07-09','0725DC07M','NA','A',2,'2',NULL),(105,6,1,'2025-07-09','0725DC07M','NA','A',5,'2',NULL),(106,1,1,'2025-07-09','0725DC08N','NA','A',50,'2',NULL),(107,6,1,'2025-07-09','0725DC08M','NA','A',15,'2',NULL),(108,1,1,'2025-07-09','0725DC08N','NA','A',10,'2',NULL),(109,1,2,'2025-07-09','0725DC08N','NA','B',28,'2',NULL),(110,6,2,'2025-07-09','0725DC07N','NA','B',22,'2',NULL),(111,5,2,'2025-07-09','0725DC07N','NA','B',11,'2',NULL),(112,1,1,'2025-07-09','0725DC08M','NA','A',2,'1','Transfer 2 of 2 in A'),(113,5,1,'2025-07-09','0725DC08M','NA','A',5,'1','Transfer 2 of 2 in A'),(114,1,2,'2025-07-09','0725DC08M','NA','B',15,'2','Transfer 2 of 2 in B'),(115,5,2,'2025-07-09','0725DC08M','NA','B',11,'2','Transfer 2 of 2 in B'),(116,1,1,'2025-07-10','0725DC08M','NA','A',1,'1','Transfer 1 of 2'),(117,3,1,'2025-07-10','0725DC08M','NA','A',10,'1','Transfer 1 of 2'),(118,3,1,'2025-07-10','0725DC08A','NA','A',43,'1','Transfer 1 of 2'),(119,4,2,'2025-07-10','0725DC08M','NA','B',25,'2','Transfer 1 of 3 in line B'),(120,4,2,'2025-07-10','0725DC09N','NA','B',30,'2','Transfer 1 of 3 in line B'),(121,1,2,'2025-07-10','0725DC08M','NA','B',5,'2','Transfer 1 of 3 in line B'),(122,1,1,'2025-07-10','0725DC09N','NA','A',14,'1','Transfer 2 of 2 in line A'),(123,4,1,'2025-07-10','0725DC08A','NA','A',10,'1','Transfer 2 of 2 in line A'),(124,4,1,'2025-07-10','0725DC09N','NA','A',4,'1','Transfer 2 of 2 in line A'),(125,5,2,'2025-07-10','0725DC08M','NA','B',10,'2','Transfer 2 of 3 in line B'),(126,1,2,'2025-07-10','0725DC08M','NA','B',12,'2','Transfer 3 of 3 in line B'),(127,1,2,'2025-07-10','0725DC08A','NA','B',17,'2','Transfer 3 of 3 in line B'),(128,4,2,'2025-07-10','0725DC08M','NA','B',16,'2','Transfer 3 of 3 in line B'),(129,4,2,'2025-07-10','0725DC09N','NA','B',7,'2','Transfer 3 of 3 in line B'),(130,4,2,'2025-07-01','0625DC30N','NA','B',8,'2',NULL),(131,4,2,'2025-07-02','0625DC30M','NA','B',8,'2','Late input into database because the supervisor lost track of batch number. Can\'t be sure it was 0625DC30M. '),(132,3,2,'2025-07-02','0625DC30N','NA','B',1,'2','delayed input blamed on late submission by the supersivor; she lost a brother'),(133,5,1,'2025-07-11','0725DC10N','NA','A',5,'1','Went with transfer 1 of 2'),(134,6,1,'2025-07-11','0725DC10N','NA','A',2,'1','Went with transfer 1 of 2'),(135,6,2,'2025-07-11','0725DC09N','NA','B',2,'2','Went with transfer 1 of 2'),(136,6,2,'2025-07-11','0725DC09N','NA','B',1,'2','Went with transfer 1 of 2'),(137,4,2,'2025-07-11','0725DC09N','NA','B',5,'2','Went with transfer 1 of 2'),(138,5,2,'2025-07-11','0725DC09N','NA','B',3,'2','Went with transfer 1 of 2'),(139,5,2,'2025-07-11','0725DC09N','NA','B',1,'2','Went with transfer 1 of 2'),(140,1,1,'2025-07-11','0725DC09N','NA','A',12,'1','Transfer 2 of 2 in A'),(141,1,1,'2025-07-11','0725DC09A','NA','A',16,'1','Transfer 2 of 2 in A'),(142,3,1,'2025-07-11','0725DC09A','NA','A',4,'1','Transfer 2 of 2 in A'),(143,3,1,'2025-07-11','0725DC09A','NA','A',1,'1','Transfer 2 of 2 in A'),(144,5,1,'2025-07-11','0725DC10N','NA','A',3,'1','Transfer 2 of 2 in A'),(145,1,1,'2025-07-11','0725DC10N','NA','A',35,'1','Transfer 2 of 2 in A'),(146,3,1,'2025-07-11','0725DC10N','NA','A',2,'1','Transfer 2 of 2 in A'),(147,1,1,'2025-07-11','0725DC10M','NA','A',14,'1','Transfer 2 of 2 in A'),(148,1,2,'2025-07-11','0725DC09N','NA','B',19,'2','Transfer 2 of 2 in B'),(149,1,2,'2025-07-11','0725DC09N','NA','B',14,'2','Transfer 2 of 2 in B'),(150,1,2,'2025-07-11','0725DC09A','NA','B',17,'2','Transfer 2 of 2 in B'),(151,1,2,'2025-07-11','0725DC10N','NA','B',11,'2','Transfer 2 of 2 in B'),(152,1,2,'2025-07-11','0725DC10N','NA','B',25,'2','Transfer 2 of 2 in B'),(153,5,2,'2025-07-11','0725DC09N','NA','B',4,'2','Transfer 2 of 2 in B'),(154,2,1,'2025-07-12','0725DC10N','NA','A',13,'1',NULL),(155,2,1,'2025-07-12','0725DC10M','NA','A',19,'1',NULL),(156,5,1,'2025-07-12','0725DC10N','NA','A',8,'1',NULL),(157,5,1,'2025-07-12','0725DC10M','NA','A',5,'1',NULL),(158,2,1,'2025-07-12','0725DC11N','NA','A',16,'1',NULL),(159,6,1,'2025-07-12','0725DC11N','NA','A',4,'1',NULL),(160,2,1,'2025-07-12','0725DC12N','NA','A',8,'1',NULL),(161,1,2,'2025-07-12','0725DC10M','NA','B',17,'2',NULL),(162,1,2,'2025-07-12','0725DC10M','NA','B',12,'2',NULL),(163,1,2,'2025-07-12','0725DC10N','NA','B',22,'2',NULL),(164,1,2,'2025-07-12','0725DC11N','NA','B',14,'2',NULL),(165,1,2,'2025-07-12','0725DC11N','NA','B',6,'2',NULL),(166,6,2,'2025-07-12','0725DC09N','NA','B',16,'2',NULL),(167,2,1,'2025-07-14','0725DC12N','NA','A',40,'1',NULL),(168,2,1,'2025-07-14','0725DC12M','NA','A',16,'1',NULL),(169,1,1,'2025-07-14','0725DC12M','NA','A',9,'1',NULL),(170,1,1,'2025-07-14','0725DC13N','NA','A',14,'1',NULL),(171,3,1,'2025-07-14','0725DC12N','NA','A',10,'1',NULL),(172,3,1,'2025-07-14','0725DC12M','NA','A',2,'1',NULL),(173,5,1,'2025-07-14','0725DC12N','NA','A',1,'1',NULL),(174,3,1,'2025-07-14','0725DC13N','NA','A',1,'1',NULL),(175,1,1,'2025-07-14','0725DC13N','NA','A',5,'1',NULL),(176,1,2,'2025-07-14','0725DC12M','NA','B',30,'2','Went with Transfer 1 of 2 in B. A did one'),(177,1,2,'2025-07-14','0725DC13M','NA','B',5,'2','Went with Transfer 1 of 2 in B. A did one'),(178,3,2,'2025-07-14','0725DC10M','NA','B',9,'2','Went with Transfer 1 of 2 in B. A did one'),(179,1,2,'2025-07-14','0725DC12N','NA','B',22,'2','Went with Transfer 2 of 2'),(180,1,2,'2025-07-14','0725DC12M','NA','B',33,'2','Went with Transfer 2 of 2'),(181,6,2,'2025-07-14','0725DC09N','NA','B',16,'2','Went with Transfer 2 of 2'),(182,1,2,'2025-07-15','0725DC13N','NA','B',11,'2','Went with Transfer 1 of 2 in B'),(183,1,2,'2025-07-15','0725DC14N','NA','B',15,'2','Went with Transfer 1 of 2 in B'),(184,2,2,'2025-07-15','0725DC14N','NA','B',20,'2','Went with Transfer 1 of 2 in B'),(185,3,2,'2025-07-15','0725DC10M','NA','B',17,'2','Went with Transfer 1 of 2 in B'),(186,3,2,'2025-07-15','0725DC11N','NA','B',11,'2','Went with Transfer 1 of 2 in B'),(187,4,2,'2025-07-15','0725DC14N','NA','B',4,'2','Went with Transfer 1 of 2 in B'),(188,5,2,'2025-07-15','0725DC13N','NA','B',5,'2','Went with Transfer 1 of 2 in B'),(189,6,2,'2025-07-15','0725DC14N','NA','B',5,'2','Went with Transfer 1 of 2 in B'),(190,1,1,'2025-07-15','0725DC13N','NA','A',8,'1','Transfer 1 of 1'),(191,1,1,'2025-07-15','0725DC14N','NA','A',11,'1','Transfer 1 of 1'),(192,1,1,'2025-07-15','0725DC14M','NA','A',4,'1','Transfer 1 of 1'),(193,2,1,'2025-07-15','0725DC13N','NA','A',2,'1','Transfer 1 of 1'),(194,2,1,'2025-07-15','0725DC14N','NA','A',18,'1','Transfer 1 of 1'),(195,2,1,'2025-07-15','0725DC14M','NA','A',16,'1','Transfer 1 of 1'),(196,3,1,'2025-07-15','0725DC14N','NA','A',6,'1','Transfer 1 of 1'),(197,2,2,'2025-07-15','0725DC14N','NA','B',6,'2','Transfer 2 of 2 in B'),(198,3,2,'2025-07-15','0725DC14N','NA','B',8,'2','Transfer 2 of 2 in B'),(199,3,2,'2025-07-16','0725DC14N','NA','B',22,'2','Transfer 1 of 1'),(200,5,2,'2025-07-16','0725DC14N','NA','B',3,'2','Transfer 1 of 1'),(201,6,2,'2025-07-16','0725DC14N','NA','B',14,'2','Transfer 1 of 1'),(202,6,2,'2025-07-16','0725DC15M','NA','B',41,'2','Transfer 1 of 1'),(203,3,1,'2025-07-16','0725DC13N','NA','A',3,'1','Transfer 1 of 1 in A'),(204,5,1,'2025-07-16','0725DC13N','NA','A',2,'1','Transfer 1 of 1 in A'),(205,3,1,'2025-07-16','0725DC14M','NA','A',11,'1','Transfer 1 of 1 in A'),(206,6,1,'2025-07-16','0725DC14M','NA','A',60,'1','Transfer 1 of 1 in A'),(207,9,1,'2025-07-04','0725DC04M','NA','A',25,'1','Special arrangement. Carded cotton sold from floor to HMA 2. No transfer to store Invoice came from Accounting'),(208,9,1,'2025-07-07','0725DC07M','NA','A',25,'1','Special arrangement. Carded cotton sold from floor to HMA 2. No transfer to store Invoice came from Accounting'),(209,1,1,'2025-07-17','0725DC15M','NA','A',7,'1',''),(210,6,1,'2025-07-17','0725DC15M','NA','A',5,'1',NULL),(211,1,1,'2025-07-17','0725DC16M','NA','A',29,'1',NULL),(212,5,1,'2025-07-17','0725DC16M','NA','A',6,'1',NULL),(213,2,1,'2025-07-17','0725DC17N','NA','A',29,'1',NULL),(214,5,1,'2025-07-17','0725DC17N','NA','A',4,'1',NULL),(215,1,2,'2025-07-17','0725DC15M','NA','B',7,'2',NULL),(216,1,2,'2025-07-17','0725DC16M','NA','B',35,'2',NULL),(217,1,2,'2025-07-17','0725DC17N','NA','B',9,'2',NULL),(218,1,2,'2025-07-17','0725DC16M','NA','B',11,'2',NULL),(219,5,2,'2025-07-17','0725DC16M','NA','B',9,'2',NULL),(220,6,2,'2025-07-17','0725DC16M','NA','B',45,'2',NULL),(221,6,2,'2025-07-17','0725DC15M','NA','B',17,'2',NULL),(222,2,1,'2025-07-18','0725DC17M','NA','A',44,'1',NULL),(223,4,1,'2025-07-18','0725DC17M','NA','A',6,'1',''),(224,5,1,'2025-07-18','0725DC17M','NA','A',8,'1',NULL),(225,6,1,'2025-07-18','0725DC17M','NA','A',2,'1',NULL),(226,2,1,'2025-07-18','0725DC17A','NA','A',22,'1',NULL),(227,5,1,'2025-07-18','0725DC17A','NA','A',2,'1',NULL),(228,1,2,'2025-07-18','0725DC17M','NA','B',29,'2',NULL),(229,2,2,'2025-07-18','0725DC17A','NA','B',42,'2',NULL),(230,4,2,'2025-07-18','0725DC16M','NA','B',6,'2',NULL),(231,6,2,'2025-07-18','0725DC15M','NA','B',20,'2',NULL),(232,5,2,'2025-07-18','0725DC15M','NA','B',10,'2',NULL),(233,1,1,'2025-07-19','0725DC17A','NA','A',22,'1','T1 of 2'),(234,1,1,'2025-07-19','0725DC18N','NA','A',4,'1','T1 of 2'),(235,4,1,'2025-07-19','0725DC17A','NA','A',7,'1','T1 of 2'),(236,4,1,'2025-07-19','0725DC18N','NA','A',2,'1','T1 of 2'),(237,5,1,'2025-07-19','0725DC18N','NA','A',22,'1','T1 of 2'),(238,2,2,'2025-07-19','0725DC18N','NA','B',16,'2','T1 of 2'),(239,5,2,'2025-07-19','0725DC17A','NA','B',22,'2','T1 of 2'),(240,5,2,'2025-07-19','0725DC18N','NA','B',56,'2','T1 of 2'),(241,4,2,'2025-07-19','0725DC18N','NA','B',19,'2','T1 of 2'),(242,5,1,'2025-07-19','0725DC18N','','A',8,'1','T2 of 2'),(243,5,2,'2025-07-19','0725DC18A','NA','B',8,'2','T2 of 2'),(244,1,1,'2025-07-21','0725DC18N','NA','A',23,'1','T1 of 1'),(245,3,1,'2025-07-21','0725DC18N','NA','A',6,'1','T1 of 1'),(246,1,1,'2025-07-21','0725DC18A','NA','A',7,'1','T1 of 1'),(247,3,1,'2025-07-21','0725DC18A','NA','A',3,'1','T1 of 1'),(248,1,1,'2025-07-21','0725DC19N','NA','A',10,'1','T1 of 1'),(249,2,1,'2025-07-21','0725DC19N','NA','A',15,'1','T1 of 1'),(250,3,1,'2025-07-21','0725DC19N','NA','A',4,'1','T1 of 1'),(251,2,1,'2025-07-21','0725DC19M','NA','A',10,'1','T1 of 1'),(252,3,1,'2025-07-21','0725DC19M','NA','A',2,'1','T1 of 1'),(253,4,1,'2025-07-21','0725DC19M','NA','A',5,'1','T1 of 1'),(254,1,2,'2025-07-21','0725DC18N','NA','B',23,'2','T1 of 1'),(255,1,2,'2025-07-21','0725DC18N','NA','B',21,'2','T1 of 1'),(256,2,2,'2025-07-21','0725DC18A','NA','B',12,'2','T1 of 1'),(257,3,2,'2025-07-21','0725DC18N','NA','B',32,'2','T1 of 1'),(258,3,2,'2025-07-21','0725DC18A','NA','B',10,'2','T1 of 1'),(259,3,2,'2025-07-21','0725DC19N','NA','B',10,'2','T1 of 1'),(260,3,2,'2025-07-21','0725DC19M','NA','B',18,'2','T1 of 1'),(261,3,2,'2025-07-21','0725DC19M','NA','B',3,'2','T1 of 1'),(262,4,2,'2025-07-21','0725DC19M','NA','B',14,'2','T1 of 1'),(263,1,1,'2025-07-22','0725DC19M','NA','A',20,'1',NULL),(264,4,1,'2025-07-22','0725DC19M','NA','A',4,'1',NULL),(265,1,1,'2025-07-22','0725DC21N','NA','A',28,'1',NULL),(266,4,1,'2025-07-22','0725DC21N','NA','A',1,'1',NULL),(267,5,1,'2025-07-22','0725DC21N','NA','A',9,'1',NULL),(268,2,1,'2025-07-22','0725DC21M','NA','A',37,'1',NULL),(269,3,1,'2025-07-22','0725DC21M','NA','A',1,'1',NULL),(270,5,1,'2025-07-22','0725DC21M','NA','A',3,'1',NULL),(271,1,2,'2025-07-22','0725DC19M','NA','B',16,'2',NULL),(272,1,2,'2025-07-22','0725DC19M','NA','B',22,'2',NULL),(273,1,2,'2025-07-22','0725DC21N','NA','B',5,'2',NULL),(274,2,2,'2025-07-22','0725DC21M','NA','B',5,'2',NULL),(275,3,2,'2025-07-22','0725DC19M','NA','B',20,'2',NULL),(276,4,2,'2025-07-22','0725DC19M','NA','B',11,'2',NULL),(277,5,2,'2025-07-22','0725DC19M','NA','B',3,'2',NULL),(278,4,2,'2025-07-22','0725DC21N','NA','B',11,'2',NULL),(279,4,2,'2025-07-22','0725DC21M','NA','B',36,'2',NULL),(280,3,2,'2025-07-22','0725DC21M','NA','B',4,'2',NULL),(281,1,1,'2025-07-23','0725DC21M','NA','A',15,'1',NULL),(282,2,1,'2025-07-23','0725DC21M','NA','A',2,'1',NULL),(283,1,1,'2025-07-23','0725DC22N','NA','A',32,'1',NULL),(284,5,1,'2025-07-23','0725DC22N','NA','A',7,'1',NULL),(285,1,1,'2025-07-23','0725DC22M','NA','A',6,'1',NULL),(286,2,1,'2025-07-23','0725DC22M','NA','A',36,'1',NULL),(287,5,1,'2025-07-23','0725DC22M','NA','A',6,'1',NULL),(288,1,2,'2025-07-23','0725DC21M','NA','B',8,'2',NULL),(289,1,2,'2025-07-23','0725DC22M','NA','B',43,'2',NULL),(290,3,2,'2025-07-23','0725DC21M','NA','B',35,'2',NULL),(291,3,2,'2025-07-23','0725DC22M','NA','B',9,'2',NULL),(292,5,2,'2025-07-23','0725DC22M','NA','B',25,'2',NULL),(293,4,2,'2025-07-23','0725DC22M','NA','B',4,'2',NULL),(294,1,1,'2025-07-24','0725DC22M','NA','A',2,'1',NULL),(295,4,1,'2025-07-24','0725DC22M','NA','A',2,'1',NULL),(296,1,1,'2025-07-24','0725DC23N','NA','A',33,'1',NULL),(297,4,1,'2025-07-24','0725DC23N','NA','A',6,'1',NULL),(298,1,1,'2025-07-24','0725DC23M','NA','A',15,'1',NULL),(299,2,1,'2025-07-24','0725DC23M','NA','A',36,'1',NULL),(300,3,1,'2025-07-24','0725DC23M','NA','A',7,'1',NULL),(301,4,1,'2025-07-24','0725DC23M','NA','A',3,'1',NULL),(302,1,2,'2025-07-24','0725DC22M','NA','B',15,'2',NULL),(303,1,2,'2025-07-24','0725DC23N','NA','B',44,'2',NULL),(304,5,2,'2025-07-24','0725DC22M','NA','B',38,'2',NULL),(305,4,2,'2025-07-24','0725DC22M','NA','B',8,'2',NULL),(306,1,2,'2025-07-24','0725DC23N','NA','B',14,'2',NULL),(310,1,1,'2025-07-25','0725DC24N','NA','A',19,'1',NULL),(311,3,1,'2025-07-25','0725DC24N','NA','A',6,'1',NULL),(312,2,1,'2025-07-25','0725DC24M','NA','A',29,'1','confirm if its 25 or 250. Record not clear on the requisition isn\'t clear'),(313,3,1,'2025-07-25','0725DC24M','NA','A',15,'1',NULL),(314,4,1,'2025-07-25','0725DC24M','NA','A',2,'1',NULL),(315,3,2,'2025-07-25','0725DC23N','NA','B',46,'2','Went with T1 of 2 in B'),(316,4,2,'2025-07-25','0725DC23M','NA','B',48,'2','Went with T1 of 2 in B'),(317,5,2,'2025-07-25','0725DC23M','NA','B',1,'2','Went with T1 of 2 in B'),(318,2,2,'2025-07-25','0725DC24N','NA','B',5,'2','T2 of 2 in B'),(319,2,2,'2025-07-25','0725DC24M','NA','B',41,'2','T2 of 2 in B'),(320,2,2,'2025-07-25','0725DC24M','NA','B',5,'2','T2 of 2 in B'),(321,3,2,'2025-07-25','0725DC24N','NA','B',25,'2','T2 of 2 in B'),(322,4,2,'2025-07-25','0725DC24M','NA','B',11,'2','T2 of 2 in B'),(323,1,1,'2025-07-26','0725DC24N','NA','A',3,'1',NULL),(324,3,1,'2025-07-26','0725DC24N','NA','A',1,'1',NULL),(325,1,1,'2025-07-26','0725DC25M','NA','A',20,'1',NULL),(326,3,1,'2025-07-26','0725DC25M','NA','A',14,'1',NULL),(327,1,2,'2025-07-26','0725DC24N','NA','B',10,'2','T1 of 2'),(328,1,2,'2025-07-26','0725DC25M','NA','B',35,'2','T1 of 2'),(329,1,2,'2025-07-26','0725DC25M','NA','B',15,'2','T1 of 2'),(330,3,2,'2025-07-26','0725DC24N','NA','B',11,'2','T1 of 2'),(331,4,2,'2025-07-26','0725DC24N','NA','B',1,'2','T1 of 2'),(332,1,2,'2025-07-26','0725DC24M','NA','B',1,'2','T1 of 2'),(333,3,2,'2025-07-26','0725DC24N','NA','B',50,'2','T2 of 2'),(334,3,1,'2025-07-28','0725DC26M','NA','A',14,'1','T1 of 2'),(335,4,1,'2025-07-28','0725DC26M','NA','A',30,'1','T1 of 2'),(336,3,2,'2025-07-28','0725DC25M','NA','B',120,'2','Done during night shift in pad'),(337,3,2,'2025-07-28','0725DC24N','NA','B',43,'2',NULL),(338,4,1,'2025-07-28','0725DC26M','NA','A',3,'1',NULL),(339,5,1,'2025-07-28','0725DC26M','NA','A',10,'1','Production delayed in line A; GM stopped every from closing'),(340,3,1,'2025-07-29','0725DC26M','NA','A',35,'1',NULL),(341,4,1,'2025-07-29','0725DC26M','NA','A',2,'1',NULL),(342,5,1,'2025-07-29','0725DC26M','NA','A',1,'1',NULL),(343,3,1,'2025-07-29','0725DC28M','NA','A',27,'1',NULL),(344,1,2,'2025-07-29','0725DC28M','NA','B',30,'2',NULL),(345,1,2,'2025-07-29','0725DC29N','NA','B',13,'2',NULL),(346,3,2,'2025-07-29','0725DC28M','NA','B',35,'2',NULL),(347,4,2,'2025-07-29','0725DC28M','NA','B',26,'2',NULL),(348,9,1,'2025-07-21','0725DC19N','NA','A',10,'1','Special arrangement'),(349,9,1,'2025-07-22','0725DC19M','NA','A',10,'1','Special arrangement'),(350,9,1,'2025-07-23','0725DC21M','NA','A',10,'1','Special arrangement'),(351,9,1,'2025-07-23','0725DC22N','NA','A',20,'1','Special arrangement'),(352,9,1,'2025-07-23','0725DC22M','NA','A',10,'1','Special arrangement'),(353,9,1,'2025-07-31','0725DC30M','NA','A',5,'1','Special arrangement'),(354,9,1,'2025-07-31','0725DC30A','NA','A',10,'1','Special arrangement'),(355,1,1,'2025-07-30','0725DC29N','NA','A',14,'1','Went with T1 of 1 in A'),(356,5,1,'2025-07-30','0725DC29N','NA','A',7,'1','Went with T1 of 1 in A'),(357,1,1,'2025-07-30','0725DC29M','NA','A',3,'1','Went with T1 of 1 in A'),(358,5,1,'2025-07-30','0725DC29M','NA','A',2,'1','Went with T1 of 1 in A'),(359,1,1,'2025-07-30','0725DC29A','NA','A',9,'1','Went with T1 of 1 in A'),(360,5,1,'2025-07-30','0725DC29A','NA','A',12,'1','Went with T1 of 1 in A'),(361,1,2,'2025-07-30','0725DC29N','NA','B',54,'2','T1 of 2 in B'),(362,1,2,'2025-07-30','0725DC29M','NA','B',10,'2','T2 of 2 in B'),(363,1,2,'2025-07-30','0725DC29A','NA','B',20,'2','T2 of 2 in B'),(364,1,2,'2025-07-30','0725DC29A','NA','B',11,'2','T2 of 2 in B'),(365,5,2,'2025-07-30','0725DC29N','NA','B',15,'2','T2 of 2 in B'),(366,5,2,'2025-07-30','0725DC29M','NA','B',10,'2','T2 of 2 in B'),(367,5,2,'2025-07-30','0725DC29A','NA','B',5,'2','T2 of 2 in B'),(368,5,2,'2025-07-30','0725DC29A','NA','B',1,'2','T2 of 2 in B'),(369,1,1,'2025-07-31','0725DC30M','NA','A',16,'1','T1 of 2'),(370,1,1,'2025-07-31','0725DC30A','NA','A',1,'1','T1 of 2'),(371,5,1,'2025-07-31','0725DC30M','NA','A',2,'1','T1 of 2'),(372,4,1,'2025-07-31','0725DC30M','NA','A',1,'1','T1 of 2'),(373,1,2,'2025-07-31','0725DC29A','NA','B',16,'2','T1 of 2 in B'),(374,1,2,'2025-07-31','0725DC30M','NA','B',10,'2','T1 of 2 in B'),(375,1,2,'2025-07-31','0725DC30M','NA','B',10,'2','T1 of 2 in B'),(376,3,2,'2025-07-31','0725DC29A','NA','B',61,'2','T1 of 2 in B'),(377,4,2,'2025-07-31','0725DC29A','NA','B',25,'2','T1 of 2 in B'),(378,5,2,'2025-07-31','0725DC30M','NA','B',37,'2','T1 of 2 in B'),(379,6,2,'2025-07-31','0725DC30M','NA','B',41,'2','T1 of 2 in B'),(380,1,1,'2025-07-31','0725DC30A','NA','A',5,'1','T2 of 2 in A'),(381,6,1,'2025-07-31','0725DC30A','NA','A',18,'1','T2 of 2 in A'),(382,1,2,'2025-07-31','0725DC30M','NA','B',2,'2','T2 of 2 in B'),(383,6,2,'2025-07-31','0725DC30M','NA','B',28,'2','T2 of 2 in B'),(384,6,2,'2025-07-31','0725DC30A','NA','B',17,'2','T2 of 2 in B'),(385,4,2,'2025-07-28','0725DC26M','NA','B',84,'2','Slip submitted late'),(386,4,2,'2025-07-09','0725DC07N','NA','B',2,'2','diff report and requisition slip'),(387,5,1,'2025-08-01','0725DC30A','NA','A',31,'1',NULL),(388,6,1,'2025-08-01','0725DC30A','NA','A',6,'1',NULL),(389,5,2,'2025-08-01','0725DC30A','NA','B',45,'2',NULL),(390,6,2,'2025-08-01','0725DC30A','NA','B',15,'2','production has 11 bales 90 pieces of 12.5 g WIP from July31. Produced by carding afternoon shift and others'),(391,3,1,'2025-08-02','0825DC01N','NA','A',62,'1',NULL),(392,3,1,'2025-08-02','0825DC01A','NA','A',1,'1',NULL),(393,5,1,'2025-08-02','0725DC30A','NA','A',2,'1',NULL),(394,5,1,'2025-08-02','0825DC01N','NA','A',2,'1',NULL),(395,3,2,'2025-08-02','0725DC30A','NA','B',8,'2',NULL),(396,5,2,'2025-08-02','0725DC30A','NA','B',3,'2',NULL),(397,3,2,'2025-08-02','0825DC01N','NA','B',79,'2',NULL),(398,3,2,'2025-08-02','0825DC01N','NA','B',11,'2',NULL),(399,3,2,'2025-08-02','0825DC01A','NA','B',20,'2',NULL),(400,1,1,'2025-08-04','0825DC01A','NA','A',14,'1',NULL),(401,3,1,'2025-08-04','0825DC01A','NA','A',5,'1',NULL),(402,4,1,'2025-08-04','0825DC01A','NA','A',6,'1',NULL),(403,1,1,'2025-08-04','0825DC02A','NA','A',29,'1',NULL),(404,4,1,'2025-08-04','0825DC02A','NA','A',4,'1',NULL),(405,1,1,'2025-08-04','0825DC04N','NA','A',2,'1',NULL),(406,1,2,'2025-08-04','0825DC01A','NA','B',23,'2',NULL),(407,1,2,'2025-08-04','0825DC02A','NA','B',30,'2',NULL),(408,3,2,'2025-08-04','0825DC01A','NA','B',18,'2',NULL),(409,4,2,'2025-08-04','0825DC01A','NA','B',7,'2',NULL),(410,4,2,'2025-08-04','0825DC02A','NA','B',10,'2',NULL),(411,4,2,'2025-08-04','0825DC04N','NA','B',3,'2',NULL),(412,1,1,'2025-08-05','0825DC04N','NA','A',25,'1',NULL),(413,3,1,'2025-08-05','0825DC04N','NA','A',2,'1',NULL),(414,4,1,'2025-08-05','0825DC04N','NA','A',7,'1',NULL),(415,1,1,'2025-08-05','0825DC04M','NA','A',17,'1',NULL),(416,3,1,'2025-08-05','0825DC04M','NA','A',6,'1',NULL),(417,1,1,'2025-08-05','0825DC05N','NA','A',22,'1',NULL),(418,3,1,'2025-08-05','0825DC05N','NA','A',7,'1',NULL),(419,1,2,'2025-08-05','0825DC02A','NA','B',10,'2',NULL),(420,1,2,'2025-08-05','0825DC04N','NA','B',9,'2',NULL),(421,1,2,'2025-08-05','0825DC04M','NA','B',24,'2',NULL),(422,1,2,'2025-08-05','0825DC05N','NA','B',28,'2',NULL),(423,4,2,'2025-08-05','0825DC04N','NA','B',20,'2',NULL),(424,3,2,'2025-08-05','0825DC04M','NA','B',7,'2',NULL),(425,3,2,'2025-08-05','0825DC05N','NA','B',8,'2',NULL),(426,3,2,'2025-08-05','0825DC05N','NA','B',1,'2',NULL),(427,1,1,'2025-08-06','0825DC05N','NA','A',13,'1','T1 of 2'),(428,3,1,'2025-08-06','0825DC05N','NA','A',6,'1','T1 of 2'),(429,1,1,'2025-08-06','0825DC05M','NA','A',30,'1','T1 of 2'),(430,3,1,'2025-08-06','0825DC05M','NA','A',7,'1','T1 of 2'),(431,1,1,'2025-08-06','0825DC05A','NA','A',4,'1','T1 of 2'),(432,3,1,'2025-08-06','0825DC05A','NA','A',3,'1','T1 of 2'),(433,2,1,'2025-08-06','0825DC05A','NA','A',21,'1','T1 of 2'),(434,5,1,'2025-08-06','0825DC05A','NA','A',5,'1','T1 of 2'),(435,1,2,'2025-08-06','0825DC05N','NA','B',11,'2','T1 of 2'),(436,1,2,'2025-08-06','0825DC05M','NA','B',26,'2','T1 of 2'),(437,2,2,'2025-08-06','0825DC05A','NA','B',18,'2','T1 of 2'),(438,3,2,'2025-08-06','0825DC05N','NA','B',2,'2','T1 of 2'),(439,5,2,'2025-08-06','0825DC05A','NA','B',1,'2','T1 of 2'),(440,5,2,'2025-08-06','0825DC05N','NA','B',5,'2','T1 of 2'),(441,5,2,'2025-08-06','0825DC05M','NA','B',10,'2','T1 of 2'),(442,5,2,'2025-08-06','0825DC05A','NA','B',5,'2','T1 of 2'),(443,5,1,'2025-08-06','0825DC05A','NA','A',3,'1','T2 of 2'),(444,5,2,'2025-08-06','0825DC05A','NA','B',7,'2','T2 of 2; both supervisors closed before the ad hocs'),(445,1,1,'2025-08-07','0825DC05A','NA','A',4,'1',NULL),(446,2,1,'2025-08-07','0825DC05A','NA','A',1,'1',NULL),(447,5,1,'2025-08-07','0825DC05A','NA','A',3,'1',NULL),(448,1,1,'2025-08-07','0825DC06N','NA','A',35,'1',NULL),(449,4,1,'2025-08-07','0825DC06N','NA','A',4,'1',NULL),(450,5,1,'2025-08-07','0825DC06N','NA','A',1,'1',NULL),(451,1,1,'2025-08-07','0825DC06A','NA','A',18,'1',NULL),(452,2,1,'2025-08-07','0825DC06A','NA','A',16,'1',NULL),(453,4,1,'2025-08-07','0825DC06A','NA','A',4,'1',NULL),(454,1,2,'2025-08-07','0825DC05A','NA','B',12,'2',NULL),(455,1,2,'2025-08-07','0825DC06N','NA','B',12,'2',NULL),(456,1,2,'2025-08-07','0825DC06N','NA','B',20,'2',NULL),(457,1,2,'2025-08-07','0825DC06A','NA','B',9,'2',NULL),(458,1,2,'2025-08-07','0825DC06A','NA','B',33,'2',NULL),(459,3,2,'2025-08-07','0825DC06N','NA','B',2,'2',NULL),(460,4,2,'2025-08-07','0825DC06A','NA','B',5,'2',NULL),(461,4,2,'2025-08-07','0825DC06N','NA','B',15,'2',NULL),(462,5,2,'2025-08-07','0825DC06A','NA','B',8,'2',NULL),(463,1,1,'2025-08-08','0825DC06A','NA','A',8,'1',NULL),(464,4,1,'2025-08-08','0825DC06A','NA','A',7,'1',NULL),(465,1,1,'2025-08-08','0825DC07N','NA','A',20,'1',NULL),(466,4,1,'2025-08-08','0825DC07N','NA','A',4,'1',NULL),(467,2,1,'2025-08-08','0825DC07M','NA','A',40,'1',NULL),(468,6,1,'2025-08-08','0825DC07M','NA','A',13,'1',NULL),(469,1,1,'2025-08-08','0825DC08N','NA','A',3,'1',NULL),(470,2,1,'2025-08-08','0825DC08N','NA','A',10,'1',NULL),(471,4,2,'2025-08-08','0825DC06A','NA','B',10,'2','T1 of 2'),(472,6,2,'2025-08-08','0825DC06A','NA','B',20,'2','T1 of 2'),(473,1,2,'2025-08-08','0825DC06A','NA','B',5,'2','T2 of 2'),(474,1,2,'2025-08-08','0825DC07N','NA','B',20,'2','T2 of 2'),(475,1,2,'2025-08-08','0825DC07N','NA','B',11,'2','T2 of 2'),(476,1,2,'2025-08-08','0825DC07M','NA','B',16,'2','T2 of 2'),(477,2,2,'2025-08-08','0825DC07M','NA','B',18,'2','T2 of 2'),(478,2,2,'2025-08-08','0825DC08N','NA','B',13,'2','T2 of 2'),(479,6,2,'2025-08-08','0825DC06A','NA','B',11,'2','T2 of 2');
/*!40000 ALTER TABLE `productions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(55) NOT NULL,
  `packaging_units` varchar(10) NOT NULL,
  `number_of_units_per_pack` int NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'500 g Dele Absorbent Cotton Wool BP','bales',20),(2,'250 g Dele Absorbent Cotton Wool BP','bales',30),(3,'100 g Dele Absorbent Cotton Wool BP','bales',50),(4,'50 g Dele Absorbent Cotton Wool BP','bales',100),(5,'25 g Dele Absorbent Cotton Wool BP','bales',100),(6,'12.5 g Dele Absorbent Cotton Wool BP','bales',120),(7,'Dele Cotton Wool Balls','cartons',20),(8,'Dele Pad','bales',24),(9,'Carded cotton','kg',0);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status` (
  `status_id` int NOT NULL AUTO_INCREMENT,
  `status_name` varchar(45) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES (1,'Supervisor'),(2,'Assistant Supervisor'),(3,'Permanent Staff'),(4,'Contract Staff'),(5,'Ad hoc Staff');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transfer_items`
--

DROP TABLE IF EXISTS `transfer_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transfer_items` (
  `transfer_id` int NOT NULL,
  `quantity_transferred` int NOT NULL,
  `product_id` int NOT NULL,
  PRIMARY KEY (`transfer_id`,`product_id`),
  KEY `fk_transfer_items_transfers1_idx` (`transfer_id`),
  KEY `fk_transfer_items_products1_idx` (`product_id`),
  CONSTRAINT `fk_transfer_items_products1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  CONSTRAINT `fk_transfer_items_transfers1` FOREIGN KEY (`transfer_id`) REFERENCES `transfers` (`transfer_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transfer_items`
--

LOCK TABLES `transfer_items` WRITE;
/*!40000 ALTER TABLE `transfer_items` DISABLE KEYS */;
INSERT INTO `transfer_items` VALUES (1,16,1),(1,42,2),(1,10,3),(1,13,4),(2,57,1),(2,11,2),(2,4,3),(2,16,4),(3,57,2),(3,12,4),(4,52,1),(4,1,3),(4,24,4),(5,51,1),(5,16,3),(5,3,4),(6,63,2),(6,2,3),(6,10,4),(8,14,2),(8,20,3),(9,22,2),(9,13,3),(9,6,6),(10,43,1),(10,19,3),(11,56,1),(11,2,3),(11,5,6),(12,6,1),(12,1,3),(13,6,3),(14,27,1),(14,28,2),(14,10,3),(14,12,4),(15,49,1),(15,6,3),(15,17,4),(16,19,1),(16,44,2),(16,9,4),(16,10,6),(17,70,1),(17,11,4),(18,14,6),(19,72,1),(19,2,4),(19,20,6),(20,28,1),(20,2,4),(20,11,5),(20,22,6),(21,2,1),(21,5,5),(22,15,1),(22,11,5),(23,1,1),(23,53,3),(24,5,1),(24,55,4),(25,10,5),(26,14,1),(26,14,4),(27,29,1),(27,23,4),(28,5,5),(28,2,6),(29,5,4),(29,4,5),(29,3,6),(30,77,1),(30,7,3),(30,3,5),(31,86,1),(31,4,5),(32,56,2),(32,13,5),(32,4,6),(33,71,1),(33,16,6),(34,28,1),(34,56,2),(34,13,3),(34,1,5),(35,35,1),(35,9,3),(36,55,1),(36,16,6),(37,26,1),(37,20,2),(37,28,3),(37,4,4),(37,5,5),(37,5,6),(38,23,1),(38,36,2),(38,6,3),(39,6,2),(39,8,3),(40,22,3),(40,3,5),(40,55,6),(41,14,3),(41,2,5),(41,60,6),(42,36,1),(42,29,2),(42,10,5),(42,5,6),(43,62,1),(43,9,5),(43,62,6),(44,66,2),(44,6,4),(44,10,5),(44,2,6),(45,29,1),(45,42,2),(45,6,4),(45,10,5),(45,20,6),(47,26,1),(47,9,4),(47,22,5),(48,16,2),(48,19,4),(48,78,5),(49,8,5),(50,8,5),(51,40,1),(51,25,2),(51,15,3),(51,5,4),(52,44,1),(52,12,2),(52,73,3),(52,14,4),(53,48,1),(53,37,2),(53,1,3),(53,5,4),(53,12,5),(54,43,1),(54,5,2),(54,24,3),(54,58,4),(54,3,5),(55,53,1),(55,38,2),(55,13,5),(56,51,1),(56,44,3),(56,4,4),(56,25,5),(57,50,1),(57,36,2),(57,7,3),(57,11,4),(58,73,1),(58,8,4),(58,38,5),(59,19,1),(59,29,2),(59,21,3),(59,2,4),(60,46,3),(60,48,4),(60,1,5),(61,51,2),(61,25,3),(61,11,4),(62,23,1),(62,15,3),(63,61,1),(63,11,3),(63,1,4),(64,50,3),(65,14,3),(65,30,4),(66,163,3),(67,3,4),(67,10,5),(68,62,3),(68,2,4),(68,1,5),(69,43,1),(69,35,3),(69,26,4),(70,26,1),(70,21,5),(71,54,1),(72,41,1),(72,31,5),(73,17,1),(73,1,4),(73,2,5),(74,36,1),(74,61,3),(74,25,4),(74,37,5),(74,41,6),(75,5,1),(75,18,6),(76,2,1),(76,45,6),(77,84,4),(78,31,5),(78,6,6),(79,45,5),(79,15,6),(80,63,3),(80,4,5),(81,118,3),(81,3,5),(82,45,1),(82,5,3),(82,10,4),(83,53,1),(83,18,3),(83,20,4),(84,64,1),(84,15,3),(84,7,4),(85,71,1),(85,16,3),(85,20,4),(86,47,1),(86,21,2),(86,16,3),(86,5,5),(87,37,1),(87,18,2),(87,2,3),(87,21,5),(88,3,5),(89,7,5),(90,57,1),(90,17,2),(90,8,4),(90,4,5),(91,86,1),(91,2,3),(91,20,4),(91,8,5),(92,31,1),(92,50,2),(92,11,4),(92,13,6),(93,10,4),(93,20,6),(94,52,1),(94,31,2),(94,11,6);
/*!40000 ALTER TABLE `transfer_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transfers`
--

DROP TABLE IF EXISTS `transfers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transfers` (
  `transfer_id` int NOT NULL AUTO_INCREMENT,
  `supervisor_employee_id` int NOT NULL,
  `date` date NOT NULL,
  `transfer_time` time NOT NULL,
  `production_line` char(1) NOT NULL,
  `notes` varchar(750) DEFAULT NULL,
  PRIMARY KEY (`transfer_id`),
  KEY `fk_transfers_employees1_idx` (`supervisor_employee_id`),
  CONSTRAINT `fk_transfers_employees1` FOREIGN KEY (`supervisor_employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transfers`
--

LOCK TABLES `transfers` WRITE;
/*!40000 ALTER TABLE `transfers` DISABLE KEYS */;
INSERT INTO `transfers` VALUES (1,1,'2025-07-01','16:30:00','A',NULL),(2,2,'2025-07-01','16:46:00','B',NULL),(3,1,'2025-07-02','16:30:00','A','Transferred same as production. i.e. all SKU package on that day was transferred'),(4,2,'2025-07-02','16:47:00','B','Transfer equals production'),(5,1,'2025-07-03','16:35:00','B','(Line: B)Tranfer equals production. Mr Oseni Supervised but production line. Reason, Mrs Abdulkabir lost a brother'),(6,1,'2025-07-03','16:46:00','A','Transfer equals production.'),(8,1,'2025-07-04','16:38:00','B','Transfer equals production (Line B.)'),(9,1,'2025-07-04','16:55:00','A','Transfer equals production (Line A)'),(10,1,'2025-07-05','15:05:00','A','Transfer 1 of 2 in production line A'),(11,2,'2025-07-05','15:25:00','B','Transfer 1 of 2 in production line B'),(12,1,'2025-07-05','15:55:00','A','Transfer 2 of 2 in production line A'),(13,2,'2025-07-05','16:35:00','B','Transfer 2 of 2 in production line B'),(14,1,'2025-07-07','16:45:00','A','Transfer equals production'),(15,2,'2025-07-07','16:49:00','B','Transfer equals production'),(16,1,'2025-07-08','16:45:00','A','Transfer equal production'),(17,2,'2025-07-08','16:33:00','B','Transfer 1 of 2 in B'),(18,2,'2025-07-08','17:01:00','B','Transfer 2 of 2 in B'),(19,1,'2025-07-09','15:23:00','A','Transfer 1 of 2 in A'),(20,2,'2025-07-09','15:39:00','B','Transfer 1 of 2 in B'),(21,1,'2025-07-09','16:55:00','A','Transfer 2 of 2 in A'),(22,2,'2025-07-09','16:45:00','B','Transfer 2 of 2 in B'),(23,1,'2025-07-10','14:25:00','A','Transfer 1 of 2 in A'),(24,2,'2025-07-10','14:45:00','B','Tranfer 1 of 3 in B'),(25,2,'2025-07-10','15:45:00','B','Transfer 2 of 3 in B'),(26,1,'2025-07-10','16:50:00','A','Transfer 2 of 2 in A'),(27,2,'2025-07-10','16:46:00','B','Transfer 3 of 3 in B'),(28,1,'2025-07-11','15:06:00','A','Transfer 1 of 2 in A'),(29,2,'2025-07-11','15:18:00','B','Transfer 1 of 2 in B'),(30,1,'2025-07-11','16:30:00','A','Transfer 2 of 2 in A'),(31,2,'2025-07-11','16:37:00','B','Transfer 2 of 2 in B'),(32,1,'2025-07-12','16:39:00','A','Transfer 1 of 1'),(33,2,'2025-07-12','16:55:00','B','Transfer 1 of 1'),(34,1,'2025-07-14','16:38:00','A','Transfer 1 of 1'),(35,2,'2025-07-14','14:31:00','B','Transfer 1 of 2 in line B'),(36,2,'2025-07-14','16:48:00','B','Transfer 2 of 2 in line B'),(37,2,'2025-07-15','15:10:00','B','Transfer 1 of 2 in B'),(38,1,'2025-07-15','16:42:00','A','Transfer 1 of 1 in A'),(39,2,'2025-07-15','16:51:00','B','Transfer 2 of 2 in B'),(40,2,'2025-07-16','16:49:00','B','Transfer 1 of 1'),(41,1,'2025-07-16','16:40:00','A','Transfer 1 of 1 in A'),(42,1,'2025-07-17','16:35:00','A','Transfer 1 of 1 '),(43,2,'2025-07-17','16:43:00','B','Transfer 1 of 1'),(44,1,'2025-07-18','16:38:00','A','Transfer 1 of 1 A'),(45,2,'2025-07-18','16:28:00','B','Transfer 1 of 1 B'),(47,1,'2025-07-19','15:57:00','A','Transfer 1 of 2 in A'),(48,2,'2025-07-19','16:05:00','B','Transfer 1 of 2 in B'),(49,1,'2025-07-19','16:48:00','A','Transfer 2 of 2 in A'),(50,2,'2025-07-19','16:40:00','B','Transfer 2 of 2 in B'),(51,1,'2025-07-21','16:46:00','A',NULL),(52,2,'2025-07-21','16:33:00','B',NULL),(53,1,'2025-07-22','16:39:00','A',''),(54,2,'2025-07-22','16:25:00','B',NULL),(55,1,'2025-07-23','16:47:00','A',''),(56,2,'2025-07-23','16:33:00','B',NULL),(57,1,'2025-07-24','16:47:00','A',NULL),(58,2,'2025-07-24','16:30:00','B',NULL),(59,1,'2025-07-25','16:30:00','A',NULL),(60,2,'2025-07-25','14:30:00','B','T1 of 2'),(61,2,'2025-07-25','16:50:00','B','T2 of 2'),(62,1,'2025-07-26','16:30:00','A',NULL),(63,2,'2025-07-26','14:20:00','B','T1 of 2'),(64,2,'2025-07-26','16:55:00','B','T2 of 2'),(65,1,'2025-07-28','16:55:00','A','T1 of 2'),(66,2,'2025-07-28','16:35:00','B','T1'),(67,1,'2025-07-28','17:45:00','A','T2 of 2'),(68,1,'2025-07-29','16:25:00','A',NULL),(69,2,'2025-07-29','16:31:00','B',NULL),(70,1,'2025-07-30','16:55:00','A','T1 of 1'),(71,2,'2025-07-30','14:05:00','B','T1 of 2 in B'),(72,2,'2025-07-30','16:45:00','B','T2 of 2 in B'),(73,1,'2025-07-31','13:19:00','A','T1 of 2'),(74,2,'2025-07-31','11:46:00','B','T1 of 2'),(75,1,'2025-07-31','16:55:00','A','T2 of 2'),(76,2,'2025-07-31','16:45:00','B','T2 of 2'),(77,2,'2025-07-28','00:00:00','B','*Anomaly:slip not submitted on time; time of transferred not picked'),(78,1,'2025-08-01','16:39:00','A',NULL),(79,2,'2025-08-01','16:45:00','B',NULL),(80,1,'2025-08-02','16:29:00','A',NULL),(81,2,'2025-08-02','16:40:00','B','Abdulkabir got suspended after this transfer'),(82,1,'2025-08-04','13:30:00','A','Cotton rollers, cutters and packagers started morning shift on this day (6 am to 2 pm)'),(83,2,'2025-08-04','13:45:00','B','Cotton rollers, cutters and packagers started morning shift on this day (6 am to 2 pm)'),(84,1,'2025-08-05','13:31:00','A',NULL),(85,2,'2025-08-05','13:25:00','B',NULL),(86,1,'2025-08-06','13:45:00','A','Transfer 1 of 2; Ad hoc and some other staff says they can\'t do morning shift'),(87,2,'2025-08-06','13:35:00','B','Transfer 1 of 2; Ad hoc and some other staff says they can\'t do morning shift'),(88,1,'2025-08-06','16:55:00','A','T2 of 2 initiated by Mrs Elizabeth'),(89,2,'2025-08-06','16:55:00','B','T2 of 2 Initiated by Mrs Elizabeth'),(90,1,'2025-08-07','15:15:00','A',NULL),(91,2,'2025-08-07','15:00:00','B',NULL),(92,1,'2025-08-08','13:55:00','A',NULL),(93,2,'2025-08-08','11:45:00','B','T1 of 2'),(94,2,'2025-08-08','13:46:00','B','T2 of 2');
/*!40000 ALTER TABLE `transfers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-10 18:08:04
