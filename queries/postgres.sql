INSERT INTO public.symptoms(id, name, "primary") VALUES
    (1, 'Febre', true),
    (2, 'Tosse', true),
    (3, 'Dor de garganta', true),
    (4, 'Dor de cabeça', false),
    (5, 'Dor de dente', false);

INSERT INTO public.methods(id, name, "primary") VALUES
	(1, 'Secreção de oro e nasofaringe', true),
	(2, 'Tecido post-mortem', true),
	(3, 'Lavado Bronco-alveolar', true);


INSERT INTO public.alembic_version(version_num) VALUES
(77adb3584ff6);
