TRUNCATE public.user CASCADE;
TRUNCATE public.user_device CASCADE;
TRUNCATE public.user_vpn_server_config CASCADE;
TRUNCATE public.ticket_status CASCADE;
TRUNCATE public.user_ticket CASCADE;

INSERT INTO public.ticket_status (id, name) VALUES (1, 'new');
INSERT INTO public.ticket_status (id, name) VALUES (2, 'in_progress');
INSERT INTO public.ticket_status (id, name) VALUES (3, 'feedback');
INSERT INTO public.ticket_status (id, name) VALUES (4, 'closed');