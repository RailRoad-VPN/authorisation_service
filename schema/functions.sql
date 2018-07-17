CREATE OR REPLACE FUNCTION deactivate_user_pincode()
  RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.user
  SET is_pin_code_activated = TRUE
  WHERE uuid = NEW.user_uuid;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;