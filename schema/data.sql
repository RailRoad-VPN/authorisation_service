INSERT INTO public."user" (uuid, email, password, enabled, is_expired, is_locked, is_password_expired, pin_code)
VALUES ('cf402144-0c02-4b97-98f2-73f7b56160cf', 't@t.t',
        'pbkdf2:sha256:50000$oUVfP1ys$df67be48a814cfe5d0958a4c4f3967230064e329b860b5a607dcdc8560054ac6', TRUE, FALSE,
        FALSE, FALSE, 1111);


-- ios and ikev2
INSERT INTO public.user_device (uuid, user_uuid, device_token, device_id, virtual_ip, device_ip, platform_id, vpn_type_id, location, is_active, is_connected)
VALUES ('78b752a5-2928-48a9-9fa7-ba8bebad9f61', 'cf402144-0c02-4b97-98f2-73f7b56160cf', '123', '321', '10.0.0.2', '192.168.0.12', 1, 2, 'Moscow', TRUE, FALSE );
-- windows and openvpn
INSERT INTO public.user_device (uuid, user_uuid, device_token, device_id, virtual_ip, device_ip, platform_id, vpn_type_id, location, is_active, is_connected)
VALUES ('4c23dffb-2cf2-4173-9d0c-e38caad6e12b', 'cf402144-0c02-4b97-98f2-73f7b56160cf', '456', '654', '10.0.1.10', '127.0.0.1', 3, 1, 'Los Angeles', TRUE, FALSE);