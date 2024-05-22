-- MySQL dump 10.13  Distrib 8.0.35, for Linux (x86_64)
--
-- Host: localhost    Database: user_information_db
-- ------------------------------------------------------
-- Server version	8.0.35-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bot_information_tab`
--

DROP TABLE IF EXISTS `bot_information_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bot_information_tab` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `botname` varchar(100) DEFAULT NULL,
  `botid` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `botid` (`botid`),
  UNIQUE KEY `botname` (`botname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bot_information_tab`
--

LOCK TABLES `bot_information_tab` WRITE;
/*!40000 ALTER TABLE `bot_information_tab` DISABLE KEYS */;
INSERT INTO `bot_information_tab` (botname, botid) VALUES ('1223','1715255618870321152'),('912','1715255310513479680'),('wei','1715259716252344320');
/*!40000 ALTER TABLE `bot_information_tab` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `developer_bot_mapping_tab`
--

DROP TABLE IF EXISTS `developer_bot_mapping_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `developer_bot_mapping_tab` (
  `id` int NOT NULL AUTO_INCREMENT,
  `developer_id` int DEFAULT NULL,
  `app_id` int DEFAULT NULL,
  `extra` varchar(255) DEFAULT NULL,
  `botname` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `developer_bot_mapping_tab`
--

LOCK TABLES `developer_bot_mapping_tab` WRITE;
/*!40000 ALTER TABLE `developer_bot_mapping_tab` DISABLE KEYS */;
INSERT INTO `developer_bot_mapping_tab` VALUES (1,1,1001,'extra information','wiwei');
/*!40000 ALTER TABLE `developer_bot_mapping_tab` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `whatsapp_user_information_tab`
--

DROP TABLE IF EXISTS `whatsapp_user_information_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `whatsapp_user_information_tab` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(100) DEFAULT NULL,
  `whatsapp_number` varchar(20) DEFAULT NULL,
  `appid` varchar(100) NOT NULL,
  `botname` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id__app_id_index` (`user_id`,`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `whatsapp_user_information_tab`
--

LOCK TABLES `whatsapp_user_information_tab` WRITE;
/*!40000 ALTER TABLE `whatsapp_user_information_tab` DISABLE KEYS */;
INSERT INTO `whatsapp_user_information_tab` (user_id, whatsapp_number, app_id, botname`) VALUES ('63cf09a4-5b99-4ff6-97bc-4f0bca9f28cf','+6587209601','35077a7b-c507-44a6-9021-d903f28705a1','chat');
/*!40000 ALTER TABLE `whatsapp_user_information_tab` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-11 15:15:35
