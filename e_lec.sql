-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: e_lec
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('75ffae90c4ff');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `articles` (
  `article_id` int NOT NULL AUTO_INCREMENT,
  `author_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `date_posted` datetime NOT NULL,
  PRIMARY KEY (`article_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `articles_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
INSERT INTO `articles` VALUES (13,6,'Geography','sedimentary rocks\ndynamite\nlimestone','2023-08-25 17:04:58'),(24,16,'Vincent Van Gogh','\nVincent Van GoghΓÇÿs paintings are adored around the world. His unique post-impressionist technique, with swathing brushstrokes and striking colors, is instantly recognizable.\n\nWhile alive, the artistΓÇÖs work was not so well received and he sold very few of his paintings. He became posthumously celebrated and now he is one of the most famous painters ever to have lived, with his original artworks selling for millions. Some of Van GoghΓÇÖs most expensive paintings include the Portrait de lΓÇÖartiste sans barbe (1889) which sold for $71.5 million in 1998 and Portrait du Docteur Gachet (1890) which sold for $82.5 million in 1990. While many original Van Gogh paintings are scattered around the worldΓÇÖs greatest museums and private collections, many of them now sit in the Van Gogh Museum in Amsterdam.\n\nVincent Van GoghΓÇÿs paintings are adored around the world. His unique post-impressionist technique, with swathing brushstrokes and striking colors, is instantly recognizable.\n\nWhile alive, the artistΓÇÖs work was not so well received and he sold very few of his paintings. He became posthumously celebrated and now he is one of the most famous painters ever to have lived, with his original artworks selling for millions. Some of Van GoghΓÇÖs most expensive paintings include the Portrait de lΓÇÖartiste sans barbe (1889) which sold for $71.5 million in 1998 and Portrait du Docteur Gachet (1890) which sold for $82.5 million in 1990. While many original Van Gogh paintings are scattered around the worldΓÇÖs greatest museums and private collections, many of them now sit in the Van Gogh Museum in Amsterdam.\n\nThe Most Famous Paintings by Vincent Van Gogh\n\nAn incredibly prolific artist ΓÇô although much of his work was created in the last 10 years of his life ΓÇô Van Gogh produced around 2000 artworks during his lifetime, and each carries with it a special part of the artistΓÇÖs legacy. Here is a selection of his most famous paintings.','2023-09-11 06:40:09'),(25,16,'Appropriation! When Art (very closely) Inspires Other Art','\nAppropriation Art\nWith the bold intention of repurposing existing and often iconic artistic imagery, those who create appropriation art borrow or copy in order to reframe it and make it their own. Whether it be a commercial artefact like a soup can, or a universally recognisable piece of fine art; appropriation art has been around for centuries, though the mid-20th century rise of consumerism led to a newfound significance and prevalence. Join us in exploring some of the most iconic works of appropriation art in contemporary art history.\n\nMarcel Duchamp, L.H.O.O.Q., 1919 \nMarcel Duchamp, L.H.O.O.Q.,, 1919\nFirst conceived in 1919 as one of his infamous readymades, DuchampsΓÇÖ term for his artistic process that took everyday objects and reformulated them to be seen in a new perspective, L.H.O.O.Q. is a postcard reproduction of Leonardo da VinciΓÇÖs ubiquitous Mona Lisa which has been doodled upon to include a moustache and beard in pencil. Recreated multiple times throughout his career, in various formats; the worksΓÇÖ title L.H.O.O.Q., is in itself a joke, when the letters pronounced in French sound out  ΓÇ£Elle a chaud au culΓÇ£, the equivalent of crudely saying ΓÇ£she is horny.ΓÇ¥ By reformatting the Mona Lisa on the cheap postcard to have masculinised features, Duchamp is able to poke fun and question preconceived notions of both gender and high art. ','2023-09-11 06:41:35'),(26,9,'SAMORI TOUR├ë (1830-1900)','Warrior king, empire builder and hero of the resistance against the French colonization of West Africa during the 19th century, Samori Tour├⌐ was born around 1830 in the Milo River Valley in present-day Guinea. His father was a trader, leading Tour├⌐ to follow his familyΓÇÖs occupation early on. In the 1850s, he enrolled in the military forces at Madina (present-day Mali) to liberate his mother, who was a member of the Malink├⌐ ethnic group, captured during a raid. He subsequently acquired military skills during various campaigns he undertook for local chiefs before starting his own career.\n\nTour├⌐ became a well-known leader, training and commanding a growing and disciplined army. He expanded his conquests, building a united empire called Mandinka. By 1874, he declared himself Faama (monarch), and established the capital of his kingdom at Bisandugu in present-day Gambia. In the 1880s, the empire expanded from Bamako, Mali, in the north, to the frontiers of British Sierra Leone, the Ivory Coast, and Liberia in the east and south. The Sudan was the eastward frontier. Tour├⌐ΓÇÖs empire reached its apogee between 1883 and 1887, a period in which he took the title of Almami, meaning the religious head of a Muslim empire.\n\nAfter the 1884 Berlin Conference which partitioned Africa, French forces began encroaching on Mandinka.  Although his army initially defeated the French, between 1885 and 1889 their military forces, which often included Senegalese troops, succeeded in pushing him further into the West African interior.   After several confrontations, Tour├⌐ in 1889 concluded various peace treaties with the French forces.\n\nIn December 1891, increasing French incursions into Tour├⌐ΓÇÖs empire led to the exodus of the entire nation eastward.  Between 1893 and 1898, Tour├⌐ΓÇÖs army conquered vast territories in present day Northern Ivory Coast.  Tour├⌐ formed a second empire and established its new capital in the city of Kong, Upper Ivory Coast.\n\nOn May 1, 1898, when the French seized the town of Sikasso, just north of the new empire, Tour├⌐ and his army took up positions in the Liberian forests to resist a second invasion.  This time, however, famine and desertion weakened his forces and the French seized Tour├⌐ on September 29, 1898, in his camp at Gu├⌐l├⌐mou in present-day Ivory Coast.  Tour├⌐ was exiled to Ndjol├⌐, Gabon, where he died of pneumonia on June 2, 1900.','2023-09-11 06:44:30'),(27,9,'Theology and the Four Princes','\'The four principles of bioethics\' have their rational basis and truth only within the wider set of moral principles. Outside that context, they demarcate a rather legalistic ethic while also, paradoxically, providing labels for rationalising almost any practice.\n\nMorality\'s principles (including \'the four\') can be recognised by anyone following reason\'s guidance, undeflected by distracting emotion, prejudice or convention. They are matter for moral philosophy. But reason\'s full implications, and morality\'s practical applications, are well understood only when full account is taken of the human situation. And our human predicament and opportunities include some realities adequately and reliably revealed only by the life and teachings of Jesus Christ, through the Church\'s scriptures and tradition. All moral principles are thus matters also for doctrine, faith, and theology. They are guides to a life which befits human nature, responds to the divine calling, and prepares people for eternal life in God\'s family. They educate conscience, shape virtues, and make possible wise decisions in particular cases.\n\nWhat is it reasonable to do? What choices \'make sense\', are \'good\', \'fair\', \'right\'? Moral philosophy begins its answer with two basic features of human persons. We are responsible, i.e. can deliberate rationally and make free choices [1], [2], [3]; and nothing short of a happiness and flourishing in which we might share can give our choices rationally sufficient point [4].\n\n. When tempted, e.g. to fabricate or steal some experimental results, we see through excuses like \'only following orders\' or \'my upbringing\' or \'I\'m slave to my passions\'. In judging oneself or others culpable, or in thinking \'if only I\'d...\', one recognizes one\'s freedom to choose and to choose rationally. Inherited characteristics, upbringing, present restrictions and pressures, all can influence but none need eliminate the demand to choose, to adopt one proposal for action (or inaction) in preference to others. (self-rule) is less a ]','2023-09-11 06:45:55'),(28,9,'Geography','Geography (from Greek: ╬│╬╡╧ë╬│╧ü╬▒╧å╬»╬▒,┬á','2023-09-14 08:59:04');
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question` (
  `question_id` int NOT NULL AUTO_INCREMENT,
  `subject` varchar(50) NOT NULL,
  `question` text NOT NULL,
  `date_posted` datetime NOT NULL,
  `author_id` int NOT NULL,
  PRIMARY KEY (`question_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (39,'Arts','what is the genesis of art','2023-08-28 07:21:23',9),(43,'Arts','Who is considered one of the most influential artists of the Renaissance period?','2023-08-28 07:37:56',9),(44,'Arts','What are some major art movements of the 20th century?','2023-08-28 07:37:56',9),(45,'Arts','How has digital technology transformed the art world?','2023-08-28 07:37:56',9),(46,'Biology','What is the role of DNA in genetics?','2023-08-28 07:37:56',9),(47,'Biology','How do cells reproduce through mitosis and meiosis?','2023-08-28 07:37:56',9),(49,'Chemistry','What are the different types of chemical reactions?','2023-08-28 07:37:56',9),(50,'Chemistry','How does the periodic table organize elements?','2023-08-28 07:37:56',9),(51,'Chemistry','Can you explain the concept of chemical bonding?','2023-08-28 07:37:56',9),(52,'Computer Science','What is the difference between a programming language and a scripting language?','2023-08-28 07:37:56',9),(53,'Computer Science','How do algorithms and data structures impact software development?','2023-08-28 07:37:56',9),(54,'Computer Science','What are some common design patterns used in software engineering?','2023-08-28 07:37:56',9),(55,'Engineering','wjdkmwlkdwkqd','2023-08-28 07:37:57',9),(56,'Engineering','How does the engineering design process work?','2023-08-28 07:37:57',9),(57,'Engineering','Can you explain the importance of ethics in engineering?','2023-08-28 07:37:57',9),(58,'Food and Nutrition','What are the essential nutrients needed for a healthy diet?','2023-08-28 07:37:57',9),(59,'Food and Nutrition','How does food labeling help consumers make informed choices?','2023-08-28 07:37:57',9),(60,'Food and Nutrition','Can you explain the impact of different cooking methods on nutritional content?minno','2023-08-28 07:37:57',9),(61,'Medicine','What is the difference between a virus and a bacteria?','2023-08-28 07:37:57',9),(62,'Medicine','How do vaccines work to prevent infectious diseases?','2023-08-28 07:37:57',9),(63,'Medicine','Can you explain the concept of personalized medicine?','2023-08-28 07:37:57',9),(64,'Mathematics','What is the significance of the Fibonacci sequence in nature?','2023-08-28 07:37:57',9),(65,'Mathematics','How does calculus relate to the concept of rate of change?','2023-08-28 07:37:57',9),(66,'Mathematics','Can you explain the difference between probability and statistics?','2023-08-28 07:37:57',9),(67,'Other','What is the role of philosophy in understanding the nature of reality?','2023-08-28 07:37:57',9),(68,'Other','How does anthropology study human cultures and societies?','2023-08-28 07:37:57',9),(69,'Other','Can you explain the concept of cultural relativism?','2023-08-28 07:37:57',9),(72,'Other','am I?','2023-08-31 12:04:51',9),(76,'Mathematics','navier stokes equation?','2023-08-31 12:27:17',9),(77,'Engineering','what is fluid dynamics?','2023-08-31 18:17:18',16),(88,'Architecture','Who designed eiffel tower?','2023-09-02 16:38:25',16),(89,'Biology','whats a dichotomous key?','2023-09-04 07:12:29',9),(90,'Architecture','What are the key principles of sustainable architecture, and how can they be integrated into modern building design?','2023-09-11 06:03:05',9),(91,'Architecture','How has technology, such as Building Information Modeling (BIM), transformed the field of architecture?','2023-09-11 06:05:00',16),(92,'Arts',' What is the significance of the Mona Lisa in the world of art, and why is it considered one of the most iconic paintings in history?','2023-09-11 06:34:12',16);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reply`
--

DROP TABLE IF EXISTS `reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reply` (
  `reply_id` int NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `date_posted` datetime NOT NULL,
  `author_id` int NOT NULL,
  `question_id` int NOT NULL,
  PRIMARY KEY (`reply_id`),
  KEY `author_id` (`author_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `reply_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `reply_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `question` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reply`
--

LOCK TABLES `reply` WRITE;
/*!40000 ALTER TABLE `reply` DISABLE KEYS */;
INSERT INTO `reply` VALUES (15,'The question of chemical reactions has many practical applications.','2023-08-28 08:13:23',9,44),(16,'Let\'s explore how this question relates to everyday processes.','2023-08-28 08:13:23',9,44),(17,'I believe understanding this concept can open doors to innovation.','2023-08-28 08:13:23',9,44),(18,'This question touches on the fundamentals of programming.','2023-08-28 08:13:23',9,45),(19,'Let\'s dive into the nuances of this software engineering challenge.','2023-08-28 08:13:23',9,45),(20,'Understanding algorithms is key to solving this coding question.','2023-08-28 08:13:24',9,45),(21,'Engineering ethics is an important aspect of this question.','2023-08-28 08:13:24',9,46),(22,'This question prompts us to consider the societal impact of technology.','2023-08-28 08:13:24',9,46),(23,'Let\'s collaborate to analyze the ethical dimensions of this issue.','2023-08-28 08:13:24',9,46),(24,'Food and nutrition play a crucial role in this question\'s context.','2023-08-28 08:13:24',9,47),(25,'Let\'s discuss the health implications and cultural significance.','2023-08-28 08:13:24',9,47),(26,'I\'m eager to learn more about this intriguing food-related question.','2023-08-28 08:13:24',9,47),(30,'Mathematics underlies the essence of this question.','2023-08-28 08:13:24',9,49),(31,'miano','2023-08-28 08:13:24',9,49),(32,'This question demonstrates the beauty of mathematical thinking.','2023-08-28 08:13:24',9,49),(33,'This question invites philosophical discussions about reality.','2023-08-28 08:13:24',9,50),(34,'Let\'s engage in a thought-provoking dialogue about this topic.','2023-08-28 08:13:24',9,50),(35,'The exploration of this question can lead to profound insights.','2023-08-28 08:13:24',9,50),(36,'This question relates to a key concept in physics. Let\'s explore it!','2023-08-28 08:13:24',9,51),(37,'As a physics enthusiast, I\'m excited to discuss this topic.','2023-08-28 08:13:24',9,51),(38,'I believe this question has deep implications for our understanding of the universe.','2023-08-28 08:13:24',9,51),(42,'This question raises intriguing ethical considerations.','2023-08-28 08:13:24',9,53),(43,'Let\'s examine how society\'s values influence our perspectives.','2023-08-28 08:13:25',9,53),(44,'Understanding the moral dimensions can guide us in answering this question.','2023-08-28 08:13:25',9,53),(45,'Understanding the concept of randomness is key to this question.','2023-08-28 08:13:25',9,54),(46,'Let\'s explore how probability theory can help us analyze this topic.','2023-08-28 08:13:25',9,54),(47,'The exploration of uncertainty leads to fascinating insights.','2023-08-28 08:13:25',9,54),(48,'The question of reality in philosophy is both timeless and contemporary.','2023-08-28 08:13:25',9,55),(49,'As a philosophy enthusiast, I\'m eager to engage in this dialogue.','2023-08-28 08:13:25',9,55),(50,'This question challenges us to consider the nature of existence.','2023-08-28 08:13:25',9,55),(51,'I find this question particularly relevant in the context of social issues.','2023-08-28 08:13:25',9,56),(52,'Let\'s discuss the implications of this question for modern society.','2023-08-28 08:13:25',9,56),(54,'This question resonates with the field of sociology.','2023-08-28 08:13:25',9,57),(55,'Let\'s analyze how different factors influence the outcomes.','2023-08-28 08:13:25',9,57),(56,'I\'m eager to learn from diverse viewpoints on this topic.','2023-08-28 08:13:25',9,57),(57,'This question involves the study of the human mind and behavior.','2023-08-28 08:13:25',9,58),(58,'Let\'s explore psychological research to answer this question.','2023-08-28 08:13:25',9,58),(59,'Understanding cognition is key to unraveling this mystery.','2023-08-28 08:13:25',9,58),(60,'The concept of time has fascinated philosophers and physicists alike.','2023-08-28 08:13:25',9,59),(61,'Let\'s engage in a philosophical discussion about time\'s nature.','2023-08-28 08:13:25',9,59),(62,'This question prompts us to question our intuitive understanding.','2023-08-28 08:13:25',9,59),(63,'This question touches on the intricacies of economics and policy.','2023-08-28 08:13:25',9,60),(64,'Let\'s discuss how economic theories can inform our answers.','2023-08-28 08:13:25',9,60),(65,'Understanding economic dynamics is crucial for addressing this issue.','2023-08-28 08:13:25',9,60),(83,'such as','2023-08-29 16:01:06',9,46),(85,'such as','2023-08-29 16:01:47',9,61),(86,'such as','2023-08-29 16:01:53',9,61),(102,'chemi what','2023-08-30 12:27:56',9,49),(114,'aki what','2023-08-30 13:23:10',9,46),(116,'such as','2023-08-30 13:24:46',9,55),(117,'yes','2023-08-30 13:24:59',9,55),(121,'ahii','2023-08-30 13:59:00',9,59),(122,'yes sree','2023-09-01 06:17:52',9,46),(141,'Barrack','2023-09-04 07:11:38',9,88),(144,'This question touches on the fundamentals of programming.','2023-09-04 08:01:21',9,52),(145,'Let\'s dive into the nuances of this software engineering challenge','2023-09-04 08:01:27',9,52),(146,'Understanding algorithms is key to solving this coding question','2023-09-04 08:01:37',9,52),(147,'passive design, the use of renewable materials, efficient water management, and reducing waste. Architects can integrate these principles by incorporating features like solar panels, green roofs, and natural ventilation systems into their designs, while also selecting eco-friendly materials and optimizing the building\'s orientation for energy efficiency','2023-09-11 06:03:53',16,90),(149,'BIM allows architects to create 3D digital models of buildings that incorporate all relevant data, from structural components to HVAC systems','2023-09-11 06:31:15',16,91),(150,'Leonardo da Vinci','2023-09-11 06:34:58',16,43),(151,'Energy Efficiency','2023-09-11 06:35:54',16,90),(152,'BIM provides a centralized platform where architects, engineers, contractors, and other stakeholders can collaborate in real-time.','2023-09-11 06:47:23',9,91);
/*!40000 ALTER TABLE `reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `passwd` varchar(255) NOT NULL,
  `deletion_requested` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'kate','katem@gmail.com','$2b$12$MUfG.cjF627f7zSojHuSXO1lpiKYAnLS9DcM7492WC6AeJ5qpVsYS',NULL),(6,'dan','dan@gmail.com','$2b$12$lQQrrOJAZOaiI4UeVl7psei4m3NQBPbECB1YiS0fpIpdAIoKZXBUC',NULL),(9,'patooo','patomiano6@gmail.com','$2b$12$uVFhE1kzTRtaJSdb9vDEROPGTBmYAgAg9blwoa5qg/jBGBpI7.YsC',NULL),(16,'njeri','njeri@gmail.com','$2b$12$HSHvn4j.ngLodavYdC820uv1t5uqzlV/NfnCXM5E2kLqN5PeAwh1W',NULL),(18,'melit','melit@gmail.com','$2b$12$lSW8.OT9EJHuHu/YaTvDfulOYkrhUUoVlM6lOZBqtKZlwyBAq0mVa',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-22 21:30:14
