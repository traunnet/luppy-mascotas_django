-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 05, 2026 at 09:43 PM
-- Server version: 8.4.3
-- PHP Version: 8.3.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dj_vettech`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Tipo de Servicio', 6, 'add_tiposervicio'),
(22, 'Can change Tipo de Servicio', 6, 'change_tiposervicio'),
(23, 'Can delete Tipo de Servicio', 6, 'delete_tiposervicio'),
(24, 'Can view Tipo de Servicio', 6, 'view_tiposervicio'),
(25, 'Can add Usuario', 9, 'add_usuario'),
(26, 'Can change Usuario', 9, 'change_usuario'),
(27, 'Can delete Usuario', 9, 'delete_usuario'),
(28, 'Can view Usuario', 9, 'view_usuario'),
(29, 'Can add Rol', 8, 'add_rol'),
(30, 'Can change Rol', 8, 'change_rol'),
(31, 'Can delete Rol', 8, 'delete_rol'),
(32, 'Can view Rol', 8, 'view_rol'),
(33, 'Can add Cliente', 7, 'add_cliente'),
(34, 'Can change Cliente', 7, 'change_cliente'),
(35, 'Can delete Cliente', 7, 'delete_cliente'),
(36, 'Can view Cliente', 7, 'view_cliente'),
(37, 'Can add Veterinario', 10, 'add_veterinario'),
(38, 'Can change Veterinario', 10, 'change_veterinario'),
(39, 'Can delete Veterinario', 10, 'delete_veterinario'),
(40, 'Can view Veterinario', 10, 'view_veterinario'),
(41, 'Can add Tipo de Producto', 16, 'add_tipoproducto'),
(42, 'Can change Tipo de Producto', 16, 'change_tipoproducto'),
(43, 'Can delete Tipo de Producto', 16, 'delete_tipoproducto'),
(44, 'Can view Tipo de Producto', 16, 'view_tipoproducto'),
(45, 'Can add Tipo de Servicio', 17, 'add_tiposervicio'),
(46, 'Can change Tipo de Servicio', 17, 'change_tiposervicio'),
(47, 'Can delete Tipo de Servicio', 17, 'delete_tiposervicio'),
(48, 'Can view Tipo de Servicio', 17, 'view_tiposervicio'),
(49, 'Can add Mascota', 15, 'add_mascota'),
(50, 'Can change Mascota', 15, 'change_mascota'),
(51, 'Can delete Mascota', 15, 'delete_mascota'),
(52, 'Can view Mascota', 15, 'view_mascota'),
(53, 'Can add Cita', 11, 'add_cita'),
(54, 'Can change Cita', 11, 'change_cita'),
(55, 'Can delete Cita', 11, 'delete_cita'),
(56, 'Can view Cita', 11, 'view_cita'),
(57, 'Can add Inventario', 14, 'add_inventario'),
(58, 'Can change Inventario', 14, 'change_inventario'),
(59, 'Can delete Inventario', 14, 'delete_inventario'),
(60, 'Can view Inventario', 14, 'view_inventario'),
(61, 'Can add Historial Clínico', 13, 'add_historialclinico'),
(62, 'Can change Historial Clínico', 13, 'change_historialclinico'),
(63, 'Can delete Historial Clínico', 13, 'delete_historialclinico'),
(64, 'Can view Historial Clínico', 13, 'view_historialclinico'),
(65, 'Can add venta', 18, 'add_venta'),
(66, 'Can change venta', 18, 'change_venta'),
(67, 'Can delete venta', 18, 'delete_venta'),
(68, 'Can view venta', 18, 'view_venta'),
(69, 'Can add Detalle de Venta', 12, 'add_detalleventa'),
(70, 'Can change Detalle de Venta', 12, 'change_detalleventa'),
(71, 'Can delete Detalle de Venta', 12, 'delete_detalleventa'),
(72, 'Can view Detalle de Venta', 12, 'view_detalleventa'),
(73, 'Can add Entrada de Producto', 19, 'add_entradaproducto'),
(74, 'Can change Entrada de Producto', 19, 'change_entradaproducto'),
(75, 'Can delete Entrada de Producto', 19, 'delete_entradaproducto'),
(76, 'Can view Entrada de Producto', 19, 'view_entradaproducto'),
(77, 'Can add Salida de Producto', 20, 'add_salidaproducto'),
(78, 'Can change Salida de Producto', 20, 'change_salidaproducto'),
(79, 'Can delete Salida de Producto', 20, 'delete_salidaproducto'),
(80, 'Can view Salida de Producto', 20, 'view_salidaproducto');

-- --------------------------------------------------------

--
-- Table structure for table `cita`
--

CREATE TABLE `cita` (
  `id` bigint NOT NULL,
  `fecha_cita` date NOT NULL,
  `hora_cita` time(6) NOT NULL,
  `estado_cita` varchar(10) NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `id_cliente` bigint DEFAULT NULL,
  `id_veterinario` bigint NOT NULL,
  `id_mascota` bigint DEFAULT NULL,
  `id_servicio` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cita`
--

INSERT INTO `cita` (`id`, `fecha_cita`, `hora_cita`, `estado_cita`, `motivo`, `created_at`, `id_cliente`, `id_veterinario`, `id_mascota`, `id_servicio`) VALUES
(1, '2026-04-12', '12:00:00.000000', 'COMPLETADA', 'Consulta general', '2026-04-02 04:39:54.452917', 6, 8, 1, 1),
(2, '2026-04-01', '11:44:00.000000', 'COMPLETADA', 'Consulta general', '2026-04-02 04:44:45.540403', 6, 8, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` bigint NOT NULL,
  `fecha_registro` date DEFAULT NULL,
  `mascotas_registradas` smallint UNSIGNED NOT NULL
) ;

--
-- Dumping data for table `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `fecha_registro`, `mascotas_registradas`) VALUES
(2, '2026-04-01', 0),
(3, NULL, 0),
(4, NULL, 0),
(5, NULL, 0),
(6, NULL, 0),
(7, '2026-04-01', 0),
(8, NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `id` bigint NOT NULL,
  `cantidad` int UNSIGNED NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `id_inventario` bigint NOT NULL,
  `id_venta` bigint NOT NULL
) ;

--
-- Dumping data for table `detalle_venta`
--

INSERT INTO `detalle_venta` (`id`, `cantidad`, `precio_unitario`, `id_inventario`, `id_venta`) VALUES
(2, 1, 10000.00, 1, 1),
(3, 1, 12000.00, 2, 1),
(4, 1, 12000.00, 2, 2),
(5, 2, 10000.00, 1, 3),
(6, 8, 10000.00, 1, 4),
(7, 1, 12000.00, 2, 6),
(8, 2, 12000.00, 2, 7),
(9, 2, 12000.00, 2, 8),
(10, 1, 12000.00, 2, 9),
(11, 1, 12000.00, 2, 10),
(12, 1, 12000.00, 2, 11),
(13, 1, 12000.00, 2, 12),
(14, 1, 10000.00, 1, 13),
(15, 5, 12000.00, 2, 13),
(16, 1, 10000.00, 1, 14),
(17, 1, 12000.00, 2, 14),
(18, 1, 10000.00, 1, 16),
(19, 1, 12000.00, 2, 16),
(20, 1, 12000.00, 2, 17),
(23, 2, 10000.00, 1, 19),
(24, 5, 12000.00, 2, 20),
(25, 1, 12000.00, 2, 21),
(26, 1, 12000.00, 2, 22),
(27, 1, 12000.00, 2, 23),
(28, 1, 12000.00, 2, 24),
(29, 2, 10000.00, 1, 25);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL
) ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2026-04-01 15:32:26.024745', '1', 'Antipulgas', 1, '[{\"added\": {}}]', 16, 1),
(2, '2026-04-01 15:34:12.468214', '1', 'Antipulgas - 10 unidades', 1, '[{\"added\": {}}]', 14, 1),
(3, '2026-04-01 16:02:08.699558', '2', 'Lupos', 1, '[{\"added\": {}}]', 16, 1),
(4, '2026-04-01 16:02:19.402517', '2', 'Lupos - 10 unidades', 1, '[{\"added\": {}}]', 14, 1),
(5, '2026-04-01 16:04:24.759902', '1', 'juan Hernandez (juan@gmail.com)', 1, '[{\"added\": {}}]', 10, 1),
(6, '2026-04-01 16:04:27.227603', '1', 'Venta object (1)', 2, '[{\"changed\": {\"fields\": [\"Id vet\", \"Estado\"]}}]', 18, 1),
(7, '2026-04-01 17:55:23.727090', '2', 'Lupos - 10 unidades', 2, '[{\"changed\": {\"fields\": [\"Cantidad\"]}}]', 14, 1),
(8, '2026-04-01 17:55:29.037950', '1', 'Antipulgas - 10 unidades', 2, '[{\"changed\": {\"fields\": [\"Cantidad\"]}}]', 14, 1),
(9, '2026-04-02 03:56:04.311666', '8', 'Camila Pardo (camila@gmail.com)', 1, '[{\"added\": {}}]', 10, 1),
(10, '2026-04-02 03:56:44.544338', '8', 'Camila Pardo (camila@gmail.com)', 3, '', 7, 1),
(11, '2026-04-02 03:57:45.181571', '3', 'VETERINARIO', 1, '[{\"added\": {}}]', 8, 1),
(12, '2026-04-02 03:57:57.886334', '8', 'Camila Pardo (camila@gmail.com)', 2, '[{\"changed\": {\"fields\": [\"Rol\"]}}]', 9, 1),
(13, '2026-04-02 04:38:45.790108', '1', 'Consulta General', 1, '[{\"added\": {}}]', 17, 1),
(14, '2026-04-04 19:33:08.040995', '1', 'Consulta General', 2, '[{\"changed\": {\"fields\": [\"Descripcion\", \"Precio\", \"Imagen\"]}}]', 17, 1),
(15, '2026-04-04 19:37:59.686106', '2', 'Control de Plagas', 1, '[{\"added\": {}}]', 17, 1),
(16, '2026-04-04 19:38:39.045980', '3', 'Asesoría Nutricional', 1, '[{\"added\": {}}]', 17, 1),
(17, '2026-04-04 19:39:34.538706', '4', 'Plan de Salud', 1, '[{\"added\": {}}]', 17, 1),
(18, '2026-04-04 19:40:30.770432', '5', 'Estética', 1, '[{\"added\": {}}]', 17, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(19, 'adminApp', 'entradaproducto'),
(20, 'adminApp', 'salidaproducto'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(11, 'clienteApp', 'cita'),
(12, 'clienteApp', 'detalleventa'),
(13, 'clienteApp', 'historialclinico'),
(14, 'clienteApp', 'inventario'),
(15, 'clienteApp', 'mascota'),
(16, 'clienteApp', 'tipoproducto'),
(17, 'clienteApp', 'tiposervicio'),
(18, 'clienteApp', 'venta'),
(4, 'contenttypes', 'contenttype'),
(6, 'inicioVet', 'tiposervicio'),
(7, 'loginVet', 'cliente'),
(8, 'loginVet', 'rol'),
(9, 'loginVet', 'usuario'),
(10, 'loginVet', 'veterinario'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-04-01 15:28:09.693429'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-04-01 15:28:10.024977'),
(3, 'auth', '0001_initial', '2026-04-01 15:28:11.126893'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-04-01 15:28:11.411732'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-04-01 15:28:11.432693'),
(6, 'auth', '0004_alter_user_username_opts', '2026-04-01 15:28:11.464648'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-04-01 15:28:11.491890'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-04-01 15:28:11.514008'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-04-01 15:28:11.546300'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-04-01 15:28:11.601039'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-04-01 15:28:11.627038'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-04-01 15:28:11.712015'),
(13, 'auth', '0011_update_proxy_permissions', '2026-04-01 15:28:11.743041'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-04-01 15:28:11.769296'),
(15, 'loginVet', '0001_initial', '2026-04-01 15:28:14.219528'),
(16, 'admin', '0001_initial', '2026-04-01 15:28:14.918894'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-04-01 15:28:14.950858'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-04-01 15:28:14.987776'),
(19, 'clienteApp', '0001_initial', '2026-04-01 15:28:19.421649'),
(20, 'inicioVet', '0001_initial', '2026-04-01 15:28:19.532777'),
(21, 'sessions', '0001_initial', '2026-04-01 15:28:19.678557'),
(22, 'loginVet', '0002_usuario_numero_documento', '2026-04-01 18:26:46.211736'),
(23, 'adminApp', '0001_initial', '2026-04-02 00:16:33.748547'),
(24, 'loginVet', '0003_alter_usuario_tipo_doc', '2026-04-02 17:22:36.513704'),
(25, 'clienteApp', '0002_tiposervicio_imagen', '2026-04-04 19:29:41.018140'),
(26, 'clienteApp', '0003_tiposervicio_actualizado_el_tiposervicio_creado_el', '2026-04-04 19:36:38.405515');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0t5zn5ca3zpn1d24guir7t6ohlkwaruc', '.eJxVjEEOwiAQRe_C2hAGhgIu3XuGZoBRqgaS0q6MdzckXej2v_f-W8y0b2XeO6_zksVZgDj9bpHSk-sA-UH13mRqdVuXKIciD9rltWV-XQ7376BQL6NO2mvjggL0PmLECbzWAM54vlmblANPGDhiSNqRYotgHE9MIQHqID5fqec2iA:1w96do:fh_lmUF28OQ2ttHgfqslkbJpnEx4zeDxAsQKu0CY_G0', '2026-04-18 19:26:44.130829'),
('46m733xxnixakri388g1x5mzj60ljeix', 'e30:1w7xbB:1-Fkwkr5ErwrLGCZNchW6QbXaFGnaKM9yuaAMQQn8H8', '2026-04-15 15:35:17.405132'),
('5glkxd7d5d1524p6qonr8bcckhv5047r', 'e30:1w95vY:LWCgy9W1soHYd3S8jq47uAEEkzn4CTtrB0BkzLpFLVo', '2026-04-18 18:41:00.906822'),
('7mlomjhmdtrzdemm02i9lec3dkdm4o7i', '.eJxVjMEOwiAQRP-FsyGwtSz16N1vINtdkKqhSWlPxn-XJj1oMqd5b-atAm1rDluNS5hEXZRXp99uJH7GsgN5ULnPmueyLtOod0UftOrbLPF1Pdy_g0w1tzUwGJdagGOk5GmInTXJISa01J-JuevFCCKgk6EBAhQkb5ExMajPF_dvOEU:1w8lAm:uOlVGXtIErZ06fXWz2MrpP4HFQkuFIi_jKX_qnF5Rb8', '2026-04-17 20:31:20.078888'),
('ck0lq7wvi4swqvrxgapwv3knde33piyb', 'e30:1w8SvH:YjyUox9M9IelQfELaNo3HE2nWBDt7XzSjCm0oH1_RB4', '2026-04-17 01:02:07.568867'),
('kumkaw7n0vyqbdxqdgpybpk1tp3oam3r', 'e30:1w8Sk9:etSb-YF13IdamFewNiSzfxrHSvKy6StHtDWhaKp2mVc', '2026-04-17 00:50:37.461340'),
('oksq7ib9yt95qlb28zkxp3idxt3isc7p', '.eJxVjMEOwiAQRP-FsyGwtSz16N1vINtdkKqhSWlPxn-XJj1oMqd5b-atAm1rDluNS5hEXZRXp99uJH7GsgN5ULnPmueyLtOod0UftOrbLPF1Pdy_g0w1tzUwGJdagGOk5GmInTXJISa01J-JuevFCCKgk6EBAhQkb5ExMajPF_dvOEU:1w9SeC:VFlC_V6u_LM_-FTphUHqftinogbeTxXaVecxobg7dyg', '2026-04-19 18:56:36.286251'),
('zzqyw8cdazexdojfsnhufoijok9utpc9', 'e30:1w89CP:2bEOxmDFDeKPAFNJJLHUmPFOnFuggM8RYXHjlx6dROE', '2026-04-16 03:58:29.243576');

-- --------------------------------------------------------

--
-- Table structure for table `entrada_producto`
--

CREATE TABLE `entrada_producto` (
  `id` bigint NOT NULL,
  `cantidad` int UNSIGNED NOT NULL,
  `precio_compra` decimal(10,2) DEFAULT NULL,
  `proveedor` varchar(120) NOT NULL,
  `observacion` longtext NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `id_inventario_id` bigint NOT NULL,
  `registrado_por_id` bigint DEFAULT NULL
) ;

--
-- Dumping data for table `entrada_producto`
--

INSERT INTO `entrada_producto` (`id`, `cantidad`, `precio_compra`, `proveedor`, `observacion`, `fecha`, `id_inventario_id`, `registrado_por_id`) VALUES
(1, 2, 100000.00, 'lucas', 'lucas', '2026-04-02 01:41:07.310590', 1, 1),
(2, 10, 100000.00, 'lucas', '', '2026-04-02 01:41:29.562811', 2, 1),
(3, 3, 10000.00, 'PetMedic', 'Ninguna', '2026-04-02 18:09:12.873432', 1, 1),
(4, 10, 120000.00, 'N/A', 'N/A', '2026-04-04 20:31:06.659218', 1, 9);

-- --------------------------------------------------------

--
-- Table structure for table `historial_clinico`
--

CREATE TABLE `historial_clinico` (
  `id` bigint NOT NULL,
  `fecha` date NOT NULL,
  `motivo_consulta` varchar(255) NOT NULL,
  `diagnostico` longtext NOT NULL,
  `tratamiento` longtext NOT NULL,
  `medicacion` varchar(150) NOT NULL,
  `frecuencia` varchar(80) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `id_cita` bigint DEFAULT NULL,
  `id_veterinario` bigint DEFAULT NULL,
  `id_mascota` bigint NOT NULL,
  `id_servicio` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `historial_clinico`
--

INSERT INTO `historial_clinico` (`id`, `fecha`, `motivo_consulta`, `diagnostico`, `tratamiento`, `medicacion`, `frecuencia`, `estado`, `created_at`, `id_cita`, `id_veterinario`, `id_mascota`, `id_servicio`) VALUES
(1, '2026-04-02', 'Rascado constante', 'sssssssssss', 'sssssssssssssssssssss', 'ssss', 'ssss', 'sss', '2026-04-02 05:05:32.954942', 2, 8, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `inventario`
--

CREATE TABLE `inventario` (
  `id` bigint NOT NULL,
  `cantidad` int UNSIGNED NOT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `id_tipo_producto` bigint NOT NULL
) ;

--
-- Dumping data for table `inventario`
--

INSERT INTO `inventario` (`id`, `cantidad`, `ubicacion`, `id_tipo_producto`) VALUES
(1, 8, 'Estante A', 1),
(2, 0, 'Estante A', 2);

-- --------------------------------------------------------

--
-- Table structure for table `mascota`
--

CREATE TABLE `mascota` (
  `id` bigint NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `edad` smallint UNSIGNED DEFAULT NULL,
  `especie` varchar(40) NOT NULL,
  `sexo` varchar(6) NOT NULL,
  `raza` varchar(50) NOT NULL,
  `color` varchar(30) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `cantidad_visitas` smallint UNSIGNED NOT NULL,
  `estado` varchar(50) NOT NULL,
  `id_cliente` bigint NOT NULL
) ;

--
-- Dumping data for table `mascota`
--

INSERT INTO `mascota` (`id`, `nombre`, `edad`, `especie`, `sexo`, `raza`, `color`, `fecha_nacimiento`, `cantidad_visitas`, `estado`, `id_cliente`) VALUES
(1, 'pepe', 1, 'Gato', 'MACHO', 'Angora', 'negro', '2025-04-01', 0, 'Activo', 6),
(2, 'max', 1, 'Perro', 'MACHO', 'Pastor Alemán', 'negro', '2025-04-01', 0, 'Activo', 6);

-- --------------------------------------------------------

--
-- Table structure for table `rol`
--

CREATE TABLE `rol` (
  `id` bigint NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `descripcion` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `rol`
--

INSERT INTO `rol` (`id`, `nombre`, `descripcion`) VALUES
(1, 'ADMINISTRADOR', ''),
(2, 'CLIENTE', ''),
(3, 'VETERINARIO', 'Atención al cliente');

-- --------------------------------------------------------

--
-- Table structure for table `salida_producto`
--

CREATE TABLE `salida_producto` (
  `id` bigint NOT NULL,
  `cantidad` int UNSIGNED NOT NULL,
  `motivo` varchar(10) NOT NULL,
  `observacion` longtext NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `id_inventario_id` bigint NOT NULL,
  `registrado_por_id` bigint DEFAULT NULL
) ;

--
-- Dumping data for table `salida_producto`
--

INSERT INTO `salida_producto` (`id`, `cantidad`, `motivo`, `observacion`, `fecha`, `id_inventario_id`, `registrado_por_id`) VALUES
(1, 2, 'BAJA', 'los', '2026-04-02 01:41:50.283647', 2, 1),
(2, 9, 'OTRO', 'Ninguna', '2026-04-02 18:08:37.038607', 1, 1),
(3, 1, 'DANO', 'N/A', '2026-04-04 20:31:28.746473', 2, 9);

-- --------------------------------------------------------

--
-- Table structure for table `tipo_producto`
--

CREATE TABLE `tipo_producto` (
  `id` bigint NOT NULL,
  `nombre_producto` varchar(120) NOT NULL,
  `categoria` varchar(60) NOT NULL,
  `descripcion` longtext NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tipo_producto`
--

INSERT INTO `tipo_producto` (`id`, `nombre_producto`, `categoria`, `descripcion`, `precio_unitario`) VALUES
(1, 'Antipulgas', 'Medicamento', 'sasasasasa', 10000.00),
(2, 'Lupos', 'sss', 'ssss', 12000.00);

-- --------------------------------------------------------

--
-- Table structure for table `tipo_servicio`
--

CREATE TABLE `tipo_servicio` (
  `id` bigint NOT NULL,
  `tipo` varchar(60) NOT NULL,
  `descripcion` varchar(250) DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `duracion` time(6) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `creado_el` datetime(6) NOT NULL,
  `actualizado_el` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tipo_servicio_cliente`
--

CREATE TABLE `tipo_servicio_cliente` (
  `id` bigint NOT NULL,
  `tipo` varchar(60) NOT NULL,
  `descripcion` varchar(250) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `duracion` time(6) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `actualizado_el` datetime(6) NOT NULL,
  `creado_el` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tipo_servicio_cliente`
--

INSERT INTO `tipo_servicio_cliente` (`id`, `tipo`, `descripcion`, `precio`, `duracion`, `imagen`, `actualizado_el`, `creado_el`) VALUES
(1, 'Consulta General', 'Valoración médica básica de la mascota', 60000.00, '00:30:00.000000', 'servicios/57952_2zCqEj8.jpg', '2026-04-04 19:36:38.164962', '2026-04-04 19:36:38.293038'),
(2, 'Control de Plagas', 'Aplicación de antipulgas y desparasitación externa', 45000.00, '00:30:00.000000', 'servicios/2208_5J8BUH2.i301.034.F.m004.c9.Grooming_salon_isometric_background.jpg', '2026-04-04 19:37:59.683502', '2026-04-04 19:37:59.683468'),
(3, 'Asesoría Nutricional', 'Evaluación y plan alimenticio personalizado', 50000.00, '00:40:00.000000', 'servicios/Asesoría_Nutricional_mascota_nnofg8t.jpg', '2026-04-04 19:38:39.042133', '2026-04-04 19:38:39.042072'),
(4, 'Plan de Salud', 'Chequeo integral preventivo con recomendaciones médicas', 140000.00, '01:00:00.000000', 'servicios/plan_salud_GDwMtFd.png', '2026-04-04 19:39:34.534563', '2026-04-04 19:39:34.534531'),
(5, 'Estética', 'Baño, corte y limpieza general de la mascota', 35000.00, '01:30:00.000000', 'servicios/estetica_aXAHyUR.jfif', '2026-04-04 19:40:30.765457', '2026-04-04 19:40:30.765415');

-- --------------------------------------------------------

--
-- Table structure for table `usuario`
--

CREATE TABLE `usuario` (
  `id` bigint NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `tipo_doc` varchar(3) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `correo` varchar(254) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(150) NOT NULL,
  `foto_perfil` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `rol_id` bigint NOT NULL,
  `numero_documento` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `usuario`
--

INSERT INTO `usuario` (`id`, `password`, `last_login`, `is_superuser`, `tipo_doc`, `nombre`, `apellido`, `correo`, `telefono`, `direccion`, `foto_perfil`, `is_active`, `is_staff`, `created_at`, `rol_id`, `numero_documento`) VALUES
(1, 'pbkdf2_sha256$1200000$hMAJuWAVrEtAprC12xqb8j$AjeNeogQ/3dMO5gMEQCSX/u+GcCiE8kTz02KgzNirSw=', '2026-04-04 19:26:44.115965', 1, 'CC', 'juan', 'Hernandez', 'juan@gmail.com', '3225623697', 'KRA 15 A ESTE N 71 -32 SUR', '', 1, 1, '2026-04-01 15:29:57.736705', 1, '1028863995'),
(2, 'pbkdf2_sha256$1200000$vaUtWtAWcV1bs34uCt9JBN$f+Ap1QsNkFImLO390cKDikbBPaSVUZvbDqeer6j2f3I=', '2026-04-03 00:43:41.936273', 0, 'CC', 'Camilo', 'Diaz', 'camilo@gmail.com', NULL, '', '', 1, 0, '2026-04-01 15:30:42.288467', 2, NULL),
(3, 'pbkdf2_sha256$1200000$NRITRSxnhF42WHWdh55hrH$OLO+HGHjMlvHqq+Z/+SYC3CJUkb9Hiuh+1y8fmkbxEI=', '2026-04-04 18:26:07.876616', 0, 'CC', 'Juan', 'Pablo', 'juanpablow820@gmail.com', '3138588221', 'KR 15 A ESTE N 71-32 SUR', 'fotos_perfil/pokeball.png', 1, 0, '2026-04-01 17:25:23.556857', 2, NULL),
(4, 'pbkdf2_sha256$1200000$iBx4xWjbCzyaOYAoxMyV99$R+9HIA7txKmFxYsw63AyJDmcuvdzfHS0M4beqT0X4Jw=', NULL, 0, 'CC', 'Pablo', 'Cadenas', 'juanpahernandezc911@gmail.com', NULL, '', '', 1, 0, '2026-04-01 17:27:01.738732', 2, NULL),
(5, 'pbkdf2_sha256$1200000$LVjBXPNm6ByxqynehvsNIm$90mmRlNg+8J7QosCg+jmNOB7SvEQe/GBWZli2fOvdfQ=', '2026-04-01 18:30:36.510961', 0, 'CC', 'Angel', 'Marulanda', 'jamarulandacardona9@gmail.com', NULL, '', '', 1, 0, '2026-04-01 18:29:12.407147', 2, NULL),
(6, 'pbkdf2_sha256$1200000$XOdeybjDtrvWGihnFBlKrW$AYw0DfktH6lhEDrndKkW3mNfhrrQ+YzmbO0HSQXk4Ys=', '2026-04-05 18:36:57.531602', 0, 'CC', 'Alexandra', 'Lopex', 'alexandra@gmail.com', '312 123 4568', 'kr 12 este 45 sur', 'fotos_perfil/Icon-192.png', 1, 0, '2026-04-01 19:01:33.133720', 2, '100000000'),
(7, 'pbkdf2_sha256$1200000$X2PedrOjNtBXMrpSlvW5Tx$Yv9hjQT8+qfUzGaYO27l9CX1vqwj6fPuoQbmImns6YE=', '2026-04-01 23:47:09.526095', 0, 'CC', 'Lucas', 'Rodriguez', 'lucas@gmail.vom', NULL, '', '', 1, 0, '2026-04-01 20:30:43.831590', 2, NULL),
(8, 'pbkdf2_sha256$1200000$6GohhE00yQWRsEdlGYQug1$L1XGNPOTyUbDN/PDYziKxlmHMPGcXREFrd4hG3ZC4Pg=', '2026-04-05 18:56:36.236097', 0, 'CC', 'Camila', 'Pardo', 'camila@gmail.com', '', '', 'fotos_perfil/plan_salud.png', 1, 0, '2026-04-02 03:55:32.675194', 3, NULL),
(9, 'pbkdf2_sha256$1200000$cZov7VAs6t1aaxSaS8vSbi$MDlRmTHvOgdTo2eQj9M1bQxhBrzacLGSHK2Xw+L8bO4=', '2026-04-05 17:14:37.209847', 1, 'CC', 'pablo', 'Cadenas', 'pablo@gmail.com', NULL, '', '', 1, 1, '2026-04-04 20:27:04.151236', 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `usuario_groups`
--

CREATE TABLE `usuario_groups` (
  `id` bigint NOT NULL,
  `usuario_id` bigint NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `usuario_user_permissions`
--

CREATE TABLE `usuario_user_permissions` (
  `id` bigint NOT NULL,
  `usuario_id` bigint NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ventas`
--

CREATE TABLE `ventas` (
  `id` bigint NOT NULL,
  `fecha_venta` datetime(6) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `estado` varchar(15) NOT NULL,
  `id_cliente` bigint DEFAULT NULL,
  `id_vet` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ventas`
--

INSERT INTO `ventas` (`id`, `fecha_venta`, `total`, `estado`, `id_cliente`, `id_vet`) VALUES
(1, '2026-04-01 15:30:59.195226', 22000.00, 'COMPLETADO', 2, 1),
(2, '2026-04-01 16:31:11.738819', 12000.00, 'COMPLETADO', 2, NULL),
(3, '2026-04-01 16:31:32.064189', 20000.00, 'COMPLETADO', 2, NULL),
(4, '2026-04-01 16:32:08.859010', 80000.00, 'COMPLETADO', 2, NULL),
(5, '2026-04-01 16:33:11.451713', 0.00, 'CARRITO', 2, NULL),
(6, '2026-04-01 17:28:39.669024', 12000.00, 'COMPLETADO', 3, NULL),
(7, '2026-04-01 17:32:17.455689', 24000.00, 'COMPLETADO', 3, NULL),
(8, '2026-04-01 17:33:29.466085', 24000.00, 'COMPLETADO', 3, NULL),
(9, '2026-04-01 17:35:14.993046', 12000.00, 'COMPLETADO', 3, NULL),
(10, '2026-04-01 17:41:56.813493', 12000.00, 'COMPLETADO', 3, NULL),
(11, '2026-04-01 17:52:39.532245', 12000.00, 'COMPLETADO', 3, NULL),
(12, '2026-04-01 17:53:12.174018', 12000.00, 'COMPLETADO', 3, NULL),
(13, '2026-04-01 17:54:40.971620', 70000.00, 'COMPLETADO', 3, NULL),
(14, '2026-04-01 17:59:24.560573', 22000.00, 'COMPLETADO', 3, NULL),
(15, '2026-04-01 18:00:55.189878', 0.00, 'CARRITO', 3, NULL),
(16, '2026-04-01 18:30:42.390717', 22000.00, 'COMPLETADO', 5, NULL),
(17, '2026-04-01 23:47:56.949690', 12000.00, 'COMPLETADO', 7, NULL),
(18, '2026-04-02 18:14:09.297468', 10000.00, 'COMPLETADO', 6, NULL),
(19, '2026-04-02 18:14:23.083037', 20000.00, 'COMPLETADO', 6, NULL),
(20, '2026-04-02 21:20:26.793708', 60000.00, 'COMPLETADO', 6, NULL),
(21, '2026-04-02 21:24:31.327037', 12000.00, 'COMPLETADO', 6, NULL),
(22, '2026-04-02 21:26:30.053681', 12000.00, 'COMPLETADO', 6, NULL),
(23, '2026-04-02 21:29:55.805645', 12000.00, 'COMPLETADO', 6, NULL),
(24, '2026-04-02 21:30:42.588959', 12000.00, 'COMPLETADO', 6, NULL),
(25, '2026-04-04 20:34:47.241372', 20000.00, 'COMPLETADO', 6, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `veterinario`
--

CREATE TABLE `veterinario` (
  `id_veterinario` bigint NOT NULL,
  `numero_licencia` varchar(30) NOT NULL,
  `especialidad` varchar(80) NOT NULL,
  `anios_experiencia` smallint UNSIGNED DEFAULT NULL
) ;

--
-- Dumping data for table `veterinario`
--

INSERT INTO `veterinario` (`id_veterinario`, `numero_licencia`, `especialidad`, `anios_experiencia`) VALUES
(1, 'LIC004', 'General', 2),
(8, 'LIC002', 'GENERAL', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `cita`
--
ALTER TABLE `cita`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cita_id_cliente_ec7405f8_fk_cliente_id_cliente` (`id_cliente`),
  ADD KEY `cita_id_veterinario_fa1b9fbb_fk_veterinario_id_veterinario` (`id_veterinario`),
  ADD KEY `cita_id_mascota_90251620_fk_mascota_id` (`id_mascota`),
  ADD KEY `cita_id_servicio_7d521265_fk_tipo_servicio_cliente_id` (`id_servicio`);

--
-- Indexes for table `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indexes for table `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `detalle_venta_id_inventario_3bf03907_fk_inventario_id` (`id_inventario`),
  ADD KEY `detalle_venta_id_venta_89bd49dc_fk_ventas_id` (`id_venta`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_usuario_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `entrada_producto`
--
ALTER TABLE `entrada_producto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `entrada_producto_id_inventario_id_7249468c_fk_inventario_id` (`id_inventario_id`),
  ADD KEY `entrada_producto_registrado_por_id_4512072e_fk_usuario_id` (`registrado_por_id`);

--
-- Indexes for table `historial_clinico`
--
ALTER TABLE `historial_clinico`
  ADD PRIMARY KEY (`id`),
  ADD KEY `historial_clinico_id_cita_8f18bc12_fk_cita_id` (`id_cita`),
  ADD KEY `historial_clinico_id_veterinario_6aeaa3cd_fk_veterinar` (`id_veterinario`),
  ADD KEY `historial_clinico_id_mascota_694742f4_fk_mascota_id` (`id_mascota`),
  ADD KEY `historial_clinico_id_servicio_58b27665_fk_tipo_serv` (`id_servicio`);

--
-- Indexes for table `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_id_tipo_producto_1fef71a3_fk_tipo_producto_id` (`id_tipo_producto`);

--
-- Indexes for table `mascota`
--
ALTER TABLE `mascota`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mascota_id_cliente_077231b7_fk_cliente_id_cliente` (`id_cliente`);

--
-- Indexes for table `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indexes for table `salida_producto`
--
ALTER TABLE `salida_producto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `salida_producto_id_inventario_id_93c4b326_fk_inventario_id` (`id_inventario_id`),
  ADD KEY `salida_producto_registrado_por_id_92ca74b6_fk_usuario_id` (`registrado_por_id`);

--
-- Indexes for table `tipo_producto`
--
ALTER TABLE `tipo_producto`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tipo_servicio`
--
ALTER TABLE `tipo_servicio`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tipo_servicio_cliente`
--
ALTER TABLE `tipo_servicio_cliente`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `telefono` (`telefono`),
  ADD KEY `usuario_rol_id_ac58b608_fk_rol_id` (`rol_id`);

--
-- Indexes for table `usuario_groups`
--
ALTER TABLE `usuario_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_groups_usuario_id_group_id_2e3cd638_uniq` (`usuario_id`,`group_id`),
  ADD KEY `usuario_groups_group_id_c67c8651_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `usuario_user_permissions`
--
ALTER TABLE `usuario_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_user_permissions_usuario_id_permission_id_3db58b8c_uniq` (`usuario_id`,`permission_id`),
  ADD KEY `usuario_user_permiss_permission_id_a8893ce7_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ventas_id_cliente_e685d518_fk_cliente_id_cliente` (`id_cliente`),
  ADD KEY `ventas_id_vet_e5c696a7_fk_veterinario_id_veterinario` (`id_vet`);

--
-- Indexes for table `veterinario`
--
ALTER TABLE `veterinario`
  ADD PRIMARY KEY (`id_veterinario`),
  ADD UNIQUE KEY `numero_licencia` (`numero_licencia`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT for table `cita`
--
ALTER TABLE `cita`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `entrada_producto`
--
ALTER TABLE `entrada_producto`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `historial_clinico`
--
ALTER TABLE `historial_clinico`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `mascota`
--
ALTER TABLE `mascota`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `rol`
--
ALTER TABLE `rol`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `salida_producto`
--
ALTER TABLE `salida_producto`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tipo_producto`
--
ALTER TABLE `tipo_producto`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tipo_servicio`
--
ALTER TABLE `tipo_servicio`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tipo_servicio_cliente`
--
ALTER TABLE `tipo_servicio_cliente`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `usuario_groups`
--
ALTER TABLE `usuario_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `usuario_user_permissions`
--
ALTER TABLE `usuario_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `cita`
--
ALTER TABLE `cita`
  ADD CONSTRAINT `cita_id_cliente_ec7405f8_fk_cliente_id_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `cita_id_mascota_90251620_fk_mascota_id` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id`),
  ADD CONSTRAINT `cita_id_servicio_7d521265_fk_tipo_servicio_cliente_id` FOREIGN KEY (`id_servicio`) REFERENCES `tipo_servicio_cliente` (`id`),
  ADD CONSTRAINT `cita_id_veterinario_fa1b9fbb_fk_veterinario_id_veterinario` FOREIGN KEY (`id_veterinario`) REFERENCES `veterinario` (`id_veterinario`);

--
-- Constraints for table `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `cliente_id_cliente_f85642a7_fk_usuario_id` FOREIGN KEY (`id_cliente`) REFERENCES `usuario` (`id`);

--
-- Constraints for table `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `detalle_venta_id_inventario_3bf03907_fk_inventario_id` FOREIGN KEY (`id_inventario`) REFERENCES `inventario` (`id`),
  ADD CONSTRAINT `detalle_venta_id_venta_89bd49dc_fk_ventas_id` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`);

--
-- Constraints for table `entrada_producto`
--
ALTER TABLE `entrada_producto`
  ADD CONSTRAINT `entrada_producto_id_inventario_id_7249468c_fk_inventario_id` FOREIGN KEY (`id_inventario_id`) REFERENCES `inventario` (`id`),
  ADD CONSTRAINT `entrada_producto_registrado_por_id_4512072e_fk_usuario_id` FOREIGN KEY (`registrado_por_id`) REFERENCES `usuario` (`id`);

--
-- Constraints for table `historial_clinico`
--
ALTER TABLE `historial_clinico`
  ADD CONSTRAINT `historial_clinico_id_cita_8f18bc12_fk_cita_id` FOREIGN KEY (`id_cita`) REFERENCES `cita` (`id`),
  ADD CONSTRAINT `historial_clinico_id_mascota_694742f4_fk_mascota_id` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id`),
  ADD CONSTRAINT `historial_clinico_id_servicio_58b27665_fk_tipo_serv` FOREIGN KEY (`id_servicio`) REFERENCES `tipo_servicio_cliente` (`id`),
  ADD CONSTRAINT `historial_clinico_id_veterinario_6aeaa3cd_fk_veterinar` FOREIGN KEY (`id_veterinario`) REFERENCES `veterinario` (`id_veterinario`);

--
-- Constraints for table `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `inventario_id_tipo_producto_1fef71a3_fk_tipo_producto_id` FOREIGN KEY (`id_tipo_producto`) REFERENCES `tipo_producto` (`id`);

--
-- Constraints for table `mascota`
--
ALTER TABLE `mascota`
  ADD CONSTRAINT `mascota_id_cliente_077231b7_fk_cliente_id_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`);

--
-- Constraints for table `salida_producto`
--
ALTER TABLE `salida_producto`
  ADD CONSTRAINT `salida_producto_id_inventario_id_93c4b326_fk_inventario_id` FOREIGN KEY (`id_inventario_id`) REFERENCES `inventario` (`id`),
  ADD CONSTRAINT `salida_producto_registrado_por_id_92ca74b6_fk_usuario_id` FOREIGN KEY (`registrado_por_id`) REFERENCES `usuario` (`id`);

--
-- Constraints for table `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_rol_id_ac58b608_fk_rol_id` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`);

--
-- Constraints for table `usuario_groups`
--
ALTER TABLE `usuario_groups`
  ADD CONSTRAINT `usuario_groups_group_id_c67c8651_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `usuario_groups_usuario_id_161fc80c_fk_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);

--
-- Constraints for table `usuario_user_permissions`
--
ALTER TABLE `usuario_user_permissions`
  ADD CONSTRAINT `usuario_user_permiss_permission_id_a8893ce7_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `usuario_user_permissions_usuario_id_693d9c50_fk_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);

--
-- Constraints for table `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_id_cliente_e685d518_fk_cliente_id_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `ventas_id_vet_e5c696a7_fk_veterinario_id_veterinario` FOREIGN KEY (`id_vet`) REFERENCES `veterinario` (`id_veterinario`);

--
-- Constraints for table `veterinario`
--
ALTER TABLE `veterinario`
  ADD CONSTRAINT `veterinario_id_veterinario_efb1fbb2_fk_usuario_id` FOREIGN KEY (`id_veterinario`) REFERENCES `usuario` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;