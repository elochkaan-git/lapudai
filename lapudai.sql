--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chats; Type: TABLE; Schema: public; Owner: manager
--

CREATE TABLE public.chats (
    id integer NOT NULL,
    adresant bigint NOT NULL,
    adresat bigint NOT NULL
);


ALTER TABLE public.chats OWNER TO manager;

--
-- Name: chats_id_seq; Type: SEQUENCE; Schema: public; Owner: manager
--

CREATE SEQUENCE public.chats_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chats_id_seq OWNER TO manager;

--
-- Name: chats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: manager
--

ALTER SEQUENCE public.chats_id_seq OWNED BY public.chats.id;


--
-- Name: services; Type: TABLE; Schema: public; Owner: manager
--

CREATE TABLE public.services (
    id integer NOT NULL,
    name text NOT NULL,
    description text,
    price text NOT NULL,
    age text NOT NULL,
    imgpath text
);


ALTER TABLE public.services OWNER TO manager;

--
-- Name: services_id_seq; Type: SEQUENCE; Schema: public; Owner: manager
--

CREATE SEQUENCE public.services_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.services_id_seq OWNER TO manager;

--
-- Name: services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: manager
--

ALTER SEQUENCE public.services_id_seq OWNED BY public.services.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: manager
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    client_id bigint NOT NULL,
    number text NOT NULL,
    name text NOT NULL,
    services text NOT NULL,
    guests text NOT NULL,
    datetime text NOT NULL
);


ALTER TABLE public.tasks OWNER TO manager;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: manager
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO manager;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: manager
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: manager
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    phone text NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.users OWNER TO manager;

--
-- Name: chats id; Type: DEFAULT; Schema: public; Owner: manager
--

ALTER TABLE ONLY public.chats ALTER COLUMN id SET DEFAULT nextval('public.chats_id_seq'::regclass);


--
-- Name: services id; Type: DEFAULT; Schema: public; Owner: manager
--

ALTER TABLE ONLY public.services ALTER COLUMN id SET DEFAULT nextval('public.services_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: manager
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Data for Name: chats; Type: TABLE DATA; Schema: public; Owner: manager
--

COPY public.chats (id, adresant, adresat) FROM stdin;
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: manager
--

COPY public.services (id, name, description, price, age, imgpath) FROM stdin;
2	Прогулка с хаски	🌲 Прогулка с хаски на поводке по живописному лесу	500 руб/30 минут	old	./img/walk_with_husky.jpg
3	Экскурсия в контактную зону с животными	🐰Подворье Лапудай — это место, где живут ручные домашние животные:\n- Декоративные и калифорнийские кролики\n- Зааненский козел Паша и близняшки — Лило и Гоша\n- Голубоглазый пони Витязь\n- Курочки-несушки и их петушок\n- Конечно же, котики и собачки\n\nВо время экскурсии всех животных можно гладить и кормить. Время пребывания неограниченно 🔥 Рекомендуем брать с собой побольше овощей и фруктов	250 руб/человек	old	./img/contact_zoo.jpg
4	Квест индийский/пиратский (без участия собак)	🏹 Разница, что индейцы стреляют из лука, а пираты взрывают петарды. Пираты могут найти клад, если детям надо что-то подарить. В модуль собаки тоже не заходят, аллергики могут чувствовать себя спокойно.\n\n<b>Продолжительность:</b> 1 час  \n\n<b>Рекомендовано</b>: Для младших школьников и выпускной для садиков	Если меньше 10 человек - 10000 рублей, если 10 и более человек - 1000 руб/ребенок	bbaby	./img/quest_indians_pirates.jpg
5	Квест "Северная игра" (без участия собак)	🏹 Поход по нашим "местам силы" со сбором артефактов для финальной сборки "ловца снов" — волшебного сибирского инструмента для исполнения желаний.  \n\n<b>Продолжительность:</b> 1,5 часа  \n\n<b>Рекомендовано:</b> Для возраста от 10 до 100 лет  \n\n<b>Группы:</b> От трех человек	1500руб/человек	old	./img/quest_indians_pirates.jpg
6	Теплый модуль	🏠 Уютный тёплый модуль.  \n\n<b>Внутри:</b>\n- Большой стол\n- Заварка и сахар\n- Деревянные скамьи с домотканым текстилем\n- Плита\n- Дровяная печь\n- Чайник с кипятком на 3 литра\n- Контейнер для мусора\n- Вешалки для одежды\n- Дрова\n\n<b>На улице:</b>\n- Мангал\n- Шампура и решетки\n- Навес в летнее время\n\n<b>Дополнительно по запросу:</b>\n- Одноразовая посуда\n- Выездной кейтеринг  \n\n<b>Размер помещения:</b> 3х9 м	1500 руб/час	old	./img/warm_module.jpg
7	Ламповая вечеринка	🌟 Пакеты услуг:\n\n<b>- 7,000 руб:</b> 2 часа теплого модуля + встреча с ручными и милыми животными (кролики, пони, козочки, кошечки) + две дрессированные собаки для вашей фотосессии\n\n<b>- 10,000 руб:</b> 2 часа тёплого модуля + встреча с ручными и милыми животными + интерактив с участием дрессированных собак\n\n<b>- 20,000 руб:</b> 3 часа теплого модуля + встреча с ручными и милыми животными + интерактив с участием дрессированных собак + накрытый праздничный стол для чаепития\n\n<b>Дополнительно:</b> Фотограф — ₽5,000/час	смотри описание	old	./img/party.jpg
8	Корпоратив	🏠 Для коллективов, которые устали от праздников в кафе, предлагаем провести корпоратив на природе.  \n\n<b>В программе:</b>\n- Аренда модуля для размещения 4 часа\n- Аренда мангальной площадки с мангалом\n- Дрова для мангала\n- Тематическая программа или катание на собачьих упряжках (по сезону)\n\n<b>Дополнительно:</b> Возможен выездной кейтеринг	25000 руб/15 человек, дальше + 1000 руб за человека	old	./img/corporate_event.jpg
9	Спортивное ориентирование с собаками	🏃 Дети делятся на пары, на каждую пару выдается собака и карта. Задача пройти по всем пунктам и составить слова по картинкам и буквам для итогового рассказа. Все проходит на территории хозяйства, обработанной от клещей.  \n\n<b>Рекомендовано:</b> Для детей начиная со средней школы и старше, либо для младших школьников при участии родителей (не менее 1 родителя на пару детей).  \n\n<b>Продолжительность:</b> Ориентировочно 1 час  	800 руб/человек	teen	./img/events_with_dogs.jpg
10	Экскурсия ко всем питомцам центра	🐾 В сопровождении экскурсовода, без ограничений по времени.	250 руб/человек	old	./img/events_with_dogs.jpg
11	Cпортивно-цирковое мероприятие	🐕 Собаки показывают трюки, в которые вовлекаются дети. В конце ставим собак для фотографий с трюками для вашей самостоятельной фотосессии. Если осталось время, можно сходить на питомник в сопровождении родителей.  \n\n<b>Продолжительность:</b> Ориентировочно 1 час  	Если меньше 10 детей - 10000 рублей, если 10 и более - 1000 руб.человек	bbaby	./img/events_with_dogs.jpg
1	Дог-трекинг	🐕 Отправляйтесь в активную пешую прогулку с дружелюбными и энергичными собаками! Они не только весёлые компаньоны, но и неутомимые помощники на подъёмах. Мы находимся в часе езды от Красноярска в окрестностях Железногорска. Для того, чтобы почувствовать себя одной командой с четвероногим спутником, для Вас будет подобрано специальное снаряжение: пояс и потяг, который сцепляет вас и собаку.\n\n<b>В программе:</b>\n- Экскурсия к ездовым собакам\n- Снаряжение\n- Инструктаж\n- Сопровождение инструктора\n- Дог-трекинг по сосновому лесу\n\n<b>Дистанция:</b> 1 км  \n\n<b>Продолжительность:</b> 25–30 мин  \n\n<b>Собака:</b> Подбирается каждому индивидуально!	900 руб/человек	old	./img/dog_tracking.jpg
12	Квест "В гости к хаски"	🌲 Лесной квест, включающий взаимодействие с собаками.	Если меньше 10 детей - 15000 рублей, если 10 и более - 1500 руб/человек	bbaby	./img/events_with_dogs.jpg
13	Катание в бесснежное время года	🌳 Катание происходит в специальном четырехколесном транспорте — карте. В упряжке находится от 4х собак (в зависимости от веса пассажира и километража). Собаками управляет опытный инструктор.\n\n<b>Важно:</b> Катание доступно для детей до 16 лет  \n\n<b>Бонус:</b> Экскурсия к ездовым собакам совершенно бесплатно🔥	1000 руб/км	teen	./img/riding_without_snow.jpg
14	Катание на собачьих упряжках	🦮 Катание происходит при управлении нарт инструктором, в нартах сидит один пассажир. До 2 лет предпочтительно в сопровождении родителя или старшего ребенка. В таком случае билет сопровождающего оплачивается отдельно.	- 1–2 км — ₽1,500\n- 3 км — ₽2,500\n- 5 км — ₽4,500\n- До 2 лет — бесплатно	old	./img/riding_with_snow.jpg
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: manager
--

COPY public.tasks (id, client_id, number, name, services, guests, datetime) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: manager
--

COPY public.users (id, phone, name) FROM stdin;
\.


--
-- Name: chats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: manager
--

SELECT pg_catalog.setval('public.chats_id_seq', 1, false);


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: manager
--

SELECT pg_catalog.setval('public.services_id_seq', 14, true);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: manager
--

SELECT pg_catalog.setval('public.tasks_id_seq', 1, false);


--
-- Name: chats chats_pkey; Type: CONSTRAINT; Schema: public; Owner: manager
--

ALTER TABLE ONLY public.chats
    ADD CONSTRAINT chats_pkey PRIMARY KEY (id);


--
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: manager
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: manager
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: manager
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

