drop table if exists colaboradores;
drop table if exists areas;
drop table if exists clientes;
create table colaboradores (
	id INTEGER PRIMARY KEY autoincrement,
	nome string not null,
	area INTEGER,
	FOREIGN KEY(area) REFERENCES areas(area_id)
);

create table areas (
	area_id INTEGER PRIMARY KEY autoincrement,
	nome string not null
);
create table clientes (
	id INTEGER PRIMARY KEY autoincrement,
	nome string not null,
	conta boolean not null default 0,
	indicacao INTEGER,
	FOREIGN KEY(indicacao) REFERENCES colaboradores(id)
);
insert into areas (nome) values ('Comunicação');
insert into areas (nome) values ('Atendimento');
insert into areas (nome) values ('Desenvolvimento');

insert into colaboradores (nome, area) values ('agomes', 1);
insert into colaboradores (nome, area) values ('fnery', 1);
insert into colaboradores (nome, area) values ('llisboa', 1);
insert into colaboradores (nome, area) values ('nsixel', 2);
insert into colaboradores (nome, area) values ('vdias', 3);