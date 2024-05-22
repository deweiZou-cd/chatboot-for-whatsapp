drop table IF EXISTS `whatsapp_user_information_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
create TABLE `whatsapp_user_information_tab` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(100) DEFAULT NULL,
  `whatsapp_number` varchar(20) DEFAULT NULL,
  `app_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id__app_id_index` (`user_id`,`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `whatsapp_user_information_tab`
--

LOCK TABLES `whatsapp_user_information_tab` WRITE;
/*!40000 ALTER TABLE `whatsapp_user_information_tab` DISABLE KEYS */;
insert into `whatsapp_user_information_tab` (user_id, whatsapp_number, app_id) VALUES ('c9a65e38-8d86-426a-8773-5d863cb696c3','+17605374600','033b0553-17a7-4ea1-8f9b-cb0d82da717b');
/*!40000 ALTER TABLE `whatsapp_user_information_tab` ENABLE KEYS */;
UNLOCK TABLES;