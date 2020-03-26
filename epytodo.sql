DROP DATABASE IF EXISTS `epytodo`;
CREATE DATABASE `epytodo`;
USE `epytodo`;

CREATE TABLE `user` (
  `user_id` int(32) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) DEFAULT CHARSET=utf8;

CREATE TABLE `task` (
  `task_id` int(32) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `begin` datetime NOT NULL DEFAULT current_timestamp(),
  `end` datetime DEFAULT NULL,
  `status` varchar(255) NOT NULL DEFAULT 'not started'
) DEFAULT CHARSET=utf8;

CREATE TABLE `user_has_task` (
  `fk_user_id` int(32) NOT NULL,
  `fk_task_id` int(32) NOT NULL,
  FOREIGN KEY(`fk_user_id`) REFERENCES `user` (`user_id`),
  FOREIGN KEY(`fk_task_id`) REFERENCES `task` (`task_id`)
) DEFAULT CHARSET=utf8;