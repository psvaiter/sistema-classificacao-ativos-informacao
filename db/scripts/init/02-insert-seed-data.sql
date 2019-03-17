USE `knoweak`;

SET @ts = CURRENT_TIMESTAMP;
INSERT INTO it_asset_category
VALUES
    (1, 'Informação', @ts, @ts), 				-- Information
    (2, 'Política', @ts, @ts), 					-- Policy
    (3, 'Pessoa', @ts, @ts),					-- People
    (4, 'Ambiente / Infraestrutura', @ts, @ts),	-- Environment / Infrastructure
    (5, 'Hardware', @ts, @ts),
    (6, 'Software', @ts, @ts);

INSERT INTO rating_level
VALUES
    (1, 'Muito baixo'),
    (2, 'Baixo'),
    (3, 'Médio'),
    (4, 'Alto'),
    (5, 'Muito alto');
    