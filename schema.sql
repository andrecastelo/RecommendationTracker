drop table if exists colaboradores;
drop table if exists clientes;
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

insert into colaboradores (nome) values ('agomes');
insert into colaboradores (nome) values ('fnery');
insert into colaboradores (nome) values ('llisboa');
insert into colaboradores (nome) values ('nsixel');
insert into colaboradores (nome) values ('vdias');