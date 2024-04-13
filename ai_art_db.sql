-- phpMyAdmin SQL Dump
-- version 4.6.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 27, 2022 at 12:34 PM
-- Server version: 5.5.50
-- PHP Version: 5.5.38

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ai_art_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `id` int(10) NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(200) NOT NULL,
  `level` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `password`, `email`, `level`) VALUES
(1, 'benjamin', 'onuorah', 'benjamin.onuorah@gmail.com', ''),
(3, 'tunji', 'badmus', 'tunji@mail.com', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `request_sample_tb`
--

CREATE TABLE `request_sample_tb` (
  `id` int(10) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `outlier_limit` varchar(50) NOT NULL,
  `req_raw_data` text NOT NULL,
  `level` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `request_sample_tb`
--

INSERT INTO `request_sample_tb` (`id`, `file_name`, `name`, `description`, `outlier_limit`, `req_raw_data`, `level`, `status`) VALUES
(1, 'love5.jpg', 'Love', 'This is the uli symbol for love.', '0.0543', '[[[255 255 255]\n  [255 255 255]\n  [255 255 255]\n  ...\n  [255 255 255]\n  [255 255 255]\n  [255 255 255]]\n\n [[255 255 255]\n  [255 255 255]\n  [255 255 255]\n  ...\n  [255 255 255]\n  [255 255 255]\n  [255 255 255]]\n\n [[255 255 255]\n  [255 255 255]\n  [255 255 255]\n  ...\n  [255 255 255]\n  [255 255 255]\n  [255 255 255]]\n\n ...\n\n [[255 255 255]\n  [255 255 255]\n  [255 255 255]\n  ...\n  [255 255 255]\n  [255 255 255]\n  [255 255 255]]\n\n [[255 255 255]\n  [255 255 255]\n  [255 255 255]\n  ...\n  [255 255 255]\n  [255 255 255]\n  [255 255 255]]\n\n [[255 255 255]\n  [255 255 255]\n  [255 255 255]\n  ...\n  [255 255 255]\n  [255 255 255]\n  [255 255 255]]]', '1', ''),
(2, 'marriage.jpg', 'Mariage', 'ss', '0.071', '[[[254 254 254]\n  [254 254 254]\n  [254 254 254]\n  ...\n  [254 254 254]\n  [254 254 254]\n  [254 254 254]]\n\n [[254 254 254]\n  [254 254 254]\n  [254 254 254]\n  ...\n  [254 254 254]\n  [254 254 254]\n  [254 254 254]]\n\n [[254 254 254]\n  [254 254 254]\n  [254 254 254]\n  ...\n  [254 254 254]\n  [254 254 254]\n  [254 254 254]]\n\n ...\n\n [[254 254 254]\n  [254 254 254]\n  [254 254 254]\n  ...\n  [254 254 254]\n  [254 254 254]\n  [254 254 254]]\n\n [[254 254 254]\n  [254 254 254]\n  [254 254 254]\n  ...\n  [254 254 254]\n  [254 254 254]\n  [254 254 254]]\n\n [[254 254 254]\n  [254 254 254]\n  [254 254 254]\n  ...\n  [254 254 254]\n  [254 254 254]\n  [254 254 254]]]', '1', '');

-- --------------------------------------------------------

--
-- Table structure for table `response_tb`
--

CREATE TABLE `response_tb` (
  `id` int(10) NOT NULL,
  `request_img` varchar(255) NOT NULL,
  `user_response_img` varchar(255) NOT NULL,
  `diff_value` varchar(100) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `request_id` varchar(50) NOT NULL,
  `date_saved` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `response_tb`
--

INSERT INTO `response_tb` (`id`, `request_img`, `user_response_img`, `diff_value`, `user_name`, `request_id`, `date_saved`) VALUES
(1, 'marriage.jpg', 'love1.jpg', '0.0067', 'Test User', '2', '2022-11-25 00:34:53.866343'),
(2, 'marriage.jpg', 'love2.jpg', '0.0036', 'Test User', '2', '2022-11-25 06:41:50.382306'),
(3, 'marriage.jpg', 'love3.jpg', '0.0342', 'Test User', '2', '2022-11-25 06:43:32.361545'),
(4, 'marriage.jpg', 'pix4.jpg', '0.1805', 'Test User', '2', '2022-11-26 01:01:50.384412'),
(5, 'marriage.jpg', 'pix3.jpg', '0.3083', 'Test User', '2', '2022-11-26 01:17:26.657400'),
(6, 'marriage.jpg', 'love4.jpg', '0.0376', 'Test User', '2', '2022-11-26 01:17:54.698021'),
(7, 'marriage.jpg', 'marriage.jpg', '0.071', 'Test User', '2', '2022-11-26 01:18:14.071000'),
(8, 'love5.jpg', 'love1.jpg', '0.0046', 'Test User', '1', '2022-11-26 01:18:56.608982'),
(9, 'love5.jpg', 'love2.jpg', '0.0076', 'Test User', '1', '2022-11-26 01:19:46.856151'),
(10, 'love5.jpg', 'love3.jpg', '0.0454', 'Test User', '1', '2022-11-26 01:20:17.023137'),
(11, 'love5.jpg', 'love1.jpg', '0.0046', 'benjamin', '1', '2022-11-27 02:03:34.501196');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `request_sample_tb`
--
ALTER TABLE `request_sample_tb`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `response_tb`
--
ALTER TABLE `response_tb`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `request_sample_tb`
--
ALTER TABLE `request_sample_tb`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `response_tb`
--
ALTER TABLE `response_tb`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
