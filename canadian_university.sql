-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 23, 2025 at 12:59 PM
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
-- Database: `canadian_university`
--

-- --------------------------------------------------------

--
-- Table structure for table `notices`
--

CREATE TABLE `notices` (
  `id` varchar(255) NOT NULL,
  `title` varchar(500) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `attachment` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notices`
--

INSERT INTO `notices` (`id`, `title`, `date`, `attachment`) VALUES
('CUB/Notice/04012024-01', 'Holiday Notice', '2024-04-01', 'notices\\CUB_Notice_04012024-01.pdf'),
('CUB/Notice/13012024-01', 'Registration Week for LLB Program', '2024-01-13', 'notices\\CUB_Notice_13012024-01.pdf'),
('CUB/Notice/14022024_02', 'Merit Based Scholarship for Summer 2022', '2024-02-14', 'notices\\CUB_Notice_14022024_02.pdf'),
('CUB/Notice/24012024_01', 'Registration Week Spring 2024 Trimester', '2024-01-24', 'notices\\CUB_Notice_24012024_01.pdf'),
('CUB/Notice/24012024_02', 'Registration for Spring 2024 Trimester', '2024-01-25', 'notices\\CUB_Notice_24012024_02.pdf'),
('CUB/Notice/24012025_01', 'Term Break for Fall 2023 Trimester', '2024-01-25', 'notices\\CUB_Notice_24012025_01.pdf'),
('CUB/Notice/RO/03082024/001', 'Contacts of Emergency Support Team', '2024-08-03', 'notices\\CUB_Notice_RO_03082024_001.pdf'),
('CUB/Notice/RO/06082024/001', 'Congratulations to Students', '2024-08-06', 'notices\\CUB_Notice_RO_06082024_001.pdf'),
('CUB/Notice/RO/17082024/001', 'Announcement for Class Resume', '2024-08-17', 'notices\\CUB_Notice_RO_17082024_001.pdf'),
('CUB/Notice/RO/31072024/001', 'Letter from Authority of CUB', '2024-07-31', 'notices\\CUB_Notice_RO_31072024_001.pdf'),
('CUB/REG/0012/20251115/01', 'Notice Fresher\'s Fall 2025', '2025-11-15', 'notices\\CUB_REG_0012_20251115_01.pdf'),
('CUB/REG/GHN/0001/20240220/01', 'Holiday', '2024-02-20', 'notices\\CUB_REG_GHN_0001_20240220_01.pdf'),
('CUB/REG/GHN/0001/20240314/01', 'Holiday', '2024-03-14', 'notices\\CUB_REG_GHN_0001_20240314_01.pdf'),
('CUB/REG/GHN/0001/20240314/02', 'Fees Payment for Midterm Exam Spring 2024', '2024-03-14', 'notices\\CUB_REG_GHN_0001_20240314_02.pdf'),
('CUB/REG/GHN/0002/20240225/01', 'Holiday', '2024-02-25', 'notices\\CUB_REG_GHN_0002_20240225_01.pdf'),
('CUB/REG/GHN/0002/20250217/01', 'Holiday Notice', '2025-02-17', 'notices\\CUB_REG_GHN_0002_20250217_01.pdf'),
('CUB/REG/GHN/0004/20240325/01', 'Holiday Notice', '2024-03-25', 'notices\\CUB_REG_GHN_0004_20240325_01.pdf'),
('CUB/REG/GHN/0004/20250412/01', 'Holiday Notice for the Occasion of Pohela Boishakh', '2025-04-13', 'notices\\CUB_REG_GHN_0004_20250412_01.pdf'),
('CUB/REG/GHN/0005/20240713/01', 'Holiday Notice', '2024-07-16', 'notices\\CUB_REG_GHN_0005_20240713_01.pdf'),
('CUB/REG/GHN/0005/20250427/01', 'Holiday Notice for May Day 2025', '2025-04-27', 'notices\\CUB_REG_GHN_0005_20250427_01.pdf'),
('CUB/REG/GHN/0006/20250508/01', 'Holiday Notice for Buddha Purnima 2025', '2025-05-10', 'notices\\CUB_REG_GHN_0006_20250508_01.pdf'),
('CUB/REG/GHN/0007/20250520/01', 'Holiday Notice for Eid Ul Adha 2025', '2025-05-20', 'notices\\CUB_REG_GHN_0007_20250520_01.pdf'),
('CUB/REG/GHN/0008/20250703/01', 'Holiday Notice Ashura 2025', '2025-07-03', 'notices\\CUB_REG_GHN_0008_20250703_01.pdf'),
('CUB/REG/GHN/0009/20250707/01', 'Notice for Trimester Break Spring 2025', '2025-07-07', 'notices\\CUB_REG_GHN_0009_20250707_01.pdf'),
('CUB/REG/GHN/0009/20250803/01', 'Holiday Notice (July Uprising Day)', '2025-08-03', 'notices\\CUB_REG_GHN_0009_20250803_01.pdf'),
('CUB/REG/GHN/0010/20250813/01', 'Holiday Notice (Janmastami) 2025', '2025-08-13', 'notices\\CUB_REG_GHN_0010_20250813_01.pdf'),
('CUB/REG/GHN/0010/20250928/01', 'Holiday Notice Durga Puja 2025', '2025-11-28', 'notices\\CUB_REG_GHN_0010_20250928_01.pdf'),
('CUB/REG/GHN/0011/20250603/01', 'Merit Based Scholarship for Summer 2024', '2025-06-03', 'notices\\CUB_REG_GHN_0011_20250603_01.pdf'),
('CUB/REG/GHN/006/20240717/01', 'Holiday Notice', '2024-07-17', 'notices\\CUB_REG_GHN_006_20240717_01.pdf'),
('CUB/REG/GN/0001/20250311/01', 'Proposal for Government-Funded Film Production for 2024-2025', '2025-03-11', 'notices\\CUB_REG_GN_0001_20250311_01.pdf'),
('CUB/REG/Notice/0001/20240529/01', 'Term Break for Spring 2024', '2024-05-29', 'notices\\CUB_REG_Notice_0001_20240529_01.pdf'),
('CUB/REG/Notice/0001/20250217/02', 'Semester Break for Fall 2024', '2025-02-17', 'notices\\CUB_REG_Notice_0001_20250217_02.pdf'),
('CUB/Reg/Notice/0006/20230607/01', 'Registration Week - Summer 2023', '2022-06-27', 'notices\\CUB_Reg_Notice_0006_20230607_01.pdf'),
('CUB/Reg/Notice/0006/20230608/01', 'Academic Events 2023 (Except LLB Program)', '2023-06-08', 'notices\\CUB_Reg_Notice_0006_20230608_01.pdf'),
('CUB/REG/Notice/0010/20230903/01', 'Holiday Notice', '2023-09-03', 'notices\\CUB_REG_Notice_0010_20230903_01.pdf'),
('CUB/REG/Notice/0011/20230813/02', 'Holiday Notice', '2023-08-13', 'notices\\CUB_REG_Notice_0011_20230813_02.pdf'),
('CUB/REG/Notice/0011/20231010/01', 'Course Registration Process', '2023-10-10', 'notices\\CUB_REG_Notice_0011_20231010_01.pdf'),
('CUB/REG/Notice/0011/20231010/02', 'Course Registration Notice', '2025-11-28', 'notices\\CUB_REG_Notice_0011_20231010_02.pdf'),
('CUB/REG/Notice/0011/20231112/01', 'Grade Review Notice', '2023-11-12', 'notices\\CUB_REG_Notice_0011_20231112_01.pdf'),
('CUB/REG/Notice/0011/20231214/01', 'Holiday Notice Victory Day', '2023-12-14', 'notices\\CUB_REG_Notice_0011_20231214_01.pdf'),
('CUB/REG/Notice/0011/20240402/01', 'Holiday Notice', '2024-04-02', 'notices\\CUB_REG_Notice_0011_20240402_01.pdf'),
('CUB/REG/Notice/0011/20240403/01', 'Holiday Notice', '2024-04-03', 'notices\\CUB_REG_Notice_0011_20240403_01.pdf'),
('CUB/REG/Notice/0011/20240406/01', 'Merit Based Scholarship Results for Fall 2022', '2024-04-24', 'notices\\CUB_REG_Notice_0011_20240406_01.pdf'),
('CUB/REG/Notice/0011/20251128/01', 'Orientation Program Fall 2025 Trimester and Summer Bi-Semester', '2025-11-27', 'notices\\CUB_REG_Notice_0011_20251128_01.pdf'),
('CUB/REG/Notice/0013/20231224/01', 'Holiday Notice Christmas Day', '2023-12-24', 'notices\\CUB_REG_Notice_0013_20231224_01.pdf'),
('CUB/REG/Notice/0013/20240430/01', 'Holiday Notice', '2024-04-30', 'notices\\CUB_REG_Notice_0013_20240430_01.pdf'),
('CUB/REG/Notice/0015/20240520/01', 'Holiday of \'Buddha Purnima\'', '2024-05-20', 'notices\\CUB_REG_Notice_0015_20240520_01.pdf'),
('CUB/REG/Notice/0017/20240612/01', 'Holiday Notice', '2024-06-12', 'notices\\CUB_REG_Notice_0017_20240612_01.pdf'),
('CUB/REG/Notice/0017/20240824/01', 'Class Resume', '2024-08-24', 'notices\\CUB_REG_Notice_0017_20240824_01.pdf'),
('CUB/REG/Notice/0017/20240824/02', 'Holiday Notice', '2024-08-24', 'notices\\CUB_REG_Notice_0017_20240824_02.pdf'),
('CUB/REG/Notice/0017/20240831/01', 'Class Resume in Hybrid Mode', '2024-08-31', 'notices\\CUB_REG_Notice_0017_20240831_01.pdf'),
('CUB/REG/Notice/0018/20240914/01', 'Holiday Notice Eid-E-Miladunnabi 2024', '2024-09-14', 'notices\\CUB_REG_Notice_0018_20240914_01.pdf'),
('CUB/REG/Notice/0020/20240924/01', 'Admit Card Collection Method for the Final Examination (Summer 2024 Semester)', '2024-09-24', 'notices\\CUB_REG_Notice_0020_20240924_01.pdf'),
('CUB/REG/Notice/0022/20240925/01', 'Holiday Notice Durga Puja 2024', '2024-10-01', 'notices\\CUB_REG_Notice_0022_20240925_01.pdf'),
('CUB/REG/Notice/0024/20241022/01', 'Notice for Semester Break for Summer 2024', '2024-10-22', 'notices\\CUB_REG_Notice_0024_20241022_01.pdf'),
('CUB/REG/Notice/0025/202412115/01', 'Holiday Notice', '2024-12-15', 'notices\\CUB_REG_Notice_0025_202412115_01.pdf'),
('CUB/REG/Notice/0025/20251215/01', 'Holiday Notice Victory Day 2025', '2025-12-15', 'notices\\CUB_REG_Notice_0025_20251215_01.pdf'),
('CUB/REG/Notice/0026/20241223/01', 'Holiday Notice for the Occasion of Christmas Day', '2024-12-24', 'notices\\CUB_REG_Notice_0026_20241223_01.pdf'),
('CUB/REG/OO/0002/20250224/01', 'Office and Class Schedule of Ramadan 2025', '2025-02-24', 'notices\\CUB_REG_OO_0002_20250224_01.pdf'),
('REG/GHN/0009/20250903/01', 'Holiday Notice Eid-e-Milad-un-Nabi 2025', '2025-09-03', 'notices\\REG_GHN_0009_20250903_01.pdf');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `notices`
--
ALTER TABLE `notices`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
