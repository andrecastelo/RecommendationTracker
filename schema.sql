drop table if exists colaboradores;
drop table if exists clientes;
drop table if exists admins;
create table colaboradores (
	id INTEGER PRIMARY KEY autoincrement,
	nome string not null
);

create table clientes (
	id INTEGER PRIMARY KEY autoincrement,
	nome string not null,
	conta boolean not null default 0,
	aplicacao boolean not null default 0,	
	indicacao INTEGER,
	FOREIGN KEY(indicacao) REFERENCES colaboradores(id)
);

create table admins (
    id INTEGER PRIMARY KEY autoincrement,
    nome STRING NOT NULL,
    password STRING NOT NULL
);

insert into colaboradores (nome) values ('agomes');
insert into colaboradores (nome) values ('fnery');
insert into colaboradores (nome) values ('llisboa');
insert into colaboradores (nome) values ('nsixel');
insert into colaboradores (nome) values ('vdias');

insert into admins (nome, password) values ('andrecastelo', 'c3d05c5fe71edf6960934a802ca1bf4257404646');
insert into admins (nome, password) values ('nsixel', '637dd3894df6b16a956ab46ed377e5d85a7b2310');