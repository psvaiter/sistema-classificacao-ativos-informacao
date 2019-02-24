USE `knoweak`;

set @ts = current_timestamp;
insert into it_asset_category 
values 
	(1, 'Informação', @ts, @ts), 				-- Information
    (2, 'Política', @ts, @ts), 					-- Policy
    (3, 'Pessoa', @ts, @ts),					-- People
    (4, 'Ambiente / Infraestrutura', @ts, @ts),	-- Environment / Infrastructure
    (5, 'Hardware', @ts, @ts),
    (6, 'Software', @ts, @ts);

insert into rating_level
values
	(1, 'Muito baixo'),
    (2, 'Baixo'),
    (3, 'Médio'),
    (4, 'Alto'),
    (5, 'Muito alto');
    