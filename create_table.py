import pymysql
from functions import connection_db
host,user,password,database = connection_db()
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cur = connection.cursor()
# cur.execute("CREATE TABLE `categories` ( `id` int(11) NOT NULL AUTO_INCREMENT,`cat_name` varchar(255) NOT NULL,`timestamp` timestamp NOT NULL DEFAULT current_timestamp(),PRIMARY KEY (`id`))")
# cur.execute("CREATE TABLE `jobs` (`id` int(11) NOT NULL AUTO_INCREMENT,`website_id` int(11) NOT NULL,`category_id` int(11) NOT NULL,`title` varchar(255) NOT NULL,`salary` varchar(30) DEFAULT NULL,`location` varchar(255) DEFAULT NULL,`job_ref` varchar(255) DEFAULT NULL,`staff_group` varchar(255) DEFAULT NULL,`description` text DEFAULT NULL,`apply_link` varchar(255) DEFAULT NULL,`timestamp` timestamp NOT NULL DEFAULT current_timestamp(),PRIMARY KEY (`id`)) ")
# cur.execute("CREATE TABLE `job_types` (`id` int(11) NOT NULL AUTO_INCREMENT,`job_id` int(11) NOT NULL,`job_type_id` int(11) NOT NULL,`timestamp` timestamp NOT NULL DEFAULT current_timestamp(),PRIMARY KEY (`id`))")
# cur.execute("CREATE TABLE `types` (`id` int(11) NOT NULL AUTO_INCREMENT,`job_type` varchar(255) NOT NULL,`timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),PRIMARY KEY (`id`))")
# cur.execute("CREATE TABLE `websites` (`id` int(11) NOT NULL AUTO_INCREMENT,`site_name` varchar(255) NOT NULL,`site_link` varchar(255) NOT NULL,`timestamp` timestamp NOT NULL DEFAULT current_timestamp(),PRIMARY KEY (`id`)) ")
# cur.execute("ALTER TABLE `jobs` ADD `agency_id` INT NULL DEFAULT NULL AFTER `category_id`")
# cur.execute("CREATE TABLE `agency` (`id` int(11) NOT NULL AUTO_INCREMENT,`name` varchar(255) NOT NULL,PRIMARY KEY (`id`))")
# cur.execute("DELETE FROM `jobs`")
# cur.execute("DELETE FROM `categories`")
# cur.execute("DELETE FROM `job_types`")
# cur.execute("DELETE FROM `types`")
# cur.execute("DELETE FROM `websites`")
# cur.execute("DELETE FROM `agency`")

# print(cur.execute("SELECT * FROM jobs"))

connection.close()