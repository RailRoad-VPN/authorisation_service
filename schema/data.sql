INSERT INTO public."user" (uuid, email, password, enabled, is_expired, is_locked, is_password_expired, created_date)
VALUES ('cf402144-0c02-4b97-98f2-73f7b56160cf', 't@t.t',
        'pbkdf2:sha256:50000$oUVfP1ys$df67be48a814cfe5d0958a4c4f3967230064e329b860b5a607dcdc8560054ac6', TRUE, FALSE,
        FALSE, FALSE, '2018-05-14 16:22:54.407438');

INSERT INTO public.user_device (uuid, user_uuid, pin_code, device_token, device_name, location, is_active, created_date)
VALUES ('71c89a6f-53bf-4f57-b1f5-414317d1ff7f', 'cf402144-0c02-4b97-98f2-73f7b56160cf', 4455, null, null, null, false,
        '2018-07-09 13:36:09.482178');