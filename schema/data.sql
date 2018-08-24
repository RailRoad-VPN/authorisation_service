INSERT INTO public."user" (uuid, email, password, enabled, is_expired, is_locked, is_password_expired, pin_code)
VALUES ('cf402144-0c02-4b97-98f2-73f7b56160cf', 't@t.t',
        'pbkdf2:sha256:50000$oUVfP1ys$df67be48a814cfe5d0958a4c4f3967230064e329b860b5a607dcdc8560054ac6', TRUE, FALSE,
        FALSE, FALSE, 1111);


-- ios and ikev2
INSERT INTO public.user_device (uuid, user_uuid, device_token, device_id, virtual_ip, device_ip, platform_id, vpn_type_id, location, is_active)
VALUES ('78b752a5-2928-48a9-9fa7-ba8bebad9f61', 'cf402144-0c02-4b97-98f2-73f7b56160cf', '123', '321', '10.0.0.2', '192.168.0.12', 1, 2, 'Moscow', TRUE);
-- windows and openvpn
INSERT INTO public.user_device (uuid, user_uuid, device_token, device_id, virtual_ip, device_ip, platform_id, vpn_type_id, location, is_active)
VALUES ('4c23dffb-2cf2-4173-9d0c-e38caad6e12b', 'cf402144-0c02-4b97-98f2-73f7b56160cf', '456', '654', '10.10.0.6', '127.0.0.1', 3, 1, 'Los Angeles', TRUE);


--
-- vpn server configuration
--

-- openvpn
INSERT INTO public.user_vpn_server_config(uuid, user_uuid, configuration, vpn_device_platform_id, vpn_type_id) VALUES ('8f525324-f752-4135-bab7-38e0f1ff96f9', 'cf402144-0c02-4b97-98f2-73f7b56160cf', 'Y2xpZW50Cgp0bHMtY2xpZW50CmF1dGggU0hBMjU2CmNpcGhlciBBRVMtMjU2LUNCQwpyZW1vdGUtY2VydC10bHMgc2VydmVyCnRscy12ZXJzaW9uLW1pbiAxLjIKCnByb3RvIHVkcApyZW1vdGUgc2VydmVyX2lwIHNlcnZlcl9wb3J0CmRldiB0dW4KCnJlc29sdi1yZXRyeSA1Cm5vYmluZAprZWVwYWxpdmUgNSAzMApjb21wLWx6bwpwZXJzaXN0LWtleQpwZXJzaXN0LXR1bgp2ZXJiIDMKCnJvdXRlLW1ldGhvZCBleGUKcm91dGUtZGVsYXkgMgojcmVnaXN0ZXItZG5zCgprZXktZGlyZWN0aW9uIDEKPGNhPgotLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS0KTUlJR21UQ0NCSUdnQXdJQkFnSUpBUHFBY29oa0R4SnRNQTBHQ1NxR1NJYjNEUUVCQ3dVQU1JR0tNUXN3Q1FZRApWUVFHRXdKU1ZURVBNQTBHQTFVRUNBd0dUVzl6WTI5M01ROHdEUVlEVlFRSERBWk5iM05qYjNjeEVUQVBCZ05WCkJBb01DRTV2ZG1sRGIzSndNUXN3Q1FZRFZRUUxEQUpQVlRFWE1CVUdBMVVFQXd3T1kyRXVibTkyYVdOdmNuQXUKY25VeElEQWVCZ2txaGtpRzl3MEJDUUVXRVdGa2JXbHVRRzV2ZG1samIzSndMbkoxTUI0WERURTRNRGd4TnpJdwpNalV3TWxvWERUSTRNRGd4TkRJd01qVXdNbG93Z1lveEN6QUpCZ05WQkFZVEFsSlZNUTh3RFFZRFZRUUlEQVpOCmIzTmpiM2N4RHpBTkJnTlZCQWNNQmsxdmMyTnZkekVSTUE4R0ExVUVDZ3dJVG05MmFVTnZjbkF4Q3pBSkJnTlYKQkFzTUFrOVZNUmN3RlFZRFZRUUREQTVqWVM1dWIzWnBZMjl5Y0M1eWRURWdNQjRHQ1NxR1NJYjNEUUVKQVJZUgpZV1J0YVc1QWJtOTJhV052Y25BdWNuVXdnZ0lpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElDRHdBd2dnSUtBb0lDCkFRRHk2YTB0bEVVSVBwK242UlhUMG5zUEtQTlkxcldQVndESXFhLzEwb2JNR2pwZW5Pc1VSeWN3RVBOdmoxVi8KQjRkNkJIRnE1MGpMblBRQlpLaUJSTnBGNTBTaUJtZlBZOHpIbjgzZzBSYWZMd1FwRlNOZFE3QTZXb3Btbm9vdQo1YXpad0x4a05lTy9CM3pUZ0xHNTBNckZNelJaTEM2UFREenh1RUNkODFiUytLcGpmZlNhYktHT0o4ZTNaRFNkCkFGT2hOa1cyaDVaZmJXbCtMVFhpQi9BWXp6TFlEb3VqaGh3VGRrTXdjV2xwMEpPUVo0aklvVGlwR08wUlc5ckoKOWNHQ0hYZHRuSVlZejdiaGlBMi9MbHdLRmdQejA4SGE0V0tZRjVmZ2hWaDlZUjI5anBPUnFqMEJnZmttZW1sRwppUXJPZjMzOVYzcjlyNndCNndTZkFvOEN4SzVLWjE5OW1xbWVmYlNEQ01Ob1N6Y0kwZ2hsQjJjZS9IRjN1OVBECkloOHRJZ2tMMVVnUzVyY2dnbkpDU21kTXJKR1VBeC9DNXp2OWpiU2I1eWJ0dnR6dnM4RmQzKzlUeno3VDdUNVoKYURHWXZranhmYlEwdE91ekF2Z1ozNjVtU0JSTkxuT29ld04wMTN5UjlWcVA3OVNZeldBZ3k3YlpxemhGZlc4SApONURDQ3o3QlFpV05uSmJRbXBqUUhvRkV4SFFkeHNiOUdEVGh3bkJTZ3RaMUlXUnJYVzV0YkVGMDNqbjhHUE5uClVXMVVGSEU1a2hIQWFsNVVnMkE1NUFwRTlxVzhKK0VIRkFXM2l2cWlEWkNwWlZPRllCQ29xMG53K1Irc1J1blUKOTdYMzZoMjZrZk13YUhNYXUzL1pGWlVSUitoNnB0UDlKM1dDYmVxSUFKS0RDd0lEQVFBQm80SC9NSUg4TUIwRwpBMVVkRGdRV0JCUlcwcGQrWEVPQ3ZRL1Y2MlVEUnVmTDMyZCtJakNCdndZRFZSMGpCSUczTUlHMGdCUlcwcGQrClhFT0N2US9WNjJVRFJ1ZkwzMmQrSXFHQmtLU0JqVENCaWpFTE1Ba0dBMVVFQmhNQ1VsVXhEekFOQmdOVkJBZ00KQmsxdmMyTnZkekVQTUEwR0ExVUVCd3dHVFc5elkyOTNNUkV3RHdZRFZRUUtEQWhPYjNacFEyOXljREVMTUFrRwpBMVVFQ3d3Q1QxVXhGekFWQmdOVkJBTU1EbU5oTG01dmRtbGpiM0p3TG5KMU1TQXdIZ1lKS29aSWh2Y05BUWtCCkZoRmhaRzFwYmtCdWIzWnBZMjl5Y0M1eWRZSUpBUHFBY29oa0R4SnRNQXdHQTFVZEV3UUZNQU1CQWY4d0N3WUQKVlIwUEJBUURBZ0VHTUEwR0NTcUdTSWIzRFFFQkN3VUFBNElDQVFDRUtVZVM2NEtUVGJKanJkdWMzcUVoMFpqNgpFeFd5UFpDbDZUMzEwdVlobU9EcnNYR3FzQVNpR1ZNcVl5UW9aOXdNOFR5eGdpRjQ4dFd3aW5jeGlzdkxWckdOCjhHVzYvVUxwK3cxZlJPV2tLeVpLSWxVMklFWTl3dURzK2FFL2VhSmtFNGV6SlJjdXJwZThOVjhPSWtCUW1uVmUKa3lrejQ0MDFzbDNpMTFualk4K1hBd29HejR6RDIxWFFjOGY1anVMTENTeERmRjQ1MUJqZVI1VHplc3pRZGRQNgpoSTlVQmpWZmk4bUNRNEhaQ0REY0VRSkpWeXpwVFhsRkRqbUFyZ0ZJZzlpNk9WMVQwYjlGcGk2RFA2UVNLNzJmClE0djhIWlJIcmNtS0gvVkZ5eVBlbW5YYVZxSEI4TnpTcm9uWURLa2pZaWluUEE1dG1Zbk90YXRsSDI3SUViTnYKZ0k2V05iaVRBMUVJcUZaL2Q2Z2JzMTFQRUFYd0JyYTZPTVZoWFpXQ3FuZW1Gb0ZZY2RCZ3NJOW1XQVIrY0NOcQp0enc2T3Q0R25CVzhOMWR6ajBWRGpwVDVuVW52eTkrUStCYUNwd0thTlQwRWhwcnJ3d0liYlFCK3pIcGZFWXBPCnhGam5MRkNHdUZYOElLMktqUDJsU2dwSWhIQTM3YzA5SUlGQTRwMHFwZ211ZithbUpMS2E2cXFncXRKTFJta1IKaTBwaW5lMVgxTm1lcUwweGN6TlFYQmVLL2ZzQitQUVc0QWRyOE8rcWVHVFdXQy9GWjQ0K1VkUitCUU1BRDNkaQpBbU42cUNqVGhDMlFWdjgrdVV1STZKR0xzdDlWZGV0ZzZsektXZGtwQWg3SWJLQlROUlY0QXlxS3RUR2N5K1ZhCjI1L2V4U01NN3UyMlFrWjh5UT09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0KCjwvY2E+Cgo8dGxzLWF1dGg+CiMKIyAyMDQ4IGJpdCBPcGVuVlBOIHN0YXRpYyBrZXkKIwotLS0tLUJFR0lOIE9wZW5WUE4gU3RhdGljIGtleSBWMS0tLS0tCjcxMTA3MTNhZTk1YTIyNzg5YTYwMzQ3NGZmMmQwMzk3CmI5YmViZGZhOGRjMzFkNmFmMWI0ZWE2MjNjY2FlODczCmFiMmFkNDI5NzVhMTA1Yzg3Mjc1NDUzYjNlMTNmNGZiCjUxOWMyMGFlZGU0MThmMTkwZWYwMWFlNjU0NDk1MzkwCjk1NGRkNTVkZDU3NWM0MWNiNDNmYmM3NzE0ZTBlNDhhCmU2YWQ5ZWQxYWVjMGVmOTRlNDlmYjQ3NWUxZGYwZmE0CjNlOWVhZmMwMmE5ZWY2OWVlMzdlZDc1ODUxZmVhNjA0CjlhZWVmNjg1NDZjMmNkMWY1MjMxOGVlODZiNmMxMTU2Cjk3MjM2NmQyZWFjMWIyNzVkNGUwMzMxNzMzOWNmN2RjCjg4YzIxYjQ3MDgzYzA3YjY2ODE2MjUyZDViZTdlYmZjCjBlZjQ1ZmNhY2VhNDQ0OTI2OTE3OTc5N2U2NGQyOWY2CjcwNTM5MzNhZjY2NDQ2OTE4ZDBiNDJhZDRhOGU4OTdkCjJhNDk3NTRiOTI5NTdmMmMyOTE4M2U3MzFkOTc3ZDMwCjE3MTI1NGI5N2QwY2EzZDc4NjVkNGU2OWQ2ZWY0ZjIzCjM2M2UwNWE0MDdiZDQ3ZjA4MDNlNWQ4ODg1N2MzMGZjCjM2ZmIxNGY5ZmE3ZjhlYWFiMTlkOWMyZGM0ZDRkMDkxCi0tLS0tRU5EIE9wZW5WUE4gU3RhdGljIGtleSBWMS0tLS0tCgo8L3Rscy1hdXRoPgoKPGNlcnQ+CkNlcnRpZmljYXRlOgogICAgRGF0YToKICAgICAgICBWZXJzaW9uOiAzICgweDIpCiAgICAgICAgU2VyaWFsIE51bWJlcjoKICAgICAgICAgICAgYzc6Y2E6ZTI6MmU6NjY6OGQ6YjU6MDE6OWY6NmY6NmY6YTY6YWY6M2I6ZjQ6YmUKICAgIFNpZ25hdHVyZSBBbGdvcml0aG06IHNoYTI1NldpdGhSU0FFbmNyeXB0aW9uCiAgICAgICAgSXNzdWVyOiBDPVJVLCBTVD1Nb3Njb3csIEw9TW9zY293LCBPPU5vdmlDb3JwLCBPVT1PVSwgQ049Y2Eubm92aWNvcnAucnUvZW1haWxBZGRyZXNzPWFkbWluQG5vdmljb3JwLnJ1CiAgICAgICAgVmFsaWRpdHkKICAgICAgICAgICAgTm90IEJlZm9yZTogQXVnIDE5IDE1OjE4OjU4IDIwMTggR01UCiAgICAgICAgICAgIE5vdCBBZnRlciA6IEF1ZyAxNiAxNToxODo1OCAyMDI4IEdNVAogICAgICAgIFN1YmplY3Q6IEM9UlUsIFNUPU1vc2NvdywgTD1Nb3Njb3csIE89Tm92aUNvcnAsIE9VPU9VLCBDTj10QHQudC9lbWFpbEFkZHJlc3M9YWRtaW5Abm92aWNvcnAucnUKICAgICAgICBTdWJqZWN0IFB1YmxpYyBLZXkgSW5mbzoKICAgICAgICAgICAgUHVibGljIEtleSBBbGdvcml0aG06IHJzYUVuY3J5cHRpb24KICAgICAgICAgICAgICAgIFB1YmxpYy1LZXk6ICg0MDk2IGJpdCkKICAgICAgICAgICAgICAgIE1vZHVsdXM6CiAgICAgICAgICAgICAgICAgICAgMDA6ZTk6N2I6ZTI6N2Y6Nzg6ZDY6MmQ6ZmM6MDQ6NWU6ZDk6OTI6YTg6NjU6CiAgICAgICAgICAgICAgICAgICAgZTE6MGE6NWM6YTg6ZTM6Y2Y6MjM6YjI6NzE6ZjU6OWM6ZWM6OWE6MWU6NjI6CiAgICAgICAgICAgICAgICAgICAgYTk6YjE6MmE6MmU6OTY6ZGY6Mjc6N2I6OWE6NTk6YzU6MTk6YWM6M2M6NWE6CiAgICAgICAgICAgICAgICAgICAgNmU6NjA6ZjY6Njk6ZmE6MmU6NjM6ZGM6YTc6Yzk6MzI6NDI6M2M6Yzk6Njk6CiAgICAgICAgICAgICAgICAgICAgMjI6YzA6MTg6ZTg6MWU6MzY6ZjE6Y2I6MzM6ZDk6NTI6YTk6NDU6MDY6ZWM6CiAgICAgICAgICAgICAgICAgICAgZWY6NDI6OWM6NTY6N2Q6ODk6MDc6OTU6ZGI6NjU6YmQ6Mzk6ZTM6NjQ6MTk6CiAgICAgICAgICAgICAgICAgICAgZjQ6Y2E6ZDI6NTk6MTQ6ZWM6N2U6Mjg6NzA6ODM6M2I6MmQ6MjA6MjI6NGU6CiAgICAgICAgICAgICAgICAgICAgZWI6MjE6OTk6NzE6OTY6MWI6NTg6YTI6Y2M6ZTc6NzE6MTM6Yzc6NjU6ZTE6CiAgICAgICAgICAgICAgICAgICAgZWM6Zjc6OTM6Zjg6ZTA6MTY6YjA6Y2Y6MmE6OWQ6MGI6Y2Y6OWQ6MjU6ZDI6CiAgICAgICAgICAgICAgICAgICAgMzM6Y2I6MDc6NGQ6YjE6ZDE6MTE6YWQ6ZTk6NmM6OGY6ZmY6MGQ6MTI6YjM6CiAgICAgICAgICAgICAgICAgICAgM2I6ZDU6ZDc6YjI6NGY6ODM6NjY6NGE6YTA6OGM6Yzg6NTM6ZTE6ZDE6MzM6CiAgICAgICAgICAgICAgICAgICAgZTI6ODU6YTk6NmY6Mjc6NWI6MmU6OTU6NmQ6NWY6MGU6NmI6MDI6MDA6MGY6CiAgICAgICAgICAgICAgICAgICAgN2I6NWU6N2U6YTQ6MTQ6ZmU6OGI6YTI6N2U6NTQ6MWM6YmM6YmU6YjI6Y2Q6CiAgICAgICAgICAgICAgICAgICAgYWQ6YWI6NDg6Nzc6MGM6MTQ6NjU6MzU6MDM6NDM6YTk6MjQ6MDM6NmI6MzU6CiAgICAgICAgICAgICAgICAgICAgZWM6YmU6ZTg6YjA6OTc6NWE6ZGI6MWE6ODg6YzI6ZmI6MmM6MjE6YTE6NzY6CiAgICAgICAgICAgICAgICAgICAgNGY6ZDg6YzA6ZDU6ZWI6ZWI6ZTU6ZGQ6M2E6ZGY6YTQ6NWY6Yjg6NWU6ZTA6CiAgICAgICAgICAgICAgICAgICAgNGY6ZDc6NzU6ZDU6ZWQ6MmQ6MmM6Mzg6Y2M6OTQ6MzI6NjM6Zjg6OWE6ZTc6CiAgICAgICAgICAgICAgICAgICAgMTM6YzQ6ODc6YTM6NGM6MTY6Mzk6Mzk6YTI6ZGU6MzU6YmE6ZTM6ZmY6OTg6CiAgICAgICAgICAgICAgICAgICAgZjc6ZmM6MzA6YmQ6M2M6NDU6Y2M6N2Y6MWQ6NzI6Nzc6YjA6MGE6Y2I6ZGY6CiAgICAgICAgICAgICAgICAgICAgOGE6YjY6OWI6Y2M6ZTg6MDg6NDk6MWY6MGI6Y2U6ZTk6ZmE6NDY6OWM6ODk6CiAgICAgICAgICAgICAgICAgICAgNzU6NTg6NjI6MDA6MjI6MmQ6Zjc6MzM6ZDk6OGQ6MjQ6MjE6NjE6N2M6ZjY6CiAgICAgICAgICAgICAgICAgICAgMDA6N2E6OGQ6ZjA6YWQ6MDc6OTY6MzQ6ZmM6MzQ6YzI6MWM6YTE6OTI6NTc6CiAgICAgICAgICAgICAgICAgICAgYzk6NWQ6MzM6NDI6NDI6MGM6ZDU6YmM6MzY6ZDE6ZWE6MjA6ODk6ZWY6OWU6CiAgICAgICAgICAgICAgICAgICAgYzg6ZWU6ODc6NmY6ZjA6NWE6MjU6OWE6NjI6NjA6YjA6ODE6ZjM6MzQ6N2I6CiAgICAgICAgICAgICAgICAgICAgMjU6ZjE6ZWI6ODM6YjY6Y2Q6NmE6YTY6YmU6N2Q6ZGY6MDM6MDE6Yjg6ODg6CiAgICAgICAgICAgICAgICAgICAgZDg6NDk6Yzk6Yzk6Njg6OGI6NmQ6OWE6ZjM6MWE6ZmY6ZmY6Njk6MDc6M2M6CiAgICAgICAgICAgICAgICAgICAgMDI6OGY6ZGI6MTE6NDI6ZTM6MmI6NTk6ZDc6YTk6ZTQ6ZjE6NjM6MjA6ZDU6CiAgICAgICAgICAgICAgICAgICAgMzY6YjU6MDQ6ODc6OGM6ZTI6M2E6ODQ6MjQ6MDE6MmE6MTQ6NWU6MTU6NGQ6CiAgICAgICAgICAgICAgICAgICAgNGY6ZmQ6NWU6MzE6MGE6ZTA6MmU6YWM6MGY6OTc6NjU6ZGE6OTI6YzI6N2Q6CiAgICAgICAgICAgICAgICAgICAgNTY6NjM6ODA6NDU6ZjA6ODE6ZTE6NzA6MWY6NTU6ZjU6Yzk6MTU6NDU6Yzk6CiAgICAgICAgICAgICAgICAgICAgZDc6NzQ6N2M6ZjI6ZTg6ZDk6NmE6ZWE6Mzg6OTc6ZmI6N2M6Njc6ZmY6OTU6CiAgICAgICAgICAgICAgICAgICAgMDM6YjQ6MWY6NzE6OTQ6Y2I6Mzg6MDM6NDQ6ZjI6Yzc6Njg6YTc6MzY6NWQ6CiAgICAgICAgICAgICAgICAgICAgMDQ6MmQ6ZTA6YTI6MjM6ODk6OGI6ODQ6ZTg6NGQ6MjE6YWQ6MDE6MTk6YWE6CiAgICAgICAgICAgICAgICAgICAgYzI6MTg6Zjk6YWQ6ZWQ6MGM6NDU6OGQ6NmY6ODk6MDk6OGU6MTg6ZDY6MmM6CiAgICAgICAgICAgICAgICAgICAgNDg6N2I6ZmYKICAgICAgICAgICAgICAgIEV4cG9uZW50OiA2NTUzNyAoMHgxMDAwMSkKICAgICAgICBYNTA5djMgZXh0ZW5zaW9uczoKICAgICAgICAgICAgWDUwOXYzIEJhc2ljIENvbnN0cmFpbnRzOiAKICAgICAgICAgICAgICAgIENBOkZBTFNFCiAgICAgICAgICAgIFg1MDl2MyBTdWJqZWN0IEtleSBJZGVudGlmaWVyOiAKICAgICAgICAgICAgICAgIDRCOjRFOkVDOkZGOkMzOjM5OjYxOjExOjNBOkQyOjU5OkNEOjMxOjE0OkFEOkJDOkY5Ojc4OjgzOjkyCiAgICAgICAgICAgIFg1MDl2MyBBdXRob3JpdHkgS2V5IElkZW50aWZpZXI6IAogICAgICAgICAgICAgICAga2V5aWQ6NTY6RDI6OTc6N0U6NUM6NDM6ODI6QkQ6MEY6RDU6RUI6NjU6MDM6NDY6RTc6Q0I6REY6Njc6N0U6MjIKICAgICAgICAgICAgICAgIERpck5hbWU6L0M9UlUvU1Q9TW9zY293L0w9TW9zY293L089Tm92aUNvcnAvT1U9T1UvQ049Y2Eubm92aWNvcnAucnUvZW1haWxBZGRyZXNzPWFkbWluQG5vdmljb3JwLnJ1CiAgICAgICAgICAgICAgICBzZXJpYWw6RkE6ODA6NzI6ODg6NjQ6MEY6MTI6NkQKCiAgICAgICAgICAgIFg1MDl2MyBFeHRlbmRlZCBLZXkgVXNhZ2U6IAogICAgICAgICAgICAgICAgVExTIFdlYiBDbGllbnQgQXV0aGVudGljYXRpb24KICAgICAgICAgICAgWDUwOXYzIEtleSBVc2FnZTogCiAgICAgICAgICAgICAgICBEaWdpdGFsIFNpZ25hdHVyZQogICAgU2lnbmF0dXJlIEFsZ29yaXRobTogc2hhMjU2V2l0aFJTQUVuY3J5cHRpb24KICAgICAgICAgZTE6ZjM6Njc6ZDI6NjE6ZTU6ZmQ6NGY6NzY6OWY6MDg6ZmY6OGU6MTI6NjQ6OTg6MTk6MDI6CiAgICAgICAgIGY1OjE3OjU2OjdiOjE4OjYwOmJmOjAzOjIxOmQwOmQyOjA5OmUyOjNjOmVlOjQ2OmJjOjBkOgogICAgICAgICAxOTphMDo3YTpkYzo1NDphNjoxZjoyYzo5NDo4MjpjNjo3NDpmZTo4Yzo3NDo5ODplZDoyOToKICAgICAgICAgZWI6M2I6YjI6NGE6NjY6OGM6NDc6ODY6OTc6NDk6ZDU6OTk6MGE6NTU6OWE6N2E6NDQ6MmM6CiAgICAgICAgIGJkOmI2OjI5OmEwOjE0OmY5Ojg5Ojk4OmVjOjQ4OjJhOjQ5OmRiOjBlOjY1Ojk2OmE2OmE3OgogICAgICAgICAxYjplYTpjOTphNjphZDpmODoyZTplMzplNjoyZDo2OTpiMjpiMDpkNjpmNjphZTo5Njo1OToKICAgICAgICAgYzA6NDg6NTc6M2Y6YWE6Njc6YzY6ZWM6ZjI6ZGQ6NWU6Mzk6MTQ6YTM6NDA6ZDI6ZTc6MTU6CiAgICAgICAgIDIzOjUwOjdmOjcyOmEzOjI0OjVlOjUzOmJkOjBmOmU5OjVlOjM3OjQzOmM4OjMwOjc5OmQ2OgogICAgICAgICBmZTplZjo3MTowNDpkMTpiODphYzo5Yjo2Njo5NDpmNjphZjplOTo2OTo5NTpiNTpkNjo5YjoKICAgICAgICAgMjU6MjI6ODg6MjE6ZTE6MTc6ZDg6MzU6YTU6MTc6Zjk6NDM6OGM6MmM6OWI6Mzc6Nzk6ZDA6CiAgICAgICAgIDAwOjZhOjM0OjNlOmNhOmRlOmRmOjQ3OmIwOmI4OmFhOjU2OmVlOjk2OmU0OjcyOjgzOjU4OgogICAgICAgICAyMjo3ZTplNzplOTo3MTowOTo4Yzo1Nzo4NTo4OToyOTphMDo5YjpkZTo5Zjo3MjozMTo2NzoKICAgICAgICAgNTU6OWY6ZDg6MjI6ZGE6ZDI6MWE6NTU6ZDc6YzQ6ZjY6ZDI6YzA6YmY6Yjg6NGY6OTI6M2Y6CiAgICAgICAgIGNjOjg1OjkxOmU2OmY3OjJjOjkwOmVhOjc4OjljOjI4OjRjOjg1OjNlOmU4Ojk1OmY1OmEwOgogICAgICAgICBlMTo3YToyZDo4NzowMTo4ZToxMzpkNjpmYjoxZToxNTozNjoyYToyODpiYjowMzo5ZDplNjoKICAgICAgICAgNDE6MmY6YmU6ZWY6OTQ6OTI6ZWQ6MWY6MjI6ZjU6Yzk6Zjg6NWU6YTc6MDU6MDg6NWI6MDE6CiAgICAgICAgIDcyOjgxOjQxOjlkOjExOjAyOmZhOmQ2OjY4OjBjOjI5OjFiOjYyOjY1OjkxOmE5OjY0OmU2OgogICAgICAgICBmMzo4NDo5MTozOTo5Mjo5OTozMDpiODo3Njo0ODoyNjpkNDo4ZjphNDozOTplNjo2ODplYjoKICAgICAgICAgYTI6ZDU6NmQ6ZmQ6ODg6MGM6Mjg6ZDE6OGY6YjQ6NWE6ZDY6Yzc6NTM6YmQ6NDc6NTA6NjE6CiAgICAgICAgIGVkOjIxOmJlOmRkOjc1OmZkOjUxOjAxOmJlOmUyOmNkOjVkOmU1OjZjOjc5OjZlOjdmOmViOgogICAgICAgICBlNjozYzoxYzpiYTphNTpmYzplYzoxYzplZDo0NDpkYTo1NTozNDo2NDoxNzpkNzpmMjpmODoKICAgICAgICAgZDc6Yjg6M2Y6NWQ6YjI6MTM6ZTI6MGU6NjA6NGI6ZWE6Yzg6N2E6ZGU6Zjk6MTA6ODk6MzY6CiAgICAgICAgIDZkOmUwOmVlOjZlOjkzOjMxOjdkOjQzOmZhOmMyOjJkOmU2OjgxOmE2OjI0OjI0OjIwOjk0OgogICAgICAgICAzNToxNDo3MDo5Yjo4MDpmNzpiODpkYTo0YzoxODo5ZDoyOToyYjpmMjoyZjo4MzozZjoyYToKICAgICAgICAgODY6M2U6ODA6N2I6NGU6YmU6Y2I6NGY6MWY6MDg6NTA6ZDc6MjA6MDI6MDY6OWQ6NTM6NmU6CiAgICAgICAgIGYxOmY5OmZhOjVjOjI2Ojg2OjkzOjNhOmVlOjI3OjE1OjJlOjViOjAwOjBmOjZmOjFkOjZlOgogICAgICAgICA3MTo4NTo5Njo0YjpiMzpkZDphMzplMDoxZDo2ZjoyMzo5Mzo2YTo0OTpiMDpmYjo3ZDo5ZDoKICAgICAgICAgZGY6MGY6M2U6M2I6ODg6ZmY6YTM6YWQ6M2I6NmU6Yzc6OTQ6YTI6MmU6ODY6NDY6MzM6Y2E6CiAgICAgICAgIGFiOjIyOmJiOmM5OmI0OjNmOmViOmVmCi0tLS0tQkVHSU4gQ0VSVElGSUNBVEUtLS0tLQpNSUlHckRDQ0JKU2dBd0lCQWdJUkFNZks0aTVtamJVQm4yOXZwcTg3OUw0d0RRWUpLb1pJaHZjTkFRRUxCUUF3CmdZb3hDekFKQmdOVkJBWVRBbEpWTVE4d0RRWURWUVFJREFaTmIzTmpiM2N4RHpBTkJnTlZCQWNNQmsxdmMyTnYKZHpFUk1BOEdBMVVFQ2d3SVRtOTJhVU52Y25BeEN6QUpCZ05WQkFzTUFrOVZNUmN3RlFZRFZRUUREQTVqWVM1dQpiM1pwWTI5eWNDNXlkVEVnTUI0R0NTcUdTSWIzRFFFSkFSWVJZV1J0YVc1QWJtOTJhV052Y25BdWNuVXdIaGNOCk1UZ3dPREU1TVRVeE9EVTRXaGNOTWpnd09ERTJNVFV4T0RVNFdqQ0JnVEVMTUFrR0ExVUVCaE1DVWxVeER6QU4KQmdOVkJBZ01CazF2YzJOdmR6RVBNQTBHQTFVRUJ3d0dUVzl6WTI5M01SRXdEd1lEVlFRS0RBaE9iM1pwUTI5eQpjREVMTUFrR0ExVUVDd3dDVDFVeERqQU1CZ05WQkFNTUJYUkFkQzUwTVNBd0hnWUpLb1pJaHZjTkFRa0JGaEZoClpHMXBia0J1YjNacFkyOXljQzV5ZFRDQ0FpSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnSVBBRENDQWdvQ2dnSUIKQU9sNzRuOTQxaTM4QkY3WmtxaGw0UXBjcU9QUEk3Sng5WnpzbWg1aXFiRXFMcGJmSjN1YVdjVVpyRHhhYm1EMgphZm91WTl5bnlUSkNQTWxwSXNBWTZCNDI4Y3N6MlZLcFJRYnM3MEtjVm4ySkI1WGJaYjA1NDJRWjlNclNXUlRzCmZpaHdnenN0SUNKTzZ5R1pjWlliV0tMTTUzRVR4MlhoN1BlVCtPQVdzTThxblF2UG5TWFNNOHNIVGJIUkVhM3AKYkkvL0RSS3pPOVhYc2srRFprcWdqTWhUNGRFejRvV3BieWRiTHBWdFh3NXJBZ0FQZTE1K3BCVCtpNkorVkJ5OAp2ckxOcmF0SWR3d1VaVFVEUTZra0EyczE3TDdvc0pkYTJ4cUl3dnNzSWFGMlQ5akExZXZyNWQwNjM2UmZ1RjdnClQ5ZDExZTB0TERqTWxESmorSnJuRThTSG8wd1dPVG1pM2pXNjQvK1k5L3d3dlR4RnpIOGRjbmV3Q3N2ZmlyYWIKek9nSVNSOEx6dW42UnB5SmRWaGlBQ0l0OXpQWmpTUWhZWHoyQUhxTjhLMEhsalQ4Tk1JY29aSlh5VjB6UWtJTQoxYncyMGVvZ2llK2V5TzZIYi9CYUpacGlZTENCOHpSN0pmSHJnN2JOYXFhK2ZkOERBYmlJMkVuSnlXaUxiWnJ6Ckd2Ly9hUWM4QW8vYkVVTGpLMW5YcWVUeFl5RFZOclVFaDR6aU9vUWtBU29VWGhWTlQvMWVNUXJnTHF3UGwyWGEKa3NKOVZtT0FSZkNCNFhBZlZmWEpGVVhKMTNSODh1alphdW80bC90OFovK1ZBN1FmY1pUTE9BTkU4c2RvcHpaZApCQzNnb2lPSmk0VG9UU0d0QVJtcXdoajVyZTBNUlkxdmlRbU9HTllzU0h2L0FnTUJBQUdqZ2dFU01JSUJEakFKCkJnTlZIUk1FQWpBQU1CMEdBMVVkRGdRV0JCUkxUdXovd3psaEVUclNXYzB4RksyOCtYaURrakNCdndZRFZSMGoKQklHM01JRzBnQlJXMHBkK1hFT0N2US9WNjJVRFJ1ZkwzMmQrSXFHQmtLU0JqVENCaWpFTE1Ba0dBMVVFQmhNQwpVbFV4RHpBTkJnTlZCQWdNQmsxdmMyTnZkekVQTUEwR0ExVUVCd3dHVFc5elkyOTNNUkV3RHdZRFZRUUtEQWhPCmIzWnBRMjl5Y0RFTE1Ba0dBMVVFQ3d3Q1QxVXhGekFWQmdOVkJBTU1EbU5oTG01dmRtbGpiM0p3TG5KMU1TQXcKSGdZSktvWklodmNOQVFrQkZoRmhaRzFwYmtCdWIzWnBZMjl5Y0M1eWRZSUpBUHFBY29oa0R4SnRNQk1HQTFVZApKUVFNTUFvR0NDc0dBUVVGQndNQ01Bc0dBMVVkRHdRRUF3SUhnREFOQmdrcWhraUc5dzBCQVFzRkFBT0NBZ0VBCjRmTm4wbUhsL1U5Mm53ai9qaEprbUJrQzlSZFdleGhndndNaDBOSUo0anp1UnJ3TkdhQjYzRlNtSHl5VWdzWjAKL294MG1PMHA2enV5U21hTVI0YVhTZFdaQ2xXYWVrUXN2Yllwb0JUNWlaanNTQ3BKMnc1bGxxYW5HK3JKcHEzNApMdVBtTFdteXNOYjJycFpad0VoWFA2cG54dXp5M1Y0NUZLTkEwdWNWSTFCL2NxTWtYbE85RCtsZU4wUElNSG5XCi91OXhCTkc0ckp0bWxQYXY2V21WdGRhYkpTS0lJZUVYMkRXbEYvbERqQ3liTjNuUUFHbzBQc3JlMzBld3VLcFcKN3Bia2NvTllJbjduNlhFSmpGZUZpU21nbTk2ZmNqRm5WWi9ZSXRyU0dsWFh4UGJTd0wrNFQ1SS96SVdSNXZjcwprT3A0bkNoTWhUN29sZldnNFhvdGh3R09FOWI3SGhVMktpaTdBNTNtUVMrKzc1U1M3UjhpOWNuNFhxY0ZDRnNCCmNvRkJuUkVDK3Rab0RDa2JZbVdScVdUbTg0U1JPWktaTUxoMlNDYlVqNlE1NW1qcm90VnQvWWdNS05HUHRGclcKeDFPOVIxQmg3U0crM1hYOVVRRys0czFkNVd4NWJuL3I1andjdXFYODdCenRSTnBWTkdRWDEvTDQxN2cvWGJJVAo0ZzVnUytySWV0NzVFSWsyYmVEdWJwTXhmVVA2d2kzbWdhWWtKQ0NVTlJSd200RDN1TnBNR0owcEsvSXZnejhxCmhqNkFlMDYreTA4ZkNGRFhJQUlHblZOdThmbjZYQ2FHa3pydUp4VXVXd0FQYngxdWNZV1dTN1BkbytBZGJ5T1QKYWttdyszMmQzdzgrTzRqL282MDdic2VVb2k2R1JqUEtxeUs3eWJRLzYrOD0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQoKPC9jZXJ0PgoKPGtleT4KLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUpRd0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQ1Mwd2dna3BBZ0VBQW9JQ0FRRHBlK0ovZU5ZdC9BUmUKMlpLb1plRUtYS2pqenlPeWNmV2M3Sm9lWXFteEtpNlczeWQ3bWxuRkdhdzhXbTVnOW1uNkxtUGNwOGt5UWp6SgphU0xBR09nZU52SExNOWxTcVVVRzdPOUNuRlo5aVFlVjIyVzlPZU5rR2ZUSzBsa1U3SDRvY0lNN0xTQWlUdXNoCm1YR1dHMWlpek9keEU4ZGw0ZXozay9qZ0ZyRFBLcDBMejUwbDBqUExCMDJ4MFJHdDZXeVAvdzBTc3p2VjE3SlAKZzJaS29JeklVK0hSTStLRnFXOG5XeTZWYlY4T2F3SUFEM3RlZnFRVS9vdWlmbFFjdkw2eXphMnJTSGNNRkdVMQpBME9wSkFOck5leSs2TENYV3RzYWlNTDdMQ0doZGsvWXdOWHI2K1hkT3Qra1g3aGU0RS9YZGRYdExTdzR6SlF5ClkvaWE1eFBFaDZOTUZqazVvdDQxdXVQL21QZjhNTDA4UmN4L0hYSjNzQXJMMzRxMm04em9DRWtmQzg3cCtrYWMKaVhWWVlnQWlMZmN6Mlkwa0lXRjg5Z0I2amZDdEI1WTAvRFRDSEtHU1Y4bGRNMEpDRE5XOE50SHFJSW52bnNqdQpoMi93V2lXYVltQ3dnZk0wZXlYeDY0TzJ6V3Ftdm4zZkF3RzRpTmhKeWNsb2kyMmE4eHIvLzJrSFBBS1AyeEZDCjR5dFoxNm5rOFdNZzFUYTFCSWVNNGpxRUpBRXFGRjRWVFUvOVhqRUs0QzZzRDVkbDJwTENmVlpqZ0VYd2dlRncKSDFYMXlSVkZ5ZGQwZlBMbzJXcnFPSmY3ZkdmL2xRTzBIM0dVeXpnRFJQTEhhS2MyWFFRdDRLSWppWXVFNkUwaApyUUVacXNJWSthM3RERVdOYjRrSmpoaldMRWg3L3dJREFRQUJBb0lDQURhajJGQ3VqYWo3Um1hUUVrTTRmRjY1CmFvak5pL1FSdVVIOUdPQXRoTHJDUFY3dllFVUx6U0JVTHJ0OUNrSEV5TzVVZHVoSGw4MGNOUytKWENtS2FwL1AKaWV4YytPbmdWUmdXMExOTTlPeXg2Y1dITDVzRjloSVNCUGlHRzNUTEY0Y05OWmplcVp0OXpvYnhhdVNQQjhJcApvNndSemVNbzZSVFRXelhOK1ppeHgwamhVRXh1a2RKY3BqRUwxVkJXeFNJNXRPeUFaMnRXN0JLeGxIbTRjdG5hCno0anUxSDhsTks4SUpyR3ZnOFJUQklmUkY3VDRmQnV4cWluZjJIMVZLbWVidkozTitwWW9HN3M1UlZkSzUwWHEKdTdtOXFMM3k5RDJVYmRUcjhmN2dPalZtZzJtUHJoNkV6WnVoRHZ1ZEVQSkNVRXNOL0VCYWwvL201MklRMjgzNgowUmZzc2IvM1hwS1Q4dlFwZC9oUHVmK05haTBLQWZTQ2hlYWc3aFNnWW9BbkRSQmpIbTJwbCtvcjM3WFpURzh0CnJxVks3VS9UcjFwaW1JT1YydXlTM3hKT0s5QWdwMXFNWldRVEw0dUhxUWd3SmIrUG9PRWQ5Sk83eDhuN2VUa2gKY2NyOUUzR015MjZ6a3RIaTFhemdFRVowY0ZwM0QyWEwxd0s5WDUwNmJORFkrOXJ3UUhwUzFJV1A0ZjZhaHFFYwo1NDhNREFFNVdFcTJXWmRUV09XaUhpNmRkNXp1MWR0K1NnWmlRVmg1amFMdzcvakM4bndXc3NjREhuWW1wQVZVCmVsYy9welN4d2h2ekcxNFh5b1cyTkt1SktLRDI3VDhDRzYvU0pzOTFXaUQxQXgxdE1FZlk0Mm9iTHlWSTVlUUMKRXgyM0VIUWxFbHhOOVY3U0JFRHhBb0lCQVFEOTZwYWNlRDF3Rlc5RG5rMVNGT1B1VVBZU0FMNDlPamhYeG1ISApXcHlJNWd6cm5LV2FiZkROZC9JS0ttMDFDWHJYRWswNTFVTVNwY1VuemJoeDVlSXRtTlMzZkNVWjFJUTljWSswCjN0QU5ZMGlRSXdzUFR4Z3NZbFFzZGZVZzYvbDJzajNZN1dUcXlvbk05WDhWM0pWZWczbjFYK3BVeVB1MStLckIKMmhMSkI0akVlOXZCK2xLc2FjT2ZIMFgzMkR2RHBYS2NmRE1QdzdXMk9KNDhEOHdtcmp5a1YycjlqcVErTjRoegpMc3FGUUhMQUFZSjNha1VQWCtSR1IxZ0lZWWJKK1hHbTF5NktaSXByMlMydG8yVjFCQlRTSE8xRFhQN1Z1b3ExClpnZEhySk1rZEd1azZkQ0hCTGluREpvckVMWTZDMkxkNDFHQkltMUM4Ri9PRnFvbkFvSUJBUURyWmwrTTY5cmgKUEl5cnNSOC83S21xWTkrb2w0MFAxMU8zb3ZRV1Z3akJ2cXVNV3FDN1pJaEZzNXpkR2d6VGJMajJ3TXdYWHVabQpJTGZTc0tUSzlsYURtWUhEdWR3MjU0SU1IMmtSS2lHQjJZSTBCM1Y0TmNXRjFjSUdoay9sWE44TmN5OXRyVGU3CmllYkNSbnhrYTg0REFNZHNCczd1VHNDY2tzbjNSYXdFYzhuc2pDQTFRVzZFaE00cEdQamdESDBBN2VkUVM5cW0KVnNhNFM3YkpWK010Z0pBMUYvcVRkc2UxZkdrcEV1SUdMenZxd0VMekFTemZFaUpnQUZMYkJhTElRWkNRdXUxUgpxbHVqMUNwNkpjNU93eDZMbzAydjJHR1JhTWNUcDdYcWQ5MC92YlhBWWR2QXVLMnV5WG5PWkNObmdEbW9XTXpCCmlybVpUQkhDeHY1cEFvSUJBUUNoNGtscHNzTkF6WG1sZTZ6Q015MXFpRldKL3MxTERlNVVEOWZSR0xVS0Z0bVAKOGN3bkhBYlZpSzVZeXRuYllaTGV3ZjFZYk40WmFuUzdQczVrVjNNUExRd1plMTNRRFF6T2U3TnFWbEFBNlJhZgpScWhMZDFyckdUbWZLd2xBbHhIeUdndVNYUy9rL1lKRG1SVVFKQlZiTDZtMnhoTUpRU1l4eXp0YTRpVHQ1QTdQCmJrUWFkUFQybFd1eDdHZFliNVVTMUUydzlRSTgvOEsvVFhPY3lWbVlJNmZvQXcva1htZmFmdDlReURrNElYSEgKZG03dW9XTXNQUysxbXRER2J4OVhiK0NFeFZZWHg2ZjB3SDc5NEZuVDgra3VXR0R3Zkw3QUZ2Rk9XNkV5a2hVeAp2Y1BQWFg2a1JsOVBxWm8wOEsrdGJBcjVlbTlCVEdpcXI4UDFDY0FyQW9JQkFRRFJtMUt4dE1JdGxURGRJTlptCm9XRmlhNVFZRnZwd2hKZnpDSkszNGIvV1pPVjBFSzdXcmVuNXhybUMxMU5jWDQ5RGlPRXlYanBoN2ZoQkR6RnQKMkhPb3N1T3RXSzRSNVlzVEtGVHlCOFhXVGN0MmNMM1UwR3lWZzRWRk1ndXFmRXZST2lPZFVZUXk1ZFFvWVlNYQpHRFJVMERqQ3BEMVdUYUdNeWRnMDZrRUZwZVREVVBMTStQcGozYTJGUXNzNUZXV3BraTFLZm9DdlpNMkdCVVU1CmU1eTZRNlFrNHJrbzNiZHVqdDFFeVoraFNpWGNIbDUrNnlqOWFMUmJMMjZYd0NqMmtBc2VGSlNGQjJDYVBLMm0KSGt2YUxqdmdzd1RWODZMTlM3TVllVm11OGhSOFVYeXBWWG5MM2FZcDRSVXBCbG5RSzRrcnNnYUF2L29MMm9SbQpIN01oQW9JQkFDL0RONVpxOWhkRjRHbzgxbDIyMzQ3UHdyYmtoR0JvWnFhWE0zK2JjWEZBTlpTa0pEVGtTN3JZClFQRmhhY01OL1NsblpEL3U1WXVZUm1oKys2Z0YrOGpHZDFic2tnaFBIR1VPTWpuNldTUG5tbmFVY2YyQk1iM1oKSzJYT1BocExaTVVjNGZLZnRBbDRUUGRxeFVJVG4zNWhRNGJJN3ZJb2lCS3JwL1dEYjl5REg5dnNQK3NYUFFhTQo3NTQ2NmhPQm5EeXJseFk3NVJRUmR3MC9xU3VKanEyRWIwd3ptNzNDUHhyMlB4VkQvRXFqLzB3NVIzSUxWNDZMCndXSU5WanBseExRc2NsUEI0UjBZdXpwWkVLelVCcXZDVGFleHl1MTFCVVdZOWl1dUd4YklsQnJCR1RrM1JvSmkKaDZQTmw2UkZPeWEwMXBHMjMzWVVHMml3MUtlZkxoUT0KLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLQoKPC9rZXk+Cg==', 3, 1);