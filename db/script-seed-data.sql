set @ts = current_timestamp;
insert into it_asset_category 
values 
	(1, 'Hardware', @ts, @ts),
    (2, 'Software', @ts, @ts),
    (3, 'Local / Infraestutura', @ts, @ts),		-- Place / Infrastucture
    (4, 'Pessoas', @ts, @ts),					-- People
    (5, 'Política', @ts, @ts), 					-- Policy
    (6, 'Informação', @ts, @ts); 				-- Information

insert into rating_level
values
	(1, 'Muito baixo'),
    (2, 'Baixo'),
    (3, 'Médio'),
    (4, 'Alto'),
    (5, 'Muito alto');
    