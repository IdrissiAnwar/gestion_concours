-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 22, 2025 at 02:03 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `concours`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `root` tinyint(1) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL COMMENT 'Stocker uniquement des mots de passe hachés (ex: bcrypt)',
  `grade` varchar(50) DEFAULT 'admin 3eme grade'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `root`, `username`, `password`, `grade`) VALUES
(1, 1, 'anwar', '$2b$12$ZMLFNuzR0.qzdBlrNVzSoOuRWRjhNgyd97eooyDE6B4EnWAFBtTr6', 'admin root'),
(6, 1, 'faraj', '$2b$12$9XUA7F.BfDXM3CgCK5cJeuoLtg1Nqq7H8Y5hUNvSebIAzYx2jhdKq', 'admin root'),
(8, 0, 'test', '$2b$12$fJimvaAhgqqI0a1ZRt6u7.ZzQjHyEO3IIrHbJ7k/mvrcaZshgbQYa', 'admin 3ème grade');

-- --------------------------------------------------------

--
-- Table structure for table `affectation`
--

CREATE TABLE `affectation` (
  `id_candi` int(11) NOT NULL,
  `id_salle` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `candidat`
--

CREATE TABLE `candidat` (
  `id_candi` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `categorie` varchar(50) DEFAULT NULL,
  `handicap` tinyint(1) DEFAULT NULL,
  `cin` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `candidat`
--

INSERT INTO `candidat` (`id_candi`, `username`, `categorie`, `handicap`, `cin`) VALUES
(1, 'anwar', 'License', 0, 'A123456');

-- --------------------------------------------------------

--
-- Table structure for table `concours`
--

CREATE TABLE `concours` (
  `id_concours` int(11) NOT NULL,
  `titre` varchar(150) DEFAULT NULL,
  `datee` date DEFAULT NULL,
  `description` text DEFAULT NULL,
  `type_concours` varchar(100) DEFAULT NULL,
  `niveau_requis` varchar(100) DEFAULT NULL,
  `nb_candidats` int(11) DEFAULT NULL,
  `faculte` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `participe`
--

CREATE TABLE `participe` (
  `id_concours` int(11) NOT NULL,
  `id_candi` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `realise`
--

CREATE TABLE `realise` (
  `id_admin` int(11) NOT NULL,
  `id_concours` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `salle`
--

CREATE TABLE `salle` (
  `id_salle` int(11) NOT NULL,
  `nom_salle` varchar(100) DEFAULT NULL,
  `capacite` int(11) DEFAULT NULL,
  `adresse` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `affectation`
--
ALTER TABLE `affectation`
  ADD PRIMARY KEY (`id_candi`),
  ADD KEY `id_salle` (`id_salle`);

--
-- Indexes for table `candidat`
--
ALTER TABLE `candidat`
  ADD PRIMARY KEY (`id_candi`),
  ADD UNIQUE KEY `cin` (`cin`);

--
-- Indexes for table `concours`
--
ALTER TABLE `concours`
  ADD PRIMARY KEY (`id_concours`);

--
-- Indexes for table `participe`
--
ALTER TABLE `participe`
  ADD PRIMARY KEY (`id_concours`,`id_candi`),
  ADD KEY `id_candi` (`id_candi`);

--
-- Indexes for table `realise`
--
ALTER TABLE `realise`
  ADD PRIMARY KEY (`id_admin`,`id_concours`),
  ADD KEY `id_concours` (`id_concours`);

--
-- Indexes for table `salle`
--
ALTER TABLE `salle`
  ADD PRIMARY KEY (`id_salle`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `candidat`
--
ALTER TABLE `candidat`
  MODIFY `id_candi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `concours`
--
ALTER TABLE `concours`
  MODIFY `id_concours` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `salle`
--
ALTER TABLE `salle`
  MODIFY `id_salle` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `affectation`
--
ALTER TABLE `affectation`
  ADD CONSTRAINT `affectation_ibfk_1` FOREIGN KEY (`id_candi`) REFERENCES `candidat` (`id_candi`),
  ADD CONSTRAINT `affectation_ibfk_2` FOREIGN KEY (`id_salle`) REFERENCES `salle` (`id_salle`);

--
-- Constraints for table `participe`
--
ALTER TABLE `participe`
  ADD CONSTRAINT `participe_ibfk_1` FOREIGN KEY (`id_concours`) REFERENCES `concours` (`id_concours`),
  ADD CONSTRAINT `participe_ibfk_2` FOREIGN KEY (`id_candi`) REFERENCES `candidat` (`id_candi`);

--
-- Constraints for table `realise`
--
ALTER TABLE `realise`
  ADD CONSTRAINT `realise_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`),
  ADD CONSTRAINT `realise_ibfk_2` FOREIGN KEY (`id_concours`) REFERENCES `concours` (`id_concours`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
