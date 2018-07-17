DROP TRIGGER IF EXISTS check_pincode_activating ON "user_device" CASCADE;

-- increment VPN Server version when any field was changed
CREATE TRIGGER check_pincode_activating
  AFTER INSERT OR UPDATE ON public.user_device
  FOR EACH ROW EXECUTE PROCEDURE deactivate_user_pincode();