set @ts = current_timestamp;
insert into it_asset_category 
values 
	(1, 'Hardware', @ts, @ts),
    (2, 'Software', @ts, @ts),
    (3, 'Place / Infrastucture', @ts, @ts),
    (4, 'People', @ts, @ts),
    (5, 'Policy', @ts, @ts),
    (6, 'Information', @ts, @ts);
    
set @ts = current_timestamp;
insert into system_administrative_role
values
	(1, 'User Admin', NULL, @ts, @ts),
    (2, 'Catalog Manager', NULL, @ts, @ts),
    (3, 'Operator', NULL, @ts, @ts);


insert into rating_level
values
	(1, 'Muito baixo'),
    (2, 'Baixo'),
    (3, 'Médio'),
    (4, 'Alto'),
    (5, 'Muito alto');
    