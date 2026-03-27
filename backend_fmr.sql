-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Mar 27, 2026 at 05:14 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `backend_fmr`
--

-- --------------------------------------------------------

--
-- Table structure for table `cases`
--

CREATE TABLE `cases` (
  `id` varchar(50) NOT NULL,
  `patientName` varchar(100) NOT NULL,
  `patientId` varchar(50) NOT NULL,
  `patientImageUrl` text DEFAULT NULL,
  `chiefComplaint` text NOT NULL,
  `complaintType` varchar(50) NOT NULL,
  `additionalDetails` text DEFAULT NULL,
  `medicalHistory` text DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  `createdDate` datetime DEFAULT NULL,
  `lastUpdated` datetime DEFAULT NULL,
  `doctorId` varchar(50) NOT NULL,
  `doctorName` varchar(100) NOT NULL,
  `clinicalFeatures` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`clinicalFeatures`)),
  `lastAIResult` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`lastAIResult`)),
  `patientAge` varchar(20) DEFAULT NULL,
  `patientGender` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cases`
--

INSERT INTO `cases` (`id`, `patientName`, `patientId`, `patientImageUrl`, `chiefComplaint`, `complaintType`, `additionalDetails`, `medicalHistory`, `status`, `createdDate`, `lastUpdated`, `doctorId`, `doctorName`, `clinicalFeatures`, `lastAIResult`, `patientAge`, `patientGender`) VALUES
('3144', 'MAHII', '2024907', 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&h=200&fit=crop', 'Chief Complaint: Difficulty Chewing', 'poor_esthetics', 'Pain teeeths', 'Age: 21, Gender: Female', 'Active', '2026-03-10 04:21:46', '2026-03-18 10:40:30', 'DR001', 'Dr. Tanu', 'null', 'null', NULL, NULL),
('4959', 'Chandu', '2024697', 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=200&h=200&fit=crop', 'Chief Complaint: Pain', 'poor_esthetics', 'Pain in lower teeth', 'Age: 21, Gender: Male', 'completed', '2026-03-19 07:05:20', '2026-03-19 07:06:25', '18', 'Prudhvii', '{}', '{}', NULL, NULL),
('8289', 'IIT', '2024416', 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=200&h=200&fit=crop', 'Chief Complaint: Pain', 'poor_esthetics', 'tuti oty', 'Age: 65, Gender: Male', 'active', '2026-03-27 04:06:47', '2026-03-27 04:06:47', '10', 'Prudhviiiii', '{}', '{}', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `doctor_profiles`
--

CREATE TABLE `doctor_profiles` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `fullName` varchar(100) NOT NULL,
  `selectedSpecialty` varchar(100) NOT NULL,
  `yearsOfExperience` varchar(50) DEFAULT NULL,
  `clinicName` varchar(200) DEFAULT NULL,
  `profileImageUrl` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor_profiles`
--

INSERT INTO `doctor_profiles` (`id`, `user_id`, `fullName`, `selectedSpecialty`, `yearsOfExperience`, `clinicName`, `profileImageUrl`) VALUES
(1, NULL, 'prudhvi reddy', 'Orthodontist', '1', 'saveeethaclinic', 'blob:http://localhost:5173/4417fbbb-a5cf-4c6f-a111-012d121383ba'),
(2, 5, 'Doctor Pruthvi', 'Dentist', '5', 'Smile', NULL),
(3, 11, 'Test User', 'Orthodontist', '10', 'Test Clinic', NULL),
(4, 12, 'Pruthvi', 'Prosthodontist', '12', 'Wwww', NULL),
(5, 13, 'Koti', 'Orthodontist', '1', 'Savetha', NULL),
(6, 14, 'Prudhvii', 'General Dentist', '2', 'Saveetha dental', NULL),
(7, 16, 'Prudhvi ', 'General Dentist', '1', 'Sabveetha ', NULL),
(8, 21, 'MAHII', 'General Dentist', '2', 'Saveetha dental', NULL),
(9, 22, 'Anna Reddy', 'General Dentist', '1', 'Saveetha dental', NULL),
(10, 23, 'Prudhviiiii', 'General Dentist', '1', 'Saveetha dental', NULL),
(11, 24, 'Prudhvi reddy', 'General Dentist', '1', 'Saveetha dental', NULL),
(12, 25, 'Annareddyy', 'General Dentist', '1', 'Saveetha dental', NULL),
(13, 26, 'Prudhvinath Annareddy', 'Select specialty', '', '', NULL),
(14, 27, 'Prudhvinatha Reddy Annareddy', 'Select specialty', '', '', NULL),
(15, 28, 'Valid Doc', 'Select specialty', '', '', NULL),
(16, 29, 'Prudhvii', 'Endodontist', '1', 'Saveetha', NULL),
(17, 30, 'Prudhvi', 'Orthodontist', '1', 'Saveetha ', NULL),
(18, 31, 'Prudhvii', 'Orthodontist', '1', 'Saveetha', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` varchar(50) NOT NULL,
  `title` varchar(200) NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `isNew` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `title`, `message`, `timestamp`, `isNew`) VALUES
('702B9A52-3139-469E-82AB-2FEC25E06DDF', 'New Case Added', 'Patient IIT has been successfully registered (ID: 2024416).', '2026-03-27 04:06:47', 1),
('EEDA5693-7689-46C2-9972-D178EBB5F709', 'Treatment Success', 'The treatment for Chandu has been successfully finalized and marked as completed.', '2026-03-19 07:06:25', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `password_hash` varchar(128) NOT NULL,
  `role` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `mobile`, `password_hash`, `role`, `created_at`) VALUES
(5, 'Doctor Pruthvi', 'Prumah@gmail.com', '44', '$2b$12$kIpVwJZVjRKnhbytrofjrupGoeMw1s1wlwjPZvgrC0dY8iwJqmEW2', 'Doctor', '2026-02-27 08:05:59'),
(6, 'Ch', 'Ch@gmail.com', '345', '$2b$12$AtIaXdwPFaa434xEqXf3.enXbIRlgzMahpKjaQsVJMd8gIaetJJie', 'Doctor', '2026-02-27 08:21:34'),
(7, 'Koti', 'Kot@gmail.com', '1234', '$2b$12$o3ptNlmN2BHfcLjcqCsdkeD25v5E283f2Km1fpQLDTrZCNz5L2kAC', 'Doctor', '2026-03-04 07:37:46'),
(8, 'Sf', 'Sdf@ds', '3424', '$2b$12$oEwyYFJpprlvhRCA1a8AeegZtCIF.lKmuHUMXNTe/e7dA9.l7vc4C', 'Doctor', '2026-03-04 08:18:07'),
(9, 'ghaghara', 'As@g', '232', '$2b$12$f9Exc7R6nCWlzu5B8q2pLevcnc2paxPYvP9VUSZroKXo8VD70q2Gi', 'Doctor', '2026-03-04 08:23:05'),
(10, 'dfdfdf', 'As@as', '2332', '$2b$12$W6ysx2nXJHlgVqGD8g7WOOeqvbsoNiYLMqTNk6f7i3KI3ZeQnHEBq', 'Doctor', '2026-03-04 08:28:39'),
(11, 'Test User', 'test1@gmail.com', '1234567890', '$2b$12$mfqQHfkicqds5hvU1pmcFupv1d8Lci8ZGL8eoO9s.X3a4P0fJ0Bsy', 'Doctor', '2026-03-04 08:36:37'),
(12, 'Pruthvi', 'Annareddy@gmail.com', '321', '$2b$12$y8uj9OqITuP7dO9cyK9qUOLerOMxLf9LmP33mXlf6R2OkZbp4x9qC', 'Doctor', '2026-03-04 09:21:54'),
(13, 'Koti', 'Koti@gmail.com', '2341', '$2b$12$L8AvKvXtb3F0SnquGtybXeIQmJ0CTNcKcGORHJM6B0lqzTzDk4FOu', 'Doctor', '2026-03-07 03:24:05'),
(14, 'Prudhvii', 'Reddy@gmail.com', '1234', '$2b$12$FctRfzHdN532xbqFCzSqz.J0UOM6/a.l1SHwatjPn0sgtpc0dRJOm', 'Doctor', '2026-03-10 03:50:19'),
(16, 'Prudhvi ', 'Reddy1@gmail.com', '1234', '$2b$12$oyWzWd.lBOYuJD7arDrmmuG/9pc7mV8BUZaMPzDZouf9f6Br1QP3C', 'Doctor', '2026-03-10 07:56:29'),
(21, 'MAHII', 'Prudhvi15@gmail.com', '1234', '$2b$12$OpU6rrfRorHagzoHrf5qGO54K1Ydr3LNcglXyQ6AtJQgkplb2T.Fa', 'Doctor', '2026-03-10 08:10:16'),
(22, 'Anna Reddy', 'Pru@gmail.com', '1234', '$2b$12$JvcYmxfz5NQC/T666JV4huWh9yo9zuks/UnA69sQZ/pGdou8utzHe', 'Doctor', '2026-03-10 08:15:26'),
(23, 'Prudhviiiii', 'Prumah15@gmail.com', '15', '$2b$12$Iq/RNgzLV.YmzylEreX6LOQiLcXwvoNErxsawmykxQZpyWKZA/oYq', 'Doctor', '2026-03-11 04:01:18'),
(24, 'Prudhvi reddy', 'Reddy04@gmail.com', '9347437299', '$2b$12$MZQ9I9d1iDaIYLq3wFQC7uqcRb9XmRffuGH5lawOqJh2XA1IPY2LC', 'Doctor', '2026-03-16 09:46:55'),
(25, 'Annareddyy', 'Prureddy@gmail.com', '9347437299', '$2b$12$ZWp25REL3WNr5wUnAcxrpORFnrZCJjbDkhfmO6q0wDWC4aSjOJ/a2', 'Doctor', '2026-03-16 10:05:58'),
(26, 'Prudhvinath Annareddy', 'prudhvireddyre@gmail.com', '+919347437299', '$2b$12$IdSL3XnKaA12.SD2SVqj7OggoCN/oXTGBLu0kLOlkrIPWj5tXhC4u', 'Doctor', '2026-03-18 04:07:13'),
(27, 'Prudhvinatha Reddy Annareddy', 'prudhvireddyre60@gmail.com', '0934743729', '$2b$12$X1m.YXNhEMUwuzwUVM3otug5SkSj0wggNU6l90zU04F4mNSya9S.i', 'Doctor', '2026-03-18 09:21:02'),
(28, 'Valid Doc', 'valid@fmr.com', '1234567890', '$2b$12$s6zn03X0fwfatbQls.spG.l2bYTm1zY2KzCH0LNoPPiWWlpRW1M32', 'Doctor', '2026-03-19 04:52:02'),
(29, 'Prudhvii', 'Anna@gmail.com', '9347437299', '$2b$12$Uu6YvCQEsFw7e6e13SN9OezkdLQL3W793h.Vc5FQSHiSFaliLAIea', 'Doctor', '2026-03-19 06:55:36'),
(30, 'Prudhvi', 'Annareddy15@gmail.com', '9347437299', '$2b$12$xc5WQ5O9ZACEbL0pYSmX5.tfoLm/GZg85ogvqUjmLaq5p2.83PWb.', 'Doctor', '2026-03-19 06:59:26'),
(31, 'Prudhvii', 'Prureddyy@gmail.com', '9347437299', '$2b$12$nw3sTIqV60kBxZMI1FjwkO577J.PD6ONGICMsplW/HznCy6qxk.Gq', 'Doctor', '2026-03-19 07:03:47');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cases`
--
ALTER TABLE `cases`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `doctor_profiles`
--
ALTER TABLE `doctor_profiles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `doctor_profiles`
--
ALTER TABLE `doctor_profiles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `doctor_profiles`
--
ALTER TABLE `doctor_profiles`
  ADD CONSTRAINT `doctor_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
