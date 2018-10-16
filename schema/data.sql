TRUNCATE public.user CASCADE;
TRUNCATE public.user_device CASCADE;
TRUNCATE public.user_vpn_server_config CASCADE;

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
INSERT INTO public.user_vpn_server_config(uuid, user_uuid, configuration, vpn_device_platform_id, vpn_type_id) VALUES ('8f525324-f752-4135-bab7-38e0f1ff96f9', 'cf402144-0c02-4b97-98f2-73f7b56160cf', 'Y2xpZW50CmRldiB0dW4KcHJvdG8gdWRwCnNuZGJ1ZiAwCnJjdmJ1ZiAwCnJlbW90ZSAxOTMuNzAuNzMuMjQyIDUxMjQyCnJlc29sdi1yZXRyeSBpbmZpbml0ZQpub2JpbmQKcGVyc2lzdC1rZXkKcGVyc2lzdC10dW4KcmVtb3RlLWNlcnQtdGxzIHNlcnZlcgphdXRoIFNIQTUxMgpjaXBoZXIgQUVTLTI1Ni1DQkMKY29tcC1sem8Kc2V0ZW52IG9wdCBibG9jay1vdXRzaWRlLWRucwprZXktZGlyZWN0aW9uIDEKdmVyYiAzCjxjYT4KLS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLekNDQWhPZ0F3SUJBZ0lKQU9aOFl3b0NQQUd5TUEwR0NTcUdTSWIzRFFFQkN3VUFNQk14RVRBUEJnTlYKQkFNTUNFTm9ZVzVuWlUxbE1CNFhEVEUzTURreU9ERXpNRFF4TWxvWERUSTNNRGt5TmpFek1EUXhNbG93RXpFUgpNQThHQTFVRUF3d0lRMmhoYm1kbFRXVXdnZ0VpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElCRHdBd2dnRUtBb0lCCkFRRGwrdzBFZ3ZnVzVtNG9SNFZOOFhiTkdIczVGNkMyaTVVMWxRaU5IcXR1MWI1cFNrRHRTNEpkcU40OEFKd3UKbDVPa2hLODFkYXkwbThCbmpzNFAveElvcmt6NTE5NVJXNGI4anFodGtrK0ZrZlI0M3F0WldJMHVMUVhicGxlZwpqdXdlLzR5MzRwdSs4VXF2cmQzenJPMDZZMXZSMXpQZ1NxM2t4Z2NELzhpTHlmNU5yTTA1U2RLNVhaWk1kbWxrCmZKd0ZsOTV5S1ZmWjJ0K3cwZ3oxWHJkcUwrRWJOUWR5SFdVYUFBM0NtY2JQSlRJWFoyaW9MQVJPVVlDbEtVaCsKemhEWEROUzFvOVI3bzdpaUlpay8wRGdnNWtaVmxuaXZuS2ZUTk8xM1R5NlpxYlhBQWxxczlhZjZaeThXZEVkTgpra2FoZXZXYlNtaVhyQ1A2K3dJd0V3T3JBZ01CQUFHamdZRXdmekFkQmdOVkhRNEVGZ1FVY3lnRU1DSmdzN3lkClNnZ0thUDdCN1dVaXcxZ3dRd1lEVlIwakJEd3dPb0FVY3lnRU1DSmdzN3lkU2dnS2FQN0I3V1VpdzFpaEY2UVYKTUJNeEVUQVBCZ05WQkFNTUNFTm9ZVzVuWlUxbGdna0E1bnhqQ2dJOEFiSXdEQVlEVlIwVEJBVXdBd0VCL3pBTApCZ05WSFE4RUJBTUNBUVl3RFFZSktvWklodmNOQVFFTEJRQURnZ0VCQU45c1NCTTRPdlZCeFFxVDFOWmJneGs1ClZmSnA0WnIrR1VkYXllWDNMUCtxTXFhZGhNWitIZ2xjTTduc2NxaloyM2ZQMUpyMzBvbmxLSDg4ZTAzR09UU0cKQUU5YzVJMnVhWjd2eWxGMS83TDV0a3pMd1ZEWlpzTEtMT2s1aTlqUmtUckNsZFpadGE2V3NXR1lScXQyTFV5RQp6K3pDRjUzcEttWkNuWjZxanNKUCtmbzdSRDVXcDhiU2VhRGIzR3lIT3dvSU5VN1ppNE12OE5HdkFoSDlyWTJ1CitJWGlIa3R3NWpHc1lnTjlvUm1qV1IwR2lUNEwydlYyL2NaVzFVWjdLZ2dsOHRqc1hFT0pWcG5IMWtTMW12ZkIKR0hHNGw3UmtoNnhuSjR4TmxlVnE4amtGYUx2VGRUQUxYUXByREtJdGFiTTNMWVFrb0FHbGZxUnhwWjY2T2J3PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCjwvY2E+CjxjZXJ0PgpDZXJ0aWZpY2F0ZToKICAgIERhdGE6CiAgICAgICAgVmVyc2lvbjogMyAoMHgyKQogICAgICAgIFNlcmlhbCBOdW1iZXI6CiAgICAgICAgICAgIGEwOmNjOmQ0OjU3OmMwOjA5OjllOjE5OjIwOjE0OjE5OjdmOmU1OjljOmQxOjdkCiAgICBTaWduYXR1cmUgQWxnb3JpdGhtOiBzaGEyNTZXaXRoUlNBRW5jcnlwdGlvbgogICAgICAgIElzc3VlcjogQ049Q2hhbmdlTWUKICAgICAgICBWYWxpZGl0eQogICAgICAgICAgICBOb3QgQmVmb3JlOiBBcHIgMTcgMDk6MDU6MDYgMjAxOCBHTVQKICAgICAgICAgICAgTm90IEFmdGVyIDogQXByIDE0IDA5OjA1OjA2IDIwMjggR01UCiAgICAgICAgU3ViamVjdDogQ049bWVfaXBob25lCiAgICAgICAgU3ViamVjdCBQdWJsaWMgS2V5IEluZm86CiAgICAgICAgICAgIFB1YmxpYyBLZXkgQWxnb3JpdGhtOiByc2FFbmNyeXB0aW9uCiAgICAgICAgICAgICAgICBQdWJsaWMtS2V5OiAoMjA0OCBiaXQpCiAgICAgICAgICAgICAgICBNb2R1bHVzOgogICAgICAgICAgICAgICAgICAgIDAwOmI3OmRmOmQzOjNhOjNiOmY1OjI1OjUyOjU2OjY4OjEwOmM3OjZiOjBlOgogICAgICAgICAgICAgICAgICAgIDNlOjYyOjZlOmNlOmI4OjQ2OjgxOjg4OmNlOjljOmViOmYwOmFkOmVjOjcyOgogICAgICAgICAgICAgICAgICAgIDVmOjE4OjU2OmFkOjU1OmYwOmNkOjdhOjk2OjRmOmNhOjVhOjQzOmFkOjJkOgogICAgICAgICAgICAgICAgICAgIGFlOmI1OjVjOmJjOmRlOjgwOjdjOjNlOmU5OjQ1OjdmOjg5OjdiOjQxOjdhOgogICAgICAgICAgICAgICAgICAgIDk1OjU3OjQ3OjI1OmVhOjVlOjY3OmZiOjBkOjU4OjMxOmFkOmQ4OjA5OmZmOgogICAgICAgICAgICAgICAgICAgIDFkOmJmOjIxOmE3OjhkOmRkOjk2OmM4OmUzOjk4OjhkOmY0OmM5OjUxOjFjOgogICAgICAgICAgICAgICAgICAgIDQ0OjljOmRkOjU2OjU5OjAyOjM2OmRkOjgzOmZmOmMxOmY1OjE1OjJhOmE0OgogICAgICAgICAgICAgICAgICAgIDUyOjNkOjBjOjI2OjQxOjIwOmVmOjg2OjYyOmJhOmFjOjFhOjIxOjQxOjc2OgogICAgICAgICAgICAgICAgICAgIGJiOmI1OjYzOjFiOjdmOmUxOmY0OjEzOjZkOmNjOmUyOjU0OmNlOmQ0OmRlOgogICAgICAgICAgICAgICAgICAgIDNlOjQ5OmQ0OjMyOjllOjY2OmRjOjUyOjZmOjdhOjEyOjkzOmY2OjJkOjM2OgogICAgICAgICAgICAgICAgICAgIGM5OmY1OmRjOjNjOmI2OjE3OjMzOmI5OmE0OmY0Ojc4OjVlOjQ2OmUwOmE0OgogICAgICAgICAgICAgICAgICAgIDRlOjkxOjdhOmViOjNjOmVkOjZhOjFmOjhmOmVkOjkwOmI4OjczOjc0OmVmOgogICAgICAgICAgICAgICAgICAgIDIwOmU0OmJiOjViOjk1OjlhOmU2OjUyOjQ0OmU0OjNhOmNiOjYxOjlmOjZiOgogICAgICAgICAgICAgICAgICAgIDZmOjQ2OjRiOjgxOjJlOjU1OmQxOmQ0OmE5OjJjOmNmOmY2OjVkOjNkOjJjOgogICAgICAgICAgICAgICAgICAgIDBhOjViOmI2OmNmOjY0OmY3Ojg4OjQzOjUyOmNmOmZiOjNjOjhkOjlmOjk3OgogICAgICAgICAgICAgICAgICAgIDFhOmZjOjFhOjE4OjZiOmUyOjEwOmY1OjEyOmExOmQ3OjMwOmI1OjczOjJhOgogICAgICAgICAgICAgICAgICAgIDc5OmYxOjAyOjE2OmE4OjlhOmMxOjlmOjY5OmI5OmZkOmQ1OmFkOmJhOmUzOgogICAgICAgICAgICAgICAgICAgIDc4OjUzCiAgICAgICAgICAgICAgICBFeHBvbmVudDogNjU1MzcgKDB4MTAwMDEpCiAgICAgICAgWDUwOXYzIGV4dGVuc2lvbnM6CiAgICAgICAgICAgIFg1MDl2MyBCYXNpYyBDb25zdHJhaW50czoKICAgICAgICAgICAgICAgIENBOkZBTFNFCiAgICAgICAgICAgIFg1MDl2MyBTdWJqZWN0IEtleSBJZGVudGlmaWVyOgogICAgICAgICAgICAgICAgREQ6QkI6MDg6RTI6NTM6Mjc6NkE6RTc6RDY6QTI6MzE6OEM6Qjg6MkE6ODM6NDk6NDU6Q0Y6OUY6QTYKICAgICAgICAgICAgWDUwOXYzIEF1dGhvcml0eSBLZXkgSWRlbnRpZmllcjoKICAgICAgICAgICAgICAgIGtleWlkOjczOjI4OjA0OjMwOjIyOjYwOkIzOkJDOjlEOjRBOjA4OjBBOjY4OkZFOkMxOkVEOjY1OjIyOkMzOjU4CiAgICAgICAgICAgICAgICBEaXJOYW1lOi9DTj1DaGFuZ2VNZQogICAgICAgICAgICAgICAgc2VyaWFsOkU2OjdDOjYzOjBBOjAyOjNDOjAxOkIyCgogICAgICAgICAgICBYNTA5djMgRXh0ZW5kZWQgS2V5IFVzYWdlOgogICAgICAgICAgICAgICAgVExTIFdlYiBDbGllbnQgQXV0aGVudGljYXRpb24KICAgICAgICAgICAgWDUwOXYzIEtleSBVc2FnZToKICAgICAgICAgICAgICAgIERpZ2l0YWwgU2lnbmF0dXJlCiAgICBTaWduYXR1cmUgQWxnb3JpdGhtOiBzaGEyNTZXaXRoUlNBRW5jcnlwdGlvbgogICAgICAgICA2MTpjMzozNToxNDozYzo3NjpjOTo2NDozOTo4MToxZTpjMjo1YzplODplNjo4MDo4YzozZToKICAgICAgICAgNjU6YTk6MzQ6NGY6ZDU6NTc6MTA6MjQ6YWQ6ODA6OWU6ZWM6N2Y6OGU6MWY6MzY6NjM6MmE6CiAgICAgICAgIGIzOmJkOmUyOmU3OjBkOmExOmQ3OjZkOjY5OmU5OjQ1OmQxOmFhOjUxOmZjOjdhOjkyOjRiOgogICAgICAgICA4MzowMjpiYzpiZjo3YjoxNToyNjo3ZjpkNjpmMDozODo2Zjo0NjpkNjpiZjpkZjo2NTo2ODoKICAgICAgICAgNGQ6OWM6Nzg6ZmM6NGM6Mzk6MDQ6MGE6MGQ6NmQ6ZGI6NWI6NTI6ODQ6ZjI6MjY6NTk6NDI6CiAgICAgICAgIDlkOjQ4Ojc3OmQ0OjVhOjE2OmEyOmVjOmEyOjYzOmM1Ojk0OjY1OjhlOjA3OjRlOjQ1OmNjOgogICAgICAgICAyMjoxYzpkNDo2NzoyMzpmMDphMDpkYjpiZDpkNDo4MDphNzowNjo5Yjo4ZTplZjphMzo1ODoKICAgICAgICAgOWE6MTI6NjA6ZDY6NWU6OWU6YTE6ZDI6Zjc6ZTA6YTE6Nzk6NjE6MWE6MDc6MzQ6NGM6Yzk6CiAgICAgICAgIDJkOjBmOmVhOmM5OmFlOjM1OmU1OmE4OmRlOjU3OmY0OjgzOjhlOmVkOjZkOmZkOmQ3OjcxOgogICAgICAgICA5ZDpiMTozNTphMzozMDo1Mzo5Mzo5NDo3Yzo0MTpjNzpmYjpkMzo1Yjo1OTpmZTphNDo3ODoKICAgICAgICAgZGE6YzM6N2U6YzY6ZjU6Mzk6MjA6ZTg6MjM6Njg6NzU6Mjc6N2I6MTU6NTk6OGI6N2I6OTQ6CiAgICAgICAgIDRiOjFkOmFhOjJkOjJhOjQ0OmQ4OjJkOjQ3OmQ1OjFiOmZkOmY4OjljOjI1OjZmOjY5OjNhOgogICAgICAgICA1OToyZjpjZTpjYjpiODpiMjphYTpiMTo0ODowZDpkZDplYzoxMTowMDo2ZTphZjo2NDoyMjoKICAgICAgICAgZWQ6MTE6NGE6NTU6OGY6ZGU6MDY6YjY6NGI6YzY6ZWE6NzI6ZmE6MjY6ZDY6MDU6ODU6NTI6CiAgICAgICAgIGE2OjQ2OjRmOjM4Ci0tLS0tQkVHSU4gQ0VSVElGSUNBVEUtLS0tLQpNSUlEUnpDQ0FpK2dBd0lCQWdJUkFLRE0xRmZBQ1o0WklCUVpmK1djMFgwd0RRWUpLb1pJaHZjTkFRRUxCUUF3CkV6RVJNQThHQTFVRUF3d0lRMmhoYm1kbFRXVXdIaGNOTVRnd05ERTNNRGt3TlRBMldoY05Namd3TkRFME1Ea3cKTlRBMldqQVVNUkl3RUFZRFZRUUREQWx0WlY5cGNHaHZibVV3Z2dFaU1BMEdDU3FHU0liM0RRRUJBUVVBQTRJQgpEd0F3Z2dFS0FvSUJBUUMzMzlNNk8vVWxVbFpvRU1kckRqNWliczY0Um9HSXpwenI4SzNzY2w4WVZxMVY4TTE2CmxrL0tXa090TGE2MVhMemVnSHcrNlVWL2lYdEJlcFZYUnlYcVhtZjdEVmd4cmRnSi94Mi9JYWVOM1piSTQ1aU4KOU1sUkhFU2MzVlpaQWpiZGcvL0I5UlVxcEZJOURDWkJJTytHWXJxc0dpRkJkcnUxWXh0LzRmUVRiY3ppVk03VQozajVKMURLZVp0eFNiM29Tay9ZdE5zbjEzRHkyRnpPNXBQUjRYa2JncEU2UmV1czg3V29maisyUXVITjA3eURrCnUxdVZtdVpTUk9RNnkyR2ZhMjlHUzRFdVZkSFVxU3pQOWwwOUxBcGJ0czlrOTRoRFVzLzdQSTJmbHhyOEdoaHIKNGhEMUVxSFhNTFZ6S25ueEFoYW9tc0dmYWJuOTFhMjY0M2hUQWdNQkFBR2pnWlF3Z1pFd0NRWURWUjBUQkFJdwpBREFkQmdOVkhRNEVGZ1FVM2JzSTRsTW5hdWZXb2pHTXVDcURTVVhQbjZZd1F3WURWUjBqQkR3d09vQVVjeWdFCk1DSmdzN3lkU2dnS2FQN0I3V1VpdzFpaEY2UVZNQk14RVRBUEJnTlZCQU1NQ0VOb1lXNW5aVTFsZ2drQTVueGoKQ2dJOEFiSXdFd1lEVlIwbEJBd3dDZ1lJS3dZQkJRVUhBd0l3Q3dZRFZSMFBCQVFEQWdlQU1BMEdDU3FHU0liMwpEUUVCQ3dVQUE0SUJBUUJod3pVVVBIYkpaRG1CSHNKYzZPYUFqRDVscVRSUDFWY1FKSzJBbnV4L2poODJZeXF6CnZlTG5EYUhYYlducFJkR3FVZng2a2t1REFyeS9leFVtZjlid09HOUcxci9mWldoTm5IajhURGtFQ2cxdDIxdFMKaFBJbVdVS2RTSGZVV2hhaTdLSmp4WlJsamdkT1Jjd2lITlJuSS9DZzI3M1VnS2NHbTQ3dm8xaWFFbURXWHA2aAowdmZnb1hsaEdnYzBUTWt0RCtySnJqWGxxTjVYOUlPTzdXMzkxM0dkc1RXak1GT1RsSHhCeC92VFcxbitwSGphCnczN0c5VGtnNkNOb2RTZDdGVm1MZTVSTEhhb3RLa1RZTFVmVkcvMzRuQ1Z2YVRwWkw4N0x1TEtxc1VnTjNld1IKQUc2dlpDTHRFVXBWajk0R3Rrdkc2bkw2SnRZRmhWS21Sazg0Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0KPC9jZXJ0Pgo8a2V5PgotLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS0KTUlJRXZRSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2N3Z2dTakFnRUFBb0lCQVFDMzM5TTZPL1VsVWxabwpFTWRyRGo1aWJzNjRSb0dJenB6cjhLM3NjbDhZVnExVjhNMTZsay9LV2tPdExhNjFYTHplZ0h3KzZVVi9pWHRCCmVwVlhSeVhxWG1mN0RWZ3hyZGdKL3gyL0lhZU4zWmJJNDVpTjlNbFJIRVNjM1ZaWkFqYmRnLy9COVJVcXBGSTkKRENaQklPK0dZcnFzR2lGQmRydTFZeHQvNGZRVGJjemlWTTdVM2o1SjFES2VadHhTYjNvU2svWXROc24xM0R5MgpGek81cFBSNFhrYmdwRTZSZXVzODdXb2ZqKzJRdUhOMDd5RGt1MXVWbXVaU1JPUTZ5MkdmYTI5R1M0RXVWZEhVCnFTelA5bDA5TEFwYnRzOWs5NGhEVXMvN1BJMmZseHI4R2hocjRoRDFFcUhYTUxWektubnhBaGFvbXNHZmFibjkKMWEyNjQzaFRBZ01CQUFFQ2dnRUFYd1pZTmpjNE9NSjFqekJrcnNuY3FhZ1VReDJFNGZ2TkV3MytCRDBUTWhQUgpYcUdrdjE2Zys3VnNWanBPbU1IRmhjT204aWhCMTJob2YyMW5jb1I5YnNLOVAvd2tnUUFUcnc3ZUE2SFQ0cmdLCnJlVVpPUHV4Y3E2R012OGNHY0hRTXVoOXEzSUtMMUJlZzlnY2lQb0piMHprcGY2WEF5cm1WUlpUNXVJUjdsdW0KOWhPK3JzL0lKVUdkSzMvSlF2U252TTZtM2JDZ2RGemJRczFldXRIRERwN0pFR3pieXVZTDBmVFcxM0htdnBxWgpMTjJiV2JUTlI0ZjhqdTAyVW90OVQwcDhmaTZ2YWZqdGZYdkZRRG5SZlNmQUhHeDErUERMMDhKZ29KMWVDRjRRCnhrM0l3Z0k4djFBQndGSHl5RVlMVjdaazQwMWV6b01UVXNlaTlaYWFVUUtCZ1FEZmh6bk1yejZhV0U3TUg2MWcKTTZSYkIrbllJT2Rlemh1N09VVlN1RE0raVlEcTM5czcySWhjbUwwdEg1QmYrbklXUFhPVzZRQUxCZE8vNldDdAp3Vm9TQjBIRFpHZC9mL2x4Zm1GR3EyRHdLSyt1dG1mdUw2b1FyejlaK01EZFBzOUdkTW5ZVXl3OHVlWWNjbGZVClJZRG1aOFdRb2IyRXdLY2dtUmk4eXpuUDZRS0JnUURTbGVuQ1FCN01Sb2EwYkRMc0RJdzZvSGJUMzZTajFFbk4KUjVLZ0JnTnN6eFVObE9rZW92UVFQMTRpbmxuN1lPTG5MZHk1bVlleWxBUXBidzJyWWxLT2JDNWp1eXE4SFd4aAp2V1IxQjRzVW8wZWdyUy8yV3B6LzhBL1VlQURYd0tFdXJTbVNxUE1uUEJ6dlZQWWZiN1BmdWxxUWJmMnJyZDFwCkdtWnhlWlE4MndLQmdRQzFWMDljN3c4cXlGbWs0RTRYcmMyNHpFSzZSSGR3UW1YZERpbGZZbkN3VzMxckR4RWQKREI0VWdSVjRkaEw2eW9PajUxYlBKMWdSbVRpZ2lRVVY4YmJReVhKZ3dpUDFIQzJTRmFWMVg3UFZJaXprNExhUQpWYnJ5cmpvSEUvZmpoZ0ZDZDUwSkV2RGdrekJNQTdlZFRvVzBacHV4S29aR0hNVjVmTHJFNzFxSGdRS0JnQVlSCjNpQUVPeDhHTldIRDhKL1BLTWVUMG5qKzdEN3dvb1B4T1MrMW5LbXBPbUVlMXExVVl4YUl6UXpRWmFXU1FGZ0wKZ1Y0MEo2NGxDQTJ0cnNZdTJsUlNsKysxK0dCZHRMOElkM25NRXQwd2E2TWMrdEh1QUxKNzErajI0SWRYZlEzYwpYZU5sVFVUblBhcEVWNmZHVDNmMlpoL2RtNzgwRHJxMTBSZ2FPZ1NiQW9HQUZ4YW9EdWRuT0JqWG1ENkRlQ21mCkJmUU05TUlYMEl0alVYeURoYTB2N3NqWDRBajJQWGxZZnRxTW4weVdnbnlJZk83aDVkeUtKRFN5QStuejRFRzQKUklBSyswR1RFU0VzS3Q1N21PRDBOa014WmhvRXFLMG1FV095OW9nc1ZOTnplK29lTWc1ejZ2bElJdFQ1azlDTgpBdUdtZmt1MXgzRGFNZmZXU1Jabjc3MD0KLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLQo8L2tleT4KPHRscy1hdXRoPgojCiMgMjA0OCBiaXQgT3BlblZQTiBzdGF0aWMga2V5CiMKLS0tLS1CRUdJTiBPcGVuVlBOIFN0YXRpYyBrZXkgVjEtLS0tLQo3NTMzOWRhYTVjOTUzYjk1NjMxNTYyZDcwYTVhMGQ5OQoyMDYyZDEyZWY2OTg2MGJiNTJjMDU5ODM2MGViNThlNwoxNjBhM2IwM2VjMDU1NzU2ODZjZGM1ZjEyYjk1OTM2ZAo5MzM3OThhMGY3ZTdiMTZiYzE5MzdkMGRlMjE4ZWNkNwphZGFjZTBhZTRkODlhZjE5NzBhMjIzZWFkYjE1Yjc2ZQpkZWQyZmQwN2ZkMmQyZThlZTNkMTM1YWUwZmYwNmIzMgphNTdiNTRiYjdmZjE0Nzk3YjcyYjhlMjYyMGQ4YjIwYwowMTNmYjQxMTdlYzQwYWU4MTdmMzRiNDFjMGQ4MTRhMAowNDcyMjViNWY0OWZhM2U0ZWQ3MGExZjExYmYzNDA0NAphNjdkMTM2MzM5ZGY4MWZiOTg4YzEzNmZkYzcyZGZjMwo5MjZiMWZkMjIzNmE5YzI3ZmRhYzI0YmEwMWNlZDkxOAo1ODIwNjkzMTZlOTdhMmQ4YTQwZDM4MDY5MDhiYzFjYgo2YzZjYjhjNWRjNjgwZTE0ZjFlNzExOTZlNjM0OTI5ZgpjZDQ3OGUwYThiMDVmMmQ4MDg1Mzg3NzA4MzJiYmQ2MgowYWViM2U2YjBhNmUxMzA0NjBmOGQzMzYxNDE3NDgxMwoxNTI4Mjk5MGViNzE1OWUxNGRiZDhlODE3YzRlMDhiZAotLS0tLUVORCBPcGVuVlBOIFN0YXRpYyBrZXkgVjEtLS0tLQo8L3Rscy1hdXRoPgo=', 3, 1);